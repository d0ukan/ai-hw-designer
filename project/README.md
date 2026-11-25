# Workflow State

`workflow-state.json` onay ve review durumunun kısa, makine tarafından okunabilir kaydıdır.

- `project_code`: proje kodu (ör. `DR00627`); çıktı adları bundan türetilir. Export ve release için zorunlu. Eski state dosyalarında alan yoksa null kabul edilir.
- `requirements_revision`: onaylanan proje girdilerinin revizyonu.
- `pcb_requirements_revision`: PCB layout girdilerinin ayrı revizyonu. Malzeme, teknoloji, geometri, ring ve diğer PCB kararları değişirse güncelle.
- `design_revision`: kartın revizyonu (ör. `R01`); çıktı adlarında ve `Manufacturing/<rev>/` klasöründe kullanılır. Yeni revizyon yalnızca REL-01'e göre açılır (`templates` adı kullanılamaz).
- `input_approval`: G0 kullanıcının gerçek gereksinim onayı, ilgili revizyon ve onay referansı.
- `pcb_input_approval`: G0.5, kullanıcının PCB girdileri için gerçek onayı, ilgili PCB girdi revizyonu ve onay referansı.
- `reviews`: bağımsız schematic/PCB/manufacturing inceleme sonucu, ilgili tasarım revizyonu ve `REVIEW_LOG.md` kanıt referansı. Şematik değişmemişse Reviewer final revizyonda bu durumu diff ile doğrulayabilir.
- `export_approval`: G1 kullanıcının ilgili tasarım revizyonu için açık üretim dosyası hazırlama onayı ve referansı.
- `blocking_issues`: açık CRITICAL/MAJOR bulgu kimlikleri (`F-001` biçimi) veya ilgili engeller.
- `deliverables`: release'te bulunması gereken çıktı listesi (INT-25); `projectctl.py deliverables ...` ile yazılır.

Kayıtlar isteğe bağlı `recorded_on` (UTC tarih), `recorded_by` ve `commit` alanlarını da taşıyabilir; `projectctl.py` komutları bunları otomatik doldurur.

**Commit bağı:** Proje bir git deposuysa `approve` ve `review` o anın commit'ini kaydeder. Aynı `R01` içinde tasarım değişirse `check-export`/`check-release` bunu yakalar: şematik review'dan sonra şematik dosyaları (`*.kicad_sch`, `*.SchDoc`, `*.sch`), PCB/manufacturing review ve G1'den sonra `Hardware/` altındaki herhangi bir dosya değiştiyse kapı kapanır ve yeniden review gerekir. Git'e eklenmemiş yeni tasarım dosyaları da değişiklik sayılır. Tasarım commit edilmeden `review ... PASS` veya `approve G1` kaydı reddedilir. EDA'nın export sırasında yeniden yazdığı `*.OutJob` dosyaları değişiklik sayılmaz. Git yoksa kontrol atlanır.

**Teslim listesi ve manifest:** `deliverables` alanı (ör. `BOM PnP Gerber SCH ASSY FAB`) release'te zorunludur; her öğe `<kod>-..._<öğe>.*` dosyası veya klasörü olarak bulunmalıdır. `review manufacturing PASS` geçerli bir manifest ister ve onun SHA-256 değerini `manifest_sha256` olarak saklar.

## Kayıt komutları

JSON'u elle düzenleme; komutlar dosyayı doğrulayıp güvenli şekilde yazar:

Tam sıra (örnek revizyon `R01`; `--revision` değeri her zaman `design_revision` ile aynı olmalı). Her an sıradaki eksik adımı ve komutu görmek için `python scripts/projectctl.py next`.

