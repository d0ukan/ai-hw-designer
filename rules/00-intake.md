<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
## 00 · Project Intake — Proje başlangıç anketi

> **ZORUNLU — TASARIMA BAŞLAMADAN ÖNCE:** Soru sırası: anlatım tercihi (INT-46) → proje kimliği (INT-49) → projenin amacı (INT-01) → kalite profili (INT-47) → tasarım hedefi (INT-48) → ilgili teknik sorular. Aşağıdaki soruları projenin kapsamına göre kullanıcıya yönelt. Daha önce verilen bilgileri tekrar sorma. Kritik gereksinimler ve tasarım tercihleri netleşmeden komponent seçimine, şematiğe veya PCB layout'a başlama.

### Başlangıç · İletişim tercihi

- [ ] **INT-46** — İlk görüşmede kullanıcıya sor: **Anlatım nasıl olsun? Caveman (çok kısa ve sade), Balanced (dengeli) veya Detailed (detaylı)?** Seçimini `Project-README.md` içinde kaydet ve sonraki kullanıcı yanıtlarında uygula. Mevcut tercih varsa yeniden sorma; kullanıcı daha sonra değiştirebilir. Yanıt alınmazsa Balanced kullan.

| Mod | Kullanıcıya anlatım biçimi |
| :--- | :--- |
| Caveman | Kısa, doğrudan, sade cümleler; yalnızca gerekli bilgiler ve kararlar. |
| Balanced | Özlü açıklama, önemli teknik gerekçeler ve gerektiğinde küçük karşılaştırmalar. |
| Detailed | Teknik ayrıntılar, hesaplamalar, varsayımlar ve alternatiflerin gerekçeleri. |

Anlatım tercihi mühendislik doğrulamasını, kritik uyarıları, gerçek kanıt kayıtlarını veya kullanıcı onay kapılarını azaltmaz. Ajanlar arası görev ve sonuç özetleri her modda gereksiz ayrıntıdan arındırılır.

### Başlangıç · Proje kimliği

- [ ] **INT-49** — Anlatım tercihinden hemen sonra sor: **proje adı, proje kodu ve revizyon** (ör. ad "Sensör kartı", kod `DR00627`, revizyon `R01`). Kod biçimini kullanıcı belirler; örnek biçimi dayatma. Varyant varsa harfini sor (A, B, …). Adı `projectctl.py set project_name`, kodu `set project_code`, revizyonu `set design_revision` ile kaydet. Bu soru ertelenemez; kod olmadan export yapılmaz.
- [ ] **INT-50** — Tüm çıktılar bu kimlikle adlandırılır (bölüm 09): `<kod>-<rev>` → `DR00627-R01`, varyant için `<kod>-<harf>V-<rev>` → `DR00627-AV-R01`. Öneki `python scripts/projectctl.py name [--variant A]` verir.

### Başlangıç · "Sonra karar ver" seçeneği

- [ ] **INT-51** — Kritik olmayan sorularda (ör. logo/ikon, silkscreen yazıları, designator görünümü, imza, renk) kullanıcıya **"Sonra karar ver"** seçeneği sun. Ertelenen soruyu `Project-README.md` "Açık kararlar" tablosuna AÇIK olarak yaz ve en geç ilgili kapıda tekrar sor: kart üzerindeki her şey (logo, yazılar, designator, imza; PCB-17…21) için **G0.5**, yani layout başlamadan önce. Hâlâ yanıt yoksa güvenli varsayılanı kullan ve kaydet (logo, imza, bakır yazı yok; designator açık). Kritik sorularda (besleme, güvenlik, izolasyon, konnektör/pinout, gerilim/akım, kalite profili, proje kimliği) bu seçenek yoktur.

### Başlangıç · Kalite profili

- [ ] **INT-47** — Proje amacını öğrendikten sonra sor: **Bu kart hangi seviyede olacak? Hobi, Endüstriyel veya Havacılık?** Seçimi `Project-README.md` içinde kaydet. Profil yalnızca kuralların sertliğini ve varsayılanları belirler; kullanıcı her varsayılanı ayrıca değiştirebilir. Tahmin ederek profil seçme; yanıt yoksa kullanıcıya önerini gerekçesiyle sun ve onay bekle.

