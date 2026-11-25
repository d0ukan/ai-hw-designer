# Changelog

## v1.13 — 2026-11-25

**AI ile kullanım ve token**
- `Hardware-Rules.md` artık bir dizin; kurallar `rules/` altında 11 bölüm dosyasına ayrıldı (içerik ve kural kimlikleri aynı). AI yalnızca ilgili bölümü okur.
- `AGENTS.md`: "Repo linkiyle başlayan AI" bölümü (neyi okuyacağı, kendi kopya, dosya erişimi olmayan web sohbeti, ilk sorular).
- `llms.txt` eklendi; README başına İngilizce özet ve "AI sohbetinde repo linkiyle başlamak" bölümü.

**projectctl**
- Commit bağı: `approve`/`review` git commit'ini kaydeder; review'dan sonra tasarım dosyaları değişirse `check-export`/`check-release` durur (şematik review yalnız şematik dosyalarına bakar).
- `check-bom`: BOM/PnP designator eşleşmesi, Qty, DNP, MPN; muadil eksikse uyarı. `check-release` bunu da çalıştırır.
- Dosya adı kontrolü alt klasörlere genişledi (önekli klasörlerin içi serbest); `templates` revizyon adı olarak yasak. 7 yeni test (toplam 41).
- `scripts/check_repo.py`: kural kimliği çakışması, tanımsız referans, bozuk link, sürüm satırları, CSV kolonları.

**Kurallar ve şablonlar**
- Bölüm 10 (BAT-01…08): batarya ve şarj, koşullu; INT-52 tetikler.
- `Manufacturing/templates/`: `bring-up-checklist.md`, `review-checklist.md`.
- `examples/DR00001-usb-c-led/`: dolu örnek proje (iki varyant, BOM/PnP, manifest); CI uçtan uca kontrol eder.

**Repo**
- CI: `check_repo.py` ve örnek proje adımları.
- `CONTRIBUTING.md`, issue ve PR şablonları; `.gitattributes` ve README'de Git LFS notu.

## v1.12 — 2026-11-25

**Proje kimliği ve çıktılar**
- INT-49/50: İlk iş proje adı, kodu, revizyon ve varyant sorulur; çıktılar `<kod>-<rev>` veya `<kod>-<harf>V-<rev>` önekiyle adlandırılır (ör. `DR00627-R01`, `DR00627-AV-R01`).
- `projectctl.py`: `project_code` alanı (eski state dosyalarıyla uyumlu), `name [--variant X]` komutu; `check-export` proje kodu ister, `check-release` kök dosya adlarının proje koduyla başlamasını kontrol eder. 7 yeni test (toplam 34).
- Bölüm 09 (REL-01…04): revizyon/varyant ayrımı, revizyon geçişinde "ne değişti, neden?" kaydı, çıktı seti ve isimleri.
- `REVISION-HISTORY.md` ve `Manufacturing/templates/` eklendi: `bom.csv`, `pnp.csv`, `schematic-outputs.md`, `assembly-drawing.md` (Draftsman tarzı `_ASSY.pdf`), `fab-notes.md`.

