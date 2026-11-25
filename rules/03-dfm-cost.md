<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
## 03 · JLCPCB / PCBWay — DFM & Cost Optimization

> Üretim maliyetini düşürmek için gerekli olmayan özel PCB teknolojilerinden kaçın; "gerekli" kararı INT-48 tasarım hedefine göre verilir. Aşağıdaki varsayılanlar standart rigid FR-4 tasarım ve Hobi/Endüstriyel profil içindir; bölüm 00B'de onaylanan farklı malzeme, teknoloji ve kalite isterleri ile Havacılık profilinde bölüm 08 önceliklidir.

| PCB özelliği | Varsayılan tercih |
| :--- | :--- |
| PCB tipi | Standart rigid FR-4 |
| PCB kalınlığı | 1.6 mm |
| Katman sayısı | Gereksinimleri karşılayan en düşük standart katman sayısı |
| Dış katman bakır kalınlığı | 1 oz |
| Solder mask | Standart yeşil |
| Via tipi | Mekanik delikli through-hole via |
| Yüzey kaplaması | Uygun maliyetli standart seçenek; pad ve temas gereksinimlerine göre |
| Stack-up | İlgili üreticinin standart stack-up seçenekleri |

- [ ] **DFM-00** — Kullanıcı medikal, askeri/havacılık, HDI, özel stack-up veya belirli bir üretici istemediyse (Hobi, Endüstriyel; INT-48 hedefi Maliyet öncelikli veya Dengeli) JLCPCB ve/veya PCBWay'in standart kabiliyetlerini ve standart stack-up'ını esas al; amaç en düşük maliyettir. Performans öncelikli hedefte standart üretim yine ilk seçenektir; ancak performans gerektiriyorsa özel üretici, laminat veya stack-up gerekçesiyle önerilir. Özel istek varsa bölüm 00B kararları ve gerekirse bölüm 08 önceliklidir.
- [ ] **DFM-01** — JLCPCB ve PCBWay'in güncel standart üretim limitlerini kontrol et.
- [ ] **DFM-02** — Tasarım kurallarını mümkün olduğunca iki üreticinin de standart üretim kabiliyetleriyle uyumlu tut.
- [ ] **DFM-03** — Gerekmedikçe blind via, buried via, microvia, HDI ve via-in-pad kullanma.
- [ ] **DFM-04** — Standart sinyal ve GND via'larını tented via olarak tanımla. Açık olması gereken CHASSIS_GND via'larında bu kuralı uygulama.
- [ ] **DFM-05** — Gerekmedikçe özel laminat, özel bakır kalınlığı, özel solder mask rengi ve maliyeti artıran ilave üretim süreçlerini seçme.
- [ ] **DFM-06** — Footprint, solder mask dam, pad aralığı ve komponent yerleşimini PCB/PCBA üretim limitleriyle uyumlu tut.
- [ ] **DFM-07** — Standart üretim dışında maliyet artışına yol açan tüm seçenekleri, gerekçeleriyle kullanıcıya bildir.
- [ ] **DFM-08** — Komponent seçimini onaylanan tedarik stratejisine ve dizgi yöntemine göre yap. Gerçek MPN, footprint, stok, lifecycle bilgisi ve üreticinin PCBA dizgi kabiliyetini doğrula; teyit edilemeyen bilgileri açıkça belirt.
- [ ] **DFM-09** — Manuel dizgi veya stencil + SMT tercih edilmişse kullanıcı tarafından onaylanan paket boyutu, pad erişimi ve rework gereksinimlerini koru. PCBA tercih edilmişse seçilen dizgi hizmetinin komponent tedarik, paket ve montaj limitlerini doğrula.
- [ ] **DFM-10** — Teknik gereksinimleri sağlayan seçenekler arasında BOM, PCB ve dizgi maliyetinin toplamını INT-48 tasarım hedefine göre değerlendir; Performans öncelikli hedefte daha pahalı ama ölçülebilir fayda sağlayan seçeneği tercih edebilirsin. Uygun olduğunda standart, yaygın ve önceden doğrulanmış komponentleri, footprint'leri ve referans devreleri yeniden kullan. Her standart pasif için kapsamlı fiyat araştırması yapma; önemli maliyet veya tedarik riski oluşturan parçaları karşılaştır.
- [ ] **DFM-11** — Kritik veya pahalı komponentlerde teknik olarak uygun, onaylanabilir alternatifleri değerlendir. Stok ve fiyat bilgilerini doğrulayabildiğin tarih itibarıyla kaydet; doğrulanmamış fiyat veya stok uydurma.
- [ ] **DFM-12** — Yeni komponent araştırmadan önce `Hardware-Library/catalog/` kayıtlarını kontrol et. Doğrulanmış symbol, footprint, CAD model ve devre bloklarını, exact MPN ve geçerlilik koşulları uyuyorsa yeniden kullan. Yeni veya değiştirilen varlıkları bağımsız review tamamlanmadan VERIFIED olarak kaydetme.
- [ ] **DFM-14** — **Muadil:** Her komponent için mümkünse en az 1 **drop-in muadil** belirle: aynı footprint ve pinout, eşdeğer veya daha iyi elektriksel/termal değer ve sıcaklık sınıfı; tercihen farklı üretici (gerçek ikinci kaynak). Parça yoksa muadil doğrudan takılıp dizgiye devam edilebilmeli. Muadili BOM'un `Alternate MPN` ve katalog `alternates` alanına yaz; bulunamazsa "muadil yok" diye işaretle. Muadil footprint/pinout'u Reviewer doğrular.
- [ ] **DFM-15** — **Footprint katman haritası:** Footprint'lerde yalnızca ortak katman haritasını kullan: bakır, solder mask, paste, silkscreen, courtyard, Fab/Assembly (gövde ve designator) ve 3D gövde. KiCad'de KiCad Library Convention (KLC) katmanları, Altium'da proje başında belirlenen tek bir mechanical katman haritası (veya component layer type) geçerlidir. Haritada olmayan özel katman kullanma; böylece çıktıda gereksiz katman oluşmaz (`Hardware-Library/README.md`).
- [ ] **DFM-13** — Onaylı hazır modülleri ve konnektör çiftlerini exact parça/revizyon ile kütüphaneye kaydet. Modülün pin/footprint/3D modeli ile uygun karşı konnektör ve montaj yönteminin eşleşmesini doğrula; her projede aynı varlıkları yeniden modelleme.
