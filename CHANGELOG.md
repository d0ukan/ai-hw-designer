# Changelog

## v1.48 — 2026-11-27

- Section 01 table completed and re-checked against the JLCPCB and PCBWay capability pages: V-cut edge, via annular ring, PTH hole and ring, NPTH hole, hole-to-hole, via/PTH/NPTH to copper, pad to pad, solder mask expansion and dam, silkscreen line/height and silk-to-pad. Defaults stay a little above the limits.

## v1.47 — 2026-11-27

- REV-22: every PCB review includes a routing review by two independent reviewers, net by net; shared findings go to REWORK, disagreements are argued once with evidence, then the Manager (or the user, if design intent changes) decides. Both lists go into `REVIEW_LOG.md`.
- LAY-23: if the target pad or via is in line, route straight; every bend needs a reason.

## v1.46 — 2026-11-27

- LAY-22: the no-trace-between-pads limit is now 0402 or smaller (was 0603).

## v1.45 — 2026-11-27

- LAY-22: no other net between the pads of a 0603 or smaller part on the same layer.
- LAY-29: run the EDA track cleanup (no dangling, duplicate or looping segments, no extra branch to an already connected pad) and zoom over every part on each side before review.

## v1.44 — 2026-11-27

- New output `<prefix>_BOM_Supplier.csv`: a short BOM to share with the assembler or supplier (designators, quantities, part and alternate part with manufacturer); fitted parts only, no price, stock or internal notes.

## v1.43 — 2026-11-27

- REL-05: all output documents share one look (SCH-14 title block on every PDF page, same font and layout, same header in the Excel BOM) with the user's logo, company name, signature or document number if given. INT-25 asks for them.

## v1.42 — 2026-11-27

- INT-25 asks the language(s) of the manufacturing documents (default English).
- REL-05: render and check every output document and drawing layer; no text over text, parts, outlines, dimensions or marked areas. REV-06 includes it.

## v1.41 — 2026-11-27

- JLCPCB BOM only with LCSC/Asia sourcing; never in the Aerospace profile (no CoC/lot traceability).
- AVI-11: Aerospace BOM columns for FMECA: Distributor, CoC/Lot, Qualification (MIL/QML/AEC-Q, VID/SMD), FIT, MTBF, Rel. Source; real values only.
- AVI-12: check each IC's errata sheet for the used revision and record design-relevant items.

## v1.40 — 2026-11-27

- PnP is delivered as CSV plus a tab-separated `.txt` copy (many PCBA houses ask for it); the example project has both.
- Optional outputs: `<prefix>_BOM_JLC.csv` (JLCPCB format) and `<prefix>_BOM.xlsx` (price, stock, line and BOM totals, source and date). INT-25 asks for them; the CSV BOM stays the checked one.

## v1.39 — 2026-11-26

