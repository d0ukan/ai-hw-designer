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

Bilinmeyen alanı boş bırak; uydurma. Hobi projelerde yalnızca gerekli sütunları doldurmak yeterlidir, Havacılık profilinde `temp_range`, `lifecycle`, `qualification` ve `alternates` zorunludur.

Katalog başlangıçta yalnızca sütun başlıklarını içerir. Hazır doğrulanmış komponent veya devre bulunduğu varsayılmamalıdır. Kopyalanmış proje kütüphanesi daha sonra kullanıcı tarafından template repository'ye review ile geri kazandırılabilir.

Katalogda MPN veya blok kimliği aramak için EDA aracının arama özelliğini ya da örneğin `rg -i --fixed-strings "MPN" Hardware-Library/catalog/components.csv` komutunu kullan. Basit katalog sorguları ayrı LLM çağrısı gerektirmez.
