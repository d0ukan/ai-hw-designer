<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
## 05 · Differential Pairs, RF & High-Speed (SI/PI)

> **Mandatory precondition:** If differential traces are present, do not set impedance or routing geometry by guessing.

### Information to verify before routing

| Information | Source |
| :--- | :--- |
| Communication interface and target differential impedance | User / interface specification / datasheet |
| Allowed impedance tolerance | User / interface specification |
| Intra-pair length matching and other length limits | User / interface specification / datasheet |
| PCB manufacturer and standard stack-up | User / JLCPCB / PCBWay |
| Layer structure, dielectric and copper thicknesses | PCB manufacturer |
| Trace width, pair spacing and required copper clearance | Manufacturer's stack-up and impedance calculation |

- [ ] **DIF-01** — Identify all differential signal pairs in the design.
- [ ] **DIF-02** — Obtain missing impedance, tolerance and length requirements from the user or the relevant technical document.
- [ ] **DIF-03** — Obtain the stack-up and impedance information for the manufacturing conditions to be used from JLCPCB and/or PCBWay.
- [ ] **DIF-04** — Define the calculated trace width and differential pair spacing values in the PCB design rules.
- [ ] **DIF-05** — For each pair, apply a continuous reference plane and the required length matching and pair spacing rules.
- [ ] **DIF-06** — Do not finalize traces that need controlled impedance without a verified manufacturer stack-up.
- [ ] **DIF-07** — If the manufacturer changes, re-verify the impedance geometry with the new manufacturer's stack-up information.
- [ ] **DIF-08** — Distinguish low-speed differential traces that need no special manufacturing from traces that need controlled impedance; do not create unnecessary manufacturing cost.
- [ ] **DIF-09** — **Pair naming the EDA recognizes:** Both nets have the same base name and the suffix the EDA uses for pairs. KiCad: `+`/`-` or `P`/`N` at the end (e.g. `USB_D+`/`USB_D-`, `LVDS_CLK_P`/`LVDS_CLK_N`); Altium: a Differential Pair directive on the pair (`_P`/`_N` names). After the netlist import into the PCB, check that the EDA lists each pair as a differential pair; if not, fix the names before routing.
- [ ] **DIF-10** — **Route as a coupled pair:** Route each pair with the EDA's differential pair router, not as two single traces. Keep width and pair spacing constant (net class / diff pair rule, DIF-04); uncouple only at pads and breakouts and keep those parts short. Place vias as a symmetric pair with a GND return via nearby (LAY-17); no stubs, no test points on the line except at a pad; no other trace between the two lines. Tune length with small bumps near the mismatch, not on one long side.
- [ ] **DIF-11** — **Pair table as evidence:** Record a table for each pair: pair name, interface, net class, target impedance, width/spacing used, intra-pair length difference vs. limit, layer changes. Put it in the review evidence; the Reviewer checks it against the board (REV-17).

### RF / High-Speed — conditional design profile

> Enable this profile only if the project has the related requirements. Do not use general PCB limits in place of controlled impedance or SI/PI requirements.

- [ ] **HS-01** — Define the relevant signal groups and the impedance, tolerance, timing, skew/length, termination, loss and noise requirements from device/interface documents in `Project-README.md` with short references.
- [ ] **HS-02** — Verify a suitable manufacturer stack-up, material, layer structure and tolerances. Choose special material or manufacturing for RF/high-speed only if there is a real technical requirement.
- [ ] **HS-03** — Transfer the approved trace requirements to EDA net classes and routing constraints. Review the relevant rules for reference plane/return path, trace transitions, and discontinuities from connectors and vias.
- [ ] **HS-04** — Determine the need for signal integrity / power integrity, PDN, thermal and EM/RF analysis from the project requirements. Field solvers, simulation or lab measurement are applied only if required; record tool access and acceptance criteria.
- [ ] **HS-05** — The Reviewer verifies that the relevant trace classes comply with the approved requirements, the manufacturer stack-up and real analysis/measurement evidence. A clean DRC alone does not verify SI/PI or RF performance.

### RF — conditional, tiered by band

> **Apply only if the board has an RF circuit.** If there is no RF, this whole part is N/A and the user is not asked RF questions. If there is RF, first learn the band, choose the tier and record it in `Project-README.md`.

| Tier | Frequency | Typical example | Default approach |
| :--- | :--- | :--- | :--- |
| **RF-A** | < 1 GHz | 433/868/915 MHz, LoRa, remote control | Standard FR-4 is usually sufficient. 50 Ω microstrip or GCPW. Via fence recommended, not mandatory. |
| **RF-B** | 1–6 GHz | GNSS, 2.4/5 GHz WiFi, BLE | FR-4 acceptable for short traces with a loss calculation. GCPW preferred. Via fence spacing ≤ λg/10, preferably ≤ λg/20. |
| **RF-C** | > 6 GHz | Radar, X-band and above, mmWave | RF laminate or hybrid stack-up (manufacturer-approved). GCPW mandatory, via fence ≤ λg/20. Connector launch per manufacturer reference. EM simulation or measurement evidence required. |

λg (wavelength in the dielectric) ≈ c / (f · √εeff). Example: 2.4 GHz, FR-4 microstrip (εeff ≈ 3.3) → λg ≈ 69 mm → λg/20 ≈ 3.4 mm. Verify values with the manufacturer's real stack-up and a calculation tool.

- [ ] **RF-01** — Is there RF? If not, N/A. If yes, obtain the band, TX/RX function, output power or sensitivity, antenna or connector type and regulatory compliance requirements.
- [ ] **RF-02** — For hobby and simple projects, first propose a **certified off-the-shelf RF module** (antenna included or with U.FL/SMA output); design a custom RF circuit only if the user asks or the requirements demand it. If a module is used, the module manufacturer's layout guide (antenna keepout, GND, supply) is binding.
- [ ] **RF-03** — Set the 50 Ω (or other approved impedance) trace geometry with the manufacturer's stack-up and a calculation tool. Prefer GCPW. Keep the reference plane under the trace continuous; do not route other signals under or beside the trace.
- [ ] **RF-04** — Apply a GND via fence on both sides along the RF trace; choose the spacing by tier. The gap between polygon and trace must equal the calculated GCPW value.
- [ ] **RF-05** — Connect RF component GND pads with Direct Connect and place multiple GND vias at the point closest to the pad. For PA/LNA exposed pads, follow the thermal via pattern in the datasheet.
- [ ] **RF-06** — Use mitered or curved transitions at bends. Apply a taper if pad and trace widths differ greatly. At high frequency, prefer small packages (0402 or smaller, if the assembly method allows).
- [ ] **RF-07** — For RF connectors (SMA, U.FL, edge-launch), use the manufacturer-recommended footprint and launch geometry. Leave no copper on any layer in the antenna keepout area. Leave a position for a tunable matching network (pi) in front of the antenna or connector.
- [ ] **RF-08** — Separate TX/RX, LO/clock, DC-DC and digital noise sources from the RF path. If needed, add a shield can footprint with a via fence around it. Keep RF traces short.
- [ ] **RF-09** — Record verification evidence: impedance calculation, simulation if any (e.g. `.s2p`) and measurement if any (VNA, spectrum analyzer). If no measurement or simulation was done, mark it "not verified".
