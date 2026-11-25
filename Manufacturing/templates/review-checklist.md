# <önek> — Aşama review checklist'i (Reviewer)

Kısa kontrol listesi; ayrıntı ilgili `rules/` bölümündedir. Bulguları `REVIEW_LOG.md` formatında yaz, sonucu PASS / REWORK / BLOCKED olarak bildir.

## Şematik (rules/04, SCH)
- [ ] Pinout ve footprint datasheet ile eşleşiyor (SCH-02, VER-01)
- [ ] Güç ağacı, decoupling, filtreler (SCH-03, SCH-04)
- [ ] Terminasyon, pull-up, ESD, strapping pinleri (SCH-05)
- [ ] Kısıtlar ve diferansiyel çiftler işaretli (SCH-06); DNP/0 Ω opsiyonları işaretli (SCH-07)
- [ ] ERC temiz veya istisnalar gerekçeli (VER-02)

## PCB (rules/02, 04, 05)
- [ ] G0.5 kararları uygulanmış (outline, stack-up, ring, silkscreen PCB-17…21)
- [ ] Yerleşim: referans layout, giriş koruması, switching döngüsü, kristal (LAY-08…13)
- [ ] Routing: en kısa yol, bölünmüş düzlem yok, güç/HV kuralları (LAY-14…24)
- [ ] SI/PI: decoupling döngüsü, empedans, length/delay matching (LAY-25…29, DIF/HS/RF)
- [ ] Silkscreen çakışmasız (LAY-30); DRC temiz (VER-02)

## Üretim (rules/09)
- [ ] Dosya adları önekle uyumlu, her varyantın BOM/PnP'si ayrı (REL-03)
- [ ] `projectctl.py check-bom` temiz; muadiller kontrol edildi (DFM-14)
- [ ] Gerber/drill katmanları ve kart sınırı doğru (VER-04); `_ASSY.pdf` ve fab notu var
- [ ] `projectctl.py manifest` ve `check-release` başarılı (REL-04)
