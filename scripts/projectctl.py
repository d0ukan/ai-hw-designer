"""Dependency-free workflow checks and record keeping.

Checks never export or change design files. Record commands (set, approve,
revoke, review, block, unblock) only update project/workflow-state.json after
validating it. The manifest command only writes Manufacturing/<rev>/MANIFEST.sha256.
The name command prints the output file prefix, e.g. DR00627-R01 or DR00627-AV-R01.
check-bom checks BOM/PnP files without changing them.

When the project is a git repository, approvals and reviews also store the git
commit they were recorded at. Export and release checks then fail if the design
files under Hardware/ changed after that commit, so a review cannot silently
cover a later design change.
"""

import argparse
import csv
import datetime
import hashlib
import json
import os
import re
import subprocess
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
OPTIONAL_RECORD_FIELDS = ("recorded_on", "recorded_by", "commit")
RESERVED_RELEASE_NAMES = {"templates"}
DESIGN_DIR = "Hardware"
SCHEMATIC_GLOBS = ("*.kicad_sch", "*.SchDoc", "*.sch")
OPTIONAL_TEXT_FIELDS = ("project_code",)
SETTABLE_FIELDS = TEXT_FIELDS + OPTIONAL_TEXT_FIELDS
NAME_PART = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.]*$")
VARIANT = re.compile(r"^[A-Z]$")
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
    code = state.get("project_code")
    if code is not None and not (isinstance(code, str) and NAME_PART.match(code)):
        raise StateError("project_code must use letters, digits, '_' or '.' (e.g. DR00627) or be null.")

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


def gate_errors(state, *, layout=False, release=False, changed=None):
    """Return unmet conditions for layout, export or final manufacturing release.

    changed(commit, scope) -> True/False/None reports whether design files
    (scope "schematic" or "design") changed since a recorded commit; None means
    it could not be verified. Records without a commit are not checked.
    """
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
    if not layout and not nonempty_text(state.get("project_code")):
        errors.append("Project code is missing (needed to name outputs).")

    def check_record(record, label, expected_status, revision, scope=None):
        if record["status"] != expected_status:
            errors.append(f"{label}: requires {expected_status}.")
        elif not nonempty_text(revision) or record["revision"] != revision:
            errors.append(f"{label}: revision does not match the current revision.")
        elif scope and changed and nonempty_text(record.get("commit")):
            result = changed(record["commit"], scope)
            if result is None:
                errors.append(f"{label}: cannot verify design files against commit {record['commit'][:12]}.")
            elif result:
                errors.append(f"{label}: design files changed after commit {record['commit'][:12]}; review again.")

    check_record(state["input_approval"], "G0 input approval", "APPROVED", requirements)
    check_record(state["pcb_input_approval"], "G0.5 PCB input approval", "APPROVED", pcb_requirements)
    check_record(state["reviews"]["schematic"], "Schematic review", "PASS", design, "schematic")
    if not layout:
        check_record(state["reviews"]["pcb"], "PCB review", "PASS", design, "design")
        check_record(state["export_approval"], "G1 export approval", "APPROVED", design, "design")
    if state["blocking_issues"]:
        errors.append("Open blocking issues: " + ", ".join(state["blocking_issues"]))
    if release:
        check_record(state["reviews"]["manufacturing"], "Manufacturing review", "PASS", design, "design")
    return errors


# --- Git helpers (optional; everything works without git) --------------------

def git_head(repo_root):
    """Return the current commit hash, or None when git or the repo is missing."""
    try:
        out = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=20,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    head = out.stdout.strip()
    return head if out.returncode == 0 and head else None


def git_change_detector(repo_root):
    """Return changed(commit, scope) for gate_errors, or None without git."""
    if git_head(repo_root) is None:
        return None

    def changed(commit, scope):
        if scope == "schematic":
            paths = [f":(glob){DESIGN_DIR}/**/{g}" for g in SCHEMATIC_GLOBS]
        else:
            paths = [DESIGN_DIR]
        try:
            out = subprocess.run(
                ["git", "-C", str(repo_root), "diff", "--quiet", commit, "--", *paths],
                capture_output=True, timeout=60,
            )
        except (OSError, subprocess.SubprocessError):
            return None
        return {0: False, 1: True}.get(out.returncode)

    return changed


# --- Record updates (pure functions on a state dict) -------------------------

def _today():
    return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


def _set_record(record, status, accepted, revision, evidence, by, commit=None):
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
    if nonempty_text(commit):
        record["commit"] = commit
    else:
        record.pop("commit", None)


def set_field(state, field, value):
    if field not in SETTABLE_FIELDS:
        raise StateError(f"Unknown field: {field}")
    state[field] = value if nonempty_text(value) else None
    return validate_state(state)


def approve(state, gate, revision, evidence, by=None, commit=None):
    _set_record(state[GATES[gate]], "APPROVED", "APPROVED", revision, evidence, by, commit)
    return validate_state(state)


def revoke(state, gate):
    _set_record(state[GATES[gate]], "PENDING", "APPROVED", None, None, None)
    return validate_state(state)


