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

To check the release folder: `python scripts/projectctl.py check-bom` (BOM/PnP consistency) and `check-release`. For a filled example, see the `examples/DR00001-usb-c-led/` folder.

The revision history is kept in `REVISION-HISTORY.md` at the root. The templates in this folder are not a release; `manifest` and `check-release` check only the `Manufacturing/<rev>/` folder.
