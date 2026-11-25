<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
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
