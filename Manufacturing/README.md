# Manufacturing

At the start this folder holds only `templates/` (empty BOM, PnP, schematic output, assembly drawing and fab note templates; see [templates/README.md](templates/README.md)). Gerber, drill, BOM, PnP/CPL, stencil or other release files are not created without G1 manufacturing file approval and a successful local `check-export`.

Once approved, use a subfolder for the design revision (e.g. `R01/`). Name files with the `projectctl.py name` prefix (e.g. `DR00627-R01_BOM.csv`, for a variant `DR00627-AV-R01_BOM.csv`); the output set is in section 09 of `Hardware-Rules.md`. All files are generated from the same approved source. The Reviewer checks them. If the design has changed, do not export with an old approval.

In a multi-PCB project, keep approved manufacturing files separately under `<revision>/<board-id>/`. If requested, use `<revision>/Assembly/` for the approved full system CAD/STEP output. Record boards and connector/cable relations consistently with the shared project revision.

Creating manufacturing files alone does not authorize ordering PCBs.

Before release, write `MANIFEST.sha256` to the revision folder with `python scripts/projectctl.py manifest`. `check-release` verifies this manifest; if a file changes after the manifest, the release is blocked.
