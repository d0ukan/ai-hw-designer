# Hardware Library

Proje içindeki ortak, tekrar kullanılabilir donanım kütüphanesi. İlk tasarım adımında katalogları ara; uygun doğrulanmış bir kayıt varsa sıfırdan araştırma veya modelleme yapma.

| Klasör | İçerik |
| :--- | :--- |
| `catalog/components.csv` | MPN bazlı doğrulanmış komponent, hazır modül, konnektör ve kaynak girişleri |
| `catalog/blocks.csv` | Devre blokları, versiyonları ve geçerlilik koşulları |
| `symbols/` | EDA schematic symbols |
| `footprints/` | EDA PCB footprints |
| `models3d/` | STEP veya EDA uyumlu 3D modeller |
| `datasheets/` | Paylaşılmasına izin verilen kaynaklar; aksi halde katalogda bağlantı |
| `design-blocks/` | Doğrulanmış ve yeniden kullanılabilir native devre blokları |

## Kullanım ve doğrulama

1. Exact MPN, manufacturer, package, symbol/pinout ve footprint eşleşmesini kontrol et.
2. Katalogdaki datasheet revizyonunu, kaynak sayfalarını ve geçerlilik koşullarını incele.
3. Uygun değilse mevcut kaydı değiştirmek yerine yeni revizyon/ayrı MPN kaydı oluştur.
4. Yeni varlıkları Designer ekler; Reviewer doğruladıktan sonra `VERIFIED` olarak işaretlenir. İncelenmemiş varlık `UNVERIFIED` veya `BLOCKED` kalır.
5. Devre bloklarını farklı besleme, yük, arayüz, tolerans veya çalışma koşullarında doğrudan doğrulanmış kabul etme.
6. Stok/fiyat gibi zamanla değişen bilgiler gerekiyorsa güncel olarak kontrol edilir. Lisans ve yeniden dağıtım izinlerini koru; izinsiz datasheet/CAD dosyalarını paylaşma.
7. Onaylı hazır modülleri ve konnektör/karşı konnektör çiftlerini ayrı exact MPN/model kayıtlarıyla takip et. Kullanıcının verdiği STEP datasını ve kaynak revizyonunu kaydet; doğrulanmamış yaklaşık CAD modeli gerçek mekanik model olarak kullanma.

### `components.csv` ek sütunları

| Sütun | İçerik | Örnek |
| :--- | :--- | :--- |
| `temp_range` | Datasheet'teki çalışma sıcaklığı | `-40..+85C` |
| `lifecycle` | Üretici yaşam döngüsü durumu ve kontrol tarihi | `Active (2026-11)` / `NRND` / `EOL` |
| `qualification` | Kalite sınıfı | `Commercial` / `Industrial` / `AEC-Q100` / `MIL` |
| `alternates` | Onaylı alternatif MPN'ler (`;` ile ayrılır) | `MPN-A;MPN-B` |
| `msl` | Nem hassasiyet seviyesi | `1` / `3` |
| `rohs` | RoHS durumu | `Yes` / `No` |

`alternates` alanına mümkünse en az 1 drop-in muadil yaz: aynı footprint ve pinout, eşdeğer veya daha iyi değerler, tercihen farklı üretici (DFM-14). Bulunamazsa `notes` alanına "muadil yok" yaz.

Bilinmeyen alanı boş bırak; uydurma. Hobi projelerde yalnızca gerekli sütunları doldurmak yeterlidir, Havacılık profilinde `temp_range`, `lifecycle`, `qualification` ve `alternates` zorunludur.

### Footprint katman haritası (DFM-15)

Footprint'ler yalnızca aşağıdaki ortak katmanları kullanır; haritada olmayan özel katman kullanılmaz. Böylece çıktı alırken gereksiz katman oluşmaz.

| İçerik | KiCad (KLC) | Altium (proje başında sabitlenir; örnek) |
| :--- | :--- | :--- |
| Bakır, solder mask, paste | `F/B.Cu`, `F/B.Mask`, `F/B.Paste` | Top/Bottom Layer, Solder, Paste |
| Silkscreen (gövde çizgisi, Pin 1) | `F/B.SilkS` | Top/Bottom Overlay |
| Courtyard | `F/B.CrtYd` | Mech 15/16 veya Courtyard layer type |
| Fab/Assembly (gövde, designator `${REFERENCE}`) | `F/B.Fab` | Mech 13/14 veya Assembly layer type |
| 3D gövde | 3D model | Mech 13/14 veya 3D Body layer type |

Altium'da mechanical katman numaraları kişiden kişiye değişir; projede seçilen haritayı `Project-README.md` içine yaz ve tüm footprint'lerde aynısını kullan. Mümkünse Altium'un component layer type (Assembly, Courtyard, 3D Body) özelliğini kullan. İsimlendirme IPC-7351'e yakın tutulur.

Katalog başlangıçta yalnızca sütun başlıklarını içerir. Hazır doğrulanmış komponent veya devre bulunduğu varsayılmamalıdır. Kopyalanmış proje kütüphanesi daha sonra kullanıcı tarafından template repository'ye review ile geri kazandırılabilir.

Katalogda MPN veya blok kimliği aramak için EDA aracının arama özelliğini ya da örneğin `rg -i --fixed-strings "MPN" Hardware-Library/catalog/components.csv` komutunu kullan. Basit katalog sorguları ayrı LLM çağrısı gerektirmez.