| Profil | Tipik kullanım | Varsayılan yaklaşım |
| :--- | :--- | :--- |
| Hobi | Kişisel proje, prototip, düşük maliyet | JLCPCB/PCBWay standart hattı, en az katman, ticari sıcaklık sınıfı (ör. 0…+70 °C) yeterliyse kabul, LCSC/JLC Parts gibi uygun tedarik, IPC Class 2 seviyesi üretim |
| Endüstriyel | Sahada uzun süre güvenilir çalışma | Genişletilmiş sıcaklık (ör. −40…+85 °C), giriş koruma devreleri, uzun ömürlü ve çok kaynaklı komponent, IPC Class 2 (gerekirse Class 3) |
| Havacılık | Uçuş, askeri veya benzeri yüksek güvenilirlik | Bölüm 08 profili zorunlu; IPC Class 3, derating politikası, izlenebilirlik, kullanıcı tarafından bildirilen standartlar ve uygun sertifikalı üretici |

Profil seçimi gereksiz maliyet oluşturmamalıdır: Hobi projeye Havacılık kuralı, Havacılık projeye Hobi varsayılanı uygulama. RF ve Havacılık bölümleri yalnızca ilgili olduğunda etkinleşir; ilgisizse N/A olarak bırakılır.

### Başlangıç · Tasarım hedefi (maliyet / performans)

- [ ] **INT-48** — Profilden sonra sor: **Tasarım hedefi nedir? Maliyet öncelikli, Dengeli (fiyat/performans) veya Performans öncelikli?** Hedef maliyet veya bütçe varsa onu da al (INT-03). Seçimi `Project-README.md` içinde kaydet. Yanıt yoksa profile göre varsayılanı öner ve onay al: Hobi → Maliyet öncelikli, Endüstriyel → Dengeli, Havacılık/askeri → Performans öncelikli (kullanıcı ayrıca maliyet hedefi vermediyse).

| Hedef | Komponent, PCB ve layout kararları |
| :--- | :--- |
| Maliyet öncelikli | Gereksinimi karşılayan en ucuz yeterli çözüm; standart üretim (DFM-00), en az katman, yaygın ve ucuz parça |
| Dengeli | Gereksinimi güvenli payla karşılayan en iyi fiyat/performans; maliyet artışı ancak ölçülebilir fayda varsa |
| Performans öncelikli | Önce elektriksel performans, güvenilirlik, pay ve uzun ömür; gerekiyorsa daha iyi komponent, ek katman, özel laminat, kontrollü empedans, daha geniş derating. Maliyet engel değildir ama gereksiz lüks de eklenmez |

Hiçbir hedefte gereksinim, güvenlik, güvenilirlik veya doğrulama maliyet uğruna kısılmaz. Performans öncelikli hedefte de maliyeti artıran her seçim gerekçesiyle bildirilir (AI-03, DFM-07); yalnızca onayı engellemez. Bu hedef yalnızca donanım kararları içindir; AI model/token verimliliği her zaman geçerlidir.

**Soru stratejisi:** Önce mevcut gereksinim dokümanlarını ve proje bilgilerini incele. Genel amacı öğrendikten sonra yalnızca ilgili teknik soru gruplarını, mümkün olduğunca tek bir toplu soru listesi halinde sor. Cevapları `Project-README.md` içinde Zorunlu / Tercih / Esnek / Belirsiz / N/A olarak kaydet. Kullanıcı açıkça kabul ederse önerilen ekonomik varsayılanları kullan. Şematik veya komponent seçimini etkileyen PCB ve mekanik kısıtları G0'dan önce öğren; kalan üretim ve mekanik ayrıntıları bölüm 00B'de netleştir.

### A · Proje amacı ve kapsamı

