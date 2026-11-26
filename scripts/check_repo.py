"""Dependency-free consistency checks for this template repository.

Checks rule IDs (unique, every reference defined, index ranges match the rule
files), relative Markdown links, version lines in both READMEs, and CSV files.
Run: python scripts/check_repo.py    Exit code 0 = OK, 1 = problems found.
"""

import csv
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
RULE_FILES = sorted((ROOT / "rules").glob("*.md")) + [ROOT / "Hardware-Roles.md"]
RULE_DEF = re.compile(r"^- \[[ xX]\] \*\*([A-Z]{2,4})-(\d+)\*\*", re.M)
REF = re.compile(r"\b([A-Z]{2,4})-(\d{2,3})\b")
LINK = re.compile(r"\]\(<?([^)>\s#]+)>?(?:#[^)]*)?\)")
FENCE = re.compile(r"```.*?```", re.S)
SKIP_DIRS = {".git", "__pycache__", ".venv"}
INDEX_ROW = re.compile(r"^\| \[[^\]]+\]\((rules/[^)]+)\) \| ([^|]*)\|", re.M)
RANGE = re.compile(r"([A-Z]{2,4})-(\d+)…\1-(\d+)")


def markdown_files():
    return [p for p in ROOT.rglob("*.md") if not SKIP_DIRS & set(p.relative_to(ROOT).parts)]


def rule_problems():
    problems, defined = [], {}
    for path in RULE_FILES:
        for prefix, number in RULE_DEF.findall(path.read_text(encoding="utf-8")):
            rule_id = f"{prefix}-{number}"
            if rule_id in defined:
                problems.append(f"Duplicate rule {rule_id}: {defined[rule_id]} and {path.name}")
            defined[rule_id] = path.name
    prefixes = {r.split("-")[0] for r in defined}
    for path in markdown_files():
        if path.name == "CHANGELOG.md":
            continue
        for prefix, number in REF.findall(path.read_text(encoding="utf-8")):
            rule_id = f"{prefix}-{number}"
            if prefix in prefixes and rule_id not in defined:
                problems.append(f"Undefined rule {rule_id} referenced in {path.relative_to(ROOT)}")
    return problems, defined


def index_problems(defined):
    """Ranges in the Hardware-Rules.md index must match the IDs in each file."""
    problems = []
    index = (ROOT / "Hardware-Rules.md").read_text(encoding="utf-8")
    for target, cell in INDEX_ROW.findall(index):
        name = Path(target).name
        actual = {}
        for rule_id, file in defined.items():
            if file == name:
                prefix, number = rule_id.split("-")
                actual.setdefault(prefix, []).append(int(number))
        listed = {p: (int(a), int(b)) for p, a, b in RANGE.findall(cell)}
        for prefix, numbers in actual.items():
            want = (min(numbers), max(numbers))
            if listed.get(prefix) != want:
                problems.append(f"Index range for {prefix} in {name} should be "
                                f"{prefix}-{want[0]:02d}…{prefix}-{want[1]:02d}")
        for prefix in set(listed) - set(actual):
            problems.append(f"Index lists {prefix} rules that {name} does not define")
    return problems


def link_problems():
    problems = []
    for path in markdown_files():
        text = FENCE.sub("", path.read_text(encoding="utf-8"))
        for target in LINK.findall(text):
            if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
                continue
            target = unquote(target)
            base = ROOT if target.startswith("/") else path.parent
            if not (base / target.lstrip("/")).exists():
                problems.append(f"Broken link in {path.relative_to(ROOT)}: {target}")
    return problems


def version_problems():
    found = {}
    patterns = {
        "README.md": r"Version: (v[\d.]+)",
        "README.tr.md": r"Sürüm: (v[\d.]+)",
        "Hardware-Rules.md": r"\*\*Version\*\* \| (v[\d.]+)",
        "Hardware-Roles.md": r"\*\*Version\*\* \| (v[\d.]+)",
        "CHANGELOG.md": r"^## (v[\d.]+)",
    }
    for name, pattern in patterns.items():
        path = ROOT / name
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        match = re.search(pattern, text, re.M)
        found[name] = match.group(1) if match else None
    if len(set(found.values())) != 1:
        return [f"Version lines differ: {found}"]
    return []


def csv_problems():
    problems = []
    for path in sorted(ROOT.rglob("*.csv")):
        rel = path.relative_to(ROOT)
        if SKIP_DIRS & set(rel.parts):
            continue
        try:
            with path.open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.reader(handle))
        except (UnicodeError, csv.Error) as exc:
            problems.append(f"{rel}: not readable as UTF-8 CSV ({exc})")
            continue
        if not rows:
            problems.append(f"Empty CSV: {rel}")
            continue
        bad = [i + 1 for i, row in enumerate(rows) if row and len(row) != len(rows[0])]
        if bad:
            problems.append(f"{rel}: wrong column count on lines {bad}")
    return problems


def main():
    rules, defined = rule_problems()
    problems = rules + index_problems(defined) + link_problems() + version_problems() + csv_problems()
    for problem in problems:
        print(f"- {problem}", file=sys.stderr)
    if problems:
        print(f"REPO CHECK FAILED: {len(problems)} problem(s).", file=sys.stderr)
        return 1
    print(f"REPO CHECK OK: {len(defined)} rules, index ranges, links, versions and CSV files consistent.")
    return 0


if __name__ == "__main__":
    for _stream in (sys.stdout, sys.stderr):
        try:  # same UTF-8 output on Windows, macOS and Linux, also when piped
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    raise SystemExit(main())
