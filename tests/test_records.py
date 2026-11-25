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
        state = projectctl.block(pending_state(), "REV-001")
        projectctl.block(state, "REV-001")  # no duplicate
        self.assertEqual(state["blocking_issues"], ["REV-001"])
        projectctl.unblock(state, "REV-001")
        self.assertEqual(state["blocking_issues"], [])
        with self.assertRaises(StateError):
            projectctl.unblock(state, "REV-404")

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
            ("review", "manufacturing", "PASS", "--revision", "R1", "--evidence", "e"),
        ]
        for step in steps:
            code, out = self.run_cli(*step)
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

        release = self.mfg / "R1"
        (release / "DR00627-R1_Gerber").mkdir(parents=True)
        (release / "DR00627-R1_Gerber" / "top.gbr").write_bytes(b"G04 test*\n")
        (release / "DR00627-R1_BOM.csv").write_text(BOM, encoding="utf-8")
        (release / "DR00627-R1_PnP.csv").write_text(PNP, encoding="utf-8")

        code, out = self.run_cli("check-release")
        self.assertEqual(code, 1)
        self.assertIn("Manifest missing", out)

        self.assertEqual(self.run_cli("manifest")[0], 0)
        self.assertEqual(self.run_cli("check-release")[0], 0)

        (release / "DR00627-R1_BOM.csv").write_text(BOM + "C9,1,,,,X,,,,,,,,\n", encoding="utf-8")
        (release / "extra.txt").write_text("x", encoding="utf-8")
        code, out = self.run_cli("check-release")
        self.assertEqual(code, 1)
        self.assertIn("Checksum mismatch: DR00627-R1_BOM.csv", out)
        self.assertIn("File not in manifest: extra.txt", out)
        self.assertIn("fitted part C9 missing from PnP", out)

    def test_nested_release_files_need_prefix(self):
        self.approve_everything()
        board = self.mfg / "R1" / "MAIN"
        board.mkdir(parents=True)
        (board / "DR00627-R1_BOM.csv").write_text(BOM, encoding="utf-8")
        (board / "notes.txt").write_text("x", encoding="utf-8")
        self.run_cli("manifest")
        code, out = self.run_cli("check-release")
        self.assertEqual(code, 1)
        self.assertIn("project code DR00627: MAIN/notes.txt", out)
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

    def test_pcb_change_after_review_blocks_export(self):
        self.approve()
        self.assertEqual(self.run_cli("check-export")[0], 0)
        (self.root / "Hardware" / "board.kicad_pcb").write_text("v2\n", encoding="utf-8")
        code, out = self.run_cli("check-export")
        self.assertEqual(code, 1)
        self.assertIn("PCB review: design files changed", out)
        self.assertIn("G1 export approval: design files changed", out)
        self.assertNotIn("Schematic review: design files changed", out)

    def test_schematic_change_blocks_layout(self):
        self.approve()
        (self.root / "Hardware" / "board.kicad_sch").write_text("v2\n", encoding="utf-8")
        code, out = self.run_cli("check-layout")
        self.assertEqual(code, 1)
        self.assertIn("Schematic review: design files changed", out)


if __name__ == "__main__":
    unittest.main()
