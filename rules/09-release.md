<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
## 09 · Revizyon, varyant ve çıktılar

- [ ] **REL-01** — **Revizyon mu, varyant mı?** Bakır, outline, delik veya stack-up değişiyorsa yeni **revizyon** olur (R01 → R02). PCB aynı kalıp yalnızca takılan parçalar veya değerler değişiyorsa **varyant** olur (`DR00627-AV-R01`, `DR00627-BV-R01`).
- [ ] **REL-02** — **Revizyon geçişi:** Revizyon atlatılırken kullanıcıya sor: **Ne değişti, neden?** Yanıtı madde madde projenin `REVISION-HISTORY.md` dosyasına yaz (tarih, değişiklikler, sebep, etkilenen kart/dosyalar, onaylayan). Önceki revizyonun bilinen hatalarını (errata) da ekle. Eski revizyonun onay ve review kayıtları yeni revizyona taşınmaz.
- [ ] **REL-03** — **Çıktı seti:** Teslim edilecek çıktıları INT-25'e göre seç; tipik set aşağıdadır. Her varyantın kendi BOM ve PnP dosyası olur; DNP parçalar PnP'den çıkarılır, BOM'da DNP olarak kalır. Template'ler `Manufacturing/templates/` içindedir.
- [ ] **REL-04** — Çıktıları `Manufacturing/<rev>/` içine koy, ardından `projectctl.py manifest` ve `check-release` çalıştır. Kök klasördeki dosya adları proje koduyla başlamalıdır.

| Çıktı | Dosya adı | Not |
| :--- | :--- | :--- |
| Gerber + drill | `<önek>_Gerber.zip` | Üreticinin istediği katman seti |
| BOM | `<önek>_BOM.csv` | Varyant başına; MPN, muadil, DNP |
| Pick & Place | `<önek>_PnP.csv` | Varyant başına; DNP hariç |
| Şematik | `<önek>_SCH.pdf` | Revizyon ve tarih başlıkta |
| Montaj çizimi (Draftsman tarzı) | `<önek>_ASSY.pdf` | Top/bottom, designator, Pin 1/polarite, DNP işaretli, ölçüler; bottom görünümün aynalı olup olmadığı yazılı |
| Fab notu | `<önek>_FAB.md` veya `.pdf` | Stack-up, kalınlık, kaplama, renk, IPC sınıfı, özel istekler |
| 3D model | `<önek>.step` | İstenirse |

`<önek>` = `projectctl.py name [--variant X]` çıktısı.
