# Project README — Projeye özel bilgiler, isterler ve kurallar

> Yeni projede bu dosya boş bir başlangıç şablonudur. Manager, gerçek kullanıcı cevaplarını, projeye özel isterleri, ek kuralları, alınan kararları ve güncel durumu burada tutar. Bu dosya proje için tek bilgi kaynağıdır; tam sohbet veya uzun teknik dokümanları kopyalama, ilgili dosya/sayfa referansını kaydet. Makine onay kaydı `project/workflow-state.json`, bağımsız review kanıtı `REVIEW_LOG.md` içindedir.

| Alan | Proje bilgisi |
| :--- | :--- |
| Proje adı / amaç | Belirlenecek |
| Kart tipi / yazılı isterler | Belirlenecek |
| Tek PCB / multi-PCB ve kart ID'leri | Belirlenecek |
| Kartlar arası bağlantı yöntemi | Belirlenecek / N/A |
| Hazır modül kullanımı / mevcut STEP-CAD | Belirlenecek |
| Harici fiziksel konnektörler / karşı parçalar | Belirlenecek |
| Diagnostik / status / haberleşme LED'leri | Belirlenecek |
| Programlama/flash/debug (on-board / off-board / N/A) | Belirlenecek |
| Komple STEP/CAD assembly teslimi | Belirlenecek |
| Besleme türü / min–nom–max | Belirlenecek |
| EDA yazılımı | Belirlenecek |
| EDA sürümü / bağlantı yöntemi | Belirlenecek |
| Gereksinim revizyonu | Belirlenecek |
| PCB girdi revizyonu | Belirlenecek |
| Üretici / dizgi | Belirlenecek |
| Hedef adet / maliyet | Belirlenecek |
| Tedarik stratejisi | Belirlenecek |
| Çalışma ortamı | Belirlenecek |
| AI bütçesi / model tercihleri | Kullanıcı tanımlarsa kaydet |
| Kullanıcı anlatım tercihi | Caveman / Balanced / Detailed — belirlenecek |
| Aktif rol / yürütme ortamı | Manager / belirlenecek |

## Onaylı gereksinimler

`Hardware-Rules.md` bölüm 00'daki proje ile ilgili cevapları burada özetle. Besleme, I/O, mekanik, şase/izolasyon, standart, test ve teslimat gereksinimlerini kapsa.

İsterleri Zorunlu / Tercih / Esnek / Belirsiz / N/A olarak ayır. Kart tipine göre gerekli elektriksel değerleri ve yazılı kaynakları kaydet; aynı soruları tekrar sorma.

| İster ID | İster / hedef | Öncelik | Kaynak / onay | Doğrulama / kabul kriteri |
| :--- | :--- | :--- | :--- | :--- |

## Projeye özel ek kurallar

| Kural ID | Uygulanacağı kart / alan | Kullanıcı kuralı veya onaylı istisna | Kaynak / onay |
| :--- | :--- | :--- | :--- |

Genel `Hardware-Rules.md` ve `Hardware-Roles.md` dosyalarını kopyalama. Projeye özgü ilave kuralları burada kaydet. Genel kuralla çelişen bir tercih varsa gerekçeyi ve kullanıcı kararını kaydet; zorunlu standart ve güvenlik gereksinimlerini ihlal eden bir istisnayı kabul edilmiş sayma.

## EDA & Tool Integration

| Bilgi | Doğrulanmış değer |
| :--- | :--- |
| EDA / sürüm | Belirlenecek |
| Bağlantı | MCP / native CLI / API-script / GUI / manuel |
| Adaptör adı, sürümü ve güvenilir kaynak | Belirlenecek / N/A |
| Dosya erişimi ve okuma/yazma yetkisi | Belirlenecek |
| Şematik, PCB, kütüphane düzenleme yetenekleri | Belirlenecek |
| ERC/DRC, export, STEP/CAD yetenekleri | Belirlenecek |
| Bağlantı testi ve bilinen kısıtlar | Belirlenecek |

