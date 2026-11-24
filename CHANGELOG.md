# Changelog

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
