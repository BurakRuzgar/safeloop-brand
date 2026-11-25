# Aşama 3: A · Kapanan Halka incelemesi

Kaynak: 01-brief.md · Tarih: 2026-11-24
Dosyalar: `concepts/a-halka-v2-symbol.svg`, `a-halka-v2-small.svg`, `a-halka-v2-lockup.svg`, üretici `concepts/src/build_a_v2.py`
Görseller: `concepts/review/` → `a-inceleme-pano.png`, `pixel-test.png`, `a-halka-v2-lockup.png`, `ozgunluk-raf.png`

## Yapılan optik düzeltmeler
| | v1 | v2 ana (≥48 px) | v2 küçük (16–32 px) |
|---|---|---|---|
| Halka kalınlığı | 36 | 36 | 44 (16 px'te 2.75 px) |
| Nokta çapı / kalınlık | 44 / 36 = 1.22 | 48 / 36 = **1.33** | 64 / 44 = 1.45 |
| Boşluk | radyal kesik, kama (13 → 19) | **yuva kesik, her yerde 12** | yuva kesik, 30 (~1.9 px) |
| Nokta açısı | −45° | −45° | −45° |
| Dosya | stroke | **dolgu (outline)** | dolgu (outline) |

- **Yuva kesik:** Halka uçları noktayla eş merkezli bir yayla kesildi. Nokta, halkanın içinde "yerine oturan parça" gibi duruyor ve boşluk her yerde aynı genişlikte.
- **Nokta oranı:** Daire, aynı kalınlıktaki çizgiden optik olarak hafif görünür. Bu yüzden nokta kalınlığın 1.33 katı yapıldı ve ağırlığı halkayla eşitlendi.
- **Açı −45°:** Tam diyagonal olduğu için hareket hissi veriyor ve ızgaraya oturuyor. Nokta halkanın dış sınırını aşmıyor, bu yüzden geometrik merkez korunuyor (kenar boşlukları 26/26).
- **Küçük kesim:** 16 px'te v1 ve v2 ana sürüm düz bir "O"ya dönüşüyor (`pixel-test.png`). Küçük kesimde nokta ve boşluk okunuyor, ters zeminde de çalışıyor.
- svg_audit: v2 ana ve küçük sürüm sorunsuz (100/100).

## Önce çözülmesi gereken (karar gerekli)
1. **Özgünlük riski: Ionic.** Ionic'in sembolü de "halka ve sağ üstteki boşluğa oturan nokta" kurgusunda (`ozgunluk-raf.png`). Farklar şunlar: bizim halkamız çok daha kalın, yuva kesikli ve ortasında dolu daire yok. Yine de yapı aynı. PyTorch (açık halka ve nokta) daha uzak, CircleCI ise farklı.
   _Seçenekler:_ (a) Bu farklarla devam edip profesyonel tescil/benzerlik araştırması yaptırmak, (b) noktanın konumunu ya da ilişkisini değiştirmek (ör. halkanın içinde, ucun devamında), (c) B'ye veya E'ye geçmek.

## Düzeltilmesi gereken
2. **Wordmark hâlâ stroke tabanlı.** Aşama 4'te dolguya (outline) çevrilmeli.
3. **Yuva uçları:** Halka uçları dış kenarda yaklaşık 60°'lik sivri uçlarla bitiyor. Büyük boyutta (tabela) uçlara küçük bir yuvarlatma denenmeli.

## İyileştirilebilir
4. 32 px'te küçük kesim biraz ağır duruyor. Gerekirse 24–32 px için ara bir kesim yapılabilir.
5. Yatay logoda sembol ile yazının ağırlık dengesi iyi. Sembol–yazı aralığı (56) Aşama 4'te koruma alanı kuralıyla sabitlenmeli.

## İyi olanlar
- Fikir tek cümlede anlatılıyor: "Halka kapanmak üzere, son parça yerine oturuyor."
- Wordmark'taki "oo", halkanın formunu tekrar ediyor ve sistem tutarlı.
- Tek renkte, ters zeminde ve 16 px'te çalışıyor (küçük kesimle).
- BRIEF kısıtlarına uyuyor: kalkan, onay işareti, baret ve sarı-siyah yok.
