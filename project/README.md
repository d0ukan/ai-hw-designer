# Workflow State

`workflow-state.json` is the short, machine-readable record of approval and review status.

- `project_name`: project name (INT-49); used in the title block (SCH-14).
- `project_code`: project code (e.g. `DR00627`); output names are derived from it. Required for export and release. If the field is missing in older state files, it is treated as null.
- `requirements_revision`: revision of the approved project inputs.
- `pcb_requirements_revision`: separate revision of the PCB layout inputs. Update it if material, technology, geometry, ring or other PCB decisions change.
- `design_revision`: the board revision (e.g. `R01`); used in output names and in the `Manufacturing/<rev>/` folder. A new revision is opened only per REL-01 (the name `templates` cannot be used).
- `input_approval`: G0, the user's real requirements approval, the related revision and approval reference.
- `pcb_input_approval`: G0.5, the user's real approval of the PCB inputs, the related PCB input revision and approval reference.
- `reviews`: independent schematic/PCB/manufacturing review result, related design revision and `REVIEW_LOG.md` evidence reference. If the schematic did not change, Reviewer can verify this with a diff at the final revision.
- `export_approval`: G1, the user's explicit approval to prepare manufacturing files for the related design revision, and its reference.
- `blocking_issues`: open CRITICAL/MAJOR finding IDs (`F-001` format) or related blockers.
- `deliverables`: list of outputs required in the release (INT-25); written with `projectctl.py deliverables ...`.
- `review_depth`: `Light`, `Medium` or `High` (INT-53); null means Medium. At High, `reviews.schematic_2` and `reviews.pcb_2` hold the second Reviewer's results (`review ... --second`); layout and G1 need both PASS records with different `--by` names.

Records may also carry optional `recorded_on` (UTC date), `recorded_by`, `commit`, `schematic_sha256` and `design_sha256` fields; `projectctl.py` commands fill them automatically.

**Commit binding:** If the project is a git repository, `approve` and `review` record the current commit. If the design changes within the same `R01`, `check-export`/`check-release` catches it: if schematic files (`*.kicad_sch`, `*.SchDoc`, `*.sch`) changed after the schematic review, or any file under `Hardware/` changed after the PCB/manufacturing review and G1, the gate closes and a new review is required. New design files not added to Git also count as changes. A `review ... PASS` or `approve G1` record is rejected if the design is not committed. `*.OutJob` files that the EDA tool rewrites during export do not count as changes. Records always store SHA-256 hashes as well; without Git (plain local folder, ZIP download, or git removed later) the checks use the hashes of the schematic files and of all design files under `Hardware/`; EDA backups, locks and local settings (`*.kicad_prl`, `*-backups/`, `*.lck` …) are ignored. `projectctl.py` never commits or pushes; the AI asks the user before any commit (AI-11).

**Deliverables and manifest:** The `deliverables` field (e.g. `BOM PnP Gerber SCH ASSY FAB`) is required for release; each item must exist as a `<code>-..._<item>.*` file or folder. `review manufacturing PASS` requires a valid manifest and stores its SHA-256 value as `manifest_sha256`.

## Record commands

Do not edit the JSON by hand; the commands validate the file and write it safely:

Full order (example revision `R01`; the `--revision` value must always match `design_revision`). To see the next missing step and its command at any time: `python scripts/projectctl.py next`.

```bash
# Start (Manager)
python scripts/projectctl.py set project_name "Sensor board"
python scripts/projectctl.py set project_code DR00627
python scripts/projectctl.py set design_revision R01
python scripts/projectctl.py set requirements_revision REQ-1
python scripts/projectctl.py set review_depth Medium   # Light | Medium | High (INT-53)
python scripts/projectctl.py approve G0 --revision REQ-1 --evidence "User approval, 2026-11-25 chat" --by "<name>"
# Schematic → review (in git: commit the design first, after the user's OK)
python scripts/projectctl.py review schematic PASS --revision R01 --evidence "REVIEW_LOG.md#R01-SCH"
# High only: second, independent Reviewer (also for pcb); use different --by names
python scripts/projectctl.py review schematic PASS --second --by "<reviewer 2>" --revision R01 --evidence "REVIEW_LOG.md#R01-SCH-2"
# G0.5 → layout
python scripts/projectctl.py set pcb_requirements_revision PCB-1
python scripts/projectctl.py approve G0.5 --revision PCB-1 --evidence "User PCB approval"
python scripts/projectctl.py check-layout
# PCB review → G1
python scripts/projectctl.py review pcb PASS --revision R01 --evidence "REVIEW_LOG.md#R01-PCB"
python scripts/projectctl.py approve G1 --revision R01 --evidence "User export approval"
python scripts/projectctl.py check-export
# Outputs (REL-04)
python scripts/projectctl.py deliverables BOM PnP Gerber SCH ASSY FAB
python scripts/projectctl.py check-bom            # Designer
python scripts/projectctl.py manifest             # Designer, last export step
python scripts/projectctl.py review manufacturing PASS --revision R01 --evidence "REVIEW_LOG.md#R01-MFG"
python scripts/projectctl.py check-release
# Other
python scripts/projectctl.py name --variant A     # DR00627-AV-R01
python scripts/projectctl.py check-bom X_BOM.csv --pnp X_PnP.csv
python scripts/projectctl.py block F-001
python scripts/projectctl.py unblock F-001
python scripts/projectctl.py revoke G1           # reset an approval to PENDING
python scripts/projectctl.py validate            # check the state file only
```

`manifest` writes the SHA-256 list of the files in `Manufacturing/<design_revision>/` as `MANIFEST.sha256`. `check-release` fails if this manifest is missing, if files changed, if a file name does not start with the project code (contents of prefixed folders, e.g. `DR00627-R01_Gerber/`, are free) or if `check-bom` finds errors. `check-bom` checks BOM and PnP designators, Qty counts, that DNP parts are absent from PnP, and MPNs; it warns if an alternate part is missing.

Approval states: PENDING / APPROVED. Review states: PENDING / PASS / REWORK / BLOCKED. A valid approval or PASS requires a revision and real evidence. Manager records the review result based on the Reviewer's record; it does not produce approvals on its own behalf.

The local check tool verifies file state; it does not replace real user approval or engineering tests. A new revision does not automatically make the previous revision's approvals valid.

`check-layout` checks G0, G0.5 and the schematic review record of the current design revision. After layout starts, the design revision may advance; before export, Reviewer verifies the schematic and PCB results for the current revision. If the schematic did not change, it can be checked with the existing evidence and the related diff.

In a multi-PCB project, `design_revision` is the shared system revision of all approved boards. Manager keeps board IDs and scope in the project records. Reviewer verifies each board and the related interfaces with evidence; it marks the system review result PASS only when the whole approved scope is complete. Do not create unnecessary per-board workflow files.

The schema version is 2. In projects using the earlier v1 schema, keep the existing requirement/review records; set `schema_version` to 2, add the `pcb_requirements_revision` field as null and the `pcb_input_approval` record as PENDING/null/null. Do not mark it APPROVED before a real G0.5 approval arrives.