- [ ] **INT-01** — **Bu projenin amacı nedir?** PCB ne yapacak, hangi cihazda veya sistemde kullanılacak ve temel fonksiyonları neler olacak?
- [ ] **INT-02** — Tasarım sıfırdan mı yapılacak, yoksa mevcut bir şematik/PCB revize mi edilecek? Gereksinim dokümanı, referans tasarım veya mevcut dosya var mı?
- [ ] **INT-03** — Tasarım prototip, seri üretim veya test/geliştirme amaçlı mı? Tahmini üretim adedi ve hedef PCB/PCBA birim maliyeti nedir?
- [ ] **INT-04** — Hangi EDA yazılımı ve sürümü kullanılacak? (KiCad, Altium Designer, EasyEDA Pro vb.) Kullanıcının mevcut ve yetkili MCP server, native CLI, API/script veya GUI erişimi var mı? Mevcut entegrasyon tercihlerini ve gerçek yeteneklerini kaydet.
- [ ] **INT-27** — Projeye ait yazılı isterler, müşteri gereksinimleri, ICD, teknik şartname, referans kart veya zorunlu komponent listesi var mı? Hangi isterler kesin, hangileri tasarımcıya bırakılmış?
- [ ] **INT-40** — Kullanıcının bu projeye özel ilave tasarım kuralları, tercihleri, kabul kriterleri veya yasakları var mı? Bunları kaynağı ve onayıyla `Project-README.md` içine kaydet; genel kurallarla çelişen noktaları netleştir.
- [ ] **INT-28** — Kartın ana işlevi/tipi nedir? Güç kaynağı veya güç dağıtımı, fonksiyonel kontrol/MCU, analog ölçüm, dijital haberleşme, RF, sensör/arayüz, motor sürücü veya karma bir kart mı? Yalnızca ilgili teknik soru grubunu aç.
- [ ] **INT-32** — **Proje tek PCB mi, yoksa multi-PCB sistem mi olacak?** Birden fazla kart varsa kart sayısı, kart isimleri/ID'leri, her kartın fonksiyonu ve varsa mevcut kartlar nelerdir? Güç ve sinyal dağılımını kart bazında netleştir.
- [ ] **INT-33** — Multi-PCB sistemde kartlar birbirine nasıl bağlanacak? Board-to-board (mezzanine/header/backplane), cable-to-board/harness, flex bağlantı veya farklı bir yöntem mi? Mevcut konnektörler, karşı konnektörler, pinout, besleme/sinyal arayüzleri ve mekanik bağlantı kısıtları var mı? Yalnızca multi-PCB projede ilgili soruları aç.

### B · Elektriksel gereksinimler

- [ ] **INT-05** — Besleme AC mi, DC mi, batarya mı, USB mi veya birden fazla kaynaktan mı sağlanacak? Minimum / nominal / maksimum giriş gerilimi, sürekli ve tepe akım/güç değerleri, gerekli çıkış beslemeleri ve mevcut besleme kaynağının sınırları nedir? AC ise frekans ve faz bilgisi; DC ise polarite, giriş dalgalanması ve varsa geçici gerilim koşullarını sor.
- [ ] **INT-06** — Giriş/çıkışlar, konnektörler, haberleşme arayüzleri ve sinyal seviyeleri nelerdir? Diferansiyel veya kontrollü empedans gerektiren hat var mı?
- [ ] **INT-07** — Ölçüm doğruluğu, frekans, örnekleme hızı, akım kapasitesi veya diğer performans gereksinimleri neler?
- [ ] **INT-08** — ESD, surge, ters polarite, aşırı gerilim/akım, EMC/EMI veya belirli bir test/standart gereksinimi bulunuyor mu?
- [ ] **INT-29** — Her giriş/çıkışın yönü, sayısı, normal ve maksimum değerleri, yük tipi, beklenen akımı, zamanlama ve açılış/kapanış koşulları nedir? Belirli konnektör ve pinout zorunluluğu var mı?
- [ ] **INT-30** — Harici kablo, bağlanacak cihaz, güç kaynağı, sensör ve yüklerin özellikleri tanımlı mı? Referans devre veya mevcut sistemle uyumluluk gerekiyor mu?
- [ ] **INT-34** — **Sistem fiziksel olarak dışarıya hangi arayüzlerle çıkacak?** Güç, veri, sensör, RF ve diğer I/O için istenen konnektör tipi, marka/MPN, pin sayısı, pinout, panel/PCB montajı, kablo çıkış yönü ve varsa karşı konnektör/kablo takımı nedir? Konnektör seçimini kullanıcı yapacak mı, yoksa AI önerip onaylatacak mı?
- [ ] **INT-41** — RF, kontrollü empedanslı veya high-speed arayüz bulunuyor mu? Varsa ilgili datasheet/interface specification, frekans/veri hızı ve kenar süresi bilgileri, hedef empedans, timing/skew/length limitleri, bağlantı/terminasyon ve doğrulama isterlerini al. Gerekli olmayan ayrıntıları sorma. **RF yoksa** bölüm 05'in RF kısmı N/A olur ve RF sorusu sorulmaz. **RF varsa** çalışma frekansını/bandını sor ve bölüm 05'teki RF kademesini (RF-A / RF-B / RF-C) belirle.

#### Kart tipine göre koşullu teknik sorular

