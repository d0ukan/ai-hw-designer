<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
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