def record_review(state, kind, status, revision=None, evidence=None, by=None, commit=None):
    if kind not in REVIEW_KEYS:
        raise StateError(f"Unknown review: {kind}")
    if status not in REVIEW_STATES:
        raise StateError(f"Unknown review status: {status}")
    _set_record(state["reviews"][kind], status, "PASS", revision, evidence, by, commit)
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


# --- Output naming -----------------------------------------------------------

def output_name(state, variant=None):
    """Return the output prefix: <code>-<rev> or <code>-<variant>V-<rev>."""
    code, rev = state.get("project_code"), state["design_revision"]
    if not nonempty_text(code):
        raise StateError("project_code is not set.")
    if not (nonempty_text(rev) and NAME_PART.match(rev)):
        raise StateError("design_revision is not set or cannot be used in a file name.")
    if variant is None:
        return f"{code}-{rev}"
    if not VARIANT.match(variant):
        raise StateError("Variant must be one capital letter (A-Z).")
    return f"{code}-{variant}V-{rev}"


def naming_errors(folder, state):
    """Release files must start with the project code.

    Files inside a folder whose name starts with the code (for example an
    unzipped DR00627-R01_Gerber/ folder) are accepted as they are. Board-ID
    folders of multi-PCB releases are checked like the top level.
    """
    code = state.get("project_code")
    folder = Path(folder)
    if not nonempty_text(code) or not folder.is_dir():
        return []
    prefix = code + "-"
    errors = []
    for rel in _release_files(folder):
        parts = rel.split("/")
        if any(part.startswith(prefix) for part in parts):
            continue
        errors.append(f"File name does not start with project code {code}: {rel}")
    return errors


# --- BOM / PnP checks ---------------------------------------------------------

BOM_REQUIRED = ("Designator", "Qty", "MPN", "DNP", "Alternate MPN")
PNP_REQUIRED = ("Designator", "Mid X", "Mid Y", "Layer", "Rotation")
DNP_TRUE = {"yes", "y", "true", "1", "dnp", "x"}
NO_ALTERNATE = ("muadil yok", "no alternate")


def _read_csv(path):
    try:
        with Path(path).open(encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    except (OSError, UnicodeError, csv.Error) as exc:
        raise StateError(f"Cannot read {path}: {exc}") from exc


def _designators(text):
    return [d for d in re.split(r"[,;\s]+", text or "") if d]


def _number(text):
    try:
        float((text or "").strip().lower().removesuffix("mm").strip())
        return True
    except ValueError:
        return False


def bom_problems(bom_path, pnp_path=None):
    """Return (errors, warnings) for a BOM and its optional PnP file."""
    errors, warnings = [], []
    bom_name = Path(bom_path).name
    rows = _read_csv(bom_path)
    header = rows[0].keys() if rows else _csv_header(bom_path)
    missing = [c for c in BOM_REQUIRED if c not in header]
    if missing:
        return [f"{bom_name}: missing columns: {', '.join(missing)}"], warnings
    seen, fitted, dnp = set(), set(), set()
    for line, row in enumerate(rows, start=2):
        refs = _designators(row["Designator"])
        if not refs:
            errors.append(f"{bom_name}:{line}: empty Designator.")
            continue
        for ref in refs:
            if ref in seen:
                errors.append(f"{bom_name}:{line}: duplicate designator {ref}.")
            seen.add(ref)
        qty = (row["Qty"] or "").strip()
        if not qty.isdigit() or int(qty) != len(refs):
            errors.append(f"{bom_name}:{line}: Qty {qty or '(empty)'} does not match {len(refs)} designators.")
        is_dnp = (row["DNP"] or "").strip().lower() in DNP_TRUE
        (dnp if is_dnp else fitted).update(refs)
        if not is_dnp and not (row["MPN"] or "").strip():
            errors.append(f"{bom_name}:{line}: fitted part without MPN ({', '.join(refs)}).")
        notes = (row.get("Notes") or "").lower()
        if not is_dnp and not (row["Alternate MPN"] or "").strip() and not any(n in notes for n in NO_ALTERNATE):
            warnings.append(f"{bom_name}:{line}: no Alternate MPN and no 'muadil yok' note ({', '.join(refs)}).")
    if pnp_path is None:
        return errors, warnings
    pnp_name = Path(pnp_path).name
    prow = _read_csv(pnp_path)
    pheader = prow[0].keys() if prow else _csv_header(pnp_path)
    missing = [c for c in PNP_REQUIRED if c not in pheader]
    if missing:
        return errors + [f"{pnp_name}: missing columns: {', '.join(missing)}"], warnings
    placed = set()
    for line, row in enumerate(prow, start=2):
        ref = (row["Designator"] or "").strip()
        if ref in placed:
            errors.append(f"{pnp_name}:{line}: duplicate designator {ref}.")
        placed.add(ref)
        if (row["Layer"] or "").strip().lower() not in ("top", "bottom"):
            errors.append(f"{pnp_name}:{line}: Layer must be Top or Bottom.")
        for col in ("Mid X", "Mid Y", "Rotation"):
            if not _number(row[col]):
                errors.append(f"{pnp_name}:{line}: {col} is not a number.")
    for ref in sorted(placed & dnp):
        errors.append(f"{pnp_name}: DNP part {ref} must not be in PnP.")
    for ref in sorted(fitted - placed):
        errors.append(f"{pnp_name}: fitted part {ref} missing from PnP.")
    for ref in sorted(placed - fitted - dnp):
        errors.append(f"{pnp_name}: {ref} is not in the BOM.")
    return errors, warnings


def _csv_header(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle), [])


