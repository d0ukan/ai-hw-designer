"""Dependency-free workflow checks and record keeping.

Checks never export or change design files. Record commands (set, approve,
revoke, review, block, unblock) only update project/workflow-state.json after
validating it. The manifest command only writes Manufacturing/<rev>/MANIFEST.sha256.
"""

import argparse
import datetime
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE = ROOT / "project" / "workflow-state.json"
DEFAULT_MANUFACTURING = ROOT / "Manufacturing"
MANIFEST_NAME = "MANIFEST.sha256"

APPROVAL_STATES = {"PENDING", "APPROVED"}
REVIEW_STATES = {"PENDING", "PASS", "REWORK", "BLOCKED"}
REVIEW_KEYS = ("schematic", "pcb", "manufacturing")
TEXT_FIELDS = ("project_name", "requirements_revision", "pcb_requirements_revision", "design_revision")
OPTIONAL_RECORD_FIELDS = ("recorded_on", "recorded_by")
GATES = {"G0": "input_approval", "G0.5": "pcb_input_approval", "G1": "export_approval"}


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

    for key in TEXT_FIELDS:
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
        for field in OPTIONAL_RECORD_FIELDS:
            if field in record and record[field] is not None and not nonempty_text(record[field]):
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


def save_state(path, state):
    """Validate, then atomically write the state file (UTF-8, LF, 2-space indent)."""
    validate_state(state)
    path = Path(path)
    text = json.dumps(state, indent=2, ensure_ascii=False) + "\n"
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".state-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


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


# --- Record updates (pure functions on a state dict) -------------------------

def _today():
    return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


def _set_record(record, status, accepted, revision, evidence, by):
    if status == "PENDING":
        record.update(status="PENDING", revision=None, evidence=None)
        for field in OPTIONAL_RECORD_FIELDS:
            record.pop(field, None)
        return
    if status == accepted and not (nonempty_text(revision) and nonempty_text(evidence)):
        raise StateError(f"{status} requires --revision and --evidence.")
    record.update(
        status=status,
        revision=revision if nonempty_text(revision) else None,
        evidence=evidence if nonempty_text(evidence) else None,
        recorded_on=_today(),
        recorded_by=by if nonempty_text(by) else None,
    )


def set_field(state, field, value):
    if field not in TEXT_FIELDS:
        raise StateError(f"Unknown field: {field}")
    state[field] = value if nonempty_text(value) else None
    return validate_state(state)


def approve(state, gate, revision, evidence, by=None):
    _set_record(state[GATES[gate]], "APPROVED", "APPROVED", revision, evidence, by)
    return validate_state(state)


def revoke(state, gate):
    _set_record(state[GATES[gate]], "PENDING", "APPROVED", None, None, None)
    return validate_state(state)


def record_review(state, kind, status, revision=None, evidence=None, by=None):
    if kind not in REVIEW_KEYS:
        raise StateError(f"Unknown review: {kind}")
    if status not in REVIEW_STATES:
        raise StateError(f"Unknown review status: {status}")
    _set_record(state["reviews"][kind], status, "PASS", revision, evidence, by)
    return validate_state(state)


def block(state, issue_id):
    if not nonempty_text(issue_id):
        raise StateError("Issue ID must be nonempty.")
    if issue_id not in state["blocking_issues"]:
        state["blocking_issues"].append(issue_id)
    return validate_state(state)


def unblock(state, issue_id):
    if issue_id not in state["blocking_issues"]:
        raise StateError(f"{issue_id} is not an open blocking issue.")
    state["blocking_issues"].remove(issue_id)
    return validate_state(state)


# --- Manufacturing manifest --------------------------------------------------

def release_dir(manufacturing_dir, revision):
    if not nonempty_text(revision):
        raise StateError("design_revision is not set.")
    if any(ch in revision for ch in "/\\:") or revision in (".", ".."):
        raise StateError("design_revision cannot be used as a folder name.")
    return Path(manufacturing_dir) / revision


def _sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _release_files(folder):
    return sorted(
        p.relative_to(folder).as_posix()
        for p in folder.rglob("*")
        if p.is_file() and p.name != MANIFEST_NAME
    )


def write_manifest(folder):
    """Write MANIFEST.sha256 (sha256sum format) for every file in folder."""
    folder = Path(folder)
    if not folder.is_dir():
        raise StateError(f"Release folder not found: {folder}")
    files = _release_files(folder)
    if not files:
        raise StateError(f"Release folder is empty: {folder}")
    lines = [f"{_sha256(folder / rel)}  {rel}" for rel in files]
    with (folder / MANIFEST_NAME).open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")
    return len(files)


