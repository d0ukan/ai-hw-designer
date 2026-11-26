# Manufacturing templates

Empty starter files. In the project, copy them into `Manufacturing/<rev>/`, rename them with `<prefix>` and fill them in. `<prefix>` = `python scripts/projectctl.py name [--variant A]` (e.g. `DR00627-R01`, `DR00627-AV-R01`). Rules: section 09 of `Hardware-Rules.md`.

| Template | Project output | Note |
| :--- | :--- | :--- |
| `bom.csv` | `<prefix>_BOM.csv` | One per variant. A part with `DNP` = `Yes` is not fitted. `Alternate MPN` holds at least 1 drop-in alternate part (DFM-14); if none, `Notes` = "no alternate". The `Comment`, `Designator`, `Footprint`, `LCSC Part #` columns match the JLCPCB upload. User-supplied parts: `Supplier`, `Notes` = "USER-SUPPLIED", `DNP` = `Yes` (DFM-16). `Lifecycle` / `Stock` / `Checked`: status, supplier stock and check date (DFM-17). |
| `pnp.csv` | `<prefix>_PnP.csv` | Units mm, angles in degrees. `Layer` = `Top` / `Bottom`. DNP parts are not listed. Check the manufacturer's rotation reference on the order screen. |
| `schematic-outputs.md` | `<prefix>_SCH.pdf` and attachments | Schematic output list |
| `assembly-drawing.md` | `<prefix>_ASSY.pdf` | Draftsman-style assembly drawing |
| `fab-notes.md` | `<prefix>_FAB.md` or `.pdf` | Fab note for the manufacturer |
| `bring-up-checklist.md` | Project record (not part of the release) | First power-up and test order (VER-09) |
| `review-checklist.md` | Project record (not part of the release) | Short stage-by-stage checklist for the Reviewer |

## What the outputs look like

`<prefix>_BOM.csv` (one row per value; values illustrative):

| Designator | Qty | Comment | Footprint | MPN | Manufacturer | Alternate MPN | Alternate Manufacturer | LCSC Part # | Lifecycle | Stock | Checked | DNP | Notes |
| :--- | :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :-: | :--- |
| R1 R2 | 2 | 5.1k | 0402 | RC0402FR-075K1L | Yageo | CRCW04025K10FKED | Vishay | C… | Active | LCSC >100k | 2026-11-26 | | |
| U1 | 1 | LM358 | SOIC-8 | LM358DR | TI | LM358DT | ST | C… | Active | LCSC >10k | 2026-11-26 | | |
| C9 | 1 | 10uF | 0805 | GRM21BR61A106KE19L | Murata | CL21A106KPFNNNE | Samsung | C… | Active | LCSC >10k | 2026-11-26 | Yes | option |
| M1 | 1 | ESP32 module | header 2×8 | … | … | | | | Active | local shop | 2026-11-26 | Yes | USER-SUPPLIED — hand assembly |

`<prefix>_PnP.csv` (fitted SMD parts only, mm and degrees):

| Designator | Mid X | Mid Y | Layer | Rotation |
| :--- | ---: | ---: | :--- | ---: |
| R1 | 9.00 | 9.50 | Top | 0 |
| U1 | 15.20 | 8.40 | Top | 90 |

PnP is delivered as CSV plus the same data as tab-separated `.txt`; `check-bom` reads only the CSV. Optional: `<prefix>_BOM_JLC.csv` (JLCPCB format) and `<prefix>_BOM.xlsx` (price, stock, totals); see section 09.

To check the release folder: `python scripts/projectctl.py check-bom` (BOM/PnP consistency) and `check-release`. For a filled example, see the `examples/DR00001-usb-c-led/` folder.

The revision history is kept in `REVISION-HISTORY.md` at the root. The templates in this folder are not a release; `manifest` and `check-release` check only the `Manufacturing/<rev>/` folder.
