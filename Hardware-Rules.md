# Hardware Rules

**Hardware Design & PCB Layout Guidelines**

| Doküman | HW AI Design Rules |
| :--- | :--- |
| **Versiyon** | v1.13 |
| **Kapsam** | Project Intake · Schematic Design · PCB Intake · PCB Layout · DFM · PCBA · Koşullu RF ve Havacılık profilleri · Revizyon, varyant ve çıktılar · Koşullu batarya/şarj |
| **Hedef üreticiler** | JLCPCB / PCBWay (Hobi varsayılanı); diğer profillerde kullanıcı onaylı üretici |
| **Tasarım önceliği** | Güvenilirlik · Üretilebilirlik · Proje hedefine göre maliyet/performans (INT-48) · Token verimliliği |

> **Temel talimat:** Bu dokümanı tüm donanım tasarımlarında uygula. Standart ve kolay üretilebilir PCB'leri tercih et; maliyet ile performans arasındaki dengeyi INT-48'de seçilen tasarım hedefine göre kur. Bir kuralın uygulanamadığı durumda gerekçeyi açıkla ve kullanıcı onayı almadan istisna oluşturma.

> **Nasıl okunur:** Bu dosya bir dizindir; kurallar `rules/` klasöründe bölüm bölüm durur. Tüm dosyaları baştan okuma: yalnızca o anki aşamanın bölümünü aç. Kural kimlikleri (ör. `LAY-23`) tüm projede tektir; "bölüm 05" gibi atıflar aşağıdaki tablodaki dosyayı gösterir. Koşullu bölümler (05, 08, 10) ilgisizse hiç okunmaz. Dosyalara erişemeyen bir AI sohbetinde kullanıcıdan yalnız ilgili bölüm dosyasını iste.

| Bölüm | Kurallar | Ne zaman oku |
| :--- | :--- | :--- |
| [00 · Project Intake — Proje başlangıç anketi](rules/00-intake.md) | INT-01…INT-51 | Her yeni projede ilk oturumda (G0 öncesi) |
| [00B · PCB Intake — Layout öncesi teknik ve mekanik kararlar](rules/00b-pcb-intake.md) | PCB-01…PCB-21 | Layout öncesi (G0.5) |
| [01 · PCB üretim parametreleri](rules/01-pcb-parameters.md) | Varsayılan limit tablosu | PCB kurallarını EDA'ya girerken |
| [02 · Chassis, Ground & Polygon](rules/02-ground-polygon.md) | GND-01…GND-08 | GND, şase ve polygon işlerinde |
| [03 · JLCPCB / PCBWay — DFM & Cost Optimization](rules/03-dfm-cost.md) | DFM-00…DFM-15 | Komponent seçimi, üretici ve maliyet kararlarında |
| [04 · Schematic, Component Placement & Routing](rules/04-schematic-layout.md) | SCH-01…SCH-07, LAY-01…LAY-31 | Şematik, yerleşim, routing, SI/PI ve silkscreen |
| [05 · Differential Pairs, RF & High-Speed (SI/PI)](rules/05-diff-rf-hs.md) | DIF-01…DIF-08, HS-01…HS-05, RF-01…RF-09 | Yalnızca diferansiyel, high-speed veya RF varsa |
| [06 · Design Review & Verification](rules/06-verification.md) | VER-01…VER-12 | Review ve doğrulama aşamalarında |
| [07 · AI çalışma kuralları](rules/07-ai-rules.md) | AI-01…AI-08 | Her oturumda (kısa) |
| [08 · Havacılık / Aviyonik — koşullu profil](rules/08-aviation.md) | AVI-01…AVI-10 | Yalnızca Havacılık profilinde |
| [09 · Revizyon, varyant ve çıktılar](rules/09-release.md) | REL-01…REL-04 | Revizyon, varyant ve üretim çıktılarında |
| [10 · Batarya ve şarj — koşullu](rules/10-battery.md) | BAT-01…BAT-08 | Yalnızca kartta şarj edilebilir batarya varsa |

---

## Üretici referansları

| Üretici | PCB üretim kabiliyetleri | Empedans ve stack-up |
| :--- | :--- | :--- |
| **JLCPCB** | [PCB Capabilities](https://jlcpcb.com/capabilities/Capabilities?type=1) | [Impedance Calculator](https://jlcpcb.com/pcb-impedance-calculator/) · [Stack-up](https://jlcpcb.com/impedance) |
| **PCBWay** | [PCB Capabilities](https://www.pcbway.com/capabilities.html) | [Impedance Calculator](https://www.pcbway.com/pcb_prototype/impedance_calculator.html) |

> **Not:** Üreticilerin üretim seçenekleri ve fiyatlandırmaları değişebilir. Sipariş öncesinde seçilen üreticinin güncel kabiliyetleri ve sipariş ekranı esas alınmalıdır. Bu dokümandaki varsayılanlar belirli bir kartın elektriksel, mekanik veya güvenlik gereksinimlerinin yerine geçmez.