| Kart tipi | Yalnızca uygulanabilen ek gereksinimleri sor |
| :--- | :--- |
| Güç kartı | Çıkış gerilim/akımları, sürekli/tepe yük, verim, ripple, sıcaklık sınırı, koruma ve izolasyon isterleri |
| Fonksiyonel / MCU kontrol kartı | Fonksiyonlar, I/O sayısı, lojik seviyeler, arayüzler, işlemci tercihi, programlama/debug, yazılım uyumluluğu |
| Analog / ölçüm kartı | Ölçüm aralığı, doğruluk, çözünürlük, örnekleme hızı, bant genişliği, gürültü sınırı, sensör arayüzü |
| Dijital / haberleşme kartı | Protokoller, veri hızı, arayüz seviyeleri, konektörler, diferansiyel empedans ve zamanlama gereksinimleri |
| RF kartı | Çalışma frekansı/bandı, RX/TX işlevi, çıkış gücü/hassasiyet, anten veya RF konnektör tipi, sertifikalı modül kabulü, düzenleyici uyumluluk (ör. CE RED, FCC), malzeme ve kontrollü empedans gereksinimi |
| Sensör / arayüz kartı | Sensör tipi, besleme, sinyal aralığı, kablo ve kalibrasyon gereksinimleri |
| Motor / aktüatör kontrol kartı | Yük tipi, elektriksel arayüz, besleme ve akım sınırları, çalışma döngüsü, geri besleme ve koruma isterleri |
| Karma kart | Yalnızca kullanılan fonksiyonların yukarıdaki isterleri |

### C · Şase, GND ve izolasyon

- [ ] **INT-09** — Cihazda metal şase/kasa, PE (Protective Earth) veya ayrı bir CHASSIS_GND bağlantısı var mı? Topraklama mimarisini belirle; kart çevresindeki CHASSIS_GND ring kullanımını ayrı bir tercih olarak bölüm 00B'de kesinleştir.
- [ ] **INT-10** — Galvanik izolasyon gerekiyor mu? Varsa hangi devreler, beslemeler ve GND bölgeleri birbirinden izole olacak? Devre GND'si ile CHASSIS_GND de izole mi olacak?
- [ ] **INT-11** — **İzolasyon yoksa ve CHASSIS_GND mevcutsa:** CHASSIS_GND ile ana devre GND'si doğrudan bağlanabilir mi? Bağlanacaksa kullanıcı hangi bağlantı şeklini ve noktasını tercih ediyor?
- [ ] **INT-12** — **İzolasyon varsa:** Maksimum çalışma ve geçici gerilimler, izolasyon tipi ve varsa uygulanacak standart nedir? Bu gerilimlere göre kullanıcı tarafından istenen minimum GND–CHASSIS_GND clearance ve creepage mesafeleri kaç mm'dir? Diğer izole bölgeler arasındaki mesafeleri de sor.
- [ ] **INT-13** — Montaj delikleri, konnektör shield'ları ve metal kasa hangi GND netine bağlanacak? Belirtilmemiş bağlantıları otomatik kurma.

| Kullanıcının kararı | AI'ın uygulaması |
| :--- | :--- |
| İzolasyon yok ve doğrudan bağlantı onaylı | CHASSIS_GND ile ana GND'yi onaylanan bağlantı mimarisine göre birleştir. |
| İzolasyon yok ancak bağlantı onaylanmadı | Netleri ayrı tut; bağlantı tercihinin belirlenmesini bekle. |
| GND–CHASSIS_GND izolasyonu gerekli | Onaylanan minimum clearance/creepage mesafelerini tüm ilgili bakır ve bağlantılar için uygula. |
| İzolasyon gereksinimi veya mesafeler bilinmiyor | Kullanıcıdan gerekli gerilim ve izolasyon bilgilerini iste; rastgele bir mesafe belirleme. |
| CHASSIS_GND ring kullanılmayacak | Çevre halkası ve ona ait stitching via/mask açıklığı oluşturma. Kullanıcı onaylı topraklama mimarisini koru. Bu olağan bir tercih olup istisna değildir. |

**Önemli:** Normal netler için tanımlanan 0.20 mm copper clearance, galvanik izolasyon mesafesi olarak kabul edilmemelidir. İzolasyon gereksinimleri projeye ve geçerli standarda göre ayrıca doğrulanmalıdır.

### D · Komponent seçimi ve tedarik stratejisi

- [ ] **INT-14** — Komponentler hangi tedarik kanallarından seçilecek?

