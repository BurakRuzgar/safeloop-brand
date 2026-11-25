# SafeLoop · Token'lar (Aşama 5)

- `safeloop.tokens.css`: CSS değişkenleri, önek `--sl-`. Açık tema varsayılan; koyu tema `data-theme="dark"` ya da sistem tercihiyle gelir. `data-theme="light"` sistem koyuyken açık temayı zorlar.
- `safeloop.tokens.json`: W3C DTCG biçimi. Primitive renkler `color.*`, temalar `theme.light|dark.color.*` (referansla).
- `kontrast.md`: semantic çiftlerin WCAG raporu (tümü geçiyor).
- `onizleme.html` / `.png`: açık ve koyu tema yan yana.
- Kaynak: `src/build_tokens.py`. Dosyalar elle düzenlenmez; değişiklik üreticide yapılır, sonra `python build_tokens.py` çalıştırılır.

## Kurallar
- Bileşenler yalnız `--sl-color-*` semantic token'larını kullanır. Primitive renkler (`--sl-lacivert` vb.) doğrudan kullanılmaz.
- **Aktif / devam eden:** `state-active*` (Turkuaz ailesi). **Kapandı:** `state-done*` (Başarılı yeşili). İkisi birbirinin yerine kullanılmaz.
- Birincil eylem: açıkta Lacivert buton; koyuda açık (Buz) buton ve Lacivert metin. Bu, logonun ters kutu mantığıyla aynı.
- Vurgu butonu (`action-accent`) iki temada da Turkuaz zemin + Lacivert metin. Ekranda tek olur.

## Aşama 4'ten sapmalar (erişilebilirlik)
- Açık temada odak halkası ve aktif sekme çizgisi Turkuaz Koyu (#0B7C71). Turkuaz beyazda 2.1:1 kalıyor, 3:1 şartını karşılamıyor. Turkuaz yalnız geniş dolguda kullanılır (`state-active-fill`: ilerleme çubuğu, grafik alanı; yanında metin şart).
- Yeni türetilmiş tonlar: koyu zeminler (#0A1320, #17263B, #22344D), koyu tema metinleri (#E8EDF3, #A3AEBD, #7D8A9D), koyu tema durum renkleri, aktif etiket zemini #E8F6F4. Hepsi `src/build_tokens.py` içinde açıklamalı.
- Tip ölçeğine 46 px (`3xl`) eklendi (1.25 oranının bir sonraki adımı).
