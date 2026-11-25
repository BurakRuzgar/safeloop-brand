# E: Kullanıcı eskizi (S + L iç içe)

Kaynak: `eskiz-kullanici.jpg` · Üretici: `src/build_e.py` · Pano: `e-pano.png`

**Okuma:** S açısal çizildiğinde üst bar, çapraz omurga ve alt bardan oluşur. L'nin gövdesi sağ üstten sol alta çapraz iner. İkisi birlikte kapalı bir "8" döngüsü kurar ve bu doğrudan "Loop" fikrine bağlanıyor. L'nin ayağı taban çizgisi olarak sağa uzar.

| | Dosya | Değerlendirme |
|---|---|---|
| E1 Açısal | `e1-acisal-symbol.svg` | Güçlü ve net bir siluet. **Risk:** belirgin şekilde kum saati gibi okunuyor (zaman/süre çağrışımı), S ve L okuması zayıf. |
| E2 Eskize sadık | `e2-eskiz-symbol.svg` | Eskizdeki tek kesintisiz çizgi korundu, S ve L okuması daha iyi. **Risk:** üstteki üçgen boşluk küçük ve 16 px'te kapanıyor. "Ƶ/∂" gibi okunabilir. |

- BRIEF kısıtları kontrol edildi: kalkan, onay işareti, baret, üçgen uyarı ve ünlem yok. Çaprazlar "X/iptal" gibi okunmuyor.
- Stroke tabanlı çalışma dosyaları. Seçilirse outline'a çevrilip optik düzeltme yapılır.
- Geliştirme önerisi (E2): üst barı biraz yükseltip omurgayı dikleştirmek. Böylece üst boşluk büyür ve 16 px'te açık kalır.

## Aşama 3b: E2 varyasyonları (karar: E2 ana aday, E1 elendi → elenen/)
Üretici: `src/build_e2v.py` · Pano: `e2-varyasyon-pano.png` · 16/32 px testi: `renders/pixel-test.png`
Sabit kalanlar: L gövdesi (sol alt → sağ üst), L ayağı ve taban (x 54–232, y 198), wordmark.
Değişenler: sol üst köşe yarıçaplı bir S kıvrımına dönüştü. Omurga, iki kıvrımın ortak teğeti oldu, bu yüzden kıvrımlar büyüdükçe yatışıyor. Kâse büyüdü.

| | Üst kıvrım | Kâse | Okuma |
|---|---|---|---|
| e2a | r28 | r48 | Köşe yumuşadı ama uzun düz üst bar yüzünden Z izi hâlâ hissediliyor |
| e2b | r34 | r50 | S ile Z dengede |
| **e2c (öneri)** | r42, sola 22 taşar | r46 | S okuması en güçlü, 16 px'te en iyi sonuç |

- **Sınır:** Taban ve ayak sabit kaldığı için kâse en fazla r50'ye kadar büyüyebiliyor. Daha büyük kâse için ayağın uzatılması gerekir.
- **Küçük sürüm (`e2*-small.svg`):** Izgara 140'tan 184 birime yükseltildi, çizgi 34, viewBox sıkı kırpıldı. 32 px'te net okunuyor. 16 px'te en iyisi e2c. e2a ve e2b'de üstteki iç boşluk yarı kapanıyor.
- **Özgünlük (`../ozgunluk-raf-e2-b.png`):** Kütüphanede yakın bir eşleşme yok. Zendesk Z ve Segment S farklı. Kütüphane teknoloji ağırlıklı, bu yüzden profesyonel tescil ve görsel arama yine gerekli.
- **Okuma riski:** Çapraz L gövdesi S'nin üstünden geçtiği için "üstü çizili S" ya da "yasak" gibi okunabilir.
- **Aşama 4 notu:** Yatay logoda sembol tabanı (y=198) ile yazı tabanı arasında yaklaşık 17 birim fark var. Bu hizalanmalı.
