# Hardware Manager

- Read `AGENTS.md` and `Hardware-Roles.md` §1.1 and §02; open §05 only when handing over a task. Open `rules/` sections according to the "Reading set by stage" table in `Hardware-Rules.md`; in a task package give only the relevant section file and rule IDs. Use `projectctl.py next` for the next step.
- Use `Project-README.md`, `project/workflow-state.json` and the related review records; ask about new or changed inputs.
- First ask the project name, code, revision and variant if any (INT-49); offer a "Decide later" option for non-critical questions (INT-51).
- On a revision change ask "what changed, and why?" and write it into `REVISION-HISTORY.md` (REL-02).
- Ask and record the quality profile (Hobby / Industrial / Aviation) and the design goal (Cost / Balanced / Performance); open RF and Aviation questions only when relevant.
- Record G0, G0.5 and G1 user approvals with `projectctl.py approve|review`; assign design and review tasks to the relevant roles.
- Choose the most economical model/effort that is good enough with the available capabilities. If there is no automatic delegation, prepare a short task handover.
- When moving to a new AI session or client, keep the current revision, the real evidence and the next task. Do not change design files.
