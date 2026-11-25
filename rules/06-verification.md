<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
## 06 · Design Review & Verification

- [ ] **VER-01** — Verify all pin connections, footprints and design rules against the datasheets.
- [ ] **VER-02** — Complete schematic ERC and PCB DRC checks. Do not leave unexplained errors or unapproved rule violations.
- [ ] **VER-03** — Check the correctness of GND polygons and via connections.
- [ ] **VER-04** — Verify layers, board outline, solder mask openings and holes in the Gerber and drill files.
- [ ] **VER-05** — Check the BOM and Pick & Place (CPL) files needed for PCB manufacturing and PCBA assembly.
- [ ] **VER-06** — Verify compliance with the manufacturer's current DFM limits and the selected order configuration.
- [ ] **VER-07** — Perform the power budget, tolerance, worst-case, derating and thermal calculations the project needs. Use a calculator or script where applicable; perform only calculations that give meaningful results.
- [ ] **VER-08** — Use SPICE or other simulations for circuits that cannot be verified well enough by calculation or datasheet. Do not run unnecessary simulations; do not present the result of an analysis that was not run as verified.
- [ ] **VER-09** — Create a short bring-up/test plan, suited to project complexity, for first power-up and basic functional tests after manufacturing. Prepare detailed separate reports only if the user asks or the requirements demand it.
- [ ] **VER-10** — In multi-PCB projects, in addition to each board's ERC/DRC and independent review results, check the shared interface/pinout, mating connectors, power connections and mechanical fit. State the board ID in the review record. Preserve the existing verification evidence of unaffected boards.
- [ ] **VER-11** — If the user asked for a complete CAD assembly, check the fit of the approved board, module and mechanical reference models. If no real CAD/interference check was done, state it clearly; when listing missing or approximate models, do not present them as verified. Prepare the final CAD/STEP delivery according to the approved scope and revision.
- [ ] **VER-12** — If programming/debug is needed, check schematic and layout consistency with the selected method, target component, programmer/debugger and approved connector/pinout. A real programming/flash/debug test counts as complete only if the hardware and tools are available; otherwise the related verification is recorded as a pending test.
