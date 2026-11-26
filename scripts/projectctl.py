"""Dependency-free workflow checks and record keeping.

Checks never export or change design files. Record commands (set, deliverables,
approve, revoke, review, block, unblock) only update project/workflow-state.json
after validating it. The manifest command only writes Manufacturing/<rev>/MANIFEST.sha256.
The name command prints the output file prefix, e.g. DR00627-R01 or DR00627-AV-R01.
check-bom checks BOM/PnP files; next prints the next missing step and its command.

When the project is a git repository, approvals and reviews also store the git
commit they were recorded at, and the manufacturing review stores the manifest
hash. Export and release checks then fail if design files under Hardware/
(tracked or new) changed after that commit, or if the release files changed
after the manufacturing review, so a review cannot silently cover a later change.
"""

import argparse
import csv
import datetime
import hashlib
import json
import math
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
SECOND_REVIEW_KEYS = {"schematic": "schematic_2", "pcb": "pcb_2"}
REVIEW_DEPTHS = ("Light", "Medium", "High")
DEFAULT_REVIEW_DEPTH = "Medium"
TEXT_FIELDS = ("project_name", "requirements_revision", "pcb_requirements_revision", "design_revision")
OPTIONAL_TEXT_FIELDS = ("project_code", "review_depth")
SETTABLE_FIELDS = TEXT_FIELDS + OPTIONAL_TEXT_FIELDS
OPTIONAL_RECORD_FIELDS = ("recorded_on", "recorded_by", "commit", "manifest_sha256")
GATES = {"G0": "input_approval", "G0.5": "pcb_input_approval", "G1": "export_approval"}
RESERVED_RELEASE_NAMES = {"templates"}
JUNK_FILES = {"thumbs.db", "desktop.ini", ".ds_store"}

DESIGN_DIR = "Hardware"
SCHEMATIC_GLOBS = ("*.kicad_sch", "*.SchDoc", "*.sch")
# Output-job files that EDA tools rewrite during export; not design changes.
DESIGN_EXCLUDE_GLOBS = ("*.OutJob",)

