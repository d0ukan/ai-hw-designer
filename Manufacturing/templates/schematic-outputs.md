# <prefix> — Schematic outputs

| Output | File | Status |
| :--- | :--- | :--- |
| Schematic PDF (all sheets, code / revision / variant / date in the title block) | `<prefix>_SCH.pdf` | Pending |
| Netlist (the EDA's standard format) | `<prefix>_NET.<ext>` | If requested |
| ERC report (clean or exceptions justified) | `<prefix>_ERC.txt` | Pending |
| Variant differences (fitted/not fitted parts) | DNP in `<prefix>_BOM.csv` | If any |

## Check

- [ ] Project name, `<prefix>`, page number and date correct in the title block
- [ ] DNP parts marked in the schematic
- [ ] Net names and differential pairs (`_P/_N`) readable
- [ ] ERC result recorded as Reviewer evidence
