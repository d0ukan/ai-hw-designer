# Hardware

Onaylı proje girdilerine göre seçilen EDA yazılımının native schematic, PCB, constraints ve projeye özel kütüphaneleri burada tutulur. Henüz EDA yazılımı veya kart amacı seçilmediğinden şablon örnek PCB dosyası içermez.

Layout öncesinde G0.5 PCB girdileri onaylanır ve check-layout kontrolü çalıştırılır. CHASSIS_GND çevre halkası yalnızca açık kullanıcı onayı varsa oluşturulur.

Tek PCB projede ortak bir EDA proje alanı yeterlidir. Multi-PCB proje onaylandıysa her kartı `Hardware/<board-id>/` gibi ayrı bir native EDA alanında tut. Kart sayısı ve ID'leri kullanıcı girdisinden gelir; gereksiz placeholder kartları oluşturma. Kartlar arası ve harici bağlantıların ortak pinout/konnektör referansını `Project-README.md` içinde koru.

Ortak `Hardware-Library/` varlıklarını mümkün olduğunca göreli yollarla kullan; başka bilgisayarda çalışmayacak mutlak kütüphane yollarından kaçın. Tasarım revizyonlarını kaydet, geçerli kullanıcı değişikliklerini koru ve gerekli ERC/DRC kontrollerini gerçek EDA aracıyla yürüt.

MCP zorunlu değildir. Seçilen EDA'nın desteklediği MCP, CLI, API/script veya GUI erişimini proje başlamadan doğrula. `Project-README.md` içinde mevcut yetenekleri ve kısıtları kaydet; aynı proje revizyonunda doğrulanmamış dönüştürme veya otomasyon sonuçlarını başarılı sayma.
