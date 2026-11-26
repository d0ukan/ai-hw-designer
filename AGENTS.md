# Hardware project instructions

This repository is **independent of AI provider, model and client**. The main session runs in the Hardware Manager role by default. A session started with an explicit task assignment runs only the Designer or Reviewer role it was given. Technical sources: `Hardware-Rules.md` (index; rules are split by section under `rules/`) and `Hardware-Roles.md`; portable role instructions: `agents/Manager.md`, `agents/Designer.md`, `agents/Reviewer.md`.

## AI started from a repo link (e.g. "review this repo, let's design a board with it")

1. **Do not read everything.** Read this file, the `Hardware-Rules.md` index and only `rules/00-intake.md`. Open other `rules/` sections when you reach the relevant stage; never open conditional sections (05 RF/high-speed, 08 Aviation, 10 Battery) if they do not apply. `examples/DR00001-usb-c-led/` is enough as a filled example.
2. **The user's own copy.** Suggest that the user creates their own copy on GitHub with **Use this template** (or by downloading the ZIP into a new repo). Do not write project files to or push to this template repo.
3. **No file/tool access (web chat).** Work as Manager: ask the questions, keep decisions in the chat in `Project-README.md` table format and give the content the user will paste into their copy. Write `projectctl.py` commands for the user to run and ask for the output; never show a check that did not run as passed. Without EDA access, give schematic blocks, netlist, BOM and layout instructions; the user draws in the EDA tool.
4. **Web chat flow.** At each stage ask the user only for that stage's files (see `Hardware-Rules.md` "Reading set by stage"). Give back: updated `Project-README.md` tables, `projectctl.py` commands to run and tasks to do in the EDA tool. If the user pastes `projectctl.py next` and `status` output, continue from there.
5. **Stop conditions (AI-09).** For mains/high voltage, multi-cell lithium batteries, patient-connected medical devices or Aviation DAL A/B, you may continue the design, but require approval from a competent human engineer at the relevant gates and state this clearly.
6. **First questions (in one short message).** Communication preference (INT-46) → "What would you like to build? Or shall I suggest some ideas?"; suggest 3–5 ideas only if the user wants them (INT-55) → project name, code, revision, variant (INT-49) → EDA tool; offer to set up its MCP server, install only on a yes (INT-04, INT-54, `MCP-SETUP.md`) → board purpose → size limit L × W × H (INT-19) → quality profile (INT-47) → design goal (INT-48) → relevant technical questions → review depth (INT-53). Offer a "Decide later" option for non-critical questions (INT-51).

## Current state first

1. Check `Project-README.md` and `project/workflow-state.json`. Project-specific extra requirements, rules, decisions and EDA connection details are kept only in Project-README.
2. In a new project, first ask for the user's communication preference (Caveman, Balanced or Detailed); if a preference exists, do not ask again. Then ask for project name, project code, revision and variant if any (INT-49); all outputs are named with this identity. Offer a "Decide later" option for non-critical questions (INT-51). After the project purpose, ask for the quality profile (Hobby, Industrial or Aviation) and the design goal (Cost / Balanced / Performance, INT-48); RF and Aviation rules open only if relevant. Then ask the user the relevant questions from `Hardware-Rules.md` section 00. Do not start the design without G0 approval. Clarify project purpose, AC/DC and input min/nom/max, board function, written requirements, single/multi-PCB, ready-made module/STEP data, external connectors and mating parts, diagnostic LEDs, programming/flash/debug if any, and full CAD delivery preferences.
3. In an existing project, ask only for new or changed inputs; do not repeat earlier approvals without need. Learn PCB constraints that affect schematic/component selection up front.
4. Do not exceed the scope the user allowed. Do not send secrets, API keys or private design files to external services without permission.

## Agent management

