# Hardware Rules

**Hardware Design & PCB Layout Guidelines**

| Doküman | HW AI Design Rules |
| :--- | :--- |
| **Versiyon** | v1.9 |
| **Kapsam** | Project Intake · Schematic Design · PCB Intake · PCB Layout · DFM · PCBA · Koşullu RF ve Havacılık profilleri |
| **Hedef üreticiler** | JLCPCB / PCBWay (Hobi varsayılanı); diğer profillerde kullanıcı onaylı üretici |
| **Tasarım önceliği** | Güvenilirlik · Üretilebilirlik · Fiyat/performans · Token verimliliği |

> **Temel talimat:** Bu dokümanı tüm donanım tasarımlarında uygula. Standart, kolay üretilebilir ve uygun maliyetli PCB'leri tercih et. Bir kuralın uygulanamadığı durumda gerekçeyi açıkla ve kullanıcı onayı almadan istisna oluşturma.

---

## 00 · Project Intake — Proje başlangıç anketi

> **ZORUNLU — TASARIMA BAŞLAMADAN ÖNCE:** İlk görüşmede anlatım tercihini, ardından projenin amacını öğren. Aşağıdaki soruları projenin kapsamına göre kullanıcıya yönelt. Daha önce verilen bilgileri tekrar sorma. Kritik gereksinimler ve tasarım tercihleri netleşmeden komponent seçimine, şematiğe veya PCB layout'a başlama.

### Başlangıç · İletişim tercihi

- [ ] **INT-46** — İlk görüşmede kullanıcıya sor: **Anlatım nasıl olsun? Caveman (çok kısa ve sade), Balanced (dengeli) veya Detailed (detaylı)?** Seçimini `Project-README.md` içinde kaydet ve sonraki kullanıcı yanıtlarında uygula. Mevcut tercih varsa yeniden sorma; kullanıcı daha sonra değiştirebilir. Yanıt alınmazsa Balanced kullan.

| Mod | Kullanıcıya anlatım biçimi |
| :--- | :--- |
| Caveman | Kısa, doğrudan, sade cümleler; yalnızca gerekli bilgiler ve kararlar. |
| Balanced | Özlü açıklama, önemli teknik gerekçeler ve gerektiğinde küçük karşılaştırmalar. |
| Detailed | Teknik ayrıntılar, hesaplamalar, varsayımlar ve alternatiflerin gerekçeleri. |

Anlatım tercihi mühendislik doğrulamasını, kritik uyarıları, gerçek kanıt kayıtlarını veya kullanıcı onay kapılarını azaltmaz. Ajanlar arası görev ve sonuç özetleri her modda gereksiz ayrıntıdan arındırılır.

### Başlangıç · Kalite profili

- [ ] **INT-47** — Proje amacını öğrendikten sonra sor: **Bu kart hangi seviyede olacak? Hobi, Endüstriyel veya Havacılık?** Seçimi `Project-README.md` içinde kaydet. Profil yalnızca kuralların sertliğini ve varsayılanları belirler; kullanıcı her varsayılanı ayrıca değiştirebilir. Tahmin ederek profil seçme; yanıt yoksa kullanıcıya önerini gerekçesiyle sun ve onay bekle.

| Profil | Tipik kullanım | Varsayılan yaklaşım |
| :--- | :--- | :--- |
| Hobi | Kişisel proje, prototip, düşük maliyet | JLCPCB/PCBWay standart hattı, en az katman, ticari sıcaklık sınıfı (ör. 0…+70 °C) yeterliyse kabul, LCSC/JLC Parts gibi uygun tedarik, IPC Class 2 seviyesi üretim |
| Endüstriyel | Sahada uzun süre güvenilir çalışma | Genişletilmiş sıcaklık (ör. −40…+85 °C), giriş koruma devreleri, uzun ömürlü ve çok kaynaklı komponent, IPC Class 2 (gerekirse Class 3) |
| Havacılık | Uçuş, askeri veya benzeri yüksek güvenilirlik | Bölüm 08 profili zorunlu; IPC Class 3, derating politikası, izlenebilirlik, kullanıcı tarafından bildirilen standartlar ve uygun sertifikalı üretici |

