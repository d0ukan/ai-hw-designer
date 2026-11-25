# <önek> — Şematik çıktıları

| Çıktı | Dosya | Durum |
| :--- | :--- | :--- |
| Şematik PDF (tüm sayfalar, başlık bloğunda kod / revizyon / varyant / tarih) | `<önek>_SCH.pdf` | Bekliyor |
| Netlist (EDA'nın standart formatı) | `<önek>_NET.<ext>` | İstenirse |
| ERC raporu (temiz veya istisnalar gerekçeli) | `<önek>_ERC.txt` | Bekliyor |
| Varyant farkları (takılan/takılmayan parçalar) | `<önek>_BOM.csv` içinde DNP | Varsa |

## Kontrol

- [ ] Başlık bloğunda proje adı, `<önek>`, sayfa no ve tarih doğru
- [ ] DNP parçalar şematikte işaretli
- [ ] Net adları ve diferansiyel çiftler (`_P/_N`) okunur
- [ ] ERC sonucu Reviewer kanıtı olarak kaydedildi
