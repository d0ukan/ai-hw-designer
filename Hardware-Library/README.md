# Hardware Library

Shared, reusable hardware library inside the project. Search the catalogs in the first design step; if a suitable verified record exists, do not research or model from scratch.

| Folder | Content |
| :--- | :--- |
| `catalog/components.csv` | MPN-based verified component, ready-made module, connector and source entries |
| `catalog/blocks.csv` | Circuit blocks, their versions and validity conditions |
| `symbols/` | EDA schematic symbols |
| `footprints/` | EDA PCB footprints |
| `models3d/` | STEP or EDA-compatible 3D models |
| `datasheets/` | Sources that may be shared; otherwise a link in the catalog |
| `design-blocks/` | Verified, reusable native circuit blocks |

## Use and verification

1. Check the exact MPN, manufacturer, package, symbol/pinout and footprint match.
2. Review the datasheet revision, source pages and validity conditions in the catalog.
3. If not suitable, create a new revision/separate MPN record instead of changing the existing record.
4. Designer adds new assets; they are marked `VERIFIED` after Reviewer verifies them. An unreviewed asset stays `UNVERIFIED` or `BLOCKED`.
5. Do not treat circuit blocks as directly verified under different supply, load, interface, tolerance or operating conditions.
6. Time-varying information such as stock/price is checked as current when needed. Respect license and redistribution permissions; do not share datasheet/CAD files without permission.
7. Track approved ready-made modules and connector/mating connector pairs with separate exact MPN/model records. Record the STEP data the user gives and its source revision; do not use an unverified approximate CAD model as the real mechanical model.

### `components.csv` extra columns

| Column | Content | Example |
| :--- | :--- | :--- |
| `temp_range` | Operating temperature from the datasheet | `-40..+85C` |
| `lifecycle` | Manufacturer lifecycle status and check date | `Active (2026-11)` / `NRND` / `EOL` |
| `qualification` | Quality class | `Commercial` / `Industrial` / `AEC-Q100` / `MIL` |
| `alternates` | Approved alternate MPNs (separated by `;`) | `MPN-A;MPN-B` |
| `msl` | Moisture sensitivity level | `1` / `3` |
| `rohs` | RoHS status | `Yes` / `No` |

In the `alternates` field, write at least 1 drop-in alternate part if possible: same footprint and pinout, equal or better ratings, preferably a different manufacturer (DFM-14). If none is found, write "no alternate" in the `notes` field.

Leave unknown fields empty; do not invent. In Hobby projects filling only the needed columns is enough; in the Aerospace profile `temp_range`, `lifecycle`, `qualification` and `alternates` are mandatory.

### Footprint layer map (DFM-15)

Footprints use only the shared layers below; no special layer outside the map is used. This way no unnecessary layers appear in the outputs.

| Content | KiCad (KLC) | Altium (fixed at project start; example) |
| :--- | :--- | :--- |
| Copper, solder mask, paste | `F/B.Cu`, `F/B.Mask`, `F/B.Paste` | Top/Bottom Layer, Solder, Paste |
| Silkscreen (body outline, Pin 1) | `F/B.SilkS` | Top/Bottom Overlay |
| Courtyard | `F/B.CrtYd` | Mech 15/16 or Courtyard layer type |
| Fab/Assembly (body, designator `${REFERENCE}`) | `F/B.Fab` | Mech 13/14 or Assembly layer type |
| 3D body | 3D model | Mech 13/14 or 3D Body layer type |

Mechanical layer numbers in Altium vary from person to person; write the map chosen for the project into `Project-README.md` and use the same one in all footprints. If possible, use Altium's component layer type (Assembly, Courtyard, 3D Body) feature. Naming is kept close to IPC-7351.

Initially the catalog contains only column headers. Do not assume that ready verified components or circuits exist. The copied project library can later be contributed back to the template repository by the user through review.

To search the catalog for an MPN or block ID, use the EDA tool's search feature or a command such as `rg -i --fixed-strings "MPN" Hardware-Library/catalog/components.csv`. Simple catalog queries do not need a separate LLM call.
