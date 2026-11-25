<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
## 02 · Chassis, Ground & Polygon

- [ ] **GND-01** — Only if CHASSIS_GND ring use was explicitly approved in section 00B, create a CHASSIS_GND copper ring at least **1.50 mm** wide around the board edge on all applicable copper layers. If the user does not want it, this item and GND-02/GND-03 are N/A.
- [ ] **GND-02** — When the CHASSIS_GND ring is used, connect the rings with stitching vias of **0.80 mm** drill diameter at **3.00 mm** spacing.
- [ ] **GND-03** — When the CHASSIS_GND ring is used, keep the ring on the top and bottom layers free of solder mask. Preserve PCB edge clearances and a suitable surface finish.
- [ ] **GND-04** — Treat the CHASSIS_GND and circuit GND nets separately. Apply the connection or isolation architecture approved in section 00. If isolation is required, maintain the project-approved clearance and creepage values on all relevant layers and connections. Do not merge the nets without user approval.
- [ ] **GND-05** — Fill suitable free copper areas on all layers with the relevant GND polygons. Preserve isolated nets, dedicated power layers and required clearances to other nets. Polygon gap and via fence next to RF or controlled-impedance lines follow section 05; do not leave an uncalculated pour next to the line, and do not pour copper into the antenna keepout area.
- [ ] **GND-06** — Use **Thermal Relief** on component pads connected to the GND polygon to ease soldering and assembly. **Exception:** RF component GND pads, high-current pads and exposed/thermal pads use Direct Connect (section 05 RF-05, LAY-02); verify the solderability of these pads separately for the assembly method.
- [ ] **GND-07** — Use **Direct Connect** for GND via connections to polygons and planes; do not apply Thermal Relief to vias.
- [ ] **GND-08** — Do not interrupt GND return paths. Remove floating copper islands.

### Polygon connection summary

| Element | Connection type |
| :--- | :--- |
| Component GND pad | Thermal Relief |
| RF / high-current / exposed pad | Direct Connect |
| GND via | Direct Connect |
| CHASSIS_GND stitching via | Direct Connect |