Profil seçimi gereksiz maliyet oluşturmamalıdır: Hobi projeye Havacılık kuralı, Havacılık projeye Hobi varsayılanı uygulama. RF ve Havacılık bölümleri yalnızca ilgili olduğunda etkinleşir; ilgisizse N/A olarak bırakılır.

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
- [ ] **INT-16** — Komponent seçiminde öncelik maliyet, performans, kalite/izlenebilirlik, stok bulunabilirliği veya uzun vadeli tedarik edilebilirlikten hangisi?
- [ ] **INT-35** — **Hazır modül kullanımı kabul ediliyor mu?** Örneğin ESP32, nRF, CC1101 veya başka hazır haberleşme/işlemci/sensör modülleri kullanılabilir mi, yoksa tasarım discrete IC ve komponentlerden mi oluşmalı? Kullanıcının elinde mevcut veya özellikle tercih ettiği modül varsa exact MPN/model/revizyonu ve datasheet'i iste. Onay olmadan hazır modül seçme.
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
- [ ] **INT-25** — Hangi dosyalar teslim edilecek? Native EDA projesi, PDF schematic, Gerber, drill, BOM, Pick & Place (CPL), stencil ve/veya 3D STEP gerekli mi?
- [ ] **INT-38** — Proje sonunda tek tek PCB 3D modelleri dışında **komple sistemin birleştirilmiş STEP/CAD assembly** dosyası isteniyor mu? PCB'ler, hazır modüller, konnektörler, karşı parçalar, varsa kasa ve mekanik referansların hangileri modele dahil olacak? Kullanıcının mevcut CAD datasını ve istenen teslim formatını baştan öğren.

### Tasarıma başlama koşulu — Design Input Approval

- [ ] **INT-26** — Projenin karmaşıklığına uygun kısa bir sistem mimarisi, fonksiyonel bloklar, arayüzler ve gerekiyorsa güç bütçesi belirle. Basit tasarımlarda birkaç maddelik özet yeterlidir; blok diyagramı ve ayrı raporları yalnızca fayda sağlayacaksa oluştur.
- [ ] **INT-39** — Multi-PCB projelerde kart kimliklerini ve kartlar arası/harici arayüzleri tek bir kısa arayüz tablosunda kaydet. Modül, konnektör ve diagnostik tercihleri şematik/komponent seçimine başlamadan önce onaylat.
- [ ] Projeye özel gereksinimleri ve alınan kararları tek bir kısa proje özeti halinde kullanıcıya sun.
- [ ] Yanıtlanmamış kritik konuları ve önerilen varsayımları açıkça belirt.
- [ ] Kullanıcının onayını aldıktan sonra tasarıma başla. Onaylanan bilgiler sonradan değişirse ilgili tasarım kararlarını yeniden değerlendir.

---

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

### G0.5 · PCB Input Approval

- [ ] PCB özelliklerini ve mekanik kararları `Project-README.md` içinde tek bir kısa özetle kaydet.
- [ ] Şematikle çelişiyorsa yalnızca etkilenen gereksinimi ve tasarım alanını yeniden değerlendir. Gerekli durumda G0 onayını ve ilgili şematik review'u güncelle.
- [ ] PCB girdilerine ait revizyon ve gerçek kullanıcı onayını kaydet. Onaylanan, değişmeyen kararları ve doğrulama kanıtlarını tekrar üretme.
- [ ] Layout'a başlamadan önce `python scripts/projectctl.py check-layout` başarılı olmalıdır.

---

## 01 · PCB üretim parametreleri

Aşağıdaki değerler üreticilerin mutlak üretim sınırları değil, standart üretim için tercih edilen **varsayılan tasarım limitleridir**.

| Parametre | Değer | Koşul |
| :--- | :---: | :--- |
| Minimum trace width | **0.20 mm** | Güç ve empedans gereksinimlerine göre artır |
| Minimum copper clearance | **0.20 mm** | Gerilim ve izolasyon gereksinimlerine göre artır |
| Minimum via hole | **0.30 mm** | Standart through-hole via |
| Minimum via pad diameter | **0.60 mm** | Annular ring gereksinimini ayrıca sağla |
| Minimum copper-to-board-edge clearance | **0.30 mm** | Üretici limitlerini de doğrula |
| CHASSIS_GND ring genişliği | **≥ 1.50 mm** | Yalnızca kullanıcı onaylı ring için |
| CHASSIS_GND stitching via hole | **0.80 mm** | Yalnızca ring onaylıysa; pad çapı ve teknoloji uygunluğunu doğrula |
| CHASSIS_GND stitching via aralığı | **3.00 mm** | Yalnızca ring onaylıysa; merkezden merkeze nominal aralık |

