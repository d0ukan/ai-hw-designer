"""Dependency-free consistency checks for this template repository.

Checks rule IDs (unique, every reference defined), relative Markdown links,
version lines, and CSV column counts. Run: python scripts/check_repo.py
Exit code 0 = OK, 1 = problems found.
"""

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULE_FILES = sorted((ROOT / "rules").glob("*.md")) + [ROOT / "Hardware-Roles.md"]
RULE_DEF = re.compile(r"^- \[ \] \*\*([A-Z]{2,4}-\d+)\*\*", re.M)
RULE_PREFIXES = ("INT", "PCB", "GND", "DFM", "SCH", "LAY", "DIF", "HS", "RF", "VER", "AI",
                 "AVI", "REL", "BAT", "MGR", "DES", "REV", "CTX", "OPT", "TOK")
RULE_REF = re.compile(r"\b(" + "|".join(RULE_PREFIXES) + r")-(\d{2,3})\b")
LINK = re.compile(r"\]\(([^)\s#]+)(?:#[^)]*)?\)")
SKIP_DIRS = {".git", "__pycache__", ".venv"}
# Example IDs used in prose, not rule references.
NOT_RULES = {"REV-001", "REV-404"}


def markdown_files():
    return [p for p in ROOT.rglob("*.md") if not SKIP_DIRS & set(p.relative_to(ROOT).parts)]


def rule_problems():
    problems, defined = [], {}
    for path in RULE_FILES:
        for rule_id in RULE_DEF.findall(path.read_text(encoding="utf-8")):
            if rule_id in defined:
                problems.append(f"Duplicate rule {rule_id}: {defined[rule_id]} and {path.name}")
            defined[rule_id] = path.name
    for path in markdown_files():
        if path.name == "CHANGELOG.md":
            continue
        for prefix, number in RULE_REF.findall(path.read_text(encoding="utf-8")):
            rule_id = f"{prefix}-{number}"
            if rule_id not in defined and rule_id not in NOT_RULES:
                problems.append(f"Undefined rule {rule_id} referenced in {path.relative_to(ROOT)}")
    return problems, defined


def link_problems():
    problems = []
    for path in markdown_files():
        for target in LINK.findall(path.read_text(encoding="utf-8")):
            if re.match(r"^[a-z]+:", target):
                continue
            if not (path.parent / target).exists():
                problems.append(f"Broken link in {path.relative_to(ROOT)}: {target}")
    return problems


def version_problems():
    found = {}
    patterns = {
        "README.md": r"Sürüm: (v[\d.]+)",
        "Hardware-Rules.md": r"\*\*Versiyon\*\* \| (v[\d.]+)",
        "Hardware-Roles.md": r"\*\*Versiyon\*\* \| (v[\d.]+)",
        "CHANGELOG.md": r"^## (v[\d.]+)",
    }
    for name, pattern in patterns.items():
        match = re.search(pattern, (ROOT / name).read_text(encoding="utf-8"), re.M)
        found[name] = match.group(1) if match else None
    if len(set(found.values())) != 1:
        return [f"Version lines differ: {found}"]
    return []


def csv_problems():
    problems = []
    for path in sorted(ROOT.rglob("*.csv")):
        if SKIP_DIRS & set(path.relative_to(ROOT).parts):
            continue
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.reader(handle))
        if not rows:
            problems.append(f"Empty CSV: {path.relative_to(ROOT)}")
            continue
        bad = [i + 1 for i, row in enumerate(rows) if row and len(row) != len(rows[0])]
        if bad:
            problems.append(f"{path.relative_to(ROOT)}: wrong column count on lines {bad}")
    return problems


def main():
    rules, defined = rule_problems()
    problems = rules + link_problems() + version_problems() + csv_problems()
    for problem in problems:
        print(f"- {problem}", file=sys.stderr)
    if problems:
        print(f"REPO CHECK FAILED: {len(problems)} problem(s).", file=sys.stderr)
        return 1
    print(f"REPO CHECK OK: {len(defined)} rules, links, versions and CSV files consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
