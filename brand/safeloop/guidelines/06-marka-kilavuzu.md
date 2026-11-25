# SafeLoop · Marka kılavuzu

**SafeLoop by Rüzgar Safety.** OSGB'ler ve İSG ekipleri için, her açılan aksiyonu kapanana kadar izleyen İSG yönetim yazılımı.
Marka özü: *Her açılan aksiyon kapanır.*

Görsel özet: [`final/teslim-pano.png`](../final/teslim-pano.png)

---

## 1. Logo

**Devir:** İki yarım yay birbirinin üstünden kayarak birleşir. Biri açılır, diğeri kapatır. Bu sürekli iyileştirme döngüsünü (PDCA) anlatır.
Aynı sembol iki yerde kullanılır: köşeleri yuvarlatılmış kutuda (ikon) ve wordmark'ın iki "o" harfinde (safel∘∘p).
Kayma yönü her yerde aynıdır: sol yarı yukarıda, sağ yarı aşağıda.

| Sürüm | Ne zaman |
|---|---|
| **Yatay lockup** (kutu + wordmark) | Varsayılan. Web üst barı, sunum, antetli kâğıt, tabela |
| **Dikey lockup** | Kare ve dikey alanlar: kapak, afiş, giriş ekranı, sosyal medya görseli |
| **İmzalı** ("by Rüzgar Safety") | Kurumsal belge, sözleşme, teklif, web sitesi alt bilgisi, fuar. Uygulama içinde kullanılmaz |
| **Yalnız wordmark** | Dar yatay alanlar: mobil üst bar, e-posta imzası, alt bilgi |
| **Yalnız kutulu sembol** | Uygulama ve PWA ikonu, favicon, sosyal medya avatarı |

Sembol kutusuz kullanılmaz. Kutusuz Devir yalnızca wordmark'ın içinde yer alır.

## 2. Boyuta göre kesim

Sembolün iki kesimi vardır. **Küçük kesimde** kayma ve orta boşluk büyütülmüştür, böylece küçük boyutta form kaybolmaz.

| Dosya | Ana kesim | Küçük kesim | En küçük |
|---|---|---|---|
| Yatay lockup | ≥ 250 px genişlik | 120–249 px | 120 px (altında yalnız sembol) |
| Yatay imzalı | ≥ 320 px | yok | 320 px |
| Dikey lockup | ≥ 200 px genişlik | 80–199 px | 80 px |
| Dikey imzalı | ≥ 200 px | yok | 200 px |
| Wordmark | tek kesim | — | 80 px genişlik |
| Kutulu sembol | ≥ 64 px | 16–63 px | 16 px |

Baskıda: 1 px ≈ 0,26 mm (96 dpi). Yatay lockup için en küçük ölçü 32 mm, imzalı için 85 mm.

## 3. Boş alan ve oranlar

