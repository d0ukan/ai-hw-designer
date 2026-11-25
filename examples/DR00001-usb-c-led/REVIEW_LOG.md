# Review Log (örnek)

| Bulgu ID | Önem | Aşama / revizyon / konum | Kanıt ve sorun | Beklenen düzeltme | Durum |
| :--- | :--- | :--- | :--- | :--- | :--- |
| F-001 | MAJOR | Şematik / R01 / R4 | R4 (0 Ω, LED'e seri) DNP işaretliydi; takılmazsa LED devresi açık kalır | R4 takılı olsun; ölçüm için sökülebilir köprü olarak not düş | VERIFIED |
| F-002 | MINOR | Şematik / R01 / R3 | 1 kΩ ile akım ≈ 3 mA; REQ-02 ~2 mA istiyor | R3 = 1.5 kΩ | VERIFIED |
| F-003 | MINOR | BOM / R01 / D1 (A varyantı) | Önerilen yeşil muadil InGaN, Vf ~3 V; drop-in değil | Muadili kaldır, "muadil yok" yaz | VERIFIED |

## Review sonuçları

| Aşama | Revizyon | Kontrol / kanıt | Sonuç |
| :--- | :--- | :--- | :--- |
| Şematik | R01 | F-001…F-003 kapandı; ERC örnekte yok (EDA dosyası yok) | PASS |
| PCB | R01 | Yerleşim ve routing kontrol listesi (örnek) | PASS |
| Üretim | R01 | `check-bom` temiz; manifest incelendi | PASS |
