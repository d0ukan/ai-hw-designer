<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
## 10 · Batarya ve şarj — koşullu

> **Yalnızca kartta şarj edilebilir batarya veya batarya ile çalışma varsa uygula** (INT-52). Yoksa bu bölüm N/A'dır ve batarya sorusu sorulmaz. Hazır sertifikalı batarya paketi ve modül kullanılıyorsa üreticinin kılavuzu bağlayıcıdır.

- [ ] **BAT-01** — Kullanıcıdan al: kimya (Li-ion, LiPo, LiFePO4, NiMH, primer/şarjsız), hücre sayısı (S/P), kapasite, nominal ve maksimum gerilim, en yüksek şarj/deşarj akımı, çalışma ve şarj sıcaklığı, hücrede koruma devresi olup olmadığı ve gereken sertifikalar (ör. IEC 62133, UN 38.3; Havacılıkta ör. RTCA DO-311A). Bilinmeyen değeri tahmin etme.
- [ ] **BAT-02** — **Koruma:** Lityum hücrelerde aşırı şarj, aşırı deşarj, aşırı akım ve kısa devre koruması olmalıdır (koruma IC + çift MOSFET). Hücrede yoksa kartta tasarla. Ters polarite koruması ve ana batarya hattında sigorta veya PTC kullan.
- [ ] **BAT-03** — **Şarj:** Kimyaya uygun şarj IC'si seç (Li-ion CC/CV 4.20 V veya hücre datasheet'indeki değer; LiFePO4 3.60 V). Şarj akımını hücre datasheet'i ve giriş kaynağının sınırıyla belirle (ör. USB 2.0 500 mA; USB-C'de CC dirençleri ve kaynak akım bildirimi). Yük çalışırken şarj gerekiyorsa power-path yönetimi kullan.
- [ ] **BAT-04** — **Sıcaklık:** Şarjı NTC ile sıcaklık penceresine bağla (tipik 0…45 °C şarj; JEITA destekleniyorsa uygula). NTC hücreye termal temaslı olsun; şarj IC'sinin termal pad'i ve via'ları datasheet'e uygun olsun.
- [ ] **BAT-05** — **Layout:** Batarya akım yolunu kısa ve geniş tut (LAY-20); akım ölçüm dirençlerini Kelvin bağla. Batarya konnektörü polariteli, ters takılamayan ve gerekiyorsa kilitli olsun; silkscreen'de `+` / `−` işaretli. Hücre ve konnektör ısı kaynaklarından uzak dursun.
- [ ] **BAT-06** — **Ölçüm ve uyku akımı:** Batarya gerilimi bölücüsünü yüksek değerli veya anahtarlı yap ki sürekli akım çekmesin. Uyku/bekleme akımı bütçesini hesapla ve kaydet. Kalan kapasite gerekiyorsa fuel gauge değerlendir.
- [ ] **BAT-07** — Primer (şarj edilemeyen) pil asla şarj devresine bağlanmaz. Birden fazla güç kaynağı paralelse (ör. USB + batarya) ters akımı ideal diyot, Schottky veya power-path ile engelle.
- [ ] **BAT-08** — **Doğrulama:** Şarj profili, koruma eşikleri, sıcaklık kesmesi, kısa devre davranışı (güvenli test ortamında) ve uyku akımı ölçümünü test planına ekle. Yapılmayan testi "doğrulanmadı" olarak kaydet; Reviewer kanıtı kontrol eder.
