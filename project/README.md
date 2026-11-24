# Workflow State

`workflow-state.json` onay ve review durumunun kısa, makine tarafından okunabilir kaydıdır.

- `requirements_revision`: onaylanan proje girdilerinin revizyonu.
- `pcb_requirements_revision`: PCB layout girdilerinin ayrı revizyonu. Malzeme, teknoloji, geometri, ring ve diğer PCB kararları değişirse güncelle.
- `design_revision`: mevcut native tasarımın revizyonu veya commit kimliği. Tasarım değiştiğinde güncelle.
- `input_approval`: G0 kullanıcının gerçek gereksinim onayı, ilgili revizyon ve onay referansı.
- `pcb_input_approval`: G0.5, kullanıcının PCB girdileri için gerçek onayı, ilgili PCB girdi revizyonu ve onay referansı.
- `reviews`: bağımsız schematic/PCB/manufacturing inceleme sonucu, ilgili tasarım revizyonu ve `REVIEW_LOG.md` kanıt referansı. Şematik değişmemişse Reviewer final revizyonda bu durumu diff ile doğrulayabilir.
- `export_approval`: G1 kullanıcının ilgili tasarım revizyonu için açık üretim dosyası hazırlama onayı ve referansı.
- `blocking_issues`: açık CRITICAL/MAJOR bulgu kimlikleri veya ilgili engeller.

Approval durumları: PENDING / APPROVED. Review durumları: PENDING / PASS / REWORK / BLOCKED. Geçerli onay veya PASS için revizyon ve gerçek kanıt gereklidir. Manager review sonucunu Reviewer'ın kaydına göre işler; onayları kendi adına üretmez.

Yerel kontrol aracı dosya durumunu doğrular; gerçek kullanıcı onayının ve mühendislik testinin yerine geçmez. Yeni revizyon öncekine ait onayları otomatik olarak geçerli kılmaz.

`check-layout` G0, G0.5 ve mevcut tasarım revizyonunun şematik review kaydını kontrol eder. Layout başladıktan sonra tasarım revizyonu ilerleyebilir; export öncesi Reviewer geçerli revizyona ait şematik ve PCB sonuçlarını doğrular. Şematik değişmediyse mevcut kanıt ve ilgili diff ile kontrol edilebilir.

Multi-PCB projede `design_revision` tüm onaylı kartların ortak sistem revizyonudur. Manager kart ID'lerini ve kapsamı proje kayıtlarında tutar. Reviewer her kartı ve ilgili arayüzleri kanıtla doğrular; sistem review sonucunu ancak tüm onaylı kapsam tamamlandığında PASS işaretler. Ayrı kart başına gereksiz workflow dosyası oluşturma.

Şema sürümü 2'dir. Önceki v1 şemasını kullanan projelerde mevcut gereksinim/review kayıtlarını koru; `schema_version` değerini 2 yap, `pcb_requirements_revision` alanını null ve `pcb_input_approval` kaydını PENDING/null/null olarak ekle. Gerçek G0.5 onayı gelmeden APPROVED işaretleme.
