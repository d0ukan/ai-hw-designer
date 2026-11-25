# Örnek proje: DR00001 — USB-C LED kartı

> **Bu bir öğretici örnektir, üretime hazır tasarım değildir.** Native EDA dosyası, Gerber ve gerçek review kanıtı yoktur. MPN'ler gerçek parçalardır ama datasheet ve stok kontrolü yapılmamıştır; kullanmadan önce doğrula.

Şablonun akışını baştan sona göstermek için küçük bir kart: USB-C'den 5 V alıp bir güç LED'i yakar.

| Ne gösterir | Dosya |
| :--- | :--- |
| Doldurulmuş proje bilgileri ve kararlar (kimlik, profil, hedef, silkscreen, açık kararlar) | [Project-README.md](Project-README.md) |
| Tüm kapıları geçmiş iş akışı kaydı | [workflow-state.json](workflow-state.json) |
| Revizyon geçmişi | [REVISION-HISTORY.md](REVISION-HISTORY.md) |
| Örnek review bulguları (F-001 …) | [REVIEW_LOG.md](REVIEW_LOG.md) |
| Ana ve A varyantı BOM/PnP, fab notu, manifest | [Manufacturing/R01/](Manufacturing/R01/) |

Teslim listesi bilerek `BOM PnP FAB` tutuldu. Gerçek bir projede `Gerber SCH ASSY` de olur; örnekte EDA dosyası olmadığı için sahte Gerber veya PDF eklenmedi.

Bu örneği yerelde kontrol et:

```bash
python scripts/projectctl.py status        --state examples/DR00001-usb-c-led/workflow-state.json --manufacturing-dir examples/DR00001-usb-c-led/Manufacturing
python scripts/projectctl.py check-bom     --state examples/DR00001-usb-c-led/workflow-state.json --manufacturing-dir examples/DR00001-usb-c-led/Manufacturing
python scripts/projectctl.py check-release --state examples/DR00001-usb-c-led/workflow-state.json --manufacturing-dir examples/DR00001-usb-c-led/Manufacturing
python scripts/projectctl.py next          --state examples/DR00001-usb-c-led/workflow-state.json --manufacturing-dir examples/DR00001-usb-c-led/Manufacturing
python scripts/projectctl.py name --variant A --state examples/DR00001-usb-c-led/workflow-state.json
```

CI her push'ta bu komutları çalıştırır.
