# <prefix> — Schematic outputs

| Output | File | Status |
| :--- | :--- | :--- |
| Schematic PDF (all sheets, code / revision / variant / date in the title block) | `<prefix>_SCH.pdf` | Pending |
| Netlist (the EDA's standard format) | `<prefix>_NET.<ext>` | If requested |
| ERC report (clean or exceptions justified) | `<prefix>_ERC.txt` | Pending |
| Variant differences (fitted/not fitted parts) | DNP in `<prefix>_BOM.csv` | If any |

## Check

- [ ] Title block complete on every sheet (SCH-14); fixed sheet order (SCH-15)
- [ ] DNP parts marked in the schematic
- [ ] Net names readable; differential pairs noted and named per SCH-13, DIF-09
- [ ] ERC result recorded as Reviewer evidence