- **Boş alan:** Logonun dört yanında en az **kutu yüksekliğinin yarısı** kadar boşluk bırakılır. Bu ölçü wordmark'ın x-yüksekliğine ("o" harfinin boyu) eşittir. Bu alana metin, görsel ya da kenar giremez.
- Yatay lockup'ta kutunun yüksekliği x-yüksekliğinin 1,94 katıdır. Kutu ile "s" harfi arasındaki boşluk kutunun 0,37'si kadardır.
- Kutunun köşe yarıçapı kenarının %22,5'i, sembol ise kutu yüksekliğinin %66'sıdır.
- Dikey lockup'ta kutu wordmark'ın ortasına hizalanır. Kutu ile harfler arasındaki boşluk kutunun 0,28'i kadardır.
- İmza (Plus Jakarta Sans SemiBold, path'e çevrildi) yatayda "s" harfinin sol kenarına hizalanır, dikeyde ortalanır.

## 4. Renk

| Sürüm | Kutu | Wordmark | İmza | Zemin |
|---|---|---|---|---|
| **renkli** | Lacivert #0F1B2D | Lacivert #0F1B2D | Arduvaz #566275 | Beyaz, Kâğıt #F5F7FA, açık görseller |
| **siyah** | #000000 | #000000 | #000000 | Tek renk baskı, faks, gazete, kabartma, lazer kesim |
| **beyaz** | #FFFFFF (sembol oyuk) | #FFFFFF | #FFFFFF | Lacivert, koyu tema #0A1320, koyu fotoğraf |

- Kutu her sürümde dolu ve sembol oyuktur: zemin rengi sembolün içinden görünür. Beyaz sürüm de bu yüzden ters kutudur.
- Turkuaz #1FC7B4 logoda kullanılmaz. Arayüzde aksan rengidir.
- Palet, kontrast oranları ve durum renkleri: [`marka-kiti/04-marka-kiti.md`](marka-kiti/04-marka-kiti.md)
- Arayüz renkleri, tipografi ve boşluklar (açık/koyu tema) token olarak tanımlıdır: [`../tokens/safeloop.tokens.css`](../tokens/safeloop.tokens.css) · [`../tokens/safeloop.tokens.json`](../tokens/safeloop.tokens.json) · [`../tokens/README.md`](../tokens/README.md)

## 5. Tipografi

- Başlık: **Plus Jakarta Sans** 700/800. Metin ve arayüz: **Inter** 400/500/600. İki font da SIL OFL lisanslı ve Türkçe karakterlerin tamamını destekliyor.
- Wordmark özel çizildi, bir fontla yazılmaz. "safeloop" yazısını fontla yeniden üretmeyin; logo dosyasını kullanın.
- Metin içinde marka adı **SafeLoop** olarak yazılır (S ve L büyük, bitişik). Logo küçük harftir.

## 6. Yapılmayacaklar

- Logoyu döndürmek, eğmek, orantısız ölçeklemek ya da yarıların kayma yönünü değiştirmek.
- Kutu ile wordmark arasındaki oranı ya da boşluğu değiştirmek.
- Sembolü kutusuz, çerçeve içinde ya da daire içinde kullanmak (yalnız PWA'nın daire maskesi istisnadır).
- Paletin dışında bir renk, degrade, gölge ya da kontur eklemek. Turkuaz ya da uyarı renklerini logoda kullanmak.
- Wordmark'taki "o" harflerini düz daire ile değiştirmek ya da wordmark'ı fontla yazmak.
- 16–63 px'te ana kesimi, ≤ 249 px lockup'ta ana kesimi kullanmak.
- Logoyu karışık fotoğrafın üstüne zemin olmadan koymak. Koyu fotoğrafta beyaz sürümü kullanın.
- İSG klişeleriyle (kalkan, onay işareti, baret, uyarı üçgeni) ya da sarı-siyah ile birlikte kullanmak.

## 7. Dosyalar

### Vektör: `final/svg/`
Tüm dosyalar outline'dır (stroke ya da font yoktur). Sınırlar sıkı kırpılmıştır; boş alanı yerleşimde siz bırakın.
Adlandırma: `safeloop-{yatay|dikey|wordmark|sembol}[-kucuk|-imza]-{renkli|siyah|beyaz}.svg`

- Yatay: `safeloop-yatay-*.svg` · küçük kesim: `safeloop-yatay-kucuk-*.svg` · imzalı: `safeloop-yatay-imza-*.svg`
- Dikey: `safeloop-dikey-*.svg` · `safeloop-dikey-kucuk-*.svg` · `safeloop-dikey-imza-*.svg`
- Wordmark: `safeloop-wordmark-*.svg`
- Sembol (kutulu): `safeloop-sembol-*.svg` · `safeloop-sembol-kucuk-*.svg`
- Tam kare (köşesiz lacivert zemin, beyaz sembol): `safeloop-sembol-kare.svg`. Apple ikonu, maskable ikon ve sosyal avatar için.
- `favicon.svg`: küçük kesimdir. Tarayıcı koyu temadaysa kendiliğinden beyaz kutuya geçer.

### Raster: `final/png/`
| Dosya | Kaynak | Kullanım |
|---|---|---|
| `favicon.ico` (16/32/48) | küçük kesim | Eski tarayıcılar |
| `favicon-16.png`, `favicon-32.png` | küçük kesim | Sekme ikonu |
| `apple-touch-icon.png` 180 | tam kare | iOS ana ekran |
| `icon-192.png`, `icon-512.png` | kutulu, saydam köşe | PWA "any" |
| `icon-maskable-512.png` | tam kare | PWA "maskable" (sembol %80 güvenli alanın içinde) |
| `safeloop-{yatay,yatay-imza,wordmark}-*-1200.png` | — | Saydam, 1200 px genişlik |
| `safeloop-{dikey,dikey-imza}-*-800.png` | — | Saydam, 800 px genişlik |
| `site.webmanifest` | — | PWA manifesti (tema rengi Lacivert, arka plan Kâğıt) |

### Web `<head>`
```html
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#0F1B2D">
```

### Üretim
Tek kaynak: `concepts-v2/src/build_devir.py` (geometri) → `final/src/build_final.py` (outline, lockup, SVG) → `final/src/render_final.py` (PNG/ICO, Chrome ile).
İmza fontu: `final/src/fonts/PlusJakartaSans-SemiBold.ttf` (OFL.txt yanında).

## 8. Açık konular
- Marka tescil araştırması bir uzmana yaptırılmalı.
- 16–32 px'te sembolün "S"/"§" ya da senkron ikonu gibi okunma riski var. Küçük kesim bu riski azaltır ama ortadan kaldırmaz.
