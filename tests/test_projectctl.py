import copy
import unittest

from scripts.projectctl import StateError, gate_errors, validate_state


class ProjectGateTests(unittest.TestCase):
    def setUp(self):
        def pending_record():
            return {"status": "PENDING", "revision": None, "evidence": None}

        # Keep unit tests independent of a user's evolving live project state.
        self.pending = {
            "schema_version": 2,
            "project_name": None,
            "requirements_revision": None,
            "pcb_requirements_revision": None,
            "design_revision": None,
            "input_approval": pending_record(),
            "pcb_input_approval": pending_record(),
            "reviews": {
                key: pending_record() for key in ("schematic", "pcb", "manufacturing")
            },
            "export_approval": pending_record(),
            "blocking_issues": [],
        }

    def approved(self):
        state = copy.deepcopy(self.pending)
        state["project_name"] = "Test fixture"
        state["requirements_revision"] = "REQ-1"
        state["pcb_requirements_revision"] = "PCB-REQ-1"
        state["design_revision"] = "R1"
        state["input_approval"] = {
            "status": "APPROVED", "revision": "REQ-1", "evidence": "test fixture G0"
        }
        state["pcb_input_approval"] = {
            "status": "APPROVED", "revision": "PCB-REQ-1", "evidence": "test fixture G0.5"
        }
        for key in ("schematic", "pcb"):
            state["reviews"][key] = {
                "status": "PASS", "revision": "R1", "evidence": "test fixture review"
            }
        state["export_approval"] = {
            "status": "APPROVED", "revision": "R1", "evidence": "test fixture G1"
        }
        return state

    def test_pending_project_is_valid_but_cannot_export(self):
        self.assertIs(validate_state(self.pending), self.pending)
        self.assertTrue(gate_errors(self.pending))
        self.assertTrue(gate_errors(self.pending, layout=True))
        self.assertTrue(gate_errors(self.pending, release=True))

    def test_export_approved_but_release_pending(self):
        state = self.approved()
        self.assertEqual(gate_errors(state), [])
        self.assertTrue(gate_errors(state, release=True))

    def test_release_requires_manufacturing_review(self):
        state = self.approved()
        state["reviews"]["manufacturing"] = {
            "status": "PASS", "revision": "R1", "evidence": "test fixture manufacturing review"
        }
        self.assertEqual(gate_errors(state, release=True), [])

    def test_layout_can_start_without_pcb_review_or_export_approval(self):
        state = self.approved()
        for record in (state["reviews"]["pcb"], state["export_approval"]):
            record.update(status="PENDING", revision=None, evidence=None)
        self.assertEqual(gate_errors(state, layout=True), [])
        self.assertTrue(gate_errors(state))

    def test_layout_requires_pcb_input_approval(self):
        state = self.approved()
        state["pcb_input_approval"].update(status="PENDING", revision=None, evidence=None)
        self.assertTrue(any("G0.5" in error for error in gate_errors(state, layout=True)))
        self.assertTrue(any("G0.5" in error for error in gate_errors(state)))

    def test_pcb_requirements_change_invalidates_layout_and_export(self):
        state = self.approved()
        state["pcb_requirements_revision"] = "PCB-REQ-2"
        self.assertTrue(any("G0.5" in error for error in gate_errors(state, layout=True)))
        self.assertTrue(any("G0.5" in error for error in gate_errors(state)))

    def test_layout_requires_current_schematic_review(self):
        state = self.approved()
        state["design_revision"] = "R2"
        self.assertTrue(any("Schematic review" in error for error in gate_errors(state, layout=True)))

    def test_missing_pcb_approval_record_is_invalid(self):
        state = self.approved()
        del state["pcb_input_approval"]
        with self.assertRaises(StateError):
            validate_state(state)

    def test_new_design_revision_invalidates_previous_reviews_and_approval(self):
        state = self.approved()
        state["design_revision"] = "R2"
        errors = gate_errors(state)
        self.assertTrue(any("G1" in error for error in errors))
        self.assertTrue(any("Schematic review" in error for error in errors))
        self.assertTrue(any("PCB review" in error for error in errors))

    def test_changed_requirements_invalidate_input_approval(self):
        state = self.approved()
        state["requirements_revision"] = "REQ-2"
        self.assertTrue(any("G0" in error for error in gate_errors(state)))

    def test_blockers_prevent_export(self):
        state = self.approved()
        state["blocking_issues"] = ["REV-001"]
        self.assertTrue(any("REV-001" in error for error in gate_errors(state)))

    def test_review_rework_prevents_export(self):
        state = self.approved()
        state["reviews"]["pcb"]["status"] = "REWORK"
        self.assertTrue(any("PCB review" in error for error in gate_errors(state)))

    def test_approved_record_without_evidence_is_invalid(self):
        state = self.approved()
        state["export_approval"]["evidence"] = None
        with self.assertRaises(StateError):
            validate_state(state)

    def test_invalid_status_is_rejected(self):
        state = self.approved()
        state["reviews"]["pcb"]["status"] = "UNKNOWN"
        with self.assertRaises(StateError):
            validate_state(state)

    def test_missing_review_is_invalid(self):
        state = self.approved()
        del state["reviews"]["pcb"]
        with self.assertRaises(StateError):
            validate_state(state)


if __name__ == "__main__":
    unittest.main()
