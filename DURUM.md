# SafeLoop Durum

## Biten
- Proje kurulumu: CLAUDE.md, BRIEF.md, DURUM.md oluşturuldu.
- Aşama 1: Brief yazıldı → brand/safeloop/guidelines/01-brief.md
- v1 konseptleri arşivlendi → brand/safeloop/_arsiv-v1/ (referans alınmaz).
- **Aşama 2 tamamlandı (v2 keşif):** 8 yön → 4 kaba eskiz → Devir seçildi → brand/safeloop/concepts-v2/
  - Pano: pano-v2.png (.svg) · 8 yön ve eleme gerekçeleri: YONLER.md
  - Diğer yönler: 2-ivme-izi, 3-yukselen-spiral, 5-kapanan-cizgi-wordmark · üretici: src/build_v2.py
  - Elenenler: elenen/ (Dört Adım, Kapanan Çizgi sembolü, alternatif B "yalnız 2. o", çerçeve koyu zemin sürümü)
- **Aşama 3 tamamlandı (Devir geliştirme + inceleme):** concepts-v2/devir/
  - Sembol kesimleri: devir-symbol.svg (64 px+) · devir-small.svg (16–32 px)
  - Kesim oranları: ana ro94/sw40/dy18/boşluk10 · küçük ro90/sw46/dy24/boşluk20 · kelime içi ro30.5/sw14.5/dy6/boşluk5 (harf kalınlığı 14)
  - Wordmark: wordmark-oo.svg (safel∘∘p) · kutusuz eski lockup: lockup-oo.svg
  - **Onaylı lockup** (lacivert): lockup-box.svg (≥ ~250 px) · lockup-box-small.svg (≤ 200 px)
  - **Onaylı koyu zemin** (ters kutu): lockup-box-ters-lacivert(-small).svg · siyah zemin: lockup-box-ters-siyah(-small).svg
  - **Onaylı ikon/favicon** (lacivert): icon-box.svg (64 px+) · icon-box-small.svg (16–32 px)
  - Testler: test-devir.png (200/120/60 px, gözlük/∞, 180°, bulanık) · pano-lockup.png (600/200/120 px; siyah kutu dönemine ait)
  - Üretici: src/build_devir.py (tüm kesimler tek fonksiyondan; sol yarı yukarı, sağ yarı aşağı)
  - Kullanım kuralı notu: guidelines/kullanim-notlari.md