---

## 02 · Chassis, Ground & Polygon

- [ ] **GND-01** — Yalnızca bölüm 00B'de CHASSIS_GND ring kullanımı açıkça onaylandıysa kart çevresinde, uygulanabilir tüm bakır katmanlarda en az **1.50 mm** genişliğinde CHASSIS_GND copper ring oluştur. Kullanıcı istemiyorsa bu madde ve GND-02/GND-03 N/A'dır.
- [ ] **GND-02** — CHASSIS_GND ring uygulandığında ring'leri, **0.80 mm** delik çapına sahip stitching via'larla **3.00 mm** aralıklarla birbirine bağla.
- [ ] **GND-03** — CHASSIS_GND ring uygulandığında üst ve alt katmandaki ring üzerinde solder mask bulunmasın. PCB kenar mesafelerini ve uygun yüzey kaplamasını koru.
- [ ] **GND-04** — CHASSIS_GND ve devre GND netlerini ayrı değerlendir. Bölüm 00'da onaylanan bağlantı veya izolasyon mimarisini uygula. İzolasyon gerekli ise proje bazlı onaylanan clearance ve creepage değerlerini tüm ilgili katmanlarda ve bağlantılarda koru. Kullanıcı onayı olmadan netleri birleştirme.
- [ ] **GND-05** — Tüm katmanlardaki uygun boş bakır alanlarını ilgili GND polygon'ları ile doldur. İzole netleri, özel güç katmanlarını ve diğer netlere ait gerekli clearance'ları koru. RF veya kontrollü empedans hatlarının yanındaki polygon boşluğu ve via fence bölüm 05'e göre belirlenir; hat yanında hesapsız pour bırakma, anten keepout alanına bakır dökme.
- [ ] **GND-06** — GND polygon'una bağlanan komponent pad'lerinde lehimleme ve dizgiyi kolaylaştırmak amacıyla **Thermal Relief** kullan. **İstisna:** RF komponent GND pad'leri, yüksek akım pad'leri ve exposed/termal pad'ler Direct Connect olur (bölüm 05 RF-05, LAY-02); bu pad'lerin lehimlenebilirliğini dizgi yöntemine göre ayrıca doğrula.
- [ ] **GND-07** — GND via'larının polygon ve plane bağlantılarında **Direct Connect** kullan; via'lara Thermal Relief uygulama.
- [ ] **GND-08** — GND dönüş yollarını kesintiye uğratma. Bağlantısız bakır adalarını (floating copper islands) kaldır.

### Polygon bağlantı özeti

| Eleman | Bağlantı tipi |
| :--- | :--- |
| Komponent GND pad'i | Thermal Relief |
| RF / yüksek akım / exposed pad | Direct Connect |
| GND via | Direct Connect |
| CHASSIS_GND stitching via | Direct Connect |

---

## 03 · JLCPCB / PCBWay — DFM & Cost Optimization

> Üretim maliyetini düşürmek için gerekli olmayan özel PCB teknolojilerinden kaçın. Aşağıdaki varsayılanlar standart rigid FR-4 tasarım ve Hobi/Endüstriyel profil içindir; bölüm 00B'de onaylanan farklı malzeme, teknoloji ve kalite isterleri ile Havacılık profilinde bölüm 08 önceliklidir.

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

