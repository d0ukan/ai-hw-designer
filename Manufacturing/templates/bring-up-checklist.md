# <önek> — Bring-up ve test checklist (VER-09)

Kartı ilk kez enerjilendirirken sırayla ilerle. Her adımın sonucunu ve ölçülen değeri yaz; yapılmayan adım "doğrulanmadı" kalır.

| # | Adım | Beklenen | Ölçülen / sonuç |
| :--- | :--- | :--- | :--- |
| 1 | Görsel kontrol: köprü, ters parça, eksik parça, polarite | Hata yok | |
| 2 | Enerji vermeden besleme–GND direnci (her ray) | Kısa devre yok | |
| 3 | Akım sınırlı kaynakla ilk enerji (düşük limit) | Beklenen boşta akım | |
| 4 | Her besleme rayının gerilimi ve ripple'ı | Tasarım değeri ± tolerans | |
| 5 | Isınan parça kontrolü (dokunma/termal kamera) | Anormal ısınma yok | |
| 6 | Reset, saat (kristal/osilatör) | Çalışıyor | |
| 7 | Programlama/debug bağlantısı (varsa) | Bağlanıyor | |
| 8 | Arayüz ve fonksiyon testleri (INT-24 kabul kriterleri) | Geçti | |
| 9 | Varsa batarya/şarj testleri (BAT-08) | Geçti | |
| 10 | Sonuçları `REVIEW_LOG.md` ve `Project-README.md` checkpoint'e işle | Kayıtlı | |
