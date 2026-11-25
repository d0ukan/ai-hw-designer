# Changelog

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
