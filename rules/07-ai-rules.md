<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
## 07 · AI çalışma kuralları

- [ ] **AI-01** — Tasarım öncesinde bölüm 00'daki Project Intake (G0), PCB tasarımı öncesinde bölüm 00B'deki PCB Intake (G0.5) sürecini tamamla. Eksik veya çelişkili gereksinimleri kullanıcıya sor; ilgili aşamanın girdileri onaylanmadan o aşamaya başlama.
- [ ] **AI-02** — Komponent, net, footprint, stack-up veya design rule değişikliklerini kullanıcı onayı olmadan yapma.
- [ ] **AI-03** — Kullanıcıya maliyet artışı yaratabilecek tasarım tercihlerini gerekçeleriyle bildir.
- [ ] **AI-04** — Tamamlanan tasarım için uygulanan kuralları, varsa istisnaları ve doğrulama sonuçlarını raporla.
- [ ] **AI-05** — Bir kontrol maddesini yalnızca gerçekten doğrulandığında tamamlanmış olarak işaretle. Doğrulanamayan maddeleri açık bırak.
- [ ] **AI-06** — Tasarım ve doğrulama kapsamını proje riskiyle orantılı tut. İlgisiz maddeleri gerekçesiyle N/A olarak işaretle; kullanıcı tarafından istenmeyen dokümanları, alternatif tasarımları ve analizleri gereksiz yere üretme.
- [ ] **AI-07** — Aşama ve revizyon değişikliklerinde mevcut Git/EDA kayıtlarını kullanarak kısa checkpoint oluştur. Kullanıcı değişikliklerini koru; yarıda kalan işleri doğrulanmış son durumdan devam ettir.
- [ ] **AI-08** — EDA entegrasyon yöntemi bağımsızdır. Mevcut ve yetkili MCP/CLI/API araçlarını önce düşük riskli okuma/bağlantı kontrolüyle doğrula. Olmayan araç fonksiyonunu varmış gibi kullanma; native otomasyon veya kullanıcı destekli alternatif mümkünse öner. Eklentileri kurmak, yetki genişletmek veya harici veri göndermek ayrı kullanıcı onayı gerektirir.