- [ ] **DFM-01** — JLCPCB ve PCBWay'in güncel standart üretim limitlerini kontrol et.
- [ ] **DFM-02** — Tasarım kurallarını mümkün olduğunca iki üreticinin de standart üretim kabiliyetleriyle uyumlu tut.
- [ ] **DFM-03** — Gerekmedikçe blind via, buried via, microvia, HDI ve via-in-pad kullanma.
- [ ] **DFM-04** — Standart sinyal ve GND via'larını tented via olarak tanımla. Açık olması gereken CHASSIS_GND via'larında bu kuralı uygulama.
- [ ] **DFM-05** — Gerekmedikçe özel laminat, özel bakır kalınlığı, özel solder mask rengi ve maliyeti artıran ilave üretim süreçlerini seçme.
- [ ] **DFM-06** — Footprint, solder mask dam, pad aralığı ve komponent yerleşimini PCB/PCBA üretim limitleriyle uyumlu tut.
- [ ] **DFM-07** — Standart üretim dışında maliyet artışına yol açan tüm seçenekleri, gerekçeleriyle kullanıcıya bildir.
- [ ] **DFM-08** — Komponent seçimini onaylanan tedarik stratejisine ve dizgi yöntemine göre yap. Gerçek MPN, footprint, stok, lifecycle bilgisi ve üreticinin PCBA dizgi kabiliyetini doğrula; teyit edilemeyen bilgileri açıkça belirt.
- [ ] **DFM-09** — Manuel dizgi veya stencil + SMT tercih edilmişse kullanıcı tarafından onaylanan paket boyutu, pad erişimi ve rework gereksinimlerini koru. PCBA tercih edilmişse seçilen dizgi hizmetinin komponent tedarik, paket ve montaj limitlerini doğrula.
- [ ] **DFM-10** — Teknik gereksinimleri sağlayan seçenekler arasında BOM, PCB ve dizgi maliyetinin toplamını değerlendir. Uygun olduğunda standart, yaygın ve önceden doğrulanmış komponentleri, footprint'leri ve referans devreleri yeniden kullan. Her standart pasif için kapsamlı fiyat araştırması yapma; önemli maliyet veya tedarik riski oluşturan parçaları karşılaştır.
- [ ] **DFM-11** — Kritik veya pahalı komponentlerde teknik olarak uygun, onaylanabilir alternatifleri değerlendir. Stok ve fiyat bilgilerini doğrulayabildiğin tarih itibarıyla kaydet; doğrulanmamış fiyat veya stok uydurma.
- [ ] **DFM-12** — Yeni komponent araştırmadan önce `Hardware-Library/catalog/` kayıtlarını kontrol et. Doğrulanmış symbol, footprint, CAD model ve devre bloklarını, exact MPN ve geçerlilik koşulları uyuyorsa yeniden kullan. Yeni veya değiştirilen varlıkları bağımsız review tamamlanmadan VERIFIED olarak kaydetme.
- [ ] **DFM-13** — Onaylı hazır modülleri ve konnektör çiftlerini exact parça/revizyon ile kütüphaneye kaydet. Modülün pin/footprint/3D modeli ile uygun karşı konnektör ve montaj yönteminin eşleşmesini doğrula; her projede aynı varlıkları yeniden modelleme.

---

## 04 · Schematic, Component Placement & Routing

- [ ] **SCH-01** — Şematiği fonksiyonel bloklara ayır; tutarlı net isimleri, referanslar ve gerekli açıklamaları kullan. Karmaşık devrelerde hiyerarşik sayfaları tercih et; küçük kartlarda gereksiz sayfalar oluşturma.
- [ ] **SCH-02** — Komponent özelliklerini, pinout'ları ve footprint ölçülerini ilgili MPN'nin üretici datasheet'i ile doğrula. Doğrulanmış kaynak, revizyon ve ilgili sayfa bilgilerini kısa biçimde kaydet; mevcut güvenilir bilgiyi gereksiz yere yeniden araştırma.

- [ ] **LAY-01** — Decoupling kapasitörlerini ilgili besleme pinlerine mümkün olduğunca yakın yerleştir; akım dönüş yolunu kısa tut.
- [ ] **LAY-02** — Güç hatları ve güç via'larını akım taşıma, gerilim düşümü ve sıcaklık artışı gereksinimlerine göre boyutlandır.
- [ ] **LAY-03** — Hassas analog devreleri, gürültülü dijital devreleri ve switching power supply bölgelerini uygun şekilde yerleştir.
- [ ] **LAY-04** — Sinyal hatlarının referans düzlemlerini ve dönüş yollarını koru.
- [ ] **LAY-05** — Routing sırasında gereksiz 90° köşelerden kaçın; mümkün olduğunda 45° geçişleri tercih et. RF hatlarında mitered veya kavisli dönüş kullan (bölüm 05, RF-06).
- [ ] **LAY-06** — Besleme hatları ve kritik sinyaller için erişilebilir test point'ler oluştur.
- [ ] **LAY-07** — Komponent referanslarını, Pin 1 ve polarite işaretlerini okunaklı ve pad'lerle çakışmayacak şekilde silkscreen üzerinde göster.

---

## 05 · Differential Pairs, RF & High-Speed (SI/PI)

> **Zorunlu ön koşul:** Diferansiyel hatlar bulunuyorsa empedans veya routing geometrisini tahmin ederek belirleme.