```bash
# Başlangıç (Manager)
python scripts/projectctl.py set project_name "Sensör kartı"
python scripts/projectctl.py set project_code DR00627
python scripts/projectctl.py set design_revision R01
python scripts/projectctl.py set requirements_revision REQ-1
python scripts/projectctl.py approve G0 --revision REQ-1 --evidence "Kullanıcı onayı, 2026-11-25 sohbet" --by "<isim>"
# Şematik → review (tasarımı önce commit et)
python scripts/projectctl.py review schematic PASS --revision R01 --evidence "REVIEW_LOG.md#R01-SCH"
# G0.5 → layout
python scripts/projectctl.py set pcb_requirements_revision PCB-1
python scripts/projectctl.py approve G0.5 --revision PCB-1 --evidence "Kullanıcı PCB onayı"
python scripts/projectctl.py check-layout
# PCB review → G1
python scripts/projectctl.py review pcb PASS --revision R01 --evidence "REVIEW_LOG.md#R01-PCB"
python scripts/projectctl.py approve G1 --revision R01 --evidence "Kullanıcı export onayı"
python scripts/projectctl.py check-export
# Çıktılar (REL-04)
python scripts/projectctl.py deliverables BOM PnP Gerber SCH ASSY FAB
python scripts/projectctl.py check-bom            # Designer
python scripts/projectctl.py manifest             # Designer, son export adımı
python scripts/projectctl.py review manufacturing PASS --revision R01 --evidence "REVIEW_LOG.md#R01-MFG"
python scripts/projectctl.py check-release
# Diğer
python scripts/projectctl.py name --variant A     # DR00627-AV-R01
python scripts/projectctl.py check-bom X_BOM.csv --pnp X_PnP.csv
python scripts/projectctl.py block F-001
python scripts/projectctl.py unblock F-001
```

`manifest`, `Manufacturing/<design_revision>/` içindeki dosyaların SHA-256 listesini `MANIFEST.sha256` olarak yazar. `check-release` bu manifest eksikse, dosyalar değişmişse, bir dosyanın adı proje koduyla başlamıyorsa (önekli klasörlerin içi, ör. `DR00627-R01_Gerber/`, serbesttir) veya `check-bom` hata bulursa başarısız olur. `check-bom` BOM ile PnP designator'larını, Qty sayılarını, DNP parçaların PnP'de olmamasını ve MPN'leri kontrol eder; muadil eksikse uyarı verir.

Approval durumları: PENDING / APPROVED. Review durumları: PENDING / PASS / REWORK / BLOCKED. Geçerli onay veya PASS için revizyon ve gerçek kanıt gereklidir. Manager review sonucunu Reviewer'ın kaydına göre işler; onayları kendi adına üretmez.

Yerel kontrol aracı dosya durumunu doğrular; gerçek kullanıcı onayının ve mühendislik testinin yerine geçmez. Yeni revizyon öncekine ait onayları otomatik olarak geçerli kılmaz.

`check-layout` G0, G0.5 ve mevcut tasarım revizyonunun şematik review kaydını kontrol eder. Layout başladıktan sonra tasarım revizyonu ilerleyebilir; export öncesi Reviewer geçerli revizyona ait şematik ve PCB sonuçlarını doğrular. Şematik değişmediyse mevcut kanıt ve ilgili diff ile kontrol edilebilir.

Multi-PCB projede `design_revision` tüm onaylı kartların ortak sistem revizyonudur. Manager kart ID'lerini ve kapsamı proje kayıtlarında tutar. Reviewer her kartı ve ilgili arayüzleri kanıtla doğrular; sistem review sonucunu ancak tüm onaylı kapsam tamamlandığında PASS işaretler. Ayrı kart başına gereksiz workflow dosyası oluşturma.

Şema sürümü 2'dir. Önceki v1 şemasını kullanan projelerde mevcut gereksinim/review kayıtlarını koru; `schema_version` değerini 2 yap, `pcb_requirements_revision` alanını null ve `pcb_input_approval` kaydını PENDING/null/null olarak ekle. Gerçek G0.5 onayı gelmeden APPROVED işaretleme.
