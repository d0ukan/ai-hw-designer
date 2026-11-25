# Üretim template'leri

Boş başlangıç dosyaları. Projede `Manufacturing/<rev>/` içine kopyala, `<önek>` ile yeniden adlandır ve doldur. `<önek>` = `python scripts/projectctl.py name [--variant A]` (ör. `DR00627-R01`, `DR00627-AV-R01`). Kurallar: `Hardware-Rules.md` bölüm 09.

| Template | Proje çıktısı | Not |
| :--- | :--- | :--- |
| `bom.csv` | `<önek>_BOM.csv` | Her varyant için ayrı. `DNP` = `Yes` olan parça takılmaz. `Alternate MPN` en az 1 drop-in muadil (DFM-14); yoksa `Notes` = "muadil yok". `Comment`, `Designator`, `Footprint`, `LCSC Part #` sütunları JLCPCB yüklemesiyle uyumludur. |
| `pnp.csv` | `<önek>_PnP.csv` | Birim mm, açı derece. `Layer` = `Top` / `Bottom`. DNP parçalar listede olmaz. Üreticinin rotasyon referansını sipariş ekranında kontrol et. |
| `schematic-outputs.md` | `<önek>_SCH.pdf` ve ekleri | Şematik çıktı listesi |
| `assembly-drawing.md` | `<önek>_ASSY.pdf` | Draftsman tarzı montaj çizimi |
| `fab-notes.md` | `<önek>_FAB.md` veya `.pdf` | Üreticiye fab notu |

Revizyon geçmişi kökteki `REVISION-HISTORY.md` dosyasında tutulur. Bu klasördeki template'ler release değildir; `manifest` ve `check-release` yalnızca `Manufacturing/<rev>/` klasörünü kontrol eder.
