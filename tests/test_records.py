import contextlib
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts import projectctl
from scripts.projectctl import StateError


def pending_state():
    def rec():
        return {"status": "PENDING", "revision": None, "evidence": None}

    return {
        "schema_version": 2,
        "project_name": None,
        "requirements_revision": None,
        "pcb_requirements_revision": None,
        "design_revision": None,
        "input_approval": rec(),
        "pcb_input_approval": rec(),
        "reviews": {k: rec() for k in ("schematic", "pcb", "manufacturing")},
        "export_approval": rec(),
        "blocking_issues": [],
    }


BOM = (
    "Designator,Qty,Comment,Description,Footprint,MPN,Manufacturer,Alternate MPN,"
    "Alternate Manufacturer,LCSC Part #,Supplier,Supplier PN,DNP,Notes\n"
    "C1 C2,2,100nF,,0402,CL05B104KO5NNNC,Samsung,GRM155R71C104KA88D,Murata,,,,,\n"
    "R1,1,10k,,0402,RC0402FR-0710KL,Yageo,,,,,,,\n"
    "R2,1,0R,,0402,RC0402JR-070RL,Yageo,,,,,,Yes,option\n"
)
PNP = "Designator,Mid X,Mid Y,Layer,Rotation\nC1,1.0,2.0,Top,0\nC2,3.0,2.0,Top,90\nR1,5mm,2,Bottom,180\n"


class RecordFunctionTests(unittest.TestCase):
    def test_approve_records_date_and_author(self):
        state = projectctl.approve(pending_state(), "G0", "REQ-1", "user said yes", "tester")
        rec = state["input_approval"]
        self.assertEqual(rec["status"], "APPROVED")
        self.assertEqual(rec["revision"], "REQ-1")
        self.assertEqual(rec["recorded_by"], "tester")
        self.assertRegex(rec["recorded_on"], r"^\d{4}-\d{2}-\d{2}$")

    def test_approve_requires_revision_and_evidence(self):
        with self.assertRaises(StateError):
            projectctl.approve(pending_state(), "G1", "R1", "  ")

    def test_revoke_clears_record(self):
        state = projectctl.approve(pending_state(), "G0.5", "PCB-1", "ok")
        state = projectctl.revoke(state, "G0.5")
        self.assertEqual(
            state["pcb_input_approval"], {"status": "PENDING", "revision": None, "evidence": None}
        )

    def test_review_rework_allows_missing_evidence(self):
        state = projectctl.record_review(pending_state(), "pcb", "REWORK", "R1")
        self.assertEqual(state["reviews"]["pcb"]["status"], "REWORK")

    def test_review_pass_requires_evidence(self):
        with self.assertRaises(StateError):
            projectctl.record_review(pending_state(), "pcb", "PASS", "R1")

    def test_block_and_unblock(self):
        state = projectctl.block(pending_state(), "F-001")
        projectctl.block(state, "F-001")  # no duplicate
        self.assertEqual(state["blocking_issues"], ["F-001"])
        projectctl.unblock(state, "F-001")
        self.assertEqual(state["blocking_issues"], [])
        with self.assertRaises(StateError):
            projectctl.unblock(state, "F-404")

    def test_set_field_and_clear(self):
        state = projectctl.set_field(pending_state(), "design_revision", "R1")
        self.assertEqual(state["design_revision"], "R1")
        projectctl.set_field(state, "design_revision", None)
        self.assertIsNone(state["design_revision"])

    def test_output_name_and_variant(self):
        state = projectctl.set_field(pending_state(), "project_code", "DR00627")
        projectctl.set_field(state, "design_revision", "R01")
        self.assertEqual(projectctl.output_name(state), "DR00627-R01")
        self.assertEqual(projectctl.output_name(state, "A"), "DR00627-AV-R01")
        with self.assertRaises(StateError):
            projectctl.output_name(state, "ab")

    def test_output_name_requires_code(self):
        state = projectctl.set_field(pending_state(), "design_revision", "R01")
        with self.assertRaises(StateError):
            projectctl.output_name(state)

    def test_invalid_project_code_rejected(self):
        with self.assertRaises(StateError):
            projectctl.set_field(pending_state(), "project_code", "DR 627/x")

    def test_old_state_without_project_code_is_valid(self):
        projectctl.validate_state(pending_state())

    def test_invalid_recorded_by_rejected(self):
        state = pending_state()
        state["input_approval"]["recorded_by"] = ""
        with self.assertRaises(StateError):
            projectctl.validate_state(state)


class CliAndManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.state_path = self.root / "workflow-state.json"
        self.mfg = self.root / "Manufacturing"
        self.state_path.write_text(json.dumps(pending_state()), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = projectctl.main(
                [*args, "--state", str(self.state_path), "--manufacturing-dir", str(self.mfg),
                 "--repo-root", str(self.root)]
            )
        return code, out.getvalue() + err.getvalue()

    def approve_everything(self):
        steps = [
            ("set", "project_name", "Test"),
            ("set", "project_code", "DR00627"),
            ("set", "requirements_revision", "REQ-1"),
            ("set", "pcb_requirements_revision", "PCB-1"),
            ("set", "design_revision", "R1"),
            ("approve", "G0", "--revision", "REQ-1", "--evidence", "e"),
            ("approve", "G0.5", "--revision", "PCB-1", "--evidence", "e"),
            ("approve", "G1", "--revision", "R1", "--evidence", "e"),
            ("review", "schematic", "PASS", "--revision", "R1", "--evidence", "e"),
            ("review", "pcb", "PASS", "--revision", "R1", "--evidence", "e"),
            ("deliverables", "BOM", "PnP"),
        ]
        for step in steps:
            code, out = self.run_cli(*step)
            self.assertEqual(code, 0, out)

    def release_files(self, folder=None):
        release = folder or self.mfg / "R1"
        release.mkdir(parents=True, exist_ok=True)
        (release / "DR00627-R1_BOM.csv").write_text(BOM, encoding="utf-8")
        (release / "DR00627-R1_PnP.csv").write_text(PNP, encoding="utf-8")
        return release

    def review_manufacturing(self):
        code, out = self.run_cli("review", "manufacturing", "PASS", "--revision", "R1", "--evidence", "e")
        self.assertEqual(code, 0, out)

    def test_cli_writes_valid_lf_json(self):
        code, _ = self.run_cli("set", "project_name", "Sensör kartı")
        self.assertEqual(code, 0)
        raw = self.state_path.read_bytes()
        self.assertNotIn(b"\r\n", raw)
        self.assertEqual(json.loads(raw.decode("utf-8"))["project_name"], "Sensör kartı")

    def test_release_requires_manifest_and_detects_changes(self):
        self.approve_everything()
        self.assertEqual(self.run_cli("check-export")[0], 0)

        release = self.release_files()
        (release / "DR00627-R1_Gerber").mkdir()
        (release / "DR00627-R1_Gerber" / "top.gbr").write_bytes(b"G04 test*\n")

        code, out = self.run_cli("review", "manufacturing", "PASS", "--revision", "R1", "--evidence", "e")
        self.assertEqual(code, 2)
        self.assertIn("Write a valid manifest", out)
        code, out = self.run_cli("check-release")
        self.assertEqual(code, 1)
        self.assertIn("Manifest missing", out)

        self.assertEqual(self.run_cli("manifest")[0], 0)
        self.review_manufacturing()
        self.assertEqual(self.run_cli("check-release")[0], 0)

        (release / "DR00627-R1_BOM.csv").write_text(BOM + "C9,1,,,,X,,,,,,,,\n", encoding="utf-8")
        (release / "extra.txt").write_text("x", encoding="utf-8")
        code, out = self.run_cli("check-release")
        self.assertEqual(code, 1)
        self.assertIn("Checksum mismatch: DR00627-R1_BOM.csv", out)
        self.assertIn("File not in manifest: extra.txt", out)
        self.assertIn("fitted part C9 missing from PnP", out)

    def test_regenerated_manifest_needs_new_review(self):
        self.approve_everything()
        release = self.release_files()
        self.run_cli("manifest")
        self.review_manufacturing()
        self.assertEqual(self.run_cli("check-release")[0], 0)
        (release / "DR00627-R1_PnP.csv").write_text(PNP + "\n", encoding="utf-8")
        self.run_cli("manifest")
        code, out = self.run_cli("check-release")
        self.assertEqual(code, 1)
        self.assertIn("changed after the review", out)

    def test_deliverable_with_dotted_revision(self):
        folder = self.root / "rel"
        folder.mkdir()
        (folder / "DR1-R1.2_BOM.csv").write_text("x\n", encoding="utf-8")
        errors = projectctl.deliverable_errors(folder, {"deliverables": ["BOM", "PnP"], "project_code": "DR1"})
        self.assertEqual(len(errors), 1)
        self.assertIn("_PnP", errors[0])

    def test_missing_deliverable_blocks_release(self):
        self.approve_everything()
        self.run_cli("deliverables", "BOM", "PnP", "Gerber")
        self.release_files()
        self.run_cli("manifest")
        self.review_manufacturing()
        code, out = self.run_cli("check-release")
        self.assertEqual(code, 1)
        self.assertIn("Deliverable missing: DR00627-..._Gerber", out)

    def test_check_bom_requires_a_bom_in_release(self):
        self.approve_everything()
        (self.mfg / "R1").mkdir(parents=True)
        code, out = self.run_cli("check-bom")
        self.assertEqual(code, 1)
        self.assertIn("No *_BOM.csv found", out)

    def test_next_command_walks_the_workflow(self):
        self.assertIn("set project_name", self.run_cli("next")[1])
        self.approve_everything()
        self.assertIn("check-bom", self.run_cli("next")[1])
        self.release_files()
        self.assertIn("manifest", self.run_cli("next")[1])
        self.run_cli("manifest")
        self.assertIn("review manufacturing PASS", self.run_cli("next")[1])
        self.review_manufacturing()
        self.assertIn("nothing missing", self.run_cli("next")[1])

    def test_next_asks_review_depth_before_g0(self):
        for step in (("set", "project_name", "T"), ("set", "project_code", "DR1"),
                     ("set", "design_revision", "R1"), ("set", "requirements_revision", "REQ-1")):
            self.run_cli(*step)
        self.assertIn("set review_depth", self.run_cli("next")[1])
        self.assertEqual(self.run_cli("set", "review_depth", "high")[0], 0)
        self.assertEqual(json.loads(self.state_path.read_text(encoding="utf-8"))["review_depth"], "High")
        self.assertIn("approve G0", self.run_cli("next")[1])
        self.assertEqual(self.run_cli("set", "review_depth", "Extreme")[0], 2)

    def test_high_depth_needs_two_independent_reviewers(self):
        self.approve_everything()
        self.run_cli("set", "review_depth", "High")
        code, out = self.run_cli("check-export")
        self.assertEqual(code, 1)
        self.assertIn("Second schematic review (High depth): requires PASS", out)
        self.assertIn("review schematic PASS --second", self.run_cli("next")[1])
        self.run_cli("review", "schematic", "PASS", "--second", "--by", "rev-a", "--revision", "R1", "--evidence", "e")
        code, out = self.run_cli("check-layout")
        self.assertEqual(code, 1)
        self.assertIn("record both reviewers with --by", out)
        self.run_cli("review", "schematic", "PASS", "--by", "REV-A", "--revision", "R1", "--evidence", "e")
        self.assertIn("different reviewer", self.run_cli("check-layout")[1])
        self.run_cli("review", "schematic", "PASS", "--by", "rev-b", "--revision", "R1", "--evidence", "e")
        self.assertEqual(self.run_cli("check-layout")[0], 0)
        code, out = self.run_cli("check-export")
        self.assertEqual(code, 1)
        self.assertIn("Second PCB review (High depth)", out)
        self.assertIn("review pcb PASS --second", self.run_cli("next")[1])
        self.run_cli("review", "pcb", "PASS", "--by", "rev-a", "--revision", "R1", "--evidence", "e")
        self.run_cli("review", "pcb", "PASS", "--second", "--by", "rev-b", "--revision", "R1", "--evidence", "e")
        self.assertEqual(self.run_cli("check-export")[0], 0)

    def test_light_and_medium_need_one_reviewer(self):
        self.approve_everything()
        for depth in ("Light", "Medium"):
            self.run_cli("set", "review_depth", depth)
            self.assertEqual(self.run_cli("check-export")[0], 0)

    def test_second_manufacturing_review_is_rejected(self):
        self.approve_everything()
        code, out = self.run_cli("review", "manufacturing", "REWORK", "--second")
        self.assertEqual(code, 2)
        self.assertIn("only for schematic and pcb", out)

    def test_corrupt_manifest_and_csv_fail_cleanly(self):
        self.approve_everything()
        release = self.release_files()
        (release / "MANIFEST.sha256").write_bytes(b"\xff\xfe")
        code, out = self.run_cli("check-release")
        self.assertEqual(code, 1)
        self.assertIn("Manifest unreadable", out)
        (release / "MANIFEST.sha256").write_text("0" * 64 + "  ../../x.json\n", encoding="utf-8")
        self.assertIn("Malformed manifest line", self.run_cli("check-release")[1])
        bad = self.root / "bad.csv"
        bad.write_bytes(b"Designator,Qty\n\xfe\xfc,1\n")
        code, out = self.run_cli("check-bom", str(bad))
        self.assertEqual(code, 2)
        self.assertIn("not UTF-8", out)
        bad.write_text("Designator;Qty;MPN\nR1;1;X\n", encoding="utf-8")
        self.assertIn("separated by ';'", self.run_cli("check-bom", str(bad))[1])

    def test_bom_parsing_details(self):
        bom = self.root / "b.csv"
        pnp = self.root / "p.csv"
        bom.write_text(BOM.replace("Designator,", "Designator ,").replace("C1 C2,2", "C1-C2,2") + ",,,,\n",
                       encoding="utf-8")
        pnp.write_text(PNP + "\n,,,,\n", encoding="utf-8")
        code, out = self.run_cli("check-bom", str(bom), "--pnp", str(pnp))
        self.assertEqual(code, 0, out)
        pnp.write_text(PNP.replace("1.0,2.0", "nan,inf") + ",1,1,Top,0\n", encoding="utf-8")
        code, out = self.run_cli("check-bom", str(bom), "--pnp", str(pnp))
        self.assertIn("not a finite number", out)
        self.assertIn("p.csv:5: empty Designator", out)

    def test_lowercase_bom_file_is_found(self):
        self.approve_everything()
        release = self.mfg / "R1"
        release.mkdir(parents=True)
        (release / "DR00627-R1_bom.csv").write_text("Designator,Qty\nR1,1\n", encoding="utf-8")
        code, out = self.run_cli("check-bom")
        self.assertIn("missing columns", out)

    def test_state_option_before_subcommand(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = projectctl.main(["--state", str(self.state_path), "--repo-root", str(self.root), "validate"])
        self.assertEqual(code, 0, err.getvalue())

    def test_nested_release_files_need_prefix(self):
        self.approve_everything()
        board = self.mfg / "R1" / "MAIN"
        board.mkdir(parents=True)
        (board / "DR00627-R1_BOM.csv").write_text(BOM, encoding="utf-8")
        (board / "notes.txt").write_text("x", encoding="utf-8")
        (board / "Thumbs.db").write_text("x", encoding="utf-8")
        self.run_cli("manifest")
        code, out = self.run_cli("check-release")
        self.assertEqual(code, 1)
        self.assertIn("project code DR00627: MAIN/notes.txt", out)
        self.assertNotIn("Thumbs.db", out)
        self.assertNotIn("MAIN/DR00627-R1_BOM.csv", out.split("Manifest")[0])

    def test_reserved_revision_name_rejected(self):
        self.run_cli("set", "design_revision", "templates")
        code, out = self.run_cli("manifest")
        self.assertEqual(code, 2)
        self.assertIn("reserved", out)

    def test_check_bom_command(self):
        bom = self.root / "b.csv"
        pnp = self.root / "p.csv"
        bom.write_text(BOM, encoding="utf-8")
        pnp.write_text(PNP, encoding="utf-8")
        code, out = self.run_cli("check-bom", str(bom), "--pnp", str(pnp))
        self.assertEqual(code, 0, out)
        self.assertIn("WARNING", out)  # R1 has no alternate and no note

        pnp.write_text(PNP + "R2,1,1,Top,0\n", encoding="utf-8")
        code, out = self.run_cli("check-bom", str(bom), "--pnp", str(pnp))
        self.assertEqual(code, 1)
        self.assertIn("DNP part R2 must not be in PnP", out)

    def test_check_bom_qty_and_columns(self):
        bom = self.root / "b.csv"
        bom.write_text(BOM.replace("C1 C2,2", "C1 C2,3"), encoding="utf-8")
        code, out = self.run_cli("check-bom", str(bom))
        self.assertEqual(code, 1)
        self.assertIn("Qty 3 does not match 2 designators", out)
        bom.write_text(BOM.replace("C1 C2,2", "C1 C2,²"), encoding="utf-8")
        code, out = self.run_cli("check-bom", str(bom))
        self.assertEqual(code, 1)
        self.assertIn("does not match 2 designators", out)
        bom.write_text("Designator,Qty\nR1,1\n", encoding="utf-8")
        code, out = self.run_cli("check-bom", str(bom))
        self.assertIn("missing columns", out)



    def test_export_requires_project_code(self):
        self.approve_everything()
        self.run_cli("set", "project_code")
        code, out = self.run_cli("check-export")
        self.assertEqual(code, 1)
        self.assertIn("Project code is missing", out)

    def test_name_command(self):
        self.approve_everything()
        self.assertEqual(self.run_cli("name")[1].strip(), "DR00627-R1")
        self.assertEqual(self.run_cli("name", "--variant", "A")[1].strip(), "DR00627-AV-R1")

    def test_release_rejects_unprefixed_file(self):
        self.approve_everything()
        release = self.mfg / "R1"
        release.mkdir(parents=True)
        (release / "bom.csv").write_text("x", encoding="utf-8")
        self.run_cli("manifest")
        self.review_manufacturing()
        code, out = self.run_cli("check-release")
        self.assertEqual(code, 1)
        self.assertIn("does not start with project code DR00627: bom.csv", out)

    def test_manifest_without_release_folder_fails(self):
        self.run_cli("set", "design_revision", "R9")
        code, out = self.run_cli("manifest")
        self.assertEqual(code, 2)
        self.assertIn("Release folder not found", out)

    def test_unsafe_revision_folder_rejected(self):
        self.run_cli("set", "design_revision", "../x")
        code, out = self.run_cli("manifest")
        self.assertEqual(code, 2)
        self.assertIn("folder name", out)


@unittest.skipUnless(shutil.which("git"), "git not installed")
class GitBindingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.git("init", "-q")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "t")
        (self.root / "Hardware").mkdir()
        (self.root / "Hardware" / "board.kicad_pcb").write_text("v1\n", encoding="utf-8")
        (self.root / "Hardware" / "board.kicad_sch").write_text("v1\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-q", "-m", "init")
        self.state_path = self.root / "workflow-state.json"
        self.state_path.write_text(json.dumps(pending_state()), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = projectctl.main([*args, "--state", str(self.state_path),
                                    "--manufacturing-dir", str(self.root / "Manufacturing"),
                                    "--repo-root", str(self.root)])
        return code, out.getvalue() + err.getvalue()

    def approve(self):
        for step in [
            ("set", "project_name", "T"), ("set", "project_code", "DR00627"),
            ("set", "requirements_revision", "REQ-1"), ("set", "pcb_requirements_revision", "PCB-1"),
            ("set", "design_revision", "R1"),
            ("approve", "G0", "--revision", "REQ-1", "--evidence", "e"),
            ("approve", "G0.5", "--revision", "PCB-1", "--evidence", "e"),
            ("review", "schematic", "PASS", "--revision", "R1", "--evidence", "e"),
            ("review", "pcb", "PASS", "--revision", "R1", "--evidence", "e"),
            ("approve", "G1", "--revision", "R1", "--evidence", "e"),
        ]:
            self.assertEqual(self.run_cli(*step)[0], 0)

    def test_commit_is_recorded(self):
        self.approve()
        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertRegex(state["export_approval"]["commit"], r"^[0-9a-f]{40}$")
        self.assertRegex(state["export_approval"]["design_sha256"], r"^[0-9a-f]{64}$")

    def test_git_removed_later_falls_back_to_hashes(self):
        self.approve()
        real = projectctl.git_head
        projectctl.git_head = lambda repo_root: None
        try:
            self.assertEqual(self.run_cli("check-export")[0], 0)
            (self.root / "Hardware" / "board.kicad_pcb").write_text("v2\n", encoding="utf-8")
            code, out = self.run_cli("check-export")
        finally:
            projectctl.git_head = real
        self.assertEqual(code, 1)
        self.assertIn("recorded design file hash", out)

    def test_pcb_change_after_review_blocks_export(self):
        self.approve()
        self.assertEqual(self.run_cli("check-export")[0], 0)
        (self.root / "Hardware" / "board.kicad_pcb").write_text("v2\n", encoding="utf-8")
        code, out = self.run_cli("check-export")
        self.assertEqual(code, 1)
        self.assertIn("PCB review: design files changed", out)
        self.assertIn("G1 export approval: design files changed", out)
        self.assertNotIn("Schematic review: design files changed", out)

    def test_untracked_design_file_blocks_layout(self):
        self.approve()
        (self.root / "Hardware" / "sub").mkdir()
        (self.root / "Hardware" / "sub" / "extra.kicad_sch").write_text("x\n", encoding="utf-8")
        code, out = self.run_cli("check-layout")
        self.assertEqual(code, 1)
        self.assertIn("Schematic review: design files changed", out)

    def test_outjob_change_is_not_a_design_change(self):
        self.approve()
        (self.root / "Hardware" / "out.OutJob").write_text("x\n", encoding="utf-8")
        self.assertEqual(self.run_cli("check-export")[0], 0)

    def test_review_refused_with_uncommitted_design(self):
        self.approve()
        (self.root / "Hardware" / "board.kicad_pcb").write_text("v3\n", encoding="utf-8")
        code, out = self.run_cli("review", "pcb", "PASS", "--revision", "R1", "--evidence", "e")
        self.assertEqual(code, 2)
        self.assertIn("commit the reviewed design first", out)

    def test_invalid_commit_value_rejected(self):
        self.approve()
        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        state["reviews"]["schematic"]["commit"] = "--output=PWNED.txt"
        self.state_path.write_text(json.dumps(state), encoding="utf-8")
        code, out = self.run_cli("check-layout")
        self.assertEqual(code, 2)
        self.assertIn("hexadecimal git commit", out)
        self.assertFalse((self.root / "PWNED.txt").exists())

    def test_default_repo_root_is_the_project(self):
        (self.root / "project").mkdir()
        state_path = self.root / "project" / "workflow-state.json"
        state_path.write_text(json.dumps(pending_state()), encoding="utf-8")
        self.assertEqual(projectctl.default_repo_root(state_path), self.root.resolve())

    def test_schematic_change_blocks_layout(self):
        self.approve()
        (self.root / "Hardware" / "board.kicad_sch").write_text("v2\n", encoding="utf-8")
        code, out = self.run_cli("check-layout")
        self.assertEqual(code, 1)
        self.assertIn("Schematic review: design files changed", out)


class NoGitBindingTests(GitBindingTests):
    """Same checks without git: records store design file hashes instead of a commit."""

    __unittest_skip__ = False  # runs even when git is not installed

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "Hardware").mkdir()
        (self.root / "Hardware" / "board.kicad_pcb").write_text("v1\n", encoding="utf-8")
        (self.root / "Hardware" / "board.kicad_sch").write_text("v1\n", encoding="utf-8")
        self.state_path = self.root / "workflow-state.json"
        self.state_path.write_text(json.dumps(pending_state()), encoding="utf-8")
        self._real_head = projectctl.git_head
        projectctl.git_head = lambda repo_root: None

    def tearDown(self):
        projectctl.git_head = self._real_head
        self.tmp.cleanup()

    def test_commit_is_recorded(self):
        self.approve()
        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        record = state["export_approval"]
        self.assertNotIn("commit", record)
        self.assertRegex(record["design_sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(record["schematic_sha256"], r"^[0-9a-f]{64}$")

    def test_review_refused_with_uncommitted_design(self):
        self.approve()
        (self.root / "Hardware" / "board.kicad_pcb").write_text("v3\n", encoding="utf-8")
        self.assertEqual(self.run_cli("review", "pcb", "PASS", "--revision", "R1", "--evidence", "e")[0], 0)
        self.assertEqual(self.run_cli("approve", "G1", "--revision", "R1", "--evidence", "e")[0], 0)
        self.assertEqual(self.run_cli("check-export")[0], 0)

    def test_invalid_commit_value_rejected(self):
        self.approve()
        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        state["reviews"]["schematic"]["design_sha256"] = "not-a-hash"
        self.state_path.write_text(json.dumps(state), encoding="utf-8")
        code, out = self.run_cli("check-layout")
        self.assertEqual(code, 2)
        self.assertIn("SHA-256", out)

    def test_commit_record_without_git_is_not_silently_accepted(self):
        self.approve()
        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        record = state["reviews"]["pcb"]
        record["commit"] = "a" * 40
        record.pop("design_sha256")
        self.state_path.write_text(json.dumps(state), encoding="utf-8")
        code, out = self.run_cli("check-export")
        self.assertEqual(code, 1)
        self.assertIn("git is not available", out)

    def test_hash_ignores_case_and_altium_previews(self):
        self.approve()
        (self.root / "Hardware" / "a.SCHDOCPREVIEW").write_text("x\n", encoding="utf-8")
        (self.root / "Hardware" / "p.PrjPcbStructure").write_text("x\n", encoding="utf-8")
        (self.root / "Hardware" / "#auto_saved_files#").mkdir()
        self.assertEqual(self.run_cli("check-export")[0], 0)

    def test_backup_and_lock_files_are_ignored(self):
        self.approve()
        (self.root / "Hardware" / "board.kicad_prl").write_text("x\n", encoding="utf-8")
        (self.root / "Hardware" / "board-backups").mkdir()
        (self.root / "Hardware" / "board-backups" / "b.zip").write_text("x\n", encoding="utf-8")
        self.assertEqual(self.run_cli("check-export")[0], 0)


if __name__ == "__main__":
    unittest.main()
