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

## Yapılmadı
- Aşama 5: Token'lar
- Aşama 6: Teslim

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

## Açık konular
- Marka tescil araştırması profesyonelce yapılmalı (kütüphane taraması yeterli değil).
- Risk: Sembol 16–32 px'te "S"/"§" ya da senkron ikonu gibi okunabilir.
- Wordmark stroke, sembol dolgu; teslimde (Aşama 6) outline'a çevrilecek. wordmark-oo.svg hâlâ #111; Aşama 4 paletiyle güncellenecek.
- Boyuta göre kesim seçimi (≤ 200 px lockup ve 16–32 px ikon → küçük kesim) kılavuza yazılacak.

## Sıradaki adım
- **Aşama 5: Token'lar** (CSS değişkenleri + JSON, açık/koyu tema) → brand/safeloop/tokens/
  - Renk anlamı token'lara yansıyacak:
    - Turkuaz = aktif / devam eden / vurgu.
    - Başarılı yeşili = yalnız tamamlandı / kapandı durumu.
    - İkisi aynı anlamda kullanılmaz.
  - Kapsam: yalnız bu depo; başka proje ya da uygulama koduna dokunulmaz.
- Onay bekleniyor: Aşama 5'e başlamak için.
