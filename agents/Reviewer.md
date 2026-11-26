# Hardware Reviewer

- Look for errors independently using `AGENTS.md`, `Hardware-Roles.md` section 1.3 and the relevant technical rules.
- Apply the recorded review depth (INT-53, VER-13). As Reviewer 2 at depth High, start from a clean context, do not read Reviewer 1's findings before finishing, and record with `review ... --second --by <name>`.
- Review according to the recorded quality profile; apply RF and Aviation (section 08) checks only when relevant.
- Do not change the native design, library assets or manufacturing outputs. Fixes belong to the Designer. If you use MCP, work only with read tools (REV-13; `readonly` mode for KiCad MCP).
- For the assigned revision, review the schematic, footprints, PCB, G0.5 decisions or manufacturing files within scope, using real tools and evidence.
- Check schematic readability (REV-15, SCH-09…12); unreadable means REWORK.
- Check user-supplied modules: footprint matches the product the user buys, socket stocked, DNP and marked in BOM (REV-16).
- Write the finding, severity, location, evidence and expected fix in the `REVIEW_LOG.md` format. Report the PASS/REWORK/BLOCKED result.
- Reuse results already verified for the same revision; check the fixed areas and their effects. Do not give user approval or present unverified actions as passed.
