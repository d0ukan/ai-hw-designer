import contextlib
import io
import json
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
                [*args, "--state", str(self.state_path), "--manufacturing-dir", str(self.mfg)]
            )
        return code, out.getvalue() + err.getvalue()

    def approve_everything(self):
        steps = [
            ("set", "project_name", "Test"),
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
        (release / "gerber").mkdir(parents=True)
        (release / "gerber" / "top.gbr").write_bytes(b"G04 test*\n")
        (release / "bom.csv").write_text("ref,mpn\n", encoding="utf-8")

        code, out = self.run_cli("check-release")
        self.assertEqual(code, 1)
        self.assertIn("Manifest missing", out)

        self.assertEqual(self.run_cli("manifest")[0], 0)
        self.assertEqual(self.run_cli("check-release")[0], 0)

        (release / "bom.csv").write_text("ref,mpn\nR1,X\n", encoding="utf-8")
        (release / "extra.txt").write_text("x", encoding="utf-8")
        code, out = self.run_cli("check-release")
        self.assertEqual(code, 1)
        self.assertIn("Checksum mismatch: bom.csv", out)
        self.assertIn("File not in manifest: extra.txt", out)

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


if __name__ == "__main__":
    unittest.main()