### Routing öncesinde doğrulanacak bilgiler

| Bilgi | Kaynak |
| :--- | :--- |
| Haberleşme arayüzü ve hedef diferansiyel empedans | Kullanıcı / interface specification / datasheet |
| İzin verilen impedance tolerance | Kullanıcı / interface specification |
| Pair içi length matching ve diğer uzunluk limitleri | Kullanıcı / interface specification / datasheet |
| PCB üreticisi ve standart stack-up | Kullanıcı / JLCPCB / PCBWay |
| Katman yapısı, dielektrik ve bakır kalınlıkları | PCB üreticisi |
| Trace width, pair spacing ve gerekli copper clearance | Üreticinin stack-up ve empedans hesabı |

- [ ] **DIF-01** — Tasarımdaki tüm diferansiyel sinyal çiftlerini tespit et.
- [ ] **DIF-02** — Eksik empedans, tolerans ve uzunluk gereksinimlerini kullanıcıdan veya ilgili teknik dokümandan al.
- [ ] **DIF-03** — JLCPCB ve/veya PCBWay'den kullanılacak üretim koşullarına ait stack-up ve empedans bilgilerini edin.
- [ ] **DIF-04** — Hesaplanan trace width ve differential pair spacing değerlerini PCB design rules içerisine tanımla.
- [ ] **DIF-05** — Her çift için sürekli referans düzlemi, gerekli length matching ve pair spacing kurallarını uygula.
- [ ] **DIF-06** — Kontrollü empedans gerektiren hatları, doğrulanmış üretici stack-up'ı olmadan finalize etme.
- [ ] **DIF-07** — Üretici değişirse empedans geometrisini yeni üreticinin stack-up bilgileriyle yeniden doğrula.
- [ ] **DIF-08** — Özel üretim gerektirmeyen düşük hızlı diferansiyel hatlar ile kontrollü empedans gerektiren hatları ayırt et; gereksiz üretim maliyeti oluşturma.

### RF / High-Speed — koşullu tasarım profili

> Yalnızca projede ilgili gereksinimler varsa bu profili etkinleştir. Genel PCB limitlerini kontrollü empedans veya SI/PI gereksiniminin yerine kullanma.

- [ ] **HS-01** — İlgili sinyal gruplarını ve cihaz/interface dokümanlarından gelen empedans, tolerans, timing, skew/length, terminasyon, kayıp ve gürültü gereksinimlerini `Project-README.md` içinde kısa referanslarla tanımla.
- [ ] **HS-02** — Uygun üretici stack-up'ı, malzeme, katman yapısı ve toleransları doğrula. RF/high-speed için özel malzeme veya üretim ancak gerçek teknik gereksinim varsa seçilsin.
- [ ] **HS-03** — Onaylanan hat şartlarını EDA net class ve routing constraint'lerine aktar. Reference plane/return path, hat geçişleri, konnektör ve via kaynaklı süreksizlikler için ilgili kuralları incele.
- [ ] **HS-04** — Proje isterlerine göre signal integrity / power integrity, PDN, termal ve EM/RF analiz ihtiyacını belirle. Alan çözücü, simülasyon veya laboratuvar ölçümü yalnızca gerekli ise uygulanır; araç erişimi ve kabul kriterini kaydet.
- [ ] **HS-05** — Reviewer, ilgili hat sınıflarının onaylı gereksinimler, üretici stack-up'ı ve gerçek analiz/ölçüm kanıtlarıyla uyumunu doğrular. DRC'nin temiz olması tek başına SI/PI veya RF performansının doğrulanması değildir.

### RF — koşullu, banda göre kademeli

> **Yalnızca kartta RF devresi varsa uygula.** RF yoksa bu kısmın tamamı N/A'dır ve kullanıcıya RF sorusu sorulmaz. RF varsa önce bandı öğren, kademeyi seç ve `Project-README.md` içine kaydet.

