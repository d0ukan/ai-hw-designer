# Changelog

## v1.16 — 2026-11-25

- Review depth (INT-53): the user picks Light, Medium (default) or High at the start; recorded with `projectctl.py set review_depth`. Risky boards (Aerospace, RF, battery, above SELV) need at least Medium.
- High uses two independent Reviewers (VER-13): clean context, preferably different models; `review schematic|pcb ... --second --by <name>` records Reviewer 2. Layout and G1 are blocked until both PASS records exist with different reviewer names.
- `next` asks for the review depth before G0 and names the second-review steps; `status` shows the depth.
- Roles, AGENTS.md, project/README.md and both READMEs updated; 4 new tests (58 total).

## v1.15 — 2026-11-25

- All rule, role, template and example files translated to English for the public repo. `README.tr.md` stays as the Turkish overview.
- Example BOM notes, workflow state and Codex agent instructions in English; example manifest and its review hash regenerated.
- `check_repo.py` reads the `**Version**` rows; the BOM warning now names the `no alternate` note (`muadil yok` is still accepted).

## v1.14 — 2026-11-25

Fixed the findings of two independent reviews and one external AI review.

**projectctl (security and correctness)**
- New design files not yet added to Git also count as changes.
- The `commit` field must be hex (it cannot be passed to git as an option).
- The default git root is now the state file's project (a project in another folder looks at the right repo).
- `review ... PASS` and `approve G1` are rejected until the design is committed.
- `review manufacturing PASS` requires a valid manifest and stores its hash; if the manifest changes later, `check-release` requires a new review.
- Deliverables: `deliverables` command and field; every output must be present at release. `check-bom` fails at release if there is no BOM.
- `next` command: the next missing step, who does it, and the exact command.
- BOM/PnP: header whitespace, blank lines, real line numbers, `R1-R3` ranges, `nan`/`inf` rejection, clear errors for semicolon and non-UTF-8 CSV, case-insensitive file lookup.
- Manifest: corrupt files and `../` entries give a clean error; `Thumbs.db`, `desktop.ini`, `.DS_Store` are ignored.
- A `*.OutJob` change does not count as a design change. Options such as `--state` can also be written before the subcommand. Input file errors are reported separately as `INPUT ERROR`.
- 13 new tests (54 total).

**check_repo**
- Rule ranges in the index are compared with the actual rules; rules marked `[x]` are counted; prefixes are derived from defined rules; the link check handles code blocks, `%20` and root-relative links correctly; non-UTF-8 CSV gives a clean error; the version lines of both READMEs are checked.

**Rules and docs**
- Fixed commands in the docs (`--revision R01`); `project/README.md` has the full command sequence from G0 to release.
- Release order clarified (REL-04): the Designer writes the manifest, the Manager records the PASS, then `check-release`.
- Finding IDs are `F-001` (so they are not confused with rule ID `REV-01`).
- Index: INT-52, battery trigger wording, "Reading set by stage" table; section 07 once in the first session.
- AI-09: stop conditions (voltage above mains/SELV, multi-cell lithium, medical, DAL A/B) require human engineer approval.
- Question order in one place; INT-49 also records `project_name`; deferred board decisions by G0.5 at the latest.
- 3W rule clarified (3W center-to-center, ≥ 2W edge-to-edge). G0.5 added to the Roles workflow diagram. REL-02: which approvals stay valid in a new revision.
- Last-checked date on `rules/01` limits; smaller Manager reading set; web chat flow and `next` in AGENTS.

**Example project**
- R4 is now a fitted series bridge (the LED did not light while it was DNP); R3 = 1.5 kΩ (~2 mA); removed the wrong alternate part for the green LED ("no alternate"); added a real DNP option (C1); added `REVIEW_LOG.md` and deliverables.

**README**
- The main `README.md` is now English; the Turkish version is `README.tr.md`. Repo name updated to `hardware-for-anything`.

## v1.13 — 2026-11-25

**Use with AI and tokens**
- `Hardware-Rules.md` is now an index; the rules are split into 11 section files under `rules/` (content and rule IDs unchanged). The AI reads only the relevant section.
- `AGENTS.md`: "AI starting from the repo link" section (what to read, own copy, web chat without file access, first questions).
- Added `llms.txt`; English summary at the top of the README and a "Starting from the repo link in an AI chat" section.

**projectctl**
- Commit binding: `approve`/`review` records the git commit; if design files change after a review, `check-export`/`check-release` stop (schematic review looks only at schematic files).
- `check-bom`: BOM/PnP designator match, Qty, DNP, MPN; warning if an alternate part is missing. `check-release` also runs it.
- File name check extended to subfolders (contents of prefixed folders are free); `templates` is forbidden as a revision name. 7 new tests (41 total).
- `scripts/check_repo.py`: rule ID collisions, undefined references, broken links, version lines, CSV columns.

**Rules and templates**
- Section 10 (BAT-01…08): battery and charging, conditional; triggered by INT-52.
- `Manufacturing/templates/`: `bring-up-checklist.md`, `review-checklist.md`.
- `examples/DR00001-usb-c-led/`: filled example project (two variants, BOM/PnP, manifest); CI checks it end to end.

