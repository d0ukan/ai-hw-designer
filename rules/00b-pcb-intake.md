<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
## 00B · PCB Intake — Layout öncesi teknik ve mekanik kararlar

> **ZORUNLU — PCB TASARIMINA GEÇMEDEN ÖNCE (G0.5):** Manager, onaylı şematik girdileri ve bilinen mekanik/üretim tercihleri üzerinden eksik PCB özelliklerini sorar. Önceden açıkça onaylanmış, değişmemiş kararları yeniden sorma; tek bir PCB tasarım özetiyle kullanıcının onayını al. Bu aşama tamamlanmadan kart sınırını, stack-up'ı, placement ve routing'i finalize etme veya PCB layout'a başlama.

### A · PCB teknolojisi, malzeme ve kalite

- [ ] **PCB-01** — Kartın fiziksel yapısı nedir? Standart rigid, flex, rigid-flex veya başka özel yapı mı?
- [ ] **PCB-02** — Hangi PCB malzemesi/altlığı gerekiyor? Standart FR-4, özel/yüksek sıcaklık FR-4, alüminyum veya bakır metal-core (MCPCB/IMS), RF laminat, polyimide veya diğer? Metal-core kartı yalnızca kalın bakır folyo ile karıştırma.
- [ ] **PCB-03** — Standart via/laminasyon yeterli mi, yoksa HDI, microvia, blind/buried via, özel katman yapısı veya başka özel işlem gerekli mi? Gereklilik ve maliyeti üreticiyle doğrula; gerekmedikçe standart üretimi seç.
- [ ] **PCB-04** — Kalite/uygulama sınıfı nedir? Standart ticari, endüstriyel, medikal, otomotiv, havacılık/askeri veya başka bir özel şart mı? Belirli standart, kalite sınıfı, test, malzeme veya izlenebilirlik zorunluluğu var mı? Uygulama sınıfını PCB malzemesi veya yapısıyla aynı seçim olarak değerlendirme; üreticinin ilgili şartları karşılayabildiğini doğrula. Seçim INT-47 kalite profiliyle tutarlı olmalıdır; Havacılık profilinde bölüm 08'i uygula.

### B · Board Outline & Mechanical

- [ ] **PCB-05** — Boyut, birim, kart şekli (dikdörtgen, daire, özel profil), maksimum kalınlık/yükseklik, varsa toleranslar ve muhafaza/STEP referansı nedir?
- [ ] **PCB-06** — Dikdörtgen veya köşeli kartta köşeler nasıl olacak? **Keskin/küt 90° köşe, radius (R) ile yuvarlatılmış köşe veya pah (chamfer)** mı? Radius değeri (mm), pah ölçüsü/açısı ve hangi köşelere uygulanacağını sor; farklı köşe tipleri varsa ayrı kaydet.
- [ ] **PCB-07** — Montaj deliklerinin konumu ve çapı, PTH/NPTH tercihi, slot/cutout, kenar boşluğu, konnektör yönleri, kasa teması ve mekanik keepout alanları nedir? İç köşe, slot ve profil detaylarını üreticinin frezeleme kabiliyetiyle doğrula.
- [ ] **PCB-08** — Kasa/soğutucu teması, komponent maksimum Z yüksekliği, özel mekanik veya flex/bükülme kısıtları var mı? Mevcut mekanik dosyaları öncelikli kullan.
- [ ] **PCB-14** — Multi-PCB projelerde her kartın ayrı outline, katman, montaj ve şase halkası tercihini; kartların yerleşim yönünü, birbirine göre konumunu, board-to-board mesafesini ve varsa kablo güzergâhı/mekanik kısıtlarını onaylat. Sadece değişen veya eksik kart girdilerini sor.
- [ ] **PCB-15** — Modül ve konnektörlerin onaylı STEP/CAD modellerini, karşı konnektör eşleşmesini, birleşim yönünü, pin 1/yön, yerleşim ve erişim sınırlarını doğrula. Toplam CAD assembly isteniyorsa kartlar ve ilgili mekanik öğeler arasında çakışma/uyum kontrolü planla.
- [ ] **PCB-16** — On-board programlama veya debug onaylandıysa ilgili konnektör/pad/fikstür için yerleşim, Pin 1, erişim ve mekanik boşluk gereksinimini doğrula. G0'da belirlenen yöntemi değiştirme; programlama gerektirmeyen ya da yalnız off-board programlanan tasarımda bu kontrolü uygun şekilde N/A bırak.

### C · Stack-up & Manufacturing