def manifest_errors(folder):
    """Return problems with the release folder's manifest; empty list means OK."""
    folder = Path(folder)
    manifest = folder / MANIFEST_NAME
    if not manifest.is_file():
        return [f"Manifest missing: {manifest}"]
    listed = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, sep, rel = line.partition("  ")
        if not sep:
            return [f"Malformed manifest line: {line}"]
        listed[rel] = digest
    errors = []
    for rel, digest in listed.items():
        path = folder / rel
        if not path.is_file():
            errors.append(f"Listed file missing: {rel}")
        elif _sha256(path) != digest:
            errors.append(f"Checksum mismatch: {rel}")
    for rel in _release_files(folder):
        if rel not in listed:
            errors.append(f"File not in manifest: {rel}")
    return errors


# --- CLI ---------------------------------------------------------------------

def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--state", type=Path, default=DEFAULT_STATE, help="Path to workflow-state.json")
    common.add_argument("--manufacturing-dir", type=Path, default=DEFAULT_MANUFACTURING,
                        help="Path to the Manufacturing folder")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("status", "validate", "check-layout", "check-export", "check-release", "manifest"):
        sub.add_parser(name, parents=[common])

    p = sub.add_parser("set", parents=[common], help="Set a revision or project name (omit value to clear)")
    p.add_argument("field", choices=TEXT_FIELDS)
    p.add_argument("value", nargs="?")

    p = sub.add_parser("approve", parents=[common], help="Record a real user approval")
    p.add_argument("gate", choices=tuple(GATES))
    p.add_argument("--revision", required=True)
    p.add_argument("--evidence", required=True)
    p.add_argument("--by")

    p = sub.add_parser("revoke", parents=[common], help="Reset an approval to PENDING")
    p.add_argument("gate", choices=tuple(GATES))

    p = sub.add_parser("review", parents=[common], help="Record a Reviewer result")
    p.add_argument("kind", choices=REVIEW_KEYS)
    p.add_argument("status", choices=sorted(REVIEW_STATES))
    p.add_argument("--revision")
    p.add_argument("--evidence")
    p.add_argument("--by")

    for name in ("block", "unblock"):
        p = sub.add_parser(name, parents=[common])
        p.add_argument("issue_id")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        state = load_state(args.state)
        cmd = args.command

        if cmd == "validate":
            print("VALID: workflow state schema.")
            return 0
        if cmd == "status":
            print("Project:", state["project_name"] or "not started")
            print("Requirements revision:", state["requirements_revision"] or "not set")
            print("PCB requirements revision:", state["pcb_requirements_revision"] or "not set")
            print("Design revision:", state["design_revision"] or "not set")
            print("Layout gate:", "BLOCKED" if gate_errors(state, layout=True) else "READY")
            print("Export gate:", "BLOCKED" if gate_errors(state) else "READY")
            print("Release gate:", "BLOCKED" if gate_errors(state, release=True) else "READY")
            print("Blocking issues:", ", ".join(state["blocking_issues"]) or "none")
            return 0

        if cmd in ("set", "approve", "revoke", "review", "block", "unblock"):
            if cmd == "set":
                set_field(state, args.field, args.value)
            elif cmd == "approve":
                approve(state, args.gate, args.revision, args.evidence, args.by)
            elif cmd == "revoke":
                revoke(state, args.gate)
            elif cmd == "review":
                record_review(state, args.kind, args.status, args.revision, args.evidence, args.by)
            elif cmd == "block":
                block(state, args.issue_id)
            else:
                unblock(state, args.issue_id)
            save_state(args.state, state)
            print(f"UPDATED: {cmd} recorded in {args.state.name}.")
            return 0

        if cmd == "manifest":
            folder = release_dir(args.manufacturing_dir, state["design_revision"])
            count = write_manifest(folder)
            print(f"MANIFEST: {count} files hashed in {folder / MANIFEST_NAME}.")
            return 0

        layout = cmd == "check-layout"
        release = cmd == "check-release"
        errors = gate_errors(state, layout=layout, release=release)
        if release and nonempty_text(state["design_revision"]):
            errors += manifest_errors(release_dir(args.manufacturing_dir, state["design_revision"]))
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
