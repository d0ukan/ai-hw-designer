# Katkı

Bu repo bir şablondur; proje dosyaları kendi kopyanızda tutulur. Şablona katkı için:

1. Kural önerisi veya hata için önce bir issue açın (şablonları kullanın).
2. Değişiklikte kural kimliklerini (ör. `LAY-23`) değiştirmeyin; yeni kural yeni numara alır.
3. Her değişiklikte `README.md` ve `CHANGELOG.md` güncellenir; sürüm satırları aynı olmalıdır.
4. Göndermeden önce yerelde çalıştırın:

```bash
python -m unittest discover -s tests
python scripts/check_repo.py
```

5. Datasheet, CAD modeli veya logo eklerken lisans/yeniden dağıtım izni olmalıdır. Gizli bilgi, API anahtarı veya müşteri tasarımı eklemeyin.