**Kurallar**
- INT-51: Kritik olmayan sorularda "Sonra karar ver" seçeneği; ertelenen karar ilgili kapıda tekrar sorulur, yanıt yoksa güvenli varsayılan.
- PCB-17…21: logo/ikon, kart kodu (silk/bakır, yüz, tarih), konnektör etiketi, designator (açık/gizli, boyut, konum), imza/easter egg soruları.
- LAY-30/31: Silkscreen her yüzde çakışmasız; işaretleme kararlarının uygulanması.
- DFM-14: Her komponente mümkünse en az 1 drop-in muadil. DFM-15: Ortak footprint katman haritası (KiCad KLC, Altium sabit mechanical harita).
- Roller: MGR-15/16, REV-13 (MCP'de Reviewer yalnız okur), REV-14 (çıktı seti kontrolü).

**MCP ve Git**
- README: KiCAD-MCP-Server ve altium-mcp kullanım notları.
- `.gitignore`: KiCad `fp-info-cache`, MCP `logs/`, Freerouting `*.dsn/*.ses`, Altium önizleme/log/çıktı klasörleri.
- `.gitattributes`: Altium tasarım dosyaları `binary`, `.PrjPcb`/`.OutJob` CRLF, EasyEDA `.epro` binary.

## v1.11.1 — 2026-11-25

- `README.md`: İş akışı şemasına şematik ve üretim kontrolü için REWORK geri dönüşleri eklendi; G1 yeniden onay kuralı açıklandı.

## v1.11 — 2026-11-25

**Kurallar (`Hardware-Rules.md`)**
- INT-48: Tasarım hedefi seçimi eklendi (Maliyet öncelikli / Dengeli / Performans öncelikli). Havacılık/askeri projede maliyet hedefi yoksa varsayılan Performans. DFM-00, DFM-10, INT-16, bölüm 03 notu ve başlık önceliği bu hedefe bağlandı; `Project-README.md`, `AGENTS.md`, MGR-14 ve `agents/Manager.md` güncellendi.

## v1.10 — 2026-11-25

**Kurallar (`Hardware-Rules.md`)**
- Bölüm 04 alt başlıklara ayrıldı: Genel, Yerleşim, Routing, SI / PI.
- SCH-03…SCH-07 şematik kuralları eklendi: güç ağacı ve ray filtreleri (PI), pin bazlı decoupling, SI hazırlığı (seri terminasyon, I²C pull-up, düşük kapasitanslı ESD, strapping pinleri), kısıtların şematikte işaretlenmesi, 0 Ω / DNP opsiyon yeri.
- DFM-00: Özel istek yoksa JLCPCB/PCBWay standart kabiliyeti ve stack-up'ı esas alınır.
- LAY-08…LAY-13 yerleşim kuralları eklendi: datasheet/app note referans layout'u, yerleşim sırası, giriş koruması, switching regülatör döngüsü, kristal, termal, hizalama ve erişim.
- LAY-14…LAY-24 routing kuralları eklendi: routing sırası, net class ve IPC-2152, katman kullanımı, bölünmüş düzlem ve dönüş via'sı, clock/3W, analog GND, güç dağıtımı ve Kelvin, yüksek gerilim, pad girişi/teardrop/acid trap, en kısa ve doğrudan yol (dolanan hat yasak, önce yerleşimi düzelt), kullanıcı onaylı free-angle/organik routing.
- LAY-25…LAY-29 SI/PI kuralları eklendi: decoupling döngüsü, kritik uzunluk (`tr × 2.5 cm`), empedans eşleştirme, length/delay matching, bitiş kontrolü.
- `README.md`: "Yerleşim ve routing" bölümü eklendi.

## v1.9 — 2026-11-25

**Kurallar (`Hardware-Rules.md`)**
- INT-47: Kalite profili seçimi eklendi: Hobi / Endüstriyel / Havacılık.
- Bölüm 05: RF kuralları isteğe bağlı ve banda göre kademeli hale getirildi (RF-A < 1 GHz, RF-B 1–6 GHz, RF-C > 6 GHz; RF-01…RF-09). RF yoksa bölüm N/A.
- Bölüm 08: Havacılık/Aviyonik koşullu profili eklendi (AVI-01…AVI-10: standartlar, IPC Class 3, derating, komponent, güç girişi, EMC, çevre, izlenebilirlik, analizler).
- GND-05/GND-06/LAY-05: RF, yüksek akım ve exposed pad istisnaları eklendi.

**Roller ve şablonlar**
- `Hardware-Roles.md`: MGR-14 (profil sorusu), MGR-09 ve REV-11 güncellendi.
- `AGENTS.md`, `agents/*.md`, `Project-README.md`: profil, RF bandı ve Havacılık alanları eklendi.
- `components.csv`: `temp_range`, `lifecycle`, `qualification`, `alternates`, `msl`, `rohs` sütunları eklendi.

**Araçlar**
- `projectctl.py`: `set`, `approve`, `revoke`, `review`, `block`, `unblock` kayıt komutları; `recorded_on` / `recorded_by` alanları.
- `projectctl.py manifest`: üretim çıktıları için SHA-256 manifest; `check-release` manifesti doğrular.
- GitHub Actions CI (Ubuntu + Windows, Python 3.10/3.12), MIT lisansı.

## v1.8

- İlk yayımlanan şablon.
