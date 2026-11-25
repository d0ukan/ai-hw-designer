# Example project: DR00001 — USB-C LED board

> **This is a teaching example, not a production-ready design.** There are no native EDA files, Gerbers or real review evidence. The MPNs are real parts, but datasheet and stock checks were not done; verify before use.

A small board that shows the template flow from start to finish: it takes 5 V from USB-C and lights a power LED.

| What it shows | File |
| :--- | :--- |
| Filled project information and decisions (identity, profile, target, silkscreen, open decisions) | [Project-README.md](Project-README.md) |
| Workflow record with all gates passed | [workflow-state.json](workflow-state.json) |
| Revision history | [REVISION-HISTORY.md](REVISION-HISTORY.md) |
| Example review findings (F-001 …) | [REVIEW_LOG.md](REVIEW_LOG.md) |
| Main and A variant BOM/PnP, fab note, manifest | [Manufacturing/R01/](Manufacturing/R01/) |

The deliverables were deliberately kept to `BOM PnP FAB`. A real project also has `Gerber SCH ASSY`; since the example has no EDA files, no fake Gerbers or PDFs were added.

Check this example locally:

```bash
python scripts/projectctl.py status        --state examples/DR00001-usb-c-led/workflow-state.json --manufacturing-dir examples/DR00001-usb-c-led/Manufacturing
python scripts/projectctl.py check-bom     --state examples/DR00001-usb-c-led/workflow-state.json --manufacturing-dir examples/DR00001-usb-c-led/Manufacturing
python scripts/projectctl.py check-release --state examples/DR00001-usb-c-led/workflow-state.json --manufacturing-dir examples/DR00001-usb-c-led/Manufacturing
python scripts/projectctl.py next          --state examples/DR00001-usb-c-led/workflow-state.json --manufacturing-dir examples/DR00001-usb-c-led/Manufacturing
python scripts/projectctl.py name --variant A --state examples/DR00001-usb-c-led/workflow-state.json
```

CI runs these commands on every push.
