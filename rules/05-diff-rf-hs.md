<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
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
