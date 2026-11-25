# Review Log (example)

| Finding ID | Severity | Stage / revision / location | Evidence and issue | Expected fix | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| F-001 | MAJOR | Schematic / R01 / R4 | R4 (0 Ω, in series with the LED) was marked DNP; if not fitted, the LED circuit stays open | Fit R4; note it as a removable bridge for measurement | VERIFIED |
| F-002 | MINOR | Schematic / R01 / R3 | With 1 kΩ the current is ≈ 3 mA; REQ-02 asks for ~2 mA | R3 = 1.5 kΩ | VERIFIED |
| F-003 | MINOR | BOM / R01 / D1 (variant A) | The suggested green alternate part is InGaN, Vf ~3 V; not drop-in | Remove the alternate part, write "no alternate" | VERIFIED |

## Review results

| Stage | Revision | Check / evidence | Result |
| :--- | :--- | :--- | :--- |
| Schematic | R01 | F-001…F-003 closed; no ERC in the example (no EDA files) | PASS |
| PCB | R01 | Layout and routing checklist (example) | PASS |
| Manufacturing | R01 | `check-bom` clean; manifest reviewed | PASS |
