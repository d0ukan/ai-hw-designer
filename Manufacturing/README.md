# Manufacturing

Bu klasör başlangıçta boştur. G1 üretim dosyası onayı ve başarılı yerel `check-export` doğrulaması olmadan Gerber, drill, BOM, PnP/CPL, stencil veya diğer release dosyaları oluşturulmaz.

Onay verildiğinde ilgili tasarım revizyonu için bir alt klasör kullan (ör. `REV-A/`). Tüm dosyalar aynı onaylı kaynaktan üretilir. Reviewer bunları kontrol eder. Tasarım değişmişse eski onayla yeni export yapılmaz.

Multi-PCB projede onaylı üretim dosyalarını `<revision>/<board-id>/` altında ayrı tut. İstenmişse onaylı komple sistem CAD/STEP çıktısı için `<revision>/Assembly/` kullan. Kartları ve konnektör/kablo ilişkilerini ortak proje revizyonuyla tutarlı kaydet.

Üretim dosyalarının oluşturulması tek başına PCB siparişi verme yetkisi değildir.

Release öncesinde `python scripts/projectctl.py manifest` ile revizyon klasörüne `MANIFEST.sha256` yaz. `check-release` bu manifesti doğrular; manifestten sonra dosya değişirse release engellenir.