| Seçenek | Tedarik yaklaşımı |
| :--- | :--- |
| Global | DigiKey, Mouser, Farnell, RS vb. |
| Asya / PCBA ekosistemi | LCSC, JLCPCB Parts ve onaylı diğer tedarikçiler |
| Hibrit | Her iki gruptan maliyet, stok, teknik uygunluk ve tedarik edilebilirliğe göre seçim |

- [ ] **INT-15** — Zorunlu üretici/marka, onaylı komponent listesi, yasaklı komponentler, stok ve lifecycle politikası veya mevcut kullanılacak parçalar var mı?
- [ ] **INT-16** — Komponent seçiminde öncelik maliyet, performans, kalite/izlenebilirlik, stok bulunabilirliği veya uzun vadeli tedarik edilebilirlikten hangisi? INT-48 tasarım hedefi varsa onunla tutarlı olsun; tekrar sorma, yalnız farkı netleştir.
- [ ] **INT-35** — **Hazır modül kullanımı kabul ediliyor mu?** Örneğin ESP32, nRF, CC1101 veya başka hazır haberleşme/işlemci/sensör modülleri kullanılabilir mi, yoksa tasarım discrete IC ve komponentlerden mi oluşmalı? Kullanıcının elinde mevcut veya özellikle tercih ettiği modül varsa exact MPN/model/revizyonu ve datasheet'i iste. Onay olmadan hazır modül seçme.
- [ ] **INT-52** — Kart batarya ile mi çalışacak veya batarya şarj edecek mi? Evetse kimya, hücre sayısı ve kapasiteyi al ve bölüm 10 (Batarya ve şarj) kurallarını aç; hayırsa bölüm 10 N/A.
- [ ] **INT-36** — Hazır modül veya önceden belirlenmiş konnektör kullanılacaksa kullanıcının elinde **STEP/3D CAD datası, footprint, symbol ve mekanik çizim** bulunuyor mu? Modülün bağlantı yöntemi, pinout'u, karşı konnektör/header, montaj ve mekanik gereksinimlerini doğrula. Model yoksa önce doğrulanmış kütüphanede veya üretici kaynağında ara; gerekirse kullanıcıdan ölçü/çizim iste. Yaklaşık envelope model ancak açık onayla kullanılabilir ve doğrulanmış STEP modeli olarak gösterilemez.

### E · PCB üretimi, mekanik tasarım ve dizgi

- [ ] **INT-17** — PCB hangi üreticide üretilecek? JLCPCB, PCBWay veya her ikisiyle uyumlu tasarım mı isteniyor?
- [ ] **INT-18** — PCB nasıl dizilecek?

| Seçenek | Dizgi yöntemi |
| :--- | :--- |
| Manuel | El lehimleme (THT / SMT) |
| Stencil + SMT | Stencil ile lehim pastası, manuel yerleştirme ve reflow |
| PCBA | Üreticinin otomatik komponent dizgi hizmeti |
| Hibrit | Otomatik PCBA ve belirli komponentlerin manuel dizgisi |

- [ ] **INT-19** — PCB'nin boyutları, şekli, maksimum komponent yüksekliği, montaj deliği konumları ve mekanik/kasa kısıtları nelerdir?
- [ ] **INT-20** — Katman sayısı, PCB kalınlığı, bakır kalınlığı veya yüzey kaplaması için özel bir şart var mı? Yoksa bölüm 03'teki ekonomik varsayılanlar kullanılabilir mi?
- [ ] **INT-21** — Çalışma ortamı ve sıcaklık aralığı nedir? Nem, titreşim, toz/su, muhafaza veya soğutmaya ilişkin özel gereksinimler var mı?
- [ ] **INT-22** — Tek veya çift taraflı komponent dizgisi tercih ediliyor mu? Kullanılabilecek en küçük komponent paketi, manuel lehimleme ve rework kısıtları var mı?
- [ ] **INT-31** — Şematik/komponent seçimini etkileyen bir PCB teknolojisi, laminat, yüksek güç/ısı dağıtımı, flex bölgesi, boyut, özel kalite veya üretim kısıtı var mı? Varsa G0 öncesinde kaydet; detayları layout öncesi kesinleştir.

### F · Test, doğrulama ve teslimat

- [ ] **INT-23** — Projede MCU, FPGA veya başka programlanabilir komponent var mı? Varsa aşağıdaki programlama/debug seçimini tamamla. Programlama gerektirmeyen analog tasarımda bu soru grubunu N/A bırak; gerektiğinde test point, test düzeneği ve üretim testini ayrıca sor.

