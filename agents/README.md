# Portable Agent Roles

Bu dosyalar belirli bir AI sağlayıcısı veya ajan API'si gerektirmez. Ortak çalışma kuralları `../AGENTS.md`, detaylı teknik kurallar `../Hardware-Rules.md` ve `../Hardware-Roles.md` içindedir.

## Otomatik ajan desteği varsa

Manager ana oturumda kalır; gerektiğinde Designer ve Reviewer rollerini ilgili modelle başlatır. Kullanılan istemcinin yeteneklerini ve desteklenen model/efor ayarlarını doğrula. Platform adaptörleri yalnızca kolaylık sağlar; ortak rol dosyaları tüm istemcilerde kullanılabilir.

## Otomatik ajan desteği yoksa / AI değiştiriliyorsa

1. Manager mevcut proje kayıtlarından kısa bir görev paketi hazırlar (Hardware-Roles.md, bölüm 05).
2. Kullanıcı ilgili rol dosyasını ve gerekli proje dosyalarını seçtiği AI oturumuna verir.
3. Görev sonucunu, gerçek dosya değişikliklerini ve review kanıtını Manager'a geri iletir.
4. Manager mevcut revizyon ve onayları koruyarak sıradaki aşamayı yönetir.

Örnek istem:

> AGENTS.md ve agents/Reviewer.md talimatlarını uygula. Atanan tasarım revizyonunu ve sadece ilgili dosyaları incele. Designer'ın tasarımını değiştirme. Gerçek bulguları kısa raporla; doğrulayamadığın işlemleri BLOCKED olarak bildir.

Farklı bir AI ile devam etmek için tüm sohbeti yeniden göndermek gerekmez. Proje dosyaları ortak kayıt kaynağıdır. Dosyaya veya EDA aracına erişemeyen istemcide işlemleri yapılmış göstermeme kuralı geçerlidir.