**Repo**
- CI: `check_repo.py` and example project steps.
- `CONTRIBUTING.md`, issue and PR templates; Git LFS note in `.gitattributes` and the README.

## v1.12 — 2026-11-25

**Project identity and outputs**
- INT-49/50: The first task asks for the project name, code, revision and variant; outputs are named with the `<code>-<rev>` or `<code>-<letter>V-<rev>` prefix (e.g. `DR00627-R01`, `DR00627-AV-R01`).
- `projectctl.py`: `project_code` field (compatible with old state files), `name [--variant X]` command; `check-export` requires a project code, `check-release` checks that root file names start with the project code. 7 new tests (34 total).
- Section 09 (REL-01…04): revision/variant distinction, "what changed, and why?" record at a revision change, output set and names.
- Added `REVISION-HISTORY.md` and `Manufacturing/templates/`: `bom.csv`, `pnp.csv`, `schematic-outputs.md`, `assembly-drawing.md` (Draftsman-style `_ASSY.pdf`), `fab-notes.md`.

**Rules**
- INT-51: "Decide later" option for non-critical questions; a deferred decision is asked again at the relevant gate, with a safe default if there is no answer.
- PCB-17…21: questions on logo/icon, board code (silk/copper, side, date), connector label, designator (shown/hidden, size, position), signature/easter egg.
- LAY-30/31: Silkscreen without overlaps on each side; applying the marking decisions.
- DFM-14: At least 1 drop-in alternate part for each component where possible. DFM-15: Common footprint layer map (KiCad KLC, Altium fixed mechanical map).
- Roles: MGR-15/16, REV-13 (Reviewer is read-only in MCP), REV-14 (output set check).

**MCP and Git**
- README: KiCAD-MCP-Server and altium-mcp usage notes.
- `.gitignore`: KiCad `fp-info-cache`, MCP `logs/`, Freerouting `*.dsn/*.ses`, Altium preview/log/output folders.
- `.gitattributes`: Altium design files `binary`, `.PrjPcb`/`.OutJob` CRLF, EasyEDA `.epro` binary.

## v1.11.1 — 2026-11-25

- `README.md`: Added REWORK loops for the schematic and manufacturing checks to the workflow diagram; explained the G1 re-approval rule.

## v1.11 — 2026-11-25

**Rules (`Hardware-Rules.md`)**
- INT-48: Added design target choice (Cost first / Balanced / Performance first). For aerospace/military projects with no cost target, the default is Performance. DFM-00, DFM-10, INT-16, the section 03 note and header priority are tied to this target; updated `Project-README.md`, `AGENTS.md`, MGR-14 and `agents/Manager.md`.

## v1.10 — 2026-11-25

**Rules (`Hardware-Rules.md`)**
- Section 04 split into subsections: General, Layout, Routing, SI / PI.
- Added SCH-03…SCH-07 schematic rules: power tree and rail filters (PI), per-pin decoupling, SI preparation (series termination, I²C pull-up, low-capacitance ESD, strapping pins), marking constraints in the schematic, 0 Ω / DNP option footprint.
- DFM-00: Unless specially requested, JLCPCB/PCBWay standard capability and stack-up are the baseline.
- Added LAY-08…LAY-13 layout rules: datasheet/app note reference layout, placement order, input protection, switching regulator loop, crystal, thermal, alignment and access.
- Added LAY-14…LAY-24 routing rules: routing order, net class and IPC-2152, layer usage, split plane and return via, clock/3W, analog GND, power distribution and Kelvin, high voltage, pad entry/teardrop/acid trap, shortest and most direct path (meandering traces forbidden, fix the placement first), user-approved free-angle/organic routing.
- Added LAY-25…LAY-29 SI/PI rules: decoupling loop, critical length (`tr × 2.5 cm`), impedance matching, length/delay matching, final check.
- `README.md`: Added a "Layout and routing" section.

## v1.9 — 2026-11-25

**Rules (`Hardware-Rules.md`)**
- INT-47: Added quality profile choice: Hobby / Industrial / Aerospace.
- Section 05: RF rules made optional and tiered by band (RF-A < 1 GHz, RF-B 1–6 GHz, RF-C > 6 GHz; RF-01…RF-09). Without RF, the section is N/A.
- Section 08: Added the Aerospace/Avionics conditional profile (AVI-01…AVI-10: standards, IPC Class 3, derating, components, power input, EMC, environment, traceability, analyses).
- GND-05/GND-06/LAY-05: Added RF, high-current and exposed pad exceptions.

**Roles and templates**
- `Hardware-Roles.md`: MGR-14 (profile question), MGR-09 and REV-11 updated.
- `AGENTS.md`, `agents/*.md`, `Project-README.md`: Added profile, RF band and Aerospace fields.
- `components.csv`: Added `temp_range`, `lifecycle`, `qualification`, `alternates`, `msl`, `rohs` columns.

**Tools**
- `projectctl.py`: `set`, `approve`, `revoke`, `review`, `block`, `unblock` record commands; `recorded_on` / `recorded_by` fields.
- `projectctl.py manifest`: SHA-256 manifest for manufacturing outputs; `check-release` verifies the manifest.
- GitHub Actions CI (Ubuntu + Windows, Python 3.10/3.12), MIT license.

## v1.8

- First published template.