#### Programlama, flash ve debug — yalnızca gerektiğinde

- [ ] **INT-42** — Programlama **kart üzerinde (in-system/on-board)** mı yapılacak, yoksa komponent kart dışında (off-board) programlanıp mı takılacak? Fabrika çıkışı programlı komponent, bootloader ile güncelleme, üretim/test fikstürü veya başka bir yöntem isteniyor mu? Geliştirme, üretim ve saha güncellemesi ihtiyaçlarını ayırt et.
- [ ] **INT-43** — On-board programlama ve/veya debug isteniyorsa hangi arayüz kullanılacak? JTAG, SWD, ISP/ICSP, UART/USB bootloader veya hedef komponentin desteklediği başka bir arayüz mü? Sadece flashlama mı, debug da mı yapılacak? Standart debugger/programmer (modeli ve dokümanı) tercih ediliyor mu?
- [ ] **INT-44** — Programlama/debug fiziksel bağlantısı nasıl olacak? Standart JTAG/SWD konnektörü, üreticiye özel header, custom konnektör, pogo-pin/test pad/Tag-Connect tarzı konnektörsüz pad-fikstür çözümü veya başka bir seçenek mi? Konnektör MPN, pin sayısı/pinout, pitch, Pin 1/yön, mating connector ve kart/kasa içindeki erişim gereksinimlerini netleştir. Kullanıcı tercihi yoksa öneri sun ve onaylat.
- [ ] **INT-45** — Seçilen hedef komponent ve programmer/debugger dokümanlarına göre gereken referans gerilim/lojik seviyeleri, kartın programlama sırasındaki besleme yöntemi, gerekli reset/boot sinyalleri ve varsa programlama/test kabul kriterlerini kaydet. Off-board programlama seçilmişse kullanıcı ayrıca on-board debug/güncelleme istemedikçe gereksiz programlama konnektörü ekleme.

#### Diagnostik, test ve teslimat

- [ ] **INT-37** — **Diagnostik ve durum göstergeleri isteniyor mu?** Power LED, MCU/status/heartbeat LED, haberleşme TX/RX veya link LED, fault/error LED, debug LED, test point, reset/programlama arayüzü gibi öğelerden hangileri gerekiyor? Göstergelerin anlamı, renk tercihi, kullanıcı tarafından görünürlüğü ve gerekirse yazılım davranışını sor. Kullanıcı istemiyorsa gereksiz LED veya debug devresi ekleme.
- [ ] **INT-24** — Tasarımın doğrulanması için hangi testler, ölçümler ve kabul kriterleri gerekli?
- [ ] **INT-25** — Hangi dosyalar teslim edilecek? Native EDA projesi, PDF schematic, Gerber, drill, BOM, Pick & Place (CPL), montaj çizimi (`_ASSY.pdf`), fab notu, stencil ve/veya 3D STEP gerekli mi? Varsayılan set ve dosya adları bölüm 09'dadır.
- [ ] **INT-38** — Proje sonunda tek tek PCB 3D modelleri dışında **komple sistemin birleştirilmiş STEP/CAD assembly** dosyası isteniyor mu? PCB'ler, hazır modüller, konnektörler, karşı parçalar, varsa kasa ve mekanik referansların hangileri modele dahil olacak? Kullanıcının mevcut CAD datasını ve istenen teslim formatını baştan öğren.

### Tasarıma başlama koşulu — Design Input Approval

- [ ] **INT-26** — Projenin karmaşıklığına uygun kısa bir sistem mimarisi, fonksiyonel bloklar, arayüzler ve gerekiyorsa güç bütçesi belirle. Basit tasarımlarda birkaç maddelik özet yeterlidir; blok diyagramı ve ayrı raporları yalnızca fayda sağlayacaksa oluştur.
- [ ] **INT-39** — Multi-PCB projelerde kart kimliklerini ve kartlar arası/harici arayüzleri tek bir kısa arayüz tablosunda kaydet. Modül, konnektör ve diagnostik tercihleri şematik/komponent seçimine başlamadan önce onaylat.
- [ ] Projeye özel gereksinimleri ve alınan kararları tek bir kısa proje özeti halinde kullanıcıya sun.
- [ ] Yanıtlanmamış kritik konuları ve önerilen varsayımları açıkça belirt.
- [ ] Kullanıcının onayını aldıktan sonra tasarıma başla. Onaylanan bilgiler sonradan değişirse ilgili tasarım kararlarını yeniden değerlendir.