- [ ] **PCB-09** — Üretici, standart katman sayısı/stack-up, bitmiş PCB kalınlığı, dış/iç copper weight, solder mask/silkscreen rengi ve yüzey kaplaması için özel istek var mı? Yoksa bölüm 03'teki fiyat/performans varsayılanlarını kullanıcıya öner.
- [ ] **PCB-10** — Kontrollü empedans, özel via, edge plating/castellation, panelleme, stencil, tek/çift taraflı dizgi veya özel üretim toleransları gerekiyor mu? Gerekiyorsa sadece ilgili üretici ve kullanıcı bilgilerini al; bölüm 05'i uygula.

### D · İsteğe bağlı CHASSIS_GND çevre halkası

- [ ] **PCB-11** — Kullanıcıdan açıkça sor: **Kartın etrafını dolaşan CHASSIS_GND copper ring istiyor musunuz? (Evet / Hayır)** Şase mevcut olsa dahi ring'i otomatik olarak oluşturma.
- [ ] **PCB-12** — Kullanıcı evet derse bölüm 01–02'deki varsayılan 1.50 mm halka, 3.00 mm via aralığı, 0.80 mm via hole ve açık solder mask tercihlerini öner; seçilen PCB teknolojisine ve üretici limitlerine uygunluğunu doğrula. Ring ana GND'ye bağlanacak mı, ayrı mı kalacak? Bölüm 00, C kısmında onaylanmış GND/izolasyon kararı geçerliyse yeniden sorma; eksikse netleştir.
- [ ] **PCB-13** — Kullanıcı hayır derse ring, ring'e ait stitching via ve ring solder mask açıklığı oluşturma; diğer devre GND polygon ve onaylı şase bağlantıları geçerlidir. Tercih belirsizse ring oluşturma ve G0.5 onayını bekle.

### E · Silkscreen ve işaretleme (her soru INT-51'e göre ertelenebilir)

- [ ] **PCB-17** — **Logo/ikon:** Kullanıcının kendi logosu veya sembolü konacak mı? Top, bottom veya ikisi? Dosyayı (tercihen SVG/PNG) ve kullanım hakkını kullanıcı sağlar; başkasına ait marka izinsiz konmaz.
- [ ] **PCB-18** — **Kart kodu:** `<kod>-<rev>` (ör. `DR00627-R01`) kart üzerine yazılsın mı? Silkscreen mi bakır mı; top, bottom veya ikisi? Tarih de eklensin mi? Bakır yazı net, RF, yüksek gerilim ve empedans hatlarından uzak, DRC uyumlu olur.
- [ ] **PCB-19** — **Konnektör etiketi:** Konnektörlerde pin numarası mı, net adı mı, ikisi mi yazılsın? Top, bottom veya ikisi?
- [ ] **PCB-20** — **Designator:** Açık mı gizli mi? Açıksa boyut (varsayılan: üretici minimumu, ör. JLCPCB için ~0.8–1.0 mm yükseklik, 0.15 mm çizgi) ve konum (parçanın içi veya kenarı/köşesi). Gizli designator kartı küçültebilir ama dizgi ve tamiri zorlaştırır; o durumda `_ASSY.pdf` zorunludur ve designator Fab/Assembly katmanında kalır. Hobi/elle dizgide ve Havacılık profilinde bu riski kullanıcıya hatırlat.
- [ ] **PCB-21** — **İmza / easter egg:** Kullanıcı isterse küçük bir imza veya çizim konabilir. DRC'yi bozmaz; RF, anten, yüksek gerilim ve test bölgelerine konmaz; uygunsuz içerik olmaz. Havacılık profilinde varsayılan kapalıdır.

### G0.5 · PCB Input Approval

- [ ] PCB özelliklerini ve mekanik kararları `Project-README.md` içinde tek bir kısa özetle kaydet.
- [ ] Şematikle çelişiyorsa yalnızca etkilenen gereksinimi ve tasarım alanını yeniden değerlendir. Gerekli durumda G0 onayını ve ilgili şematik review'u güncelle.
- [ ] PCB girdilerine ait revizyon ve gerçek kullanıcı onayını kaydet. Onaylanan, değişmeyen kararları ve doğrulama kanıtlarını tekrar üretme.
- [ ] INT-51 ile ertelenen kritik olmayan kararları (PCB-17…21) tekrar sor; yanıt yoksa güvenli varsayılanı kaydet.
- [ ] Layout'a başlamadan önce `python scripts/projectctl.py check-layout` başarılı olmalıdır.
