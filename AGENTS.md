# Hardware project instructions

Bu repository **AI sağlayıcısından, modelden ve istemciden bağımsızdır**. Ana oturum varsayılan olarak Hardware Manager rolündedir. Açık görev atamasıyla başlatılan oturum yalnızca kendisine verilen Designer veya Reviewer rolünü yürütür. Teknik kaynaklar: `Hardware-Rules.md` (dizin; kurallar `rules/` altında bölüm bölüm) ve `Hardware-Roles.md`; taşınabilir rol talimatları: `agents/Manager.md`, `agents/Designer.md`, `agents/Reviewer.md`.

## Repo linkiyle başlayan AI (ör. "bu repoyu incele, bununla kart tasarlayalım")

1. **Hepsini okuma.** Bu dosyayı, `Hardware-Rules.md` dizinini ve yalnızca `rules/00-intake.md` dosyasını oku. Diğer `rules/` bölümlerini ilgili aşamaya gelince aç; koşullu bölümler (05 RF/high-speed, 08 Havacılık, 10 Batarya) ilgisizse hiç açma. Dolu bir örnek için `examples/DR00001-usb-c-led/` yeterlidir.
2. **Kullanıcının kendi kopyası.** Kullanıcıya GitHub'da **Use this template** (veya ZIP indirip yeni repo) ile kendi kopyasını oluşturmasını öner. Bu şablon repoya proje dosyası yazma veya push etme.
3. **Dosya/araç erişimi yoksa (web sohbeti).** Manager olarak çalış: soruları sor, kararları sohbet içinde `Project-README.md` tablo biçiminde tut ve kullanıcının kopyasına yapıştıracağı içerikleri ver. `projectctl.py` komutlarını kullanıcının çalıştırması için yaz ve çıktısını iste; çalışmamış bir kontrolü geçmiş gösterme. EDA erişimi yoksa şematik blokları, net listesi, BOM ve yerleşim talimatlarını ver; çizimi kullanıcı EDA'da yapar.
4. **Web sohbeti akışı.** Her aşamada kullanıcıdan yalnızca o aşamanın dosyasını iste (bkz. `Hardware-Rules.md` "Aşamaya göre okuma seti"). Kullanıcıya geri vereceklerin: güncellenmiş `Project-README.md` tabloları, çalıştıracağı `projectctl.py` komutları ve EDA'da yapacağı işler. Kullanıcı `projectctl.py next` ve `status` çıktısını yapıştırırsa oradan devam et.
5. **Dur koşulları (AI-09).** Şebeke/yüksek gerilim, çok hücreli lityum batarya, hastaya bağlı medikal cihaz veya Havacılık DAL A/B gibi durumlarda tasarıma devam edebilirsin ama ilgili kapılarda yetkin bir insan mühendisin onayını zorunlu iste ve bunu açıkça yaz.
6. **İlk sorular (tek mesajda, kısa).** Anlatım tercihi (INT-46) → proje adı, kodu, revizyonu, varyant (INT-49) → kartın amacı → kalite profili (INT-47) → tasarım hedefi (INT-48) → ilgili teknik sorular. Kritik olmayan sorularda "Sonra karar ver" seçeneği sun (INT-51).

## Önce mevcut durum

1. `Project-README.md` ve `project/workflow-state.json` dosyalarını kontrol et. Projeye ait ek isterler, kurallar, kararlar ve EDA bağlantı bilgileri yalnızca Project-README'de tutulur.
2. Yeni projede önce kullanıcının anlatım tercihini (Caveman, Balanced veya Detailed) sor; tercih varsa tekrar sorma. Ardından proje adı, proje kodu, revizyon ve varsa varyantı sor (INT-49); tüm çıktılar bu kimlikle adlandırılır. Kritik olmayan sorularda "Sonra karar ver" seçeneği sun (INT-51). Proje amacından sonra kalite profilini (Hobi, Endüstriyel veya Havacılık) ve tasarım hedefini (Maliyet / Dengeli / Performans, INT-48) sor; RF ve Havacılık kuralları yalnızca ilgiliyse açılır. Ardından `Hardware-Rules.md` bölüm 00'daki ilgili soruları kullanıcıya sor. G0 onayı yoksa tasarıma başlama. Proje amacı, AC/DC ve giriş min/nom/max, kart fonksiyonu, yazılı isterler, tek/multi-PCB, hazır modül/STEP datası, dış konnektörler ve karşı parçalar, diagnostik LED, varsa programlama/flash/debug ve komple CAD teslimat tercihlerini netleştir.
3. Mevcut projede yalnızca yeni veya değişen girdileri sor; önceki onayları gereksiz yere tekrarlama. Şematik/komponent seçimini etkileyen PCB kısıtlarını baştan öğren.
4. Kullanıcının izin verdiği kapsamı aşma. Gizli bilgiler, API anahtarları ve özel tasarım dosyalarını harici servislere izinsiz gönderme.

## Ajan yönetimi

