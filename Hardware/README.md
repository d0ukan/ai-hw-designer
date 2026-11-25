# Hardware

This folder holds the native schematic, PCB, constraints and project-specific libraries of the EDA software chosen from the approved project inputs. The template has no sample PCB file because no EDA software or board purpose has been chosen yet.

Before layout, the G0.5 PCB inputs are approved and the check-layout check is run. A CHASSIS_GND perimeter ring is created only with explicit user approval.

A single-PCB project needs one shared EDA project area. If a multi-PCB project is approved, keep each board in its own native EDA area, such as `Hardware/<board-id>/`. The number of boards and their IDs come from user input; do not create unneeded placeholder boards. Keep the shared pinout/connector reference for inter-board and external connections in `Project-README.md`.

Use shared `Hardware-Library/` assets with relative paths where possible; avoid absolute library paths that will not work on another computer. Save design revisions, keep valid user changes, and run the required ERC/DRC checks with the real EDA tool.

MCP is not required. Verify the MCP, CLI, API/script or GUI access supported by the chosen EDA before the project starts. Record the available capabilities and limits in `Project-README.md`; do not count unverified conversion or automation results as successful in the same project revision.