| Kademe | Frekans | Tipik örnek | Varsayılan yaklaşım |
| :--- | :--- | :--- | :--- |
| **RF-A** | < 1 GHz | 433/868/915 MHz, LoRa, kumanda | Standart FR-4 genellikle yeterli. 50 Ω microstrip veya GCPW. Via fence önerilir, zorunlu değil. |
| **RF-B** | 1–6 GHz | GNSS, 2.4/5 GHz WiFi, BLE | FR-4 kısa hatlarda kayıp hesabıyla kabul edilebilir. GCPW tercih edilir. Via fence aralığı ≤ λg/10, tercihen ≤ λg/20. |
| **RF-C** | > 6 GHz | Radar, X-band ve üzeri, mmWave | RF laminat veya hibrit stack-up (üretici onaylı). GCPW zorunlu, via fence ≤ λg/20. Konnektör launch'u üretici referansına göre. EM simülasyonu veya ölçüm kanıtı gerekir. |

λg (dielektrik içindeki dalga boyu) ≈ c / (f · √εeff). Örnek: 2.4 GHz, FR-4 microstrip (εeff ≈ 3.3) → λg ≈ 69 mm → λg/20 ≈ 3.4 mm. Değerleri üreticinin gerçek stack-up'ı ve hesap aracıyla doğrula.

- [ ] **RF-01** — RF var mı? Yoksa N/A. Varsa band, TX/RX işlevi, çıkış gücü veya hassasiyet, anten ya da konnektör tipi ve düzenleyici uyumluluk isterlerini al.
- [ ] **RF-02** — Hobi ve basit projelerde önce **sertifikalı hazır RF modülünü** (anten dahil veya U.FL/SMA çıkışlı) öner; kendi RF devresini kullanıcı isterse veya gereksinim zorunlu kılarsa tasarla. Modül kullanılıyorsa modül üreticisinin layout kılavuzu (anten keepout, GND, besleme) bağlayıcıdır.
- [ ] **RF-03** — 50 Ω (veya onaylı başka empedans) hat geometrisini üreticinin stack-up'ı ve hesap aracıyla belirle. Tercihen GCPW kullan. Hattın altındaki referans düzlemi kesintisiz olsun; hattın altından veya yanından başka sinyal geçirme.
- [ ] **RF-04** — RF hattı boyunca iki yanda GND via fence uygula; aralığı kademeye göre seç. Polygon ile hat arasındaki boşluk hesaplanan GCPW değerine eşit olsun.
- [ ] **RF-05** — RF komponentlerin GND pad'lerini Direct Connect bağla ve pad'e en yakın noktaya birden fazla GND via koy. PA/LNA exposed pad'leri için datasheet'teki termal via düzenini uygula.
- [ ] **RF-06** — Dönüşlerde mitered veya kavisli geçiş kullan. Pad ile hat genişliği arasında büyük fark varsa taper uygula. Yüksek frekansta küçük paket (0402 veya daha küçük, dizgi yöntemi izin veriyorsa) tercih et.
- [ ] **RF-07** — RF konnektör (SMA, U.FL, edge-launch) için üreticinin önerdiği footprint ve launch geometrisini kullan. Antenin keepout alanında tüm katmanlarda bakır bırakma. Anten veya konnektör önüne ayarlanabilir eşleştirme ağı (pi) yeri bırak.
- [ ] **RF-08** — TX/RX, LO/clock, DC-DC ve dijital gürültü kaynaklarını RF yolundan ayır. Gerekiyorsa shield can footprint'i ve çevresine via fence ekle. RF hatlarını kısa tut.
- [ ] **RF-09** — Doğrulama kanıtını kaydet: empedans hesabı, varsa simülasyon (ör. `.s2p`) ve varsa ölçüm (VNA, spektrum analizörü). Ölçüm veya simülasyon yapılmadıysa "doğrulanmadı" olarak işaretle.

---

## 06 · Design Review & Verification

