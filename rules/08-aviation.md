<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
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
