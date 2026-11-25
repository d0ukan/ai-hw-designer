<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
## 01 · PCB üretim parametreleri

Aşağıdaki değerler üreticilerin mutlak üretim sınırları değil, standart üretim için tercih edilen **varsayılan tasarım limitleridir**. Son kontrol: 2026-11 (JLCPCB/PCBWay standart kabiliyetleri). Sipariş öncesinde üreticinin güncel sayfasıyla karşılaştır; tarih eskidiyse yeniden kontrol et.

| Parametre | Değer | Koşul |
| :--- | :---: | :--- |
| Minimum trace width | **0.20 mm** | Güç ve empedans gereksinimlerine göre artır |
| Minimum copper clearance | **0.20 mm** | Gerilim ve izolasyon gereksinimlerine göre artır |
| Minimum via hole | **0.30 mm** | Standart through-hole via |
| Minimum via pad diameter | **0.60 mm** | Annular ring gereksinimini ayrıca sağla |
| Minimum copper-to-board-edge clearance | **0.30 mm** | Üretici limitlerini de doğrula |
| CHASSIS_GND ring genişliği | **≥ 1.50 mm** | Yalnızca kullanıcı onaylı ring için |
| CHASSIS_GND stitching via hole | **0.80 mm** | Yalnızca ring onaylıysa; pad çapı ve teknoloji uygunluğunu doğrula |
| CHASSIS_GND stitching via aralığı | **3.00 mm** | Yalnızca ring onaylıysa; merkezden merkeze nominal aralık |
