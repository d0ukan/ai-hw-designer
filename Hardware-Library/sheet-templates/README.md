# Sheet templates

Standard schematic sheet layout for every project (SCH-14).

## KiCad

File: [hfa-title-block.kicad_wks](hfa-title-block.kicad_wks), the drawing sheet with border and title block.

1. Copy it into the project folder under `Hardware/`.
2. Schematic Editor → File → Page Settings → Drawing sheet → pick the file. Paper: A4 landscape (A3 for crowded sheets).
3. Fill the title block fields (Page Settings, "apply to all sheets"):

| Field | Value |
| :--- | :--- |
| Title | project name (`project_name`) |
| Revision | design revision (`design_revision`), e.g. `R01` |
| Issue date | date of this revision |
| Company | company or owner (optional) |
| Comment 1 | project code (`project_code`), e.g. `DR00627` |
| Comment 2 | variant letter, or `—` |
| Comment 3 | designer |
| Comment 4 | reviewer |

Sheet name and "Sheet x/y" fill themselves.

Written to the KiCad 7+ drawing sheet format and not yet opened in every KiCad version. If KiCad reports an error or the layout looks wrong, fix it in the Drawing Sheet Editor (`pl_editor`) and save it back here.

## Altium Designer

Use a sheet template with the same fields: `Title`, `Revision`, `Date`, `DocumentNumber` (project code), `Variant`, `DrawnBy`, `CheckedBy`, `SheetNumber`/`SheetTotal`. Set them in Project Options → Parameters so every sheet shows the same values.

## Other EDA

Same fields and the same sheet order (SCH-14). If the tool has no template, write the fields as text in the bottom right corner.
