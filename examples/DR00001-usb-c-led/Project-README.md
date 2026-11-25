# Project README — DR00001 USB-C LED kartı (örnek)

| Alan | Proje bilgisi |
| :--- | :--- |
| Proje adı / amaç | USB-C LED kartı — USB-C'den 5 V alıp güç LED'i yakmak |
| Proje kodu / revizyon / varyantlar (INT-49) | `DR00001` / `R01` / A (yeşil LED) |
| Çıktı öneki | `DR00001-R01`, `DR00001-AV-R01` |
| Kalite profili | Hobi |
| Tasarım hedefi (INT-48) | Maliyet öncelikli |
| RF | N/A |
| Batarya (INT-52) | N/A |
| Tek PCB / multi-PCB | Tek PCB |
| Besleme | USB-C sink, 5 V, < 50 mA |
| EDA / bağlantı | KiCad 9 / GUI (örnekte EDA dosyası yok) |
| Üretici / dizgi | JLCPCB, PCBA tek yüz. LCSC numaraları sipariş öncesi JLC kataloğundan doğrulanıp BOM'a yazılır (örnekte uydurulmadı) |
| Kullanıcı anlatım tercihi | Caveman |

## Onaylı gereksinimler

| İster ID | İster / hedef | Öncelik | Kaynak / onay | Doğrulama |
| :--- | :--- | :--- | :--- | :--- |
| REQ-01 | USB-C 5 V kaynağından besleme, CC 5.1 kΩ pull-down | Zorunlu | Kullanıcı, G0 | Multimetre ile VBUS |
| REQ-02 | Güç LED'i, ~2 mA | Zorunlu | Kullanıcı, G0 | R4 sökülüp akım ölçülür |
| REQ-03 | Kart ≤ 20 × 14 mm | Tercih | Kullanıcı, G0 | Mekanik ölçü |

## Onaylı PCB girdileri — G0.5

| Alan | Karar |
| :--- | :--- |
| Yapı / laminat | Rigid FR-4, 2 katman, 1.6 mm |
| Outline | 20 × 14 mm, köşeler R1.0 |
| CHASSIS_GND halkası | Hayır |
| Logo / ikon — PCB-17 | Yok |
| Kart kodu — PCB-18 | Silkscreen, bottom, `DR00001-R01` + tarih |
| Konnektör etiketi — PCB-19 | Yok (tek USB-C) |
| Designator — PCB-20 | Açık, 0.8 mm, parçanın kenarında |
| İmza — PCB-21 | Sonra karar ver → G0.5'te "Yok" |

## Açık kararlar ("Sonra karar ver", INT-51)

| ID | Ertelenen karar | En geç | Sonuç |
| :--- | :--- | :--- | :--- |
| OD-01 | İmza / easter egg | G0.5 | Kullanıcı "yok" dedi, kapandı |

## Varyantlar

| Varyant | Önek | Fark | BOM / PnP |
| :--- | :--- | :--- | :--- |
| — | `DR00001-R01` | Kırmızı LED | `DR00001-R01_BOM.csv` / `_PnP.csv` |
| A | `DR00001-AV-R01` | Yeşil LED | `DR00001-AV-R01_BOM.csv` / `_PnP.csv` |

## Mimari ve tasarım kararları

| ID | Karar | Kaynak |
| :--- | :--- | :--- |
| D-01 | LED akımı: (5.0 V − 2.0 V) / 1.5 kΩ ≈ 2.0 mA. Vf ≈ 2.0 V, LTST-C191KRKT/KGKT datasheet'indeki tipik değer; 2 mA'deki Vf'i datasheet eğrisinden doğrula | Hesap |
| D-02 | R4 0 Ω takılı seri köprü: sökülüp yerine ampermetre bağlanır | SCH-07 |
| D-03 | C1 10 µF DNP: VBUS bulk opsiyonu; uzun kabloda veya ESD testinde gerekirse takılır | SCH-07 |
| D-04 | A varyantında yeşil LED'in drop-in muadili yok (farklı Vf); BOM'da "muadil yok" | DFM-14 |