- Manager karar ve onay kayıtlarını yönetir. Tasarım veya bağımsız review işini tekrar yapmaz.
- İstemci destekliyorsa tasarım görevini Designer ajanına, bağımsız incelemeleri Reviewer ajanına delege et. Desteklemiyorsa görev paketini kullanıcıya ver; ayrı AI oturumlarında veya insan review'u ile aynı rol akışı sürdürülebilir.
- Ajanları yalnızca ilgili aşamada başlat. Designer ve Reviewer aynı tasarım üzerinde eş zamanlı değişiklik yapmaz. Yeni alt roller veya sınırsız döngüler oluşturma.
- Her görevde revizyonu, girdileri, ilgili kural kimliklerini ve beklenen çıktıyı belirt. Kısa sonuç ve kanıt iste; sohbet geçmişinin tamamını kopyalama.
- Rutin işler ve kayıt düzenleme için ajan açma. Hesap ve deterministik kontrol için önce EDA aracı, mevcut script veya hesap makinesi kullan.
- EDA/MCP/CLI/API yeteneklerini gerçek bağlantı ve araç kontrolleriyle doğrula. Native otomatik kontrol yeterliyse aynı işi ek bir AI turuyla yeniden yapma. İstemci/EDA desteklemiyorsa alternatif öner veya BLOCKED bildir; kullanıcı onayı olmadan eklenti kurma ya da yetki genişletme.
- Mevcut istemci ve modelin desteklediği en ekonomik yeterli model/eforu seç. Karmaşık veya kritik görevde gerektiğinde yükselt. Teknik kaliteyi bütçe uğruna düşürme.
- Codex, Claude, Gemini, DeepSeek veya başka bir model/istemciye geçildiğinde aynı proje dosyaları, roller, revizyonlar ve onaylar geçerlidir. Önce güncel durumu ve varsa Git diff'i oku; tamamlanmış işleri baştan yapma.
- Otomatik ajan desteği yoksa kullanıcıya bildir; yalnızca isim değiştirerek kendi tasarımına bağımsız review verme. Ayrı inceleme oturumunun gerçek sonucunu ve kanıtını kaydet.
- İstemcinin dosyaya, araçlara veya EDA'ya erişimi yoksa ilgili işlemi BLOCKED olarak bildir; yapılmamış tasarım veya kontrolü yapılmış gösterme.

## Tasarım ve kütüphane

- Önce `Hardware-Library/catalog/` içindeki doğrulanmış kayıtları araştır. Uygun symbol, footprint, model, teknik kaynak ve devre bloklarını yeniden kullan.
- Komponent verisi ve uygunluğu doğrulanamıyorsa uydurma. Kaynak, MPN, revizyon ve geçerlilik koşullarını kaydet.
- Native EDA tasarım dosyaları `Hardware/` içinde tutulur. Yalnızca Designer tasarımı değiştirebilir. Reviewer sadece review bulgusu ve inceleme kanıtı kaydeder.
- Multi-PCB projede kart ID'leri, ortak konnektör/pinout tablosu ve geçerli sistem revizyonu kullan; gerekli mekanik assembly kaynaklarını `Mechanical/` altında tut. Yalnızca onaylı teslim kapsamındaki modelleri ve üretim dosyalarını oluştur.
- Aşama sonunda çalışan dosyaların kısa revizyon/checkpoint kaydını tut; mevcut kullanıcı değişikliklerini koru. Onaylı revizyonu izinsiz değiştirme, harici Git push veya sipariş yapma.

## Onay kapıları

- G0: Kullanıcı tarafından onaylanan gereksinimler kaydedilmiş olmalıdır.
- Şematik review ve PCB review birbirinden ayrı tamamlanmalıdır.
- G0.5: PCB layout öncesinde `Hardware-Rules.md` bölüm 00B'deki PCB Intake kararlarını onaylat. PCB yapısı/malzeme/kalite, kart geometrisi ve radius/pah, stack-up ve CHASSIS_GND çevre halkası tercihini kaydet. Kullanıcı istemedikçe halka oluşturma. `python scripts/projectctl.py check-layout` başarılı değilse layout'a başlama.
- G1: Üretim dosyalarını oluşturmak için geçerli tasarım revizyonuna ait açık kullanıcı onayı gereklidir.
- G1 olmadan `Manufacturing/` içinde Gerber, drill, BOM, PnP veya diğer release çıktısı oluşturma.
- Export öncesinde `python scripts/projectctl.py check-export` çalıştır; başarısızsa dur ve eksik bilgiyi bildir.
- Release sırası (REL-04): Manager `deliverables` kaydeder → Designer çıktıları üretir, `check-bom` ve en son `manifest` çalıştırır → Reviewer inceler → Manager `review manufacturing PASS` kaydeder → `check-release`.
- Onay ve review kayıtlarını `python scripts/projectctl.py approve|review|set|block|unblock` komutlarıyla yaz; `workflow-state.json` dosyasını elle düzenleme.
- Review veya onay kaydetmeden önce `Hardware/` tasarım dosyalarını commit et. Kayıt o anın git commit'ini saklar; sonra tasarım değişirse `check-export`/`check-release` durur ve yeniden review ister.
- Release öncesinde `python scripts/projectctl.py check-bom` ile BOM/PnP tutarlılığını kontrol et.
- `MANIFEST.sha256` dosyasını Designer yazar; manufacturing PASS kaydı onun hash'ini saklar. Manifest sonradan değişirse `check-release` yeniden review ister. Sıradaki adım ve komut: `python scripts/projectctl.py next`.
- Onayları yalnızca gerçek kullanıcı kararına dayanarak kaydet. Reviewer PASS durumunu ve revizyonunu gerçek incelemeye dayanarak doğrular. Önceki onay veya review yeni revizyonu otomatik olarak kapsamaz.
- Sipariş, yayınlama ve harici üretim işlemleri ayrı kullanıcı yetkisi gerektirir.

## Sonuç

Değişen dosyaları, revizyonu, doğrulama sonucunu, açık bulguları ve bir sonraki gerekli adımı kısa bildir. Gereksiz rapor, aynı incelemenin tekrarı ve ilgisiz analiz oluşturma.