- **Aşama 4 tamamlandı ve onaylandı (marka kiti):** brand/safeloop/guidelines/marka-kiti/
  - Spec: 04-marka-kiti.md (palet HEX/RGB/görev/kontrast, durum renkleri, fontlar, kurallar, yapılmayacaklar)
  - Pano: marka-kiti-pano.png (.html): palet, tipografi, butonlar, durum etiketleri, iş izni kartları
  - Tüm logo dosyaları lacivert/beyaz yapıldı (src/build_devir.py, K = #0F1B2D). Yeni: lockup-box-ters(-small).svg, wordmark-oo-beyaz.svg, icon-box-ters.svg (saydam)
  - pano-lockup.png yeni dosya yapısıyla yeniden üretildi
  - Siyah sürümler (lockup-box-ters-siyah*) → concepts-v2/elenen/
  - kullanim-notlari.md güncellendi

- **Aşama 5 tamamlandı ve onaylandı (token'lar):** brand/safeloop/tokens/
  - safeloop.tokens.css (--sl- önekli, açık/koyu + sistem tercihi + reduced-motion) · safeloop.tokens.json (W3C DTCG)
  - kontrast.md (26 çift × 2 tema, tümü WCAG'ı geçiyor) · onizleme.html/.png · README.md
  - Üretici: tokens/src/build_tokens.py (tek kaynak)

- **Aşama 6 tamamlandı ve onaylandı (teslim):** brand/safeloop/final/
  - svg/ (29 dosya, tümü outline, sıkı kırpım): yatay · yatay-kucuk · yatay-imza · dikey · dikey-kucuk · dikey-imza · wordmark · sembol · sembol-kucuk × renkli/siyah/beyaz + sembol-kare + favicon.svg
  - png/: favicon.ico (16/32/48) · favicon-16/32 · apple-touch-icon 180 · icon-192/512 · icon-maskable-512 · lockup PNG'leri (yatay/wordmark 1200, dikey 800; saydam) · site.webmanifest
  - Kontrol panosu: final/teslim-pano.png (.html)
  - Marka kılavuzu: guidelines/06-marka-kilavuzu.md (sürümler, boyuta göre kesim, boş alan, renk, yapılmayacaklar, dosya listesi, <head> kodu, token bağlantısı)
  - Üretici: final/src/build_final.py → render_final.py · ttf.py (bağımlılıksız font→path) · fonts/PlusJakartaSans-SemiBold.ttf + OFL.txt
  - Doğrulama: outline ile stroke farkı yalnız kenar yumuşatması (piksel fark testi); SVG'lerde stroke/text yok.
- **PDF marka kılavuzu tamamlandı ve onaylandı:** brand/safeloop/guidelines/SafeLoop-Marka-Kilavuzu.pdf (A4, 9 sayfa)
  - 04-marka-kiti.md + 06-marka-kilavuzu.md birleştirildi; logolar final/svg/'den vektör olarak gömülü.
  - Sayfalar: kapak · marka · logo sürümleri · boyut/kesim/boş alan · renk sürümleri · palet ve durum renkleri · tipografi · kullanım ve yapılmayacaklar (görsel örnekli) · dosyalar/web/token'lar/açık konular.
  - 04'teki eski dosya yolları (concepts-v2/devir/) PDF'e alınmadı; yerine final/ dosyaları anlatıldı.
  - Üretici: guidelines/src/build_kilavuz_pdf.py (headless Chrome; Inter ve Plus Jakarta Sans Google Fonts'tan yükleniyor, ağ gerekli).

## Yapılmadı
- (yok — tüm aşamalar tamamlandı)

## Kararlar
- Marka özü: "Her açılan aksiyon kapanır." (kapalı döngü / PDCA)
- Sıfatlar: sistematik, güvenilir, kesintisiz, modern, kurumsal.
- Font adayları (taslak): Inter, Manrope, Plus Jakarta Sans. Kesin değil.
- v1 konseptleri arşivlendi, sıfırdan yeni keşif başlatıldı; eski wordmark kullanılmaz.
- v2'de kaçınılacaklar: halka + nokta; düz S monogramı; kum saati; Z ya da 8 gibi okunan form; üstü çizili harf / yasak işareti; kapsül; konuşma balonu; ∞; BRIEF'teki İSG klişeleri.
- **Logo: Devir.** İki yarım yay kayarak birleşir. Sembol hem soldaki kutuda hem de "safeloop"un iki "o"sunda kullanılır (safel∘∘p). Kayma yönü her yerde aynı. Sembol oranları onaylı.
- **Lockup:** sembol, köşeleri yuvarlatılmış kare kutuda zemin renginde oyuk olarak durur (app ikonu gibi). Wordmark beyaz zeminde koyu.
- **Ana renk: lacivert #0F1B2D** (kutu + wordmark). Siyah değil.
- **Koyu zemin: ters kutu.** Beyaz kutu, sembol zemin renginde; wordmark beyaz. Çerçeve seçeneği elendi.
- Kutulu lockup, favicon ve uygulama ikonu onaylandı.
- **KARAR (Aşama 4): Palet, durum renkleri ve fontlar onaylandı.**
  - Aksan: Turkuaz #1FC7B4; açık zeminde metin için Turkuaz Koyu #0B7C71.
  - Durum renkleri: Başarılı #1B7741, Uyarı #A8570A, Hata #C0303C.
  - Fontlar: Plus Jakarta Sans (başlık) + Inter (metin).
  - Spec: guidelines/marka-kiti/04-marka-kiti.md
- Renk anlamı: Turkuaz = aktif / devam eden / vurgu; Başarılı yeşili = yalnız tamamlandı / kapandı. İkisi aynı anlamda kullanılmaz.
- Slogan adayı: "Her açılan aksiyon kapanır." (guidelines/marka-kiti/04-marka-kiti.md)
- Çalışma kapsamı: yalnız bu depo; başka proje ya da uygulama koduna dokunulmaz.
- Kullanım kuralı: kutulu sembol + wordmark geniş alanlarda; yalnız wordmark dar alanlarda; yalnız kutulu sembol ikon ve favicon olarak.

- **KARAR (Aşama 6): Teslim onaylandı.**
  - "Renkli" sürüm = Lacivert kutu + wordmark, imza Arduvaz #566275. Siyah/beyaz sürümlerde imza tek renk.
  - İmza: Plus Jakarta Sans SemiBold, path'e çevrildi; yatayda "s"ye sola hizalı, dikeyde ortalı. Yalnız ana kesimle (yatay ≥ 320 px, dikey ≥ 200 px).
  - Dikey lockup: kutu 200 birim, wordmark'a ortalı, kutu–harf boşluğu 56 birim.
  - Boş alan = kutu yüksekliğinin yarısı (≈ x-yüksekliği).
  - Kesim sınırları: yatay ana ≥ 250 px, küçük 120–249 px; dikey ana ≥ 200 px, küçük 80–199 px; sembol ana ≥ 64 px, küçük 16–63 px.
  - apple-touch ve maskable ikon: tam kare lacivert + beyaz sembol (sembol-kare). PWA "any": saydam köşeli kutu.
  - favicon.svg koyu tarayıcı temasında beyaz kutuya geçer.

- **KARAR (Aşama 5): Token'lar onaylandı.**
  - Semantic token'lar: state-active* = Turkuaz (aktif/devam eden), state-done* = Başarılı yeşili (yalnız kapandı).
  - Koyu temada birincil buton ters: Buz #E8EDF3 zemin + Lacivert metin. Vurgu butonu iki temada Turkuaz + Lacivert metin.
  - Açık temada odak halkası ve aktif sekme çizgisi Turkuaz Koyu (Turkuaz beyazda 2.1:1). Turkuaz yalnız geniş dolguda (state-active-fill).
  - Koyu tema zemini #0A1320, kart Lacivert #0F1B2D. Boşluk 4 px taban, tip ölçeği 12–46 px.

## Açık konular
- Marka tescil araştırması profesyonelce yapılmalı (kütüphane taraması yeterli değil).
- Risk: Sembol 16–32 px'te "S"/"§" ya da senkron ikonu gibi okunabilir.
- Çözüldü (Aşama 6): wordmark outline'a çevrildi; wordmark-oo.svg zaten #0F1B2D idi; kesim seçimi kılavuzda.

## Sıradaki adım
- Proje teslim edildi. İsteğe bağlı: tescil araştırması, sosyal medya şablonları, antetli kâğıt/kartvizit.