- LAY-34: a missing 3D model is reported to the user with three choices: user shares the STEP · AI draws it in an installed CAD tool · AI installs FreeCAD + a FreeCAD MCP (only with the user's OK).

## v1.38 — 2026-11-26

- PCB-23: minimum part-to-part gap per density (0.25 / 0.5 / 1.0 mm), courtyards never overlap.
- PCB-24: ask the parts-to-board-edge distance (default 3 mm without edge rails, 1 mm with rails/panel).
- PCB-25: ask via tenting (all / except chosen nets / per net class); via size per net class, power vias larger and optionally untented. DFM-04 follows it.
- LAY-30: silk-to-pad/mask/silk DRC checks set to error plus a top/bottom render; designators that do not fit are moved or follow PCB-20.
- LAY-34: every part, module and mechanical part has a 3D model; missing ones are drawn from datasheet dimensions. REV-21 for the Reviewer.

## v1.37 — 2026-11-26

- PCB-23: ask component density before layout: High · Medium (default) · Low. A size limit or enclosure sets it automatically and the user is told. LAY-13 follows it.

## v1.36 — 2026-11-26

- PCB-22: ask before layout whether parts go on one side (Top) or both sides; default one side. If both, which parts may go on the bottom. LAY-13 follows the answer.

## v1.35 — 2026-11-26

- INT-58: test point options are now explicit: No · Probe pads (1.5 × 1.5 mm default) · Pogo-pin fixture (≥ 1.0 mm pads, ≥ 2.54 mm spacing, one side, 2–3 tooling holes, pin type).

## v1.34 — 2026-11-26

- INT-58: ask early whether test points are wanted, on which nets and with which pad size (default 1.5 × 1.5 mm SMD; 1.0 mm on small boards; pogo fixtures ≥ 1.0 mm at ≥ 2.54 mm, one side). LAY-06 uses the answer.
- `Manufacturing/templates/README.md` shows example BOM and PnP tables (incl. manufacturer and alternate manufacturer, user-supplied module row).
- PnP: CSV is the checked format; `.txt` / `.pos` / `.xlsx` copies only on request (REL-03 table).

## v1.33 — 2026-11-26

- DFM-17: no NRND / Last Time Buy / EOL / Obsolete parts without the user's OK ("user approved" in the BOM); stock of several times the build quantity, ideally multi-source; whole BOM re-checked before G1.
- BOM template and example BOMs get `Lifecycle`, `Stock`, `Checked` columns; `check-bom` warns on a fitted part with no lifecycle or a risky lifecycle without approval. REV-20 for the Reviewer.

## v1.32 — 2026-11-26

- Simpler, strictly sequential flow: the parallel PCB prep rule from v1.31 is removed; PCB work starts only after the schematic and G0.5. The PCB notes rule is now SCH-16.
- LAY-33: on a schematic problem found during layout, go back to the schematic stage, fix it and tell the user what changed and why; show it for their OK if they chose the SCH-08 check; re-review, then continue the PCB.

## v1.31 — 2026-11-26

- SCH-16: netlist-free PCB prep (outline, holes, connector positions, stack-up/impedance, footprints, G0.5 questions) may run while the schematic is finished; no placement or routing before G0.5.
- SCH-17: the schematic ends with short PCB notes in `Project-README.md` (critical loops, grouped parts, diff pairs, hot parts, analog, connectors, test points); the PCB review checks the layout against them.
- LAY-33: schematic change during layout: change and record it, inform the user (show and wait for OK if they chose the SCH-08 check), schematic re-review of the changed area, update the PCB and continue; G0.5 again only if PCB inputs change.
- DES-16, REV-19, role files, workflow charts and both READMEs updated. One Designer still owns schematic and PCB (no hand-off loss, fewer tokens).

## v1.30 — 2026-11-26

Full repo review fixes.

- projectctl: records always store design file hashes too, so a record made with git is still checked when git is missing later (ZIP download, `.git` removed, untrusted drive); a commit-only record without git now reports "cannot verify" instead of passing. Hashing is the same on Windows, macOS and Linux (case-insensitive patterns, NFC names), skips Altium previews/`.PrjPcbStructure` and KiCad `#auto_saved_files#`, and never crashes on odd file names. File errors give a clean message (exit 2). Deliverables work with dotted revisions (`R1.2`); BOM Qty accepts only ASCII digits; duplicate manifest lines are rejected; `next` validates the revision folder; git runs with `core.fsmonitor=false`.
- `.gitattributes`: files under any `Manufacturing/` folder keep their exact bytes, so `MANIFEST.sha256` matches on every computer.
- CI: Python 3.13 added; a no-git end-to-end step checks that a design change is detected. No-git tests now run even when git is not installed (72 tests).
- Docs: first-question order kept in one place (`rules/00-intake.md`) and referenced elsewhere (shorter AGENTS.md and Manager.md); stale rule ranges and question order in READMEs fixed; profile name "Aerospace" everywhere (section 08 stays "Aviation rules"); "DNP in the BOM, omitted from the PnP" for user-supplied parts; commit notes point to AI-11; INT-56 refers to INT-18 for assembly; SCH-06 refers to DIF-09.
- New role duties: MGR-17 (INT-53…57, AI-11), DES-12…15 (readable schematics and sheets, diff pairs, user-supplied parts and alternates, silkscreen). Reading set, templates (review checklist, Project-README, assembly drawing, schematic outputs, BOM convention) and repository layout updated.

## v1.29 — 2026-11-26

- Works without git: in a plain local folder, approvals and reviews store SHA-256 hashes of the schematic files and of all design files under `Hardware/` (new optional record fields `schematic_sha256`, `design_sha256`). A later design change closes the gate as with git; EDA backups, locks and local settings are ignored.
- AI-11: the AI never commits, pushes, runs `git init` or changes branches on its own; it asks before any commit and pushes only when the user asks. `projectctl.py` never commits or pushes. AGENTS.md updated.
- Tests: the git binding tests also run without git (67 tests).

## v1.28 — 2026-11-26

- Cross-platform: CI now runs on Linux, Windows and macOS. Scripts always print UTF-8 (Turkish or other non-ASCII project names work on any console, also when piped).
- READMEs: per-OS Python table (`python` / `python3` / `py`) and an OS badge. AGENTS.md tells the AI to use the user's OS syntax and `python3` when `python` is missing.
- GitHub language stats now count Markdown (the rules), not only Python.

## v1.27 — 2026-11-26

- READMEs: banner and workflow images (`docs/assets/`, English and Turkish), badges, an "At a glance" table, team, first-question and sheet-order diagrams, a review depth table and colored workflow chart. No rule changes.

## v1.26 — 2026-11-26

- SCH-14: standard schematic sheet: A4 landscape, one template for all sheets, full title block (name, code, revision, variant, sheet name, sheet x/y, date, designer, reviewer), EDA default styles.
- SCH-15: fixed sheet order: cover (block diagram, revision history, notes) → power input → regulators → MCU → interfaces/RF/sensors → connectors, mechanical, test points; one block per sheet.
- New `Hardware-Library/sheet-templates/` with a KiCad drawing sheet (`hfa-title-block.kicad_wks`) and field mapping for KiCad and Altium. Not yet opened in every KiCad version; fix in `pl_editor` if needed.
- REV-18: the Reviewer checks template, title block and sheet order. Role files and both READMEs updated.

## v1.25 — 2026-11-26

- SCH-13: differential pairs are visible in the schematic: drawn side by side, series parts as matching pairs, and a note with interface and impedance (e.g. "USB D+/D− · 90 Ω diff").
- DIF-09: pair net names the EDA recognizes (KiCad `+`/`-` or `P`/`N`, Altium diff pair directive); checked after netlist import.
- DIF-10: route with the EDA's diff pair router, constant width/spacing, symmetric vias with GND return via, no stubs, local length tuning.
- DIF-11 and REV-17: a pair table (impedance, width/spacing, length difference) as review evidence, checked by the Reviewer. Role files and both READMEs updated.

## v1.24 — 2026-11-26

- INT-56: ask the user's country/region and where the board is assembled (PCBA house or by hand).
- INT-57: for a ready module, header module or part the PCBA house does not stock, ask where the user buys it, check local availability when possible, offer socket/header vs. castellated mounting, and get the exact product (clones often differ in pinout, pitch or row spacing).
- DFM-16: user-supplied parts are marked in the BOM (supplier, USER-SUPPLIED note), DNP in the PCBA BOM/PnP, shown in the assembly drawing; the footprint follows the exact product.
- REV-16: the Reviewer checks user-supplied parts. Designer/Reviewer role files and both READMEs updated.

## v1.23 — 2026-11-26

- Schematic readability rules SCH-09…12: real wires inside blocks and few net labels (harness/global labels only when needed), power symbols for supplies, left-to-right flow and grouped blocks on grid with junction dots, no overlapping text, and an AI self-check after each drawing step (PNG review, ERC, short net list).
- REV-15: the Reviewer returns REWORK when the schematic is hard for a human to read. The SCH-08 user check now includes the net list. Designer/Reviewer role files and both READMEs updated.

## v1.22 — 2026-11-26

- AI-10: the project stays in one conversation. The AI never asks the user to open a new session or chat. Roles run as in-session subagents, or the main session does the Designer work; for the independent review the AI asks the user how it should be done.
- MCP tools that load only at client start: set them up at project start and resume the same conversation after a restart (INT-54, MCP-SETUP.md).
- AGENTS.md, Hardware-Roles.md (CTX-15, review depth), agents/README.md, Manager.md and both READMEs updated.

## v1.21 — 2026-11-26

- SCH-08 (optional): after the schematic review PASS the AI asks "The schematic is done. Do you want to check it?" On no it notes it and continues. On yes the Designer exports a draft schematic PDF and per-sheet PNGs to `Review/<rev>/`, shows them in the chat and asks the user to open the schematic in the EDA tool; the user's OK or skip goes into the G0.5 evidence. Skipping never skips the G0.5 / G1 approval.
- LAY-32 (optional): the same for the PCB before G1, with PDF, 3D top/bottom and layer images.
- DES-11, workflow charts, AGENTS.md, role files and `next` messages updated; `Review/` is git-ignored.

## v1.20 — 2026-11-26

- INT-19 moved right after the project purpose and made explicit: maximum envelope L × W × H in mm including connectors, mating cables and the tallest part, or "as small as possible" / "no limit"; shape, mounting holes and enclosure STEP.
- INT-20: "Do you have a target layer count, or shall I choose (2, 4, 6, 8 …)?" The AI picks the lowest suitable count and gives a one-line reason; PCB-09 confirms it at G0.5.

## v1.19 — 2026-11-26

- INT-55: the AI no longer proposes projects on its own. It asks in one question "What would you like to build? Or shall I suggest some ideas?"; only if the user wants ideas does it suggest 3–5, based on the user's earlier projects in the repo and stated interests (no searching other files without permission). The user always picks.

## v1.18 — 2026-11-26

- EDA question moved to the start (INT-04, right after project identity).
- INT-54: the AI offers to set up the matching MCP server (KiCad, Altium, EasyEDA), asks the scope (this project only or all projects), installs only after the user's yes and verifies the connection.
- New `MCP-SETUP.md` (per EDA and AI client, Reviewer read-only entry) and `examples/mcp/kicad.mcp.example.json`.
- `.gitignore` ignores local `.mcp.json` and `.cursor/mcp.json`; `llms.txt` no longer says the template is in Turkish.

## v1.17 — 2026-11-26

- Workflow charts (README.md, README.tr.md, Hardware-Roles.md): added the rare return path from the PCB review and the manufacturing review to the schematic (dashed arrows). The note says what is redone: schematic review, PCB update and review, G1.

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
