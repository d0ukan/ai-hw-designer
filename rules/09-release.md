<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
## 09 · Revision, variant and outputs

- [ ] **REL-01** — **Revision or variant?** If copper, outline, holes or stack-up change, it is a new **revision** (R01 → R02). If the PCB stays the same and only populated parts or values change, it is a **variant** (`DR00627-AV-R01`, `DR00627-BV-R01`).
- [ ] **REL-02** — **Revision change:** When bumping the revision, ask the user: **What changed, and why?** Write the answer item by item into the project's `REVISION-HISTORY.md` file (date, changes, reason, affected boards/files, approver). Also add the known errors (errata) of the previous revision. In the new revision, design reviews, G1 and the manufacturing review are redone. G0 and G0.5 stay valid only if the requirements (`requirements_revision`) and PCB input revision (`pcb_requirements_revision`) did not change; if they changed, approval is obtained again.
- [ ] **REL-03** — **Output set:** Select the outputs to deliver according to INT-25; the typical set is below. Each variant has its own BOM and PnP file; DNP parts are removed from the PnP and stay in the BOM as DNP (user-supplied parts too, DFM-16). Templates are in `Manufacturing/templates/`.
- [ ] **REL-04** — **Release order:** (1) The Manager records the deliverables: `projectctl.py deliverables BOM PnP Gerber SCH ASSY FAB` (according to INT-25). (2) The Designer generates the outputs with the prefix into `Manufacturing/<rev>/`, runs `check-bom` and writes the `manifest` as the last step. (3) The Reviewer inspects the files and the manifest. (4) The Manager records PASS with `review manufacturing PASS`; the record stores the manifest hash. (5) `check-release` is run. If the manifest changes after PASS, a new review is required. File names must start with the project code.

| Output | File name | Note |
| :--- | :--- | :--- |
| Gerber + drill | `<prefix>_Gerber.zip` | Layer set the manufacturer requires |
| BOM | `<prefix>_BOM.csv` | Per variant; MPN, alternate part, DNP |
| Pick & Place | `<prefix>_PnP.csv` | Per variant; DNP excluded |
| Schematic | `<prefix>_SCH.pdf` | Revision and date in the title block |
| Assembly drawing (Draftsman style) | `<prefix>_ASSY.pdf` | Top/bottom, designators, Pin 1/polarity, DNP marked, dimensions; states whether the bottom view is mirrored |
| Fab note | `<prefix>_FAB.md` or `.pdf` | Stack-up, thickness, finish, color, IPC class, special requests |
| 3D model | `<prefix>.step` | If requested |

`<prefix>` = output of `projectctl.py name [--variant X]`.
