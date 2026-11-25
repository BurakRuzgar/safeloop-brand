# SafeLoop · Marka kiti (Aşama 4)

**Konumlanma:** OSGB'ler ve İSG ekipleri için SafeLoop, her açılan aksiyonu kapanana kadar izleyen İSG yönetim yazılımıdır.

Pano: `marka-kiti-pano.png` (.html) · Lockup panosu: `../../concepts-v2/devir/pano-lockup.png`

## Marka paleti
| Ad | HEX | RGB | Görev | Kontrast |
|---|---|---|---|---|
| Lacivert | #0F1B2D | 15 27 45 | Ana renk: logo, başlık, birincil buton, üst bar | Beyazda 17.3:1 |
| Turkuaz | #1FC7B4 | 31 199 180 | Aksan: vurgu butonu (lacivert yazıyla), aktif sekme, odak, grafik | Lacivertle 8.1:1 · beyazda metin olarak kullanılmaz (2.1:1) |
| Turkuaz Koyu | #0B7C71 | 11 124 113 | Açık zeminde bağlantı ve aksan metni | Beyazda 5.1:1, Kâğıtta 4.7:1 |
| Arduvaz | #566275 | 86 98 117 | İkincil metin, etiket | Beyazda 6.2:1 |
| Çizgi | #DDE3EA | 221 227 234 | Kenarlık, ayraç, boş ilerleme | Metin için değil |
| Kâğıt | #F5F7FA | 245 247 250 | Uygulama arka planı (kartlar beyaz) | Lacivert metin 16.1:1 |

**Aksan gerekçesi:** Turkuaz temiz, dijital ve kurumsal bir his veriyor. İSG sektörünün sarı, turuncu ve kırmızı uyarı dilinden net biçimde ayrışıyor ve lacivertle güçlü kontrast kuruyor. Turkuaz Koyu, aynı tonun açık zeminde okunabilir sürümü.

## Uygulama durum renkleri (yalnız arayüz)
| Durum | Metin/ikon | Zemin | Oran (kendi zemininde) |
|---|---|---|---|
| Başarılı | #1B7741 | #E5F3EA | 4.9:1 |
| Uyarı | #A8570A | #FCF0E1 | 4.6:1 |
| Hata | #C0303C | #FBE9EB | 4.8:1 |

- Uyarı rengi koyu kehribar. Kullanıcı alışkanlığı nedeniyle arayüzde gerekli, ama marka, pazarlama ve logo yüzeylerinde kullanılmaz. Bu yüzden İSG sarısı gibi bir marka rengine dönüşmez.
- Başarılı rengi, Turkuaz'dan ayrışsın diye daha yeşil ve daha koyu seçildi.
- Durum her zaman renk + ikon + metinle gösterilir. Bilgi mesajları için Lacivert ya da Turkuaz Koyu kullanılır; ayrı bir mavi renk eklenmedi.

## Tipografi
- **Başlık:** Plus Jakarta Sans 700/800 (SIL Open Font License, Google Fonts). Yuvarlak, geometrik formları wordmark'ın "o" ve "a" harfleriyle uyumlu.
- **Metin ve arayüz:** Inter 400/500/600 (SIL OFL). Küçük boyutta yüksek okunabilirlik sunuyor, tablo rakamları var.
- İki font da Türkçe karakterlerin tamamını destekliyor (ç ğ ı İ ö ş ü).
- Yedek font sırası: `"Plus Jakarta Sans", Inter, system-ui, sans-serif` / `Inter, system-ui, sans-serif`
- Ölçek: oran 1.25, gövde 15 px → 12 · 15 · 19 · 23 · 29 · 37
- Wordmark bir font değil; özel çizildiği için font lisansı gerekmiyor.

## Logo dosyaları (concepts-v2/devir/)
- Açık zemin: lockup-box.svg · lockup-box-small.svg (≤ 200 px) · wordmark-oo.svg
- Koyu zemin (ters kutu, saydam): lockup-box-ters.svg · lockup-box-ters-small.svg · wordmark-oo-beyaz.svg · icon-box-ters.svg
- İkon/favicon: icon-box.svg (64 px+) · icon-box-small.svg (16–32 px)
- Kutusuz sembol: devir-symbol.svg · devir-small.svg

## Slogan adayı
- **"Her açılan aksiyon kapanır."** Marka özünden geliyor ve kapalı döngü / PDCA fikrini taşıyor. Aday; kesinleşmedi. İngilizce karşılığı ileride değerlendirilecek.

## Renk anlamı (token'lara yansıyacak)
- **Turkuaz** = aktif / devam eden / vurgu (ör. "Çalışmada" adımı, aktif sekme, vurgu butonu).
- **Başarılı yeşili** = yalnız tamamlandı / kapandı durumu.
- İkisi aynı anlamda kullanılmaz: devam eden iş yeşil, kapanmış iş turkuaz gösterilmez.

## Kullanım kuralları
- Ekranda tek bir Turkuaz vurgu butonu olur; birincil eylem Lacivert'tir.
- Logo yalnız Lacivert, Beyaz ya da (koyu zeminde) ters kutu sürümüyle kullanılır.
- Arka plan Kâğıt, kartlar Beyaz olur; renkli kart zemini kullanılmaz.

## Yapılmayacaklar
1. Logoyu Turkuaz, durum renkleri ya da sarı/turuncu tonlarda kullanmak.
2. Turkuaz'ı beyaz zeminde metin ya da ince ikon rengi olarak kullanmak.
3. Durumu yalnız renkle göstermek (ikon ve metin şart).

## Not
- Panodaki ekran görüntüsü çevrimdışı oluşturuldu; Inter ve Plus Jakarta Sans yüklenmediği için sistem fontuyla göründü. HTML'yi tarayıcıda açınca doğru fontlar Google Fonts'tan gelir.