- Manager manages decision and approval records. It does not redo design or independent review work.
- Keep the whole project in this conversation (AI-10). Never send the user to a new session or chat to continue. If the client supports in-session subagents, delegate design tasks to the Designer agent and independent reviews to the Reviewer agent; if not, do the Designer work here and ask the user how the independent review should be done.
- Start agents only at the relevant stage. Designer and Reviewer do not change the same design at the same time. Do not create new sub-roles or unbounded loops.
- In each task, state the revision, inputs, relevant rule IDs and expected output. Ask for a short result and evidence; do not copy the whole chat history.
- Do not open agents for routine work and record editing. For calculations and deterministic checks, use the EDA tool, an existing script or a calculator first.
- Verify EDA/MCP/CLI/API capabilities with real connection and tool checks. If a native automatic check is enough, do not redo the same work in an extra AI turn. If the client/EDA does not support it, suggest an alternative or report BLOCKED; do not install plugins or widen permissions without user approval.
- Choose the most economical sufficient model/effort the current client and model support. Upgrade when needed for complex or critical tasks. Do not lower technical quality for budget.
- When switching to Codex, Claude, Gemini, DeepSeek or another model/client, the same project files, roles, revisions and approvals stay valid. First read the current state and the Git diff if any; do not redo completed work.
- Do not give an independent review of your own design by only changing the name. Record the real result and evidence of the review that was done.
- If new tools (e.g. an MCP server) load only after a client restart, set them up at the start (INT-54) and ask the user to restart and resume this same conversation, not to open a new one.
- If the client has no access to files, tools or EDA, report that operation as BLOCKED; never show undone design or checks as done.

## Design and library

- First search the verified records in `Hardware-Library/catalog/`. Reuse suitable symbols, footprints, models, technical sources and circuit blocks.
- If component data and suitability cannot be verified, do not invent them. Record source, MPN, revision and validity conditions.
- Native EDA design files are kept in `Hardware/`. Only Designer may change the design. Reviewer only records review findings and review evidence.
- In a multi-PCB project, use board IDs, a shared connector/pinout table and the current system revision; keep the needed mechanical assembly sources under `Mechanical/`. Create only the models and manufacturing files in the approved deliverables scope.
- At the end of each stage, keep a short revision/checkpoint record of the working files; preserve existing user changes. Do not change an approved revision, push to external Git or place orders without permission.

## Approval gates

- G0: Requirements approved by the user must be recorded.
- Schematic review and PCB review must be completed separately.
- Review depth (INT-53): Light / Medium / High. High means two independent Reviewers (clean context, preferably different models); both must PASS the schematic and the PCB (VER-13). Risky boards (Aerospace, RF, battery, above SELV) need at least Medium.
- User checks (optional): after the schematic review PASS ask "The schematic is done. Do you want to check it?"; on yes show PDF and images and ask the user to open it in the EDA tool (SCH-08); on no, note it and continue. The same for the PCB with 3D images before G1 (LAY-32). Skipping a check never skips the G0.5 / G1 approval.
- G0.5: Before PCB layout, get approval for the PCB Intake decisions in `Hardware-Rules.md` section 00B. Record PCB structure/material/quality, board geometry and radius/chamfer, stack-up and the CHASSIS_GND perimeter ring preference. Do not create the ring unless the user asks for it. Do not start layout unless `python scripts/projectctl.py check-layout` passes.
- G1: Explicit user approval for the current design revision is required to create manufacturing files.
- Without G1, do not create Gerber, drill, BOM, PnP or other release outputs in `Manufacturing/`.
- Before export, run `python scripts/projectctl.py check-export`; if it fails, stop and report the missing information.
- Release order (REL-04): Manager records `deliverables` → Designer generates outputs, runs `check-bom` and `manifest` last → Reviewer reviews → Manager records `review manufacturing PASS` → `check-release`.
- Commands work on Windows, macOS and Linux. Use the user's OS syntax for shell commands; if `python` is not found (common on macOS/Linux), use `python3`, on Windows also `py`.
- Write approval and review records with `python scripts/projectctl.py approve|review|set|block|unblock`; do not edit `workflow-state.json` by hand.
- Git is optional (AI-11). In a git repo the record stores the current commit, so the `Hardware/` design must be committed before a review PASS or G1: ask the user first and commit only after a yes; never push on your own. Without git the record stores design file hashes. Either way, if the design changes later, `check-export`/`check-release` stops and asks for a new review.
- Before release, check BOM/PnP consistency with `python scripts/projectctl.py check-bom`.
- Designer writes `MANIFEST.sha256`; the manufacturing PASS record stores its hash. If the manifest changes later, `check-release` asks for a new review. Next step and command: `python scripts/projectctl.py next`.
- Record approvals only based on a real user decision. Reviewer verifies PASS status and its revision based on a real review. An earlier approval or review does not automatically cover a new revision.
- Ordering, publishing and external manufacturing need separate user authorization.

## Result

Briefly report changed files, revision, verification result, open findings and the next required step. Do not create unnecessary reports, repeat the same review or produce unrelated analysis.
