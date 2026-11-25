<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
## 04 · Schematic, Component Placement & Routing

- [ ] **SCH-01** — Şematiği fonksiyonel bloklara ayır; tutarlı net isimleri, referanslar ve gerekli açıklamaları kullan. Karmaşık devrelerde hiyerarşik sayfaları tercih et; küçük kartlarda gereksiz sayfalar oluşturma.
- [ ] **SCH-02** — Komponent özelliklerini, pinout'ları ve footprint ölçülerini ilgili MPN'nin üretici datasheet'i ile doğrula. Doğrulanmış kaynak, revizyon ve ilgili sayfa bilgilerini kısa biçimde kaydet; mevcut güvenilir bilgiyi gereksiz yere yeniden araştırma.
- [ ] **SCH-03** — **PI / güç ağacı:** Her ray için kaynak, tüketiciler, toplam akım, regülatör kapasitesi ve payı, ripple/gürültü sınırı ve açılma sırasını içeren kısa bir güç ağacı çıkar. Analog, PLL, ADC referansı ve RF raylarına datasheet'in önerdiği ferrit/LC filtreyi veya ayrı LDO'yu ekle.
- [ ] **SCH-04** — **Decoupling:** Her besleme pinine datasheet'in önerdiği yerel kapasitörü (yoksa tipik 100 nF), her raya bulk kapasitör koy. Şematikte kapasitörü bağlı olduğu IC pininin yanına çiz ve hangi pine ait olduğunu belli et; layout bu eşleşmeyi izler (LAY-25).
- [ ] **SCH-05** — **SI hazırlığı:** Clock ve hızlı kenarlı sinyallerde sürücüye yakın seri terminasyon yeri bırak (tipik 22–33 Ω veya 0 Ω). I²C pull-up değerini hız ve bus kapasitansına göre hesapla. Hızlı arayüzlerde düşük kapasitanslı ESD koruması seç. Kullanılmayan ve strapping/reset/boot pinlerini datasheet'e göre bağla; yüzen giriş bırakma.
- [ ] **SCH-06** — **Kısıtları şematikte işaretle:** Diferansiyel çiftleri `_P/_N` (veya EDA'nın beklediği) adlarla, kritik netleri net class veya kural notuyla (Power, Diff/HS, RF, HV) işaretle; layout kurallarını bu işaretlerden üret.
- [ ] **SCH-07** — **Opsiyon yeri (0 Ω / DNP):** Değeri veya gerekliliği kesin olmayan noktalara 0 Ω köprü veya takılmayan (DNP / N/A) parça yeri koy: ör. seri terminasyon, pull-up/pull-down, filtre, empedans eşleştirme (pi/L), konfigürasyon seçimi, ölçüm noktası. DNP parçaları şematikte ve BOM'da açıkça işaretle. Bu yerleri yalnız gerçek belirsizlikte kullan; gereksiz parça, alan ve maliyet ekleme.

### Genel

- [ ] **LAY-01** — Decoupling kapasitörlerini ilgili besleme pinlerine mümkün olduğunca yakın yerleştir; akım dönüş yolunu kısa tut.
- [ ] **LAY-02** — Güç hatları ve güç via'larını akım taşıma, gerilim düşümü ve sıcaklık artışı gereksinimlerine göre boyutlandır.
- [ ] **LAY-03** — Hassas analog devreleri, gürültülü dijital devreleri ve switching power supply bölgelerini uygun şekilde yerleştir.
- [ ] **LAY-04** — Sinyal hatlarının referans düzlemlerini ve dönüş yollarını koru.
- [ ] **LAY-05** — Routing sırasında gereksiz 90° köşelerden kaçın; mümkün olduğunda 45° geçişleri tercih et. RF hatlarında mitered veya kavisli dönüş kullan (bölüm 05, RF-06).
- [ ] **LAY-06** — Besleme hatları ve kritik sinyaller için erişilebilir test point'ler oluştur.
- [ ] **LAY-07** — Komponent referanslarını, Pin 1 ve polarite işaretlerini okunaklı ve pad'lerle çakışmayacak şekilde silkscreen üzerinde göster.

### Yerleşim (placement)

- [ ] **LAY-08** — **Referans layout:** Komponentin datasheet'inde, application note'unda veya evaluation board'unda önerilen yerleşim/routing varsa onu esas al. Kartın alan, hacim, katman veya mekanik kısıtları izin veriyorsa aynısını, vermiyorsa en yakın eşdeğerini uygula; farkları ve gerekçesini kaydet. Kaynağın adını ve revizyonunu `Project-README.md` içinde belirt.
- [ ] **LAY-09** — Yerleşim sırası: önce mekanik olarak sabit parçalar (konnektör, montaj deliği, buton, LED, ekran, anten), sonra güç girişi ve koruma, sonra ana IC'ler, en son pasifler. Giriş korumasını (sigorta, TVS, ters polarite) konnektöre en yakın yere koy; korumasız hat kart içine girmesin.
- [ ] **LAY-10** — Switching regülatörde yüksek di/dt döngüsünü (giriş kapasitörü – anahtar – diyot/low-side FET) en küçük alanda tut ve datasheet layout örneğini uygula. SW düğümünü küçük tut; altından veya yanından hassas hat geçirme. Feedback hattını çıkış kapasitöründen/yükten al, SW düğümü ve indüktörden uzak götür.
- [ ] **LAY-11** — Kristal/osilatörü ilgili IC pinine yakın, yük kapasitörlerini bitişik yerleştir. Altından ve yakınından başka sinyal geçirme; GND koruması ve keepout için datasheet önerisini uygula.
- [ ] **LAY-12** — Isı üreten parçaları (regülatör, güç FET, LED sürücü) dağıt; termal pad altına datasheet'e uygun termal via ve bakır alan ver. Isıya hassas parçaları (kristal, referans, sensör, elektrolitik) sıcak bölgeden uzak tut.
- [ ] **LAY-13** — Benzer parçaları aynı yönde ve hizalı yerleştir; polarize parçalarda tutarlı yön kullan. Tek taraflı dizgi seçildiyse tüm SMD parçalar aynı yüzde olsun. Konnektör, test point ve buton erişimini mekanik modelle; komponent–kart kenarı mesafesini panel/V-cut ve üretici limitine göre kontrol et.

### Routing

- [ ] **LAY-14** — Routing sırası: önce kritik hatlar (RF, diferansiyel çift, clock, switching ve yüksek akım), sonra hassas analog, sonra genel dijital, en son düşük öncelikli hatlar. Kritik hatlarda autorouter kullanma; diğer hatlarda kullanıldıysa sonucu manuel incele.
- [ ] **LAY-15** — Net class tanımla (ör. Power, Signal, Diff/HS, RF, HV); trace width, clearance ve via ölçüsünü net class üzerinden ver. Güç hattı genişliğini akım ve izin verilen sıcaklık artışına göre IPC-2152 veya üretici hesaplayıcısıyla hesapla; iç katmanların daha az akım taşıdığını hesaba kat.
- [ ] **LAY-16** — Katman kullanımı: 2 katmanda alt katmanı mümkün olduğunca kesintisiz GND bırak; alt katmandaki atlamalar kısa olsun. 4 katmanda varsayılan yığın Sinyal / GND / PWR / Sinyal'dir; hızlı sinyalleri GND'ye komşu katmanda yürüt. Komşu sinyal katmanlarında hatlar birbirine dik ilerlesin.
- [ ] **LAY-17** — Hiçbir sinyal, referans düzlemindeki bölünme, slot veya boşluğun üzerinden geçmesin. Hat katman değiştirip referans düzlemi de değişiyorsa sinyal via'sının yanına GND dönüş via'sı (ya da farklı net düzlemler arasında stitching kapasitörü) koy.
- [ ] **LAY-18** — Clock ve hızlı kenarlı sinyalleri kısa tut; diğer hatlardan en az 3W aralık bırak veya GND ile koru; uzun paralel koşmalardan kaçın. Gereksiz stub, ağaç topoloji ve açık uçlu bakır bırakma; seri terminasyon gerekiyorsa sürücüye yakın koy.
- [ ] **LAY-19** — Analog ve hassas hatları (ADC girişi, referans, sensör, ses) gürültü kaynaklarından uzak yürüt. Varsayılan tek, kesintisiz GND'dir; bölünmüş AGND/DGND yalnızca datasheet veya ölçülmüş gerekçeyle ve tek bağlantı noktasıyla uygulanır.
- [ ] **LAY-20** — Güç dağıtımını geniş hat veya polygon ile yap; akıma yetecek sayıda paralel via kullan; darboğaz bırakma. Yüksek akım dönüşünü hassas GND dönüşünden ayır. Akım ölçüm (shunt) hatlarını pad'in içinden ayrı Kelvin bağlantısıyla, birbirine yakın ve paralel çek.
- [ ] **LAY-21** — Yüksek gerilim varsa onaylı clearance/creepage değerlerini (IPC-2221, IEC 62368-1 veya proje standardı) HV net class'ına işle. Gerekiyorsa izolasyon slotu kullan; HV hatlarını kart kenarından ve düşük gerilim bölgesinden uzak tut.
- [ ] **LAY-22** — Küçük pasiflerde iki pad'e simetrik ve pad'den dar hatla gir (tombstone ve köprü riskini azaltır). Dar açılı (acid trap) birleşme bırakma. Teardrop'u Havacılık profilinde ve ince hat–via geçişlerinde kullan. Via-in-pad gerekmedikçe kullanma (DFM-03); zorunluysa dolgulu ve kapaklı (filled & capped) olarak üreticiye bildir.
- [ ] **LAY-23** — **En kısa ve doğrudan yol:** Hattı ratsnest'in gösterdiği en yakın aynı net pad'ine doğrudan bağla; kartı dolaşan, geri dönen veya gereksiz katman değiştiren hat çekme. Dolanma gerekiyorsa önce parçayı döndür/kaydır veya izin verilen pin/gate swap'ı yap; yerleşimi düzeltmek, hattı uzatmaktan önce gelir. GND gibi polygon netlerinde yakın pad'i en yakın via veya polygon ile bağla, uzun ayrı hat çekme. Length matching dışında hat uzunluğu kuş uçuşu mesafenin yaklaşık 1.5 katını geçiyorsa yeniden çiz veya gerekçesini yaz.
- [ ] **LAY-24** — **Free-angle / organik routing:** Varsayılan 45° routing'dir. Gerekli bölgelerde (RF hatları, kavisli/dar alanlar, flex, yoğun BGA çıkışları) free-angle, kavisli (arc) veya organik routing kullanıcıya sorulur ve onaylanırsa uygulanır. EDA aracının bunu desteklediğini, DRC'nin geçtiğini ve üreticinin kabul ettiğini doğrula.

### SI / PI (tüm kartlar)

- [ ] **LAY-25** — **PI:** Decoupling kapasitörünü bağlı olduğu besleme pinine en yakın yere, en küçük değerliyi en yakına koy. Döngü pin → kapasitör → GND via şeklinde olsun; via'yı pad'in hemen yanına koy, kısa ve geniş bağla; mümkünse kapasitörler arasında via paylaşma. Güç polygon/düzlemini GND düzlemine komşu katmanda tut.
- [ ] **LAY-26** — **SI:** Kenar süresi kısa sinyalde hat uzunluğu kritik uzunluğu (FR-4'te yaklaşık `tr[ns] × 2.5 cm`) geçiyorsa hattı iletim hattı say: kontrollü empedans, sürekli referans düzlemi ve terminasyon uygula (bölüm 05). Kenar süresini bilmiyorsan datasheet'ten al; tahmin etme.
- [ ] **LAY-27** — **Empedans eşleştirme:** Eşleştirme gereken hatlarda üç adımı birlikte ele al: (1) şematikte kaynak/yük empedansını ve eşleştirme ağını (terminasyon, pi/L, gerekirse DNP opsiyon, SCH-07) tanımla; (2) hat geometrisini onaylı üretici stack-up'ı ve hesap aracıyla belirle (DIF-03…07, RF-03); (3) via, konnektör, pad ve katman geçişi kaynaklı süreksizlikleri azalt. Hesap ve varsayımları kaydet; stack-up değişirse yeniden hesapla.
- [ ] **LAY-28** — **Length ve delay matching:** Yüksek hızlı hatlarda (ör. USB, Ethernet, HDMI, MIPI, DDR, paralel bus) arayüz spesifikasyonundaki pair içi ve grup içi toleransları uygula. Hatlar farklı katmanlardan geçiyorsa uzunluk yerine gecikmeyi (ps) eşle; datasheet veriyorsa paket pin gecikmesini ve via gecikmesini de hesaba kat. Pair içi uyumsuzluğu oluştuğu yere yakın düzelt. Serpentine yaparken kıvrım aralığını en az 3W tut ve pad/via yakınına koyma.
- [ ] **LAY-29** — **Bitiş kontrolü:** Bağlanmamış net sayısı 0, DRC/ERC temiz veya her istisna gerekçesiyle kayıtlı, polygon'lar yeniden dökülmüş, floating copper yok, silkscreen pad üstünde değil, LAY-23'e göre gereksiz uzun/dolanan hat yok, LAY-25'e göre her decoupling kapasitörü kendi pinine yakın, LAY-28'e göre eşleşme toleransları sağlanmış. Sonucu Reviewer kanıtı olarak kaydet.

### Silkscreen ve işaretleme

- [ ] **LAY-30** — Silkscreen her yüzde çakışmasız olur: silk silk'e, pad'e, açık maskeye, via açıklığına ve kart kenarına değmez. Logo, kart kodu, konnektör etiketi, designator ve imza bu kontrole dahildir; her yüz için DRC ile doğrula. Bottom yazılar doğru (aynalı) yönde olur.
- [ ] **LAY-31** — PCB-17…21 kararlarını uygula: logo, kart kodu, konnektör etiketi, designator ve imza onaylı yüzlerde, onaylı boyut ve konumda. Ertelenmiş ve hâlâ yanıtsız kararlarda INT-51 güvenli varsayılanını kullan.