- [ ] **VER-01** — Tüm pin bağlantılarını, footprint'leri ve design rule'ları datasheet'lerle doğrula.
- [ ] **VER-02** — Schematic ERC ve PCB DRC kontrollerini tamamla. Açıklanmamış hata veya onaysız kural ihlali bırakma.
- [ ] **VER-03** — GND polygon'larının ve via bağlantılarının doğruluğunu kontrol et.
- [ ] **VER-04** — Gerber ve drill dosyalarında katmanları, kart sınırlarını, solder mask açıklıklarını ve delikleri doğrula.
- [ ] **VER-05** — PCB üretimi ve PCBA dizgi için gerekli BOM ve Pick & Place (CPL) dosyalarını kontrol et.
- [ ] **VER-06** — Üreticinin güncel DFM limitlerine ve seçilen sipariş konfigürasyonuna uygunluğu doğrula.
- [ ] **VER-07** — Proje için gerekli güç bütçesi, tolerans, worst-case, derating ve termal hesapları yap. Uygulanabilir hesaplarda hesap makinesi veya script kullan; yalnızca anlamlı sonuç veren hesapları gerçekleştir.
- [ ] **VER-08** — SPICE veya diğer simülasyonları, hesapla ya da datasheet ile yeterince doğrulanamayan devrelerde kullan. Gereksiz simülasyon yapma; çalıştırılmamış analizin sonucunu doğrulanmış olarak gösterme.
- [ ] **VER-09** — Üretim sonrası ilk çalıştırma ve temel fonksiyonel testler için proje karmaşıklığına uygun kısa bir bring-up/test planı oluştur. Ayrıntılı ayrı raporları yalnızca kullanıcı isterse veya gereksinimler zorunlu kılarsa hazırla.
- [ ] **VER-10** — Multi-PCB projelerde her kartın ERC/DRC ve bağımsız review sonuçlarına ek olarak ortak arayüz/pinout, eşleşen konnektörler, güç bağlantıları ve mekanik uyumu kontrol et. Review kaydında kart ID'sini belirt. Etkilenmeyen kartların mevcut doğrulama kanıtlarını koru.
- [ ] **VER-11** — Kullanıcı komple CAD assembly istediyse onaylı kart, modül ve mekanik referans modellerinin uyumunu kontrol et. Gerçek CAD/çakışma kontrolü yapılmadıysa bunu açıkça belirt; eksik veya yaklaşık modelleri listelerken doğrulanmış gibi gösterme. Nihai CAD/STEP teslimini onaylanan kapsam ve revizyona göre hazırla.
- [ ] **VER-12** — Programlama/debug gerekiyorsa seçilen yöntem, hedef komponent, programmer/debugger ve onaylı konnektör/pinout ile şematik ve layout uyumunu kontrol et. Gerçek programlama/flash/debug testi yalnızca donanım ve araç mevcutsa tamamlanmış sayılır; aksi halde ilgili doğrulama bekleyen test olarak kaydedilir.

---

## 07 · AI çalışma kuralları

- [ ] **AI-01** — Tasarım öncesinde bölüm 00'daki Project Intake (G0), PCB tasarımı öncesinde bölüm 00B'deki PCB Intake (G0.5) sürecini tamamla. Eksik veya çelişkili gereksinimleri kullanıcıya sor; ilgili aşamanın girdileri onaylanmadan o aşamaya başlama.
- [ ] **AI-02** — Komponent, net, footprint, stack-up veya design rule değişikliklerini kullanıcı onayı olmadan yapma.
- [ ] **AI-03** — Kullanıcıya maliyet artışı yaratabilecek tasarım tercihlerini gerekçeleriyle bildir.
- [ ] **AI-04** — Tamamlanan tasarım için uygulanan kuralları, varsa istisnaları ve doğrulama sonuçlarını raporla.
- [ ] **AI-05** — Bir kontrol maddesini yalnızca gerçekten doğrulandığında tamamlanmış olarak işaretle. Doğrulanamayan maddeleri açık bırak.
- [ ] **AI-06** — Tasarım ve doğrulama kapsamını proje riskiyle orantılı tut. İlgisiz maddeleri gerekçesiyle N/A olarak işaretle; kullanıcı tarafından istenmeyen dokümanları, alternatif tasarımları ve analizleri gereksiz yere üretme.
- [ ] **AI-07** — Aşama ve revizyon değişikliklerinde mevcut Git/EDA kayıtlarını kullanarak kısa checkpoint oluştur. Kullanıcı değişikliklerini koru; yarıda kalan işleri doğrulanmış son durumdan devam ettir.
- [ ] **AI-08** — EDA entegrasyon yöntemi bağımsızdır. Mevcut ve yetkili MCP/CLI/API araçlarını önce düşük riskli okuma/bağlantı kontrolüyle doğrula. Olmayan araç fonksiyonunu varmış gibi kullanma; native otomasyon veya kullanıcı destekli alternatif mümkünse öner. Eklentileri kurmak, yetki genişletmek veya harici veri göndermek ayrı kullanıcı onayı gerektirir.

---

## 08 · Havacılık / Aviyonik — koşullu profil