def release_bom_problems(folder):
    """Check every *_BOM.csv in a release folder with its matching *_PnP.csv."""
    errors, warnings = [], []
    folder = Path(folder)
    if not folder.is_dir():
        return errors, warnings
    for bom in sorted(folder.rglob("*_BOM.csv")):
        pnp = bom.with_name(bom.name[: -len("_BOM.csv")] + "_PnP.csv")
        e, w = bom_problems(bom, pnp if pnp.is_file() else None)
        errors += e
        warnings += w
    return errors, warnings


# --- Manufacturing manifest --------------------------------------------------

def release_dir(manufacturing_dir, revision):
    if not nonempty_text(revision):
        raise StateError("design_revision is not set.")
    if any(ch in revision for ch in "/\\:") or revision in (".", ".."):
        raise StateError("design_revision cannot be used as a folder name.")
    if revision.lower() in RESERVED_RELEASE_NAMES:
        raise StateError(f"design_revision '{revision}' is a reserved folder name.")
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
    common.add_argument("--repo-root", type=Path, default=ROOT,
                        help="Git repository used to bind approvals to commits")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("status", "validate", "check-layout", "check-export", "check-release", "manifest"):
        sub.add_parser(name, parents=[common])

    p = sub.add_parser("set", parents=[common], help="Set a revision or project name (omit value to clear)")
    p.add_argument("field", choices=SETTABLE_FIELDS)
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

    p = sub.add_parser("check-bom", parents=[common],
                       help="Check a BOM (and PnP); without arguments, every BOM in Manufacturing/<rev>/")
    p.add_argument("bom", nargs="?", type=Path)
    p.add_argument("--pnp", type=Path)

    p = sub.add_parser("name", parents=[common], help="Print the output file prefix")
    p.add_argument("--variant", help="Variant letter, e.g. A -> <code>-AV-<rev>")

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
            print("Project code:", state.get("project_code") or "not set")
            print("Requirements revision:", state["requirements_revision"] or "not set")
            print("PCB requirements revision:", state["pcb_requirements_revision"] or "not set")
            print("Design revision:", state["design_revision"] or "not set")
            changed = git_change_detector(args.repo_root)
            print("Layout gate:", "BLOCKED" if gate_errors(state, layout=True, changed=changed) else "READY")
            print("Export gate:", "BLOCKED" if gate_errors(state, changed=changed) else "READY")
            print("Release gate:", "BLOCKED" if gate_errors(state, release=True, changed=changed) else "READY")
            print("Blocking issues:", ", ".join(state["blocking_issues"]) or "none")
            return 0

        if cmd == "check-bom":
            if args.bom:
                errors, warnings = bom_problems(args.bom, args.pnp)
            else:
                errors, warnings = release_bom_problems(
                    release_dir(args.manufacturing_dir, state["design_revision"]))
            for warning in warnings:
                print(f"WARNING: {warning}")
            if errors:
                print("BOM BLOCKED:", file=sys.stderr)
                for error in errors:
                    print(f"- {error}", file=sys.stderr)
                return 1
            print("BOM OK.")
            return 0

        if cmd in ("set", "approve", "revoke", "review", "block", "unblock"):
            commit = git_head(args.repo_root)
            if cmd == "set":
                set_field(state, args.field, args.value)
            elif cmd == "approve":
                approve(state, args.gate, args.revision, args.evidence, args.by, commit)
            elif cmd == "revoke":
                revoke(state, args.gate)
            elif cmd == "review":
                record_review(state, args.kind, args.status, args.revision, args.evidence, args.by, commit)
            elif cmd == "block":
                block(state, args.issue_id)
            else:
                unblock(state, args.issue_id)
            save_state(args.state, state)
            print(f"UPDATED: {cmd} recorded in {args.state.name}.")
            return 0

        if cmd == "name":
            print(output_name(state, args.variant))
            return 0

        if cmd == "manifest":
            folder = release_dir(args.manufacturing_dir, state["design_revision"])
            count = write_manifest(folder)
            print(f"MANIFEST: {count} files hashed in {folder / MANIFEST_NAME}.")
            return 0

        layout = cmd == "check-layout"
        release = cmd == "check-release"
        errors = gate_errors(state, layout=layout, release=release,
                             changed=git_change_detector(args.repo_root))
        if release and nonempty_text(state["design_revision"]):
            folder = release_dir(args.manufacturing_dir, state["design_revision"])
            bom_errors, bom_warnings = release_bom_problems(folder)
            for warning in bom_warnings:
                print(f"WARNING: {warning}")
            errors += naming_errors(folder, state) + bom_errors + manifest_errors(folder)
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
