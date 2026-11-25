# Manufacturing

Bu klasör başlangıçta yalnızca `templates/` içerir (boş BOM, PnP, şematik çıktı, montaj çizimi ve fab notu şablonları; bkz. [templates/README.md](templates/README.md)). G1 üretim dosyası onayı ve başarılı yerel `check-export` doğrulaması olmadan Gerber, drill, BOM, PnP/CPL, stencil veya diğer release dosyaları oluşturulmaz.

Onay verildiğinde ilgili tasarım revizyonu için bir alt klasör kullan (ör. `R01/`). Dosyaları `projectctl.py name` önekiyle adlandır (ör. `DR00627-R01_BOM.csv`, varyant için `DR00627-AV-R01_BOM.csv`); çıktı seti `Hardware-Rules.md` bölüm 09'dadır. Tüm dosyalar aynı onaylı kaynaktan üretilir. Reviewer bunları kontrol eder. Tasarım değişmişse eski onayla yeni export yapılmaz.

Multi-PCB projede onaylı üretim dosyalarını `<revision>/<board-id>/` altında ayrı tut. İstenmişse onaylı komple sistem CAD/STEP çıktısı için `<revision>/Assembly/` kullan. Kartları ve konnektör/kablo ilişkilerini ortak proje revizyonuyla tutarlı kaydet.

Üretim dosyalarının oluşturulması tek başına PCB siparişi verme yetkisi değildir.

Release öncesinde `python scripts/projectctl.py manifest` ile revizyon klasörüne `MANIFEST.sha256` yaz. `check-release` bu manifesti doğrular; manifestten sonra dosya değişirse release engellenir.
