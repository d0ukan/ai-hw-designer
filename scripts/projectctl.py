"""Dependency-free workflow checks. This tool never exports or changes files."""

import argparse
import json
import sys
from pathlib import Path


DEFAULT_STATE = Path(__file__).resolve().parents[1] / "project" / "workflow-state.json"
APPROVAL_STATES = {"PENDING", "APPROVED"}
REVIEW_STATES = {"PENDING", "PASS", "REWORK", "BLOCKED"}
REVIEW_KEYS = ("schematic", "pcb", "manufacturing")


class StateError(ValueError):
    """Invalid or unreadable workflow-state file."""


def nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def validate_state(state):
    """Validate the schema without treating a new, pending project as invalid."""
    if not isinstance(state, dict):
        raise StateError("State must be a JSON object.")
    if type(state.get("schema_version")) is not int or state["schema_version"] != 2:
        raise StateError("Unsupported or missing schema_version (expected 2; see project/README.md).")

    for key in ("project_name", "requirements_revision", "pcb_requirements_revision", "design_revision"):
        if key not in state or (
            state[key] is not None and not nonempty_text(state[key])
        ):
            raise StateError(f"{key} must be a nonempty string or null.")

    def validate_record(record, name, statuses, accepted):
        if not isinstance(record, dict):
            raise StateError(f"{name} must be an object.")
        status = record.get("status")
        if not isinstance(status, str) or status not in statuses:
            raise StateError(f"{name}.status is invalid.")
        for field in ("revision", "evidence"):
            if field not in record or (
                record[field] is not None and not nonempty_text(record[field])
            ):
                raise StateError(f"{name}.{field} must be a nonempty string or null.")
        if status == accepted and not (
            nonempty_text(record["revision"]) and nonempty_text(record["evidence"])
        ):
            raise StateError(f"{name} {accepted} requires a revision and evidence.")

    validate_record(state.get("input_approval"), "input_approval", APPROVAL_STATES, "APPROVED")
    validate_record(state.get("pcb_input_approval"), "pcb_input_approval", APPROVAL_STATES, "APPROVED")
    validate_record(state.get("export_approval"), "export_approval", APPROVAL_STATES, "APPROVED")
    reviews = state.get("reviews")
    if not isinstance(reviews, dict):
        raise StateError("reviews must be an object.")
    for key in REVIEW_KEYS:
        validate_record(reviews.get(key), f"reviews.{key}", REVIEW_STATES, "PASS")

    blockers = state.get("blocking_issues")
    if not isinstance(blockers, list) or not all(nonempty_text(x) for x in blockers):
        raise StateError("blocking_issues must be an array of nonempty issue IDs.")
    if len(blockers) != len(set(blockers)):
        raise StateError("blocking_issues contains duplicate IDs.")
    return state


def load_state(path):
    """Load a valid UTF-8 state file."""
    try:
        with Path(path).open(encoding="utf-8") as handle:
            state = json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise StateError(f"Cannot read state: {exc}") from exc
    return validate_state(state)


def gate_errors(state, *, layout=False, release=False):
    """Return unmet conditions for layout, export or final manufacturing release."""
    if layout and release:
        raise ValueError("Choose one gate.")
    validate_state(state)
    errors = []
    requirements = state["requirements_revision"]
    pcb_requirements = state["pcb_requirements_revision"]
    design = state["design_revision"]
    if not nonempty_text(state["project_name"]):
        errors.append("Project name is missing.")
    if not nonempty_text(requirements):
        errors.append("Requirements revision is missing.")
    if not nonempty_text(pcb_requirements):
        errors.append("PCB requirements revision is missing.")
    if not nonempty_text(design):
        errors.append("Design revision is missing.")

    def check_record(record, label, expected_status, revision):
        if record["status"] != expected_status:
            errors.append(f"{label}: requires {expected_status}.")
        elif not nonempty_text(revision) or record["revision"] != revision:
            errors.append(f"{label}: revision does not match the current revision.")

    check_record(state["input_approval"], "G0 input approval", "APPROVED", requirements)
    check_record(state["pcb_input_approval"], "G0.5 PCB input approval", "APPROVED", pcb_requirements)
    check_record(state["reviews"]["schematic"], "Schematic review", "PASS", design)
    if not layout:
        check_record(state["reviews"]["pcb"], "PCB review", "PASS", design)
        check_record(state["export_approval"], "G1 export approval", "APPROVED", design)
    if state["blocking_issues"]:
        errors.append("Open blocking issues: " + ", ".join(state["blocking_issues"]))
    if release:
        check_record(state["reviews"]["manufacturing"], "Manufacturing review", "PASS", design)
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("status", "validate", "check-layout", "check-export", "check-release"))
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE, help="Path to workflow-state.json")
    args = parser.parse_args(argv)
    try:
        state = load_state(args.state)
        if args.command == "validate":
            print("VALID: workflow state schema.")
            return 0
        if args.command == "status":
            print("Project:", state["project_name"] or "not started")
            print("Requirements revision:", state["requirements_revision"] or "not set")
            print("PCB requirements revision:", state["pcb_requirements_revision"] or "not set")
            print("Design revision:", state["design_revision"] or "not set")
            print("Layout gate:", "BLOCKED" if gate_errors(state, layout=True) else "READY")
            print("Export gate:", "BLOCKED" if gate_errors(state) else "READY")
            print("Release gate:", "BLOCKED" if gate_errors(state, release=True) else "READY")
            return 0

        layout = args.command == "check-layout"
        release = args.command == "check-release"
        errors = gate_errors(state, layout=layout, release=release)
        label = "LAYOUT" if layout else ("RELEASE" if release else "EXPORT")
        if errors:
            print(f"{label} BLOCKED:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print(f"{label} READY: recorded approvals and review revisions are consistent.")
        return 0
    except StateError as exc:
        print(f"INVALID STATE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