NAME_PART = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.]*$")
VARIANT = re.compile(r"^[A-Z]$")
COMMIT = re.compile(r"^[0-9a-f]{7,64}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


class StateError(ValueError):
    """Invalid or unreadable workflow-state file."""


class InputError(StateError):
    """Unreadable or malformed input file other than the state (BOM, PnP, manifest)."""


def nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


# --- State schema -------------------------------------------------------------

def validate_state(state):
    """Validate the schema without treating a new, pending project as invalid."""
    if not isinstance(state, dict):
        raise StateError("State must be a JSON object.")
    if type(state.get("schema_version")) is not int or state["schema_version"] != 2:
        raise StateError("Unsupported or missing schema_version (expected 2; see project/README.md).")

    for key in TEXT_FIELDS:
        if key not in state or (state[key] is not None and not nonempty_text(state[key])):
            raise StateError(f"{key} must be a nonempty string or null.")
    code = state.get("project_code")
    if code is not None and not (isinstance(code, str) and NAME_PART.match(code)):
        raise StateError("project_code must use letters, digits, '_' or '.' (e.g. DR00627) or be null.")
    deliverables = state.get("deliverables")
    if deliverables is not None and not (
        isinstance(deliverables, list)
        and all(isinstance(d, str) and NAME_PART.match(d) for d in deliverables)
        and len({d.lower() for d in deliverables}) == len(deliverables)
    ):
        raise StateError("deliverables must be a list of unique names like BOM, PnP, Gerber, or null.")
    depth = state.get("review_depth")
    if depth is not None and depth not in REVIEW_DEPTHS:
        raise StateError("review_depth must be Light, Medium, High or null (null means Medium).")

    def validate_record(record, name, statuses, accepted):
        if not isinstance(record, dict):
            raise StateError(f"{name} must be an object.")
        status = record.get("status")
        if not isinstance(status, str) or status not in statuses:
            raise StateError(f"{name}.status is invalid.")
        for field in ("revision", "evidence"):
            if field not in record or (record[field] is not None and not nonempty_text(record[field])):
                raise StateError(f"{name}.{field} must be a nonempty string or null.")
        for field in OPTIONAL_RECORD_FIELDS:
            if field in record and record[field] is not None and not nonempty_text(record[field]):
                raise StateError(f"{name}.{field} must be a nonempty string or null.")
        if record.get("commit") is not None and not COMMIT.match(record["commit"]):
            raise StateError(f"{name}.commit must be a hexadecimal git commit id.")
        if record.get("manifest_sha256") is not None and not SHA256.match(record["manifest_sha256"]):
            raise StateError(f"{name}.manifest_sha256 must be a SHA-256 hex digest.")
        if status == accepted and not (nonempty_text(record["revision"]) and nonempty_text(record["evidence"])):
            raise StateError(f"{name} {accepted} requires a revision and evidence.")

    validate_record(state.get("input_approval"), "input_approval", APPROVAL_STATES, "APPROVED")
    validate_record(state.get("pcb_input_approval"), "pcb_input_approval", APPROVAL_STATES, "APPROVED")
    validate_record(state.get("export_approval"), "export_approval", APPROVAL_STATES, "APPROVED")
    reviews = state.get("reviews")
    if not isinstance(reviews, dict):
        raise StateError("reviews must be an object.")
    for key in REVIEW_KEYS:
        validate_record(reviews.get(key), f"reviews.{key}", REVIEW_STATES, "PASS")
    for key in SECOND_REVIEW_KEYS.values():
        if key in reviews:
            validate_record(reviews[key], f"reviews.{key}", REVIEW_STATES, "PASS")

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


# --- Gates --------------------------------------------------------------------

def review_depth(state):
    return state.get("review_depth") or DEFAULT_REVIEW_DEPTH


def _pending():
    return {"status": "PENDING", "revision": None, "evidence": None}


def second_review_errors(state, kind, revision, scope, changed=None):
    """High review depth: a second, independent PASS by a different reviewer."""
    if review_depth(state) != "High":
        return []
    first = state["reviews"][kind]
    second = state["reviews"].get(SECOND_REVIEW_KEYS[kind]) or _pending()
    label = "Second schematic review (High depth)" if kind == "schematic" else "Second PCB review (High depth)"
    problem = record_problem(second, label, "PASS", revision, scope, changed)
    if problem:
        return [problem]
    a, b = first.get("recorded_by"), second.get("recorded_by")
    if not (nonempty_text(a) and nonempty_text(b)):
        return [f"{label}: record both reviewers with --by."]
    if a.strip().lower() == b.strip().lower():
        return [f"{label}: must be a different reviewer than the first review."]
    return []


def record_problem(record, label, expected_status, revision, scope=None, changed=None):
    """Return the first problem with one approval/review record, or None."""
    if record["status"] != expected_status:
        return f"{label}: requires {expected_status}."
    if not nonempty_text(revision) or record["revision"] != revision:
        return f"{label}: revision does not match the current revision."
    if scope and changed and nonempty_text(record.get("commit")):
        result = changed(record["commit"], scope)
        if result is None:
            return f"{label}: cannot verify design files against commit {record['commit'][:12]}."
        if result:
            return f"{label}: design files changed after commit {record['commit'][:12]}; review again."
    return None


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

    checks = [
        (state["input_approval"], "G0 input approval", "APPROVED", requirements, None),
        (state["pcb_input_approval"], "G0.5 PCB input approval", "APPROVED", pcb_requirements, None),
        (state["reviews"]["schematic"], "Schematic review", "PASS", design, "schematic"),
    ]
    if not layout:
        checks += [
            (state["reviews"]["pcb"], "PCB review", "PASS", design, "design"),
            (state["export_approval"], "G1 export approval", "APPROVED", design, "design"),
        ]
    if release:
        checks.append((state["reviews"]["manufacturing"], "Manufacturing review", "PASS", design, "design"))
        if not state.get("deliverables"):
            errors.append("Deliverables are not set (e.g. projectctl.py deliverables BOM PnP Gerber SCH ASSY FAB).")
    for record, label, status, revision, scope in checks:
        problem = record_problem(record, label, status, revision, scope, changed)
        if problem:
            errors.append(problem)
    errors += second_review_errors(state, "schematic", design, "schematic", changed)
    if not layout:
        errors += second_review_errors(state, "pcb", design, "design", changed)
    if state["blocking_issues"]:
        errors.append("Open blocking issues: " + ", ".join(state["blocking_issues"]))
    return errors


# --- Git helpers (optional; everything works without git) --------------------

def _git(repo_root, *args, timeout=60):
    try:
        return subprocess.run(["git", "-C", str(repo_root), *args], capture_output=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return None


def default_repo_root(state_path):
    """Project root for a state file: the parent of project/, else its own folder."""
    folder = Path(state_path).resolve().parent
    return folder.parent if folder.name == "project" else folder


def git_head(repo_root):
    """Return the current commit hash, or None when git or the repo is missing."""
    out = _git(repo_root, "rev-parse", "HEAD", timeout=20)
    head = out.stdout.decode().strip() if out else ""
    return head if out and out.returncode == 0 and COMMIT.match(head) else None


def _design_paths(scope):
    if scope == "schematic":
        return [f":(glob){DESIGN_DIR}/**/{g}" for g in SCHEMATIC_GLOBS]
    return [DESIGN_DIR] + [f":(exclude,glob){DESIGN_DIR}/**/{g}" for g in DESIGN_EXCLUDE_GLOBS]


def design_dirty(repo_root):
    """True when Hardware/ has uncommitted or untracked changes; None without git."""
    if git_head(repo_root) is None:
        return None
    out = _git(repo_root, "status", "--porcelain", "--untracked-files=all", "--", *_design_paths("design"))
    if out is None or out.returncode != 0:
        return None
    return bool(out.stdout.strip())


def git_change_detector(repo_root):
    """Return changed(commit, scope) for gate_errors, or None without git."""
    if git_head(repo_root) is None:
        return None

    def changed(commit, scope):
        if not COMMIT.match(commit or ""):
            return None
        paths = _design_paths(scope)
        diff = _git(repo_root, "diff", "--quiet", commit, "--", *paths)
        if diff is None or diff.returncode not in (0, 1):
            return None
        if diff.returncode == 1:
            return True
        new = _git(repo_root, "ls-files", "--others", "--exclude-standard", "--", *paths)
        if new is None or new.returncode != 0:
            return None
        return bool(new.stdout.strip())

    return changed


# --- Record updates (pure functions on a state dict) -------------------------

def _today():
    return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


def _set_record(record, status, accepted, revision, evidence, by, commit=None, extra=None):
    for field in OPTIONAL_RECORD_FIELDS:
        record.pop(field, None)
    if status == "PENDING":
        record.update(status="PENDING", revision=None, evidence=None)
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
    for key, value in (extra or {}).items():
        if value is not None:
            record[key] = value


def set_field(state, field, value):
    if field not in SETTABLE_FIELDS:
        raise StateError(f"Unknown field: {field}")
    if field == "review_depth" and nonempty_text(value):
        value = value.strip().capitalize()
    state[field] = value if nonempty_text(value) else None
    return validate_state(state)


def set_deliverables(state, names):
    state["deliverables"] = list(names) or None
    return validate_state(state)


def approve(state, gate, revision, evidence, by=None, commit=None):
    _set_record(state[GATES[gate]], "APPROVED", "APPROVED", revision, evidence, by, commit)
    return validate_state(state)


def revoke(state, gate):
    _set_record(state[GATES[gate]], "PENDING", "APPROVED", None, None, None)
    return validate_state(state)


def record_review(state, kind, status, revision=None, evidence=None, by=None, commit=None, manifest_sha256=None,
                  second=False):
    if kind not in REVIEW_KEYS:
        raise StateError(f"Unknown review: {kind}")
    if status not in REVIEW_STATES:
        raise StateError(f"Unknown review status: {status}")
    key = kind
    if second:
        if kind not in SECOND_REVIEW_KEYS:
            raise StateError("A second review exists only for schematic and pcb.")
        key = SECOND_REVIEW_KEYS[kind]
        state["reviews"].setdefault(key, _pending())
    _set_record(state["reviews"][key], status, "PASS", revision, evidence, by, commit,
                {"manifest_sha256": manifest_sha256})
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
    return [
        f"File name does not start with project code {code}: {rel}"
        for rel in _release_files(folder)
        if not any(part.startswith(prefix) for part in rel.split("/"))
    ]


def deliverable_errors(folder, state):
    """Every deliverable (e.g. BOM, Gerber) must exist as <code>-..._<name>.* in the release."""
    names = state.get("deliverables") or []
    code = state.get("project_code")
    folder = Path(folder)
    if not names or not nonempty_text(code):
        return []
    files = [rel.split("/")[-1].lower() for rel in _release_files(folder)] if folder.is_dir() else []
    folders = [p.name.lower() for p in folder.rglob("*") if p.is_dir()] if folder.is_dir() else []
    errors = []
    for name in names:
        tag = f"_{name.lower()}"
        found = any(
            entry.startswith(code.lower() + "-") and (entry.split(".")[0].endswith(tag))
            for entry in files + folders
        )
        if not found:
            errors.append(f"Deliverable missing: {code}-..._{name}.* (see deliverables in workflow-state.json)")
    return errors


# --- BOM / PnP checks ---------------------------------------------------------

BOM_REQUIRED = ("Designator", "Qty", "MPN", "DNP", "Alternate MPN")
PNP_REQUIRED = ("Designator", "Mid X", "Mid Y", "Layer", "Rotation")
DNP_TRUE = {"yes", "y", "true", "1", "dnp", "x"}
NO_ALTERNATE = ("muadil yok", "no alternate")
RANGE = re.compile(r"^([A-Za-z]+)(\d+)-(?:\1)?(\d+)$")


def _read_csv(path):
    """Return (header, [(line_number, row_dict)]) with stripped names; skip blank rows."""
    name = Path(path).name
    try:
        with Path(path).open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            header = [h.strip() for h in next(reader, [])]
            rows = []
            for raw in reader:
                if not any(cell.strip() for cell in raw):
                    continue
                rows.append((reader.line_num, dict(zip(header, (c.strip() for c in raw)))))
    except UnicodeError as exc:
        raise InputError(f"{name}: not UTF-8 text; save the CSV as UTF-8 ({exc.reason}).") from exc
    except (OSError, csv.Error) as exc:
        raise InputError(f"Cannot read {name}: {exc}") from exc
    if len(header) == 1 and ";" in header[0]:
        raise InputError(f"{name}: columns are separated by ';'; save the CSV with ',' separators.")
    return header, rows


def _designators(text):
    refs = []
    for token in (t for t in re.split(r"[,;\s]+", text or "") if t):
        match = RANGE.match(token)
        if match and int(match.group(2)) <= int(match.group(3)) and int(match.group(3)) - int(match.group(2)) < 1000:
            refs += [f"{match.group(1)}{n}" for n in range(int(match.group(2)), int(match.group(3)) + 1)]
        else:
            refs.append(token)
    return refs


def _number(text):
    value = (text or "").strip().lower()
    if value.endswith("mm"):
        value = value[:-2].strip()
    try:
        return math.isfinite(float(value))
    except ValueError:
        return False


def bom_problems(bom_path, pnp_path=None):
    """Return (errors, warnings) for a BOM and its optional PnP file."""
    errors, warnings = [], []
    bom_name = Path(bom_path).name
    header, rows = _read_csv(bom_path)
    missing = [c for c in BOM_REQUIRED if c not in header]
    if missing:
        return [f"{bom_name}: missing columns: {', '.join(missing)}"], warnings
    seen, fitted, dnp = set(), set(), set()
    for line, row in rows:
        refs = _designators(row.get("Designator"))
        if not refs:
            errors.append(f"{bom_name}:{line}: empty Designator.")
            continue
        for ref in refs:
            if ref in seen:
                errors.append(f"{bom_name}:{line}: duplicate designator {ref}.")
            seen.add(ref)
        qty = row.get("Qty") or ""
        if not qty.isdigit() or int(qty) != len(refs):
            errors.append(f"{bom_name}:{line}: Qty {qty or '(empty)'} does not match {len(refs)} designators.")
        is_dnp = (row.get("DNP") or "").lower() in DNP_TRUE
        (dnp if is_dnp else fitted).update(refs)
        if not is_dnp and not row.get("MPN"):
            errors.append(f"{bom_name}:{line}: fitted part without MPN ({', '.join(refs)}).")
        notes = (row.get("Notes") or "").lower()
        if not is_dnp and not row.get("Alternate MPN") and not any(n in notes for n in NO_ALTERNATE):
            warnings.append(f"{bom_name}:{line}: no Alternate MPN and no 'no alternate' note ({', '.join(refs)}).")
    if pnp_path is None:
        return errors, warnings
    pnp_name = Path(pnp_path).name
    pheader, prow = _read_csv(pnp_path)
    missing = [c for c in PNP_REQUIRED if c not in pheader]
    if missing:
        return errors + [f"{pnp_name}: missing columns: {', '.join(missing)}"], warnings
    placed = set()
    for line, row in prow:
        ref = row.get("Designator") or ""
        if not ref:
            errors.append(f"{pnp_name}:{line}: empty Designator.")
            continue
        if ref in placed:
            errors.append(f"{pnp_name}:{line}: duplicate designator {ref}.")
        placed.add(ref)
        if (row.get("Layer") or "").lower() not in ("top", "bottom"):
            errors.append(f"{pnp_name}:{line}: Layer must be Top or Bottom.")
        for col in ("Mid X", "Mid Y", "Rotation"):
            if not _number(row.get(col)):
                errors.append(f"{pnp_name}:{line}: {col} is not a finite number.")
    for ref in sorted(placed & dnp):
        errors.append(f"{pnp_name}: DNP part {ref} must not be in PnP.")
    for ref in sorted(fitted - placed):
        errors.append(f"{pnp_name}: fitted part {ref} missing from PnP.")
    for ref in sorted(placed - fitted - dnp):
        errors.append(f"{pnp_name}: {ref} is not in the BOM.")
    return errors, warnings


def release_bom_problems(folder, require=False):
    """Check every *_BOM.csv in a release folder with its matching *_PnP.csv."""
    errors, warnings = [], []
    folder = Path(folder)
    boms = sorted(p for p in folder.rglob("*") if p.is_file() and p.name.lower().endswith("_bom.csv")) \
        if folder.is_dir() else []
    if require and not boms:
        return [f"No *_BOM.csv found in {folder}"], warnings
    for bom in boms:
        stem = bom.name[: -len("_BOM.csv")].lower()
        pnp = next((p for p in bom.parent.iterdir()
                    if p.is_file() and p.name.lower() == f"{stem}_pnp.csv"), None)
        e, w = bom_problems(bom, pnp)
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
        for p in Path(folder).rglob("*")
        if p.is_file() and p.name != MANIFEST_NAME and p.name.lower() not in JUNK_FILES
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


def manifest_hash(folder):
    manifest = Path(folder) / MANIFEST_NAME
    return _sha256(manifest) if manifest.is_file() else None


def manifest_errors(folder):
    """Return problems with the release folder's manifest; empty list means OK."""
    folder = Path(folder)
    manifest = folder / MANIFEST_NAME
    if not manifest.is_file():
        return [f"Manifest missing: {manifest}"]
    try:
        text = manifest.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"Manifest unreadable: {exc}"]
    listed = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        digest, sep, rel = line.partition("  ")
        parts = rel.replace("\\", "/").split("/")
        if not sep or not SHA256.match(digest) or rel.startswith(("/", "\\")) or ".." in parts or ":" in rel:
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


def manufacturing_review_errors(folder, state):
    """The manufacturing PASS must cover the current manifest."""
    record = state["reviews"]["manufacturing"]
    if record["status"] != "PASS" or not record.get("manifest_sha256"):
        return []
    if manifest_hash(folder) != record["manifest_sha256"]:
        return ["Manufacturing review: release files or manifest changed after the review; review again."]
    return []


# --- Next step ----------------------------------------------------------------

def next_step(state, folder, changed=None):
    """Return (who, what, command) for the first missing workflow step, or None."""
    design = state["design_revision"] or "<R01>"
    steps = [
        (not nonempty_text(state["project_name"]), "Manager", "Record the project name",
         'python scripts/projectctl.py set project_name "<name>"'),
        (not nonempty_text(state.get("project_code")), "Manager", "Record the project code",
         "python scripts/projectctl.py set project_code <DR00627>"),
        (not nonempty_text(state["design_revision"]), "Manager", "Record the design revision",
         "python scripts/projectctl.py set design_revision <R01>"),
        (not nonempty_text(state["requirements_revision"]), "Manager", "Record the requirements revision",
         "python scripts/projectctl.py set requirements_revision <REQ-1>"),
        (not state.get("review_depth") and state["input_approval"]["status"] != "APPROVED", "Manager",
         "Ask the user for the review depth (INT-53: Light / Medium / High)",
         "python scripts/projectctl.py set review_depth <Medium>"),
    ]
    for cond, who, what, cmd in steps:
        if cond:
            return who, what, cmd
    req, pcb = state["requirements_revision"], state["pcb_requirements_revision"]
    ordered = [
        (state["input_approval"], "G0 input approval", "APPROVED", req, None,
         "Manager", "Record the user's G0 approval",
         f'python scripts/projectctl.py approve G0 --revision {req} --evidence "<approval reference>"'),
        (state["reviews"]["schematic"], "Schematic review", "PASS", design, "schematic",
         "Reviewer", "Review the schematic; commit the design; record the result",
         f'python scripts/projectctl.py review schematic PASS --revision {design} --evidence "REVIEW_LOG.md#..."'),
    ]
    for record, label, status, rev, scope, who, what, cmd in ordered:
        if record_problem(record, label, status, rev, scope, changed):
            return who, what, cmd
    if second_review_errors(state, "schematic", design, "schematic", changed):
        return "Reviewer 2", "Independent second schematic review (VER-13, clean context)", \
            f'python scripts/projectctl.py review schematic PASS --second --by "<reviewer 2>" --revision {design} --evidence "REVIEW_LOG.md#..."'
    if not nonempty_text(pcb):
        return "Manager", "Record the PCB input revision (G0.5 questions)", \
            "python scripts/projectctl.py set pcb_requirements_revision <PCB-1>"
    ordered = [
        (state["pcb_input_approval"], "G0.5", "APPROVED", pcb, None,
         "Manager", "Ask if the user wants to check the schematic (SCH-08); record the user's G0.5 approval; then layout",
         f'python scripts/projectctl.py approve G0.5 --revision {pcb} --evidence "<approval reference>"'),
        (state["reviews"]["pcb"], "PCB review", "PASS", design, "design",
         "Reviewer", "Review the PCB; commit the design; record the result",
         f'python scripts/projectctl.py review pcb PASS --revision {design} --evidence "REVIEW_LOG.md#..."'),
    ]
    for record, label, status, rev, scope, who, what, cmd in ordered:
        if record_problem(record, label, status, rev, scope, changed):
            return who, what, cmd
    if second_review_errors(state, "pcb", design, "design", changed):
        return "Reviewer 2", "Independent second PCB review (VER-13, clean context)", \
            f'python scripts/projectctl.py review pcb PASS --second --by "<reviewer 2>" --revision {design} --evidence "REVIEW_LOG.md#..."'
    if record_problem(state["export_approval"], "G1", "APPROVED", design, "design", changed):
        return ("Manager", "Ask if the user wants to check the PCB (LAY-32); record the user's G1 export approval",
                f'python scripts/projectctl.py approve G1 --revision {design} --evidence "<approval reference>"')

    if not state.get("deliverables"):
        return "Manager", "Record the deliverables (INT-25)", \
            "python scripts/projectctl.py deliverables BOM PnP Gerber SCH ASSY FAB"
    if deliverable_errors(folder, state) or not Path(folder).is_dir():
        return "Designer", "Create the outputs in Manufacturing/<rev>/ with the prefix; then check-bom", \
            "python scripts/projectctl.py check-bom"
    if manifest_errors(folder):
        return "Designer", "Write the manifest (last export step)", "python scripts/projectctl.py manifest"
    if record_problem(state["reviews"]["manufacturing"], "Manufacturing review", "PASS", design, "design", changed) \
            or manufacturing_review_errors(folder, state):
        return "Reviewer", "Review the manufacturing files; the Manager records the result", \
            f'python scripts/projectctl.py review manufacturing PASS --revision {design} --evidence "REVIEW_LOG.md#..."'
    if state["blocking_issues"]:
        return "Designer", "Close the open blocking findings", "python scripts/projectctl.py unblock <F-001>"
    return None


# --- CLI ---------------------------------------------------------------------

def _add_common(parser, suppress=False):
    default = (lambda value: argparse.SUPPRESS) if suppress else (lambda value: value)
    parser.add_argument("--state", type=Path, default=default(DEFAULT_STATE), help="Path to workflow-state.json")
    parser.add_argument("--manufacturing-dir", type=Path, default=default(None),
                        help="Path to the Manufacturing folder (default: next to the project)")
    parser.add_argument("--repo-root", type=Path, default=default(None),
                        help="Git repository root used to bind records to commits (default: the project root)")


def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    _add_common(common, suppress=True)

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    _add_common(parser)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("status", "validate", "check-layout", "check-export", "check-release", "manifest", "next"):
        sub.add_parser(name, parents=[common])

    p = sub.add_parser("set", parents=[common], help="Set a revision, project name or code (omit value to clear)")
    p.add_argument("field", choices=SETTABLE_FIELDS)
    p.add_argument("value", nargs="?")

    p = sub.add_parser("deliverables", parents=[common],
                       help="Set the required outputs, e.g. BOM PnP Gerber SCH ASSY FAB (none clears)")
    p.add_argument("names", nargs="*")

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
    p.add_argument("--second", action="store_true",
                   help="Record the independent second review (review_depth High; schematic or pcb)")

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


def _print_problems(label, errors, warnings=()):
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        print(f"{label} BLOCKED:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    return 0


def main(argv=None):
    args = build_parser().parse_args(argv)
    project_root = default_repo_root(args.state)
    repo_root = args.repo_root or project_root
    manufacturing = args.manufacturing_dir or (project_root / "Manufacturing")
    try:
        state = load_state(args.state)
        cmd = args.command
        changed = git_change_detector(repo_root)

        if cmd == "validate":
            print("VALID: workflow state schema.")
            return 0
        if cmd == "status":
            print("Project:", state["project_name"] or "not started")
            print("Project code:", state.get("project_code") or "not set")
            print("Requirements revision:", state["requirements_revision"] or "not set")
            print("PCB requirements revision:", state["pcb_requirements_revision"] or "not set")
            print("Design revision:", state["design_revision"] or "not set")
            print("Deliverables:", " ".join(state.get("deliverables") or []) or "not set")
            print("Review depth:", state.get("review_depth") or f"not set ({DEFAULT_REVIEW_DEPTH})")
            print("Layout gate:", "BLOCKED" if gate_errors(state, layout=True, changed=changed) else "READY")
            print("Export gate:", "BLOCKED" if gate_errors(state, changed=changed) else "READY")
            print("Release gate:", "BLOCKED" if gate_errors(state, release=True, changed=changed) else "READY")
            print("Blocking issues:", ", ".join(state["blocking_issues"]) or "none")
            return 0

        if cmd == "next":
            folder = (manufacturing / state["design_revision"]) if nonempty_text(state["design_revision"]) \
                else manufacturing / "_"
            step = next_step(state, folder, changed)
            if step is None:
                print("NEXT: nothing missing; run check-release to confirm.")
            else:
                who, what, command = step
                print(f"NEXT ({who}): {what}\n  {command}")
            return 0

        if cmd == "check-bom":
            if args.bom:
                errors, warnings = bom_problems(args.bom, args.pnp)
            else:
                errors, warnings = release_bom_problems(
                    release_dir(manufacturing, state["design_revision"]), require=True)
            if _print_problems("BOM", errors, warnings):
                return 1
            print("BOM OK.")
            return 0

        if cmd in ("set", "deliverables", "approve", "revoke", "review", "block", "unblock"):
            commit = git_head(repo_root)
            design_record = (cmd == "review" and args.status == "PASS") or (cmd == "approve" and args.gate == "G1")
            if design_record and design_dirty(repo_root):
                raise StateError(f"Uncommitted changes under {DESIGN_DIR}/; commit the reviewed design first.")
            if cmd == "set":
                set_field(state, args.field, args.value)
            elif cmd == "deliverables":
                set_deliverables(state, args.names)
            elif cmd == "approve":
                approve(state, args.gate, args.revision, args.evidence, args.by, commit)
            elif cmd == "revoke":
                revoke(state, args.gate)
            elif cmd == "review":
                digest = None
                if args.kind == "manufacturing" and args.status == "PASS":
                    folder = release_dir(manufacturing, state["design_revision"])
                    if manifest_errors(folder):
                        raise StateError("Write a valid manifest before the manufacturing PASS "
                                         "(projectctl.py manifest), then review those files.")
                    digest = manifest_hash(folder)
                record_review(state, args.kind, args.status, args.revision, args.evidence, args.by, commit, digest,
                              args.second)
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
            folder = release_dir(manufacturing, state["design_revision"])
            count = write_manifest(folder)
            print(f"MANIFEST: {count} files hashed in {folder / MANIFEST_NAME}.")
            return 0

        layout = cmd == "check-layout"
        release = cmd == "check-release"
        errors = gate_errors(state, layout=layout, release=release, changed=changed)
        warnings = []
        if release and nonempty_text(state["design_revision"]):
            folder = release_dir(manufacturing, state["design_revision"])
            bom_errors, warnings = release_bom_problems(folder)
            errors += (naming_errors(folder, state) + deliverable_errors(folder, state) + bom_errors
                       + manifest_errors(folder) + manufacturing_review_errors(folder, state))
        label = "LAYOUT" if layout else ("RELEASE" if release else "EXPORT")
        if _print_problems(label, errors, warnings):
            return 1
        print(f"{label} READY: recorded approvals and review revisions are consistent.")
        return 0
    except InputError as exc:
        print(f"INPUT ERROR: {exc}", file=sys.stderr)
        return 2
    except StateError as exc:
        print(f"INVALID STATE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    for _stream in (sys.stdout, sys.stderr):
        try:  # same UTF-8 output on Windows, macOS and Linux, also when piped
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    raise SystemExit(main())