> **Yalnızca INT-47'de Havacılık profili seçildiyse uygula.** Hobi ve Endüstriyel projelerde bu bölüm N/A'dır. Bu şablon sertifikasyon sağlamaz; DO-254 uyumu ve uçuşa elverişlilik organizasyonel süreç, yetkili otorite ve bağımsız onay gerektirir.

- [ ] **AVI-01** — Uygulanacak standartları ve seviyeleri kullanıcıdan veya müşteri şartnamesinden al: DO-254 DAL, DO-160 test kategorileri, MIL-STD-461 / 704 / 810, şirket standartları. Kategori veya seviye uydurma; bilinmeyeni Belirsiz olarak kaydet.
- [ ] **AVI-02** — PCB ve montaj kalite sınıfını kaydet: tasarım için IPC-2221/2222, bare board için IPC-6012 Class 3 (veya 3/A), montaj için IPC-A-610 Class 3. Uygun sertifikalı (ör. AS9100) üretici gerekip gerekmediğini sor. Standart düşük maliyetli hatların genelde Class 2 olduğunu kullanıcıya bildir.
- [ ] **AVI-03** — Derating politikasını kullanıcıdan al (ör. şirket politikası, ECSS-Q-ST-30-11, NASA EEE-INST-002). Her komponent için gerilim, akım, güç ve sıcaklık derating'ini politikaya göre kontrol et ve kısa tabloyla kaydet.
- [ ] **AVI-04** — Komponent seçiminde onaylı sıcaklık aralığını (ör. −55…+125 °C veya istenen değer), lifecycle/obsolescence durumunu, çok kaynaklılığı ve yetkili distribütör tedarikini doğrula. MSL ve saf kalay kaplama (kalay bıyığı) riskini lehim/kaplama politikasıyla birlikte değerlendir.
- [ ] **AVI-05** — Uçak güç girişi varsa (ör. 28 VDC) ilgili standarttaki normal/anormal gerilim aralıkları, geçici rejimler, kesinti/hold-up, inrush ve ters polarite isterlerini al ve koruma devresini buna göre tasarla. Yıldırım kaynaklı geçici gerilim koruması konnektör girişinde olmalıdır.
- [ ] **AVI-06** — EMC isterlerine göre filtrelemeyi konnektör girişinde uygula; şase bağlantısını ve kablo shield sonlandırmasını (tercihen 360°) onaylı topraklama mimarisine göre tasarla.
- [ ] **AVI-07** — Titreşim, şok, nem ve tuz isterlerine göre ağır komponent sabitleme (staking/underfill), conformal coating (ör. IPC-CC-830) ve konnektör kilitleme gereksinimlerini kaydet.
- [ ] **AVI-08** — İzlenebilirlik: her ister için tasarım referansı ve doğrulama yöntemi `Project-README.md` ister tablosunda bulunmalıdır. Üretim çıktıları için `python scripts/projectctl.py manifest` ile checksum manifest oluştur; BOM ve çıktıların aynı revizyondan geldiğini manifest ile doğrula.
- [ ] **AVI-09** — Kullanıcı veya standart gerektiriyorsa FMEA, güvenilirlik tahmini (ör. MIL-HDBK-217F, FIDES), worst-case ve termal analiz yap. Yapılmamış analizi tamamlanmış gösterme.
- [ ] **AVI-10** — Havacılık profilinde Reviewer bu bölümün maddelerini ayrıca kontrol eder; doğrulanamayan maddeler PASS sayılmaz.

---

## Üretici referansları

| Üretici | PCB üretim kabiliyetleri | Empedans ve stack-up |
| :--- | :--- | :--- |
| **JLCPCB** | [PCB Capabilities](https://jlcpcb.com/capabilities/Capabilities?type=1) | [Impedance Calculator](https://jlcpcb.com/pcb-impedance-calculator/) · [Stack-up](https://jlcpcb.com/impedance) |
| **PCBWay** | [PCB Capabilities](https://www.pcbway.com/capabilities.html) | [Impedance Calculator](https://www.pcbway.com/pcb_prototype/impedance_calculator.html) |

> **Not:** Üreticilerin üretim seçenekleri ve fiyatlandırmaları değişebilir. Sipariş öncesinde seçilen üreticinin güncel kabiliyetleri ve sipariş ekranı esas alınmalıdır. Bu dokümandaki varsayılanlar belirli bir kartın elektriksel, mekanik veya güvenlik gereksinimlerinin yerine geçmez.