Sadece gerçekten test edilmiş yetenekleri kullanılabilir olarak kaydet. API anahtarı veya gizli bilgileri bu dosyaya yazma.

## Kartlar ve fiziksel arayüzler

Yalnızca uygulanıyorsa doldur. Tek PCB ve basit arayüzlerde kısa özet yeterlidir.

| Kart ID | Fonksiyon | Native EDA yolu / mekanik referans |
| :--- | :--- | :--- |

| Arayüz ID | Kaynak → hedef | Bağlantı tipi / pinout referansı | Konnektör / karşı konnektör / STEP referansı |
| :--- | :--- | :--- | :--- |

Onaylı hazır modüller ve gerekli 3D modeller için `Hardware-Library/catalog/components.csv` kayıtlarına referans ver. Diagnostik göstergeleri ve anlamlarını kısa gereksinim notu olarak kaydet.

## Programlama ve Debug — yalnızca programlanabilir komponent varsa

| Hedef komponent / kart ID | On-board / off-board / fabrika programlı | Arayüz / programmer-debugger | Konnektör / pinout / besleme / test referansı |
| :--- | :--- | :--- | :--- |

Flash, debug ve saha güncellemesi gereksinimlerini ayrı değerlendir. Standart veya custom konnektör, pads/fikstür, Pin 1, besleme yöntemi ve mekanik erişim tercihlerini onay referansıyla kaydet. Programlama gerektirmeyen proje için N/A.

## Onaylı PCB girdileri — G0.5

| Alan | Karar / onay referansı |
| :--- | :--- |
| Fiziksel PCB yapısı / laminat / teknoloji | Belirlenecek |
| Kalite sınıfı / özel standartlar | Belirlenecek |
| Board outline / ölçüler / radius / pah | Belirlenecek |
| Montaj delikleri / slot / keepout / yükseklik | Belirlenecek |
| Üretici / stack-up / copper weight / kaplama | Belirlenecek |
| CHASSIS_GND çevre halkası (Evet / Hayır) | Belirlenecek — açık onay olmadan oluşturulmaz |
| GND bağlantısı / izolasyon | Bölüm 00'daki onaylı karara referans ver |

Varsa ilgili mekanik dosyalar ve doğrulanmış üretici parametrelerine referans ekle. Değişmeyen girdileri yeniden yazma.

Multi-PCB projede farklı kartların özelliklerini kart ID bazında kaydet. Komple assembly kapsamı ve eşleşen konnektör/mekanik referansları için `Mechanical/` kaynaklarına referans ver.

## Mimari ve tasarım kararları

| ID | Karar / gereksinim | Kaynak veya kullanıcı onayı |
| :--- | :--- | :--- |

## RF / High-Speed / SI-PI — yalnızca uygulanıyorsa

| Hat / arayüz ID | Kaynak ister / standart | Onaylı empedans, zamanlama ve diğer limitler | Stack-up / analiz / kabul kriteri referansı |
| :--- | :--- | :--- | :--- |

İlgili üretici stack-up'ı, malzeme, hat sınıfları, model ve ölçüm gereksinimlerinin kaynağını belirt. Alakasız projelerde bu bölümü N/A olarak bırak.

## Güncel durum ve checkpoint

| Revizyon | Değişiklik / kontrol | Kısa kanıt veya commit |
| :--- | :--- | :--- |

**Son tamamlanan aşama:** Belirlenecek · **Sıradaki görev / bekleyen onay:** Belirlenecek.

Başka AI veya istemciye geçerken mevcut revizyon, yalnızca ilgili dosyalar, açık bulgular ve sıradaki görev üzerinden devam et. Eski sohbeti yeniden analiz etme.

## Doğrulanmış teknik kaynaklar

Ortak komponent/kütüphane kayıtlarına referans ver. Yeni kaynakları MPN, revizyon, ilgili sayfa ve geçerlilik koşuluyla özetle.

## Açık konular

| ID | Açık konu | Sonraki adım |
| :--- | :--- | :--- |
