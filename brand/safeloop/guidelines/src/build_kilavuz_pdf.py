"""SafeLoop marka kılavuzu PDF'i: 04-marka-kiti.md + 06-marka-kilavuzu.md tek belgede.
Logolar final/svg/ dosyalarından satır içine gömülür. Çıktı: guidelines/SafeLoop-Marka-Kilavuzu.pdf
"""
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
SVG = os.path.join(ROOT, "final", "svg")
OUT_HTML = os.path.join(HERE, "kilavuz.html")
OUT_PDF = os.path.join(ROOT, "guidelines", "SafeLoop-Marka-Kilavuzu.pdf")
FONT = os.path.join(ROOT, "final", "src", "fonts", "PlusJakartaSans-SemiBold.ttf").replace("\\", "/")
CHROME = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
          r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]


def logo(name, width=None, height=None, style="", recolor=None):
    s = open(os.path.join(SVG, name), encoding="utf-8").read()
    s = re.sub(r"<title>.*?</title>\n?", "", s)
    s = re.sub(r'\swidth="[\d.]+" height="[\d.]+"', "", s, count=1)
    if recolor:
        for a, b in recolor.items():
            s = s.replace(a, b)
    size = (f"width:{width}px;" if width else "") + (f"height:{height}px;" if height else "")
    return s.replace("<svg ", f'<svg style="display:block;{size}{style}" ', 1)


def devir_bare(col, w):
    """Kutusuz Devir (yalnız 'yapılmayacak' örneği için)."""
    import sys
    sys.dont_write_bytecode = True
    sys.path.insert(0, os.path.join(ROOT, "concepts-v2", "src"))
    import build_devir as D
    return (f'<svg viewBox="20 10 216 236" style="display:block;width:{w}px"><path fill="{col}" '
            f'd="{D.devir_d(128, 128, **D.MAIN)}"/></svg>')


PALETTE = [
    ("Lacivert", "#0F1B2D", "15 27 45", "Ana renk: logo, başlık, birincil buton, üst bar", "Beyazda 17.3:1", "#fff"),
    ("Turkuaz", "#1FC7B4", "31 199 180", "Aksan: vurgu butonu (lacivert yazıyla), aktif sekme, odak, grafik",
     "Lacivertle 8.1:1 · beyazda metin olarak kullanılmaz (2.1:1)", "#0F1B2D"),
    ("Turkuaz Koyu", "#0B7C71", "11 124 113", "Açık zeminde bağlantı ve aksan metni", "Beyazda 5.1:1, Kâğıtta 4.7:1", "#fff"),
    ("Arduvaz", "#566275", "86 98 117", "İkincil metin, etiket, imza", "Beyazda 6.2:1", "#fff"),
    ("Çizgi", "#DDE3EA", "221 227 234", "Kenarlık, ayraç, boş ilerleme", "Metin için değil", "#0F1B2D"),
    ("Kâğıt", "#F5F7FA", "245 247 250", "Uygulama arka planı (kartlar beyaz)", "Lacivert metin 16.1:1", "#0F1B2D"),
]
STATUS = [("Başarılı", "#1B7741", "#E5F3EA", "4.9:1", "Tamamlandı"),
          ("Uyarı", "#A8570A", "#FCF0E1", "4.6:1", "Süresi yaklaşıyor"),
          ("Hata", "#C0303C", "#FBE9EB", "4.8:1", "Gecikti")]

CSS = f"""
@font-face{{font-family:"PJS Local";src:url("file:///{FONT}");font-weight:600}}
@page{{size:A4;margin:0}}
*{{box-sizing:border-box}}
html,body{{margin:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font:10pt/1.5 Inter,system-ui,sans-serif;color:#0F1B2D}}
h1,h2,h3,.disp{{font-family:"Plus Jakarta Sans","PJS Local",Inter,sans-serif}}
.page{{width:210mm;height:297mm;padding:18mm 18mm 16mm;position:relative;page-break-after:always;overflow:hidden;background:#fff}}
.compact h2{{margin-top:4.5mm}} .compact pre{{margin-bottom:2mm}}
.page:last-child{{page-break-after:auto}}
.foot{{position:absolute;left:18mm;right:18mm;bottom:9mm;display:flex;justify-content:space-between;font-size:7.5pt;color:#566275;border-top:1px solid #DDE3EA;padding-top:2.5mm}}
.kicker{{font:600 7.5pt Inter,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#0B7C71;margin:0 0 2mm}}
h1{{font-size:24pt;font-weight:800;margin:0 0 5mm;line-height:1.15}}
h2{{font-size:12.5pt;font-weight:700;margin:7mm 0 2.5mm}}
h3{{font-size:10pt;font-weight:700;margin:0 0 1.5mm}}
p{{margin:0 0 2.5mm}} .lead{{font-size:11.5pt;line-height:1.45;max-width:150mm}}
.muted{{color:#566275}} .small{{font-size:8pt}}
table{{border-collapse:collapse;width:100%;font-size:8.6pt;margin:1mm 0 3mm}}
th{{text-align:left;font-weight:600;color:#566275;border-bottom:1.5px solid #0F1B2D;padding:1.6mm 2mm 1.6mm 0}}
td{{border-bottom:1px solid #DDE3EA;padding:1.8mm 2mm 1.8mm 0;vertical-align:top}}
code{{font:8.2pt/1.45 Consolas,"Cascadia Mono",monospace;background:#F5F7FA;padding:.3mm 1mm;border-radius:1mm}}
pre{{font:8.2pt/1.5 Consolas,"Cascadia Mono",monospace;background:#0F1B2D;color:#E8EDF3;padding:4mm;border-radius:2mm;margin:1mm 0 3mm;white-space:pre-wrap}}
ul{{margin:0 0 3mm;padding-left:4.5mm}} li{{margin:0 0 1.2mm}}
.grid{{display:grid;gap:4mm}} .g2{{grid-template-columns:repeat(2,minmax(0,1fr))}} .g3{{grid-template-columns:repeat(3,minmax(0,1fr))}} .g4{{grid-template-columns:repeat(4,minmax(0,1fr))}}
svg{{max-width:100%}}
.tight td{{padding:1.1mm 2mm 1.1mm 0}} .tight th{{padding:1.1mm 2mm 1.1mm 0}}
.tile{{border-radius:2.5mm;padding:6mm;display:flex;flex-direction:column;justify-content:space-between;gap:4mm}}
.paper{{background:#F5F7FA}} .white{{background:#fff;border:1px solid #DDE3EA}} .navy{{background:#0F1B2D;color:#E8EDF3}}
.cap{{font-size:7.8pt;color:#566275}} .navy .cap{{color:#A9B4C3}}
.center{{display:flex;align-items:center;justify-content:center}}
.cover{{background:#0F1B2D;color:#fff;padding:0}}
.no{{position:relative}} .no:after{{content:"";position:absolute;inset:0;background:
 linear-gradient(to top right,transparent calc(50% - .6px),#C0303C calc(50% - .6px),#C0303C calc(50% + .6px),transparent calc(50% + .6px))}}
.x{{color:#C0303C;font-weight:600}}
.sw{{border-radius:2.5mm;overflow:hidden;border:1px solid #DDE3EA}}
.sw .c{{height:24mm;padding:3mm;display:flex;align-items:flex-end;font:700 10pt "Plus Jakarta Sans","PJS Local",sans-serif}}
.sw .m{{padding:3mm;font-size:7.8pt;line-height:1.45}}
"""


def foot(n):
    return f'<div class="foot"><span>SafeLoop · Marka kılavuzu · v1.0</span><span>{n}</span></div>'


def page(n, body, cls=""):
    return f'<section class="page {cls}">{body}{foot(n) if n else ""}</section>'


pages = []

# 1 — kapak
pages.append(page(0, f"""
<div style="height:100%;display:flex;flex-direction:column;justify-content:space-between;padding:22mm 20mm 18mm">
 <div class="small" style="letter-spacing:.14em;text-transform:uppercase;color:#1FC7B4;font-weight:600">Marka kılavuzu · v1.0</div>
 <div>{logo("safeloop-yatay-imza-beyaz.svg", width=470)}
  <p class="disp" style="font-size:20pt;font-weight:700;margin:16mm 0 0;line-height:1.25;color:#fff">Her açılan aksiyon kapanır.</p></div>
 <div class="small" style="color:#A9B4C3;display:flex;justify-content:space-between">
  <span>Logo · renk · tipografi · kullanım · dosyalar</span><span>Kasım 2026</span></div>
</div>""", "cover"))

# 2 — marka
pages.append(page(2, f"""
<p class="kicker">01 · Marka</p><h1>SafeLoop by Rüzgar Safety</h1>
<p class="lead">OSGB'ler ve İSG ekipleri için SafeLoop, her açılan aksiyonu kapanana kadar izleyen İSG yönetim yazılımıdır.
İş izinleri, düzeltici faaliyetler, saha bildirimleri, kaza ve ramak kala kayıtları ile JSA tek bir kapalı döngüde yönetilir.</p>
<div class="grid g3" style="margin:6mm 0 2mm">
 <div class="tile paper"><div class="cap">Marka özü</div><div class="disp" style="font-size:13pt;font-weight:700;line-height:1.3">Her açılan aksiyon kapanır.</div></div>
 <div class="tile paper"><div class="cap">Kişilik</div><div style="font-weight:600">Sistematik · güvenilir · kesintisiz · modern · kurumsal</div></div>
 <div class="tile paper"><div class="cap">Kitle</div><div style="font-weight:600">OSGB'ler; inşaat, maden ve imalat şirketleri; İSG uzmanları</div></div>
</div>
<h2>Logo fikri: Devir</h2>
<div class="grid g2" style="align-items:center;grid-template-columns:62mm 1fr">
 <div class="tile paper center" style="height:62mm">{logo("safeloop-sembol-renkli.svg", width=150)}</div>
 <div><p>İki yarım yay birbirinin üstünden kayarak birleşir. Biri açılır, diğeri kapatır. Bu, sürekli iyileştirme döngüsünü (PDCA) ve kapanan aksiyonu anlatır.</p>
 <p>Aynı sembol iki yerde kullanılır: köşeleri yuvarlatılmış kutuda (ikon) ve wordmark'ın iki "o" harfinde (safel∘∘p).
 Kayma yönü her yerde aynıdır: <b>sol yarı yukarıda, sağ yarı aşağıda.</b></p>
 <p class="muted">İSG klişeleri (kalkan, onay işareti, baret, uyarı üçgeni) ve sarı-siyah bilinçli olarak kullanılmaz.</p></div>
</div>
<div class="tile white center" style="margin-top:6mm;height:42mm">{logo("safeloop-wordmark-renkli.svg", width=330)}</div>
<p class="cap" style="margin-top:2mm">Wordmark özel çizildi; bir fontla yazılmaz. Metin içinde marka adı <b>SafeLoop</b> olarak yazılır.</p>
"""))

# 3 — sürümler
pages.append(page(3, f"""
<p class="kicker">02 · Logo</p><h1>Logo sürümleri</h1>
<div class="grid g2">
 <div class="tile white" style="height:57mm"><div class="center" style="flex:1">{logo("safeloop-yatay-renkli.svg", width=270)}</div>
  <div><h3>Yatay lockup · varsayılan</h3><div class="cap">Web üst barı, sunum, antetli kâğıt, tabela</div></div></div>
 <div class="tile white" style="height:57mm"><div class="center" style="flex:1">{logo("safeloop-dikey-renkli.svg", height=105)}</div>
  <div><h3>Dikey lockup</h3><div class="cap">Kapak, afiş, giriş ekranı, sosyal medya görseli</div></div></div>
 <div class="tile white" style="height:57mm"><div class="center" style="flex:1">{logo("safeloop-yatay-imza-renkli.svg", width=270)}</div>
  <div><h3>İmzalı · "by Rüzgar Safety"</h3><div class="cap">Kurumsal belge, sözleşme, teklif, site alt bilgisi, fuar. Uygulamaların giriş ekranında kullanılabilir; uygulama içinde kullanılmaz.</div></div></div>
 <div class="tile white" style="height:57mm"><div class="center" style="flex:1">{logo("safeloop-dikey-imza-renkli.svg", height=108)}</div>
  <div><h3>Dikey imzalı</h3><div class="cap">Kapak ve afişte kurumsal imza gerektiğinde</div></div></div>
 <div class="tile white" style="height:46mm"><div class="center" style="flex:1">{logo("safeloop-wordmark-renkli.svg", width=200)}</div>
  <div><h3>Yalnız wordmark</h3><div class="cap">Dar yatay alanlar: mobil üst bar, e-posta imzası, alt bilgi</div></div></div>
 <div class="tile white" style="height:44mm"><div class="center" style="flex:1;gap:7mm">{logo("safeloop-sembol-renkli.svg", width=64)}{logo("safeloop-sembol-kucuk-renkli.svg", width=32)}{logo("safeloop-sembol-kucuk-renkli.svg", width=16)}</div>
  <div><h3>Yalnız kutulu sembol</h3><div class="cap">Uygulama ve PWA ikonu, favicon, sosyal medya avatarı</div></div></div>
</div>
<p class="small muted" style="margin-top:4mm">Sembol kutusuz kullanılmaz. Kutusuz Devir yalnız wordmark'ın içinde yer alır.</p>
"""))

# 4 — kesim, boş alan
W = 300                      # boş alan çiziminde lockup genişliği (px)
k = W / 666
clear = 62 * k
pages.append(page(4, f"""
<p class="kicker">02 · Logo</p><h1>Boyut, kesim ve boş alan</h1>
<p>Sembolün iki kesimi vardır. <b>Küçük kesimde</b> kayma ve orta boşluk büyütülmüştür, böylece küçük boyutta form kaybolmaz.</p>
<div class="grid g2" style="margin:4mm 0">
 <div class="tile paper"><div class="center" style="gap:5mm;align-items:flex-end;flex:1">
  {logo("safeloop-sembol-renkli.svg", width=96)}{logo("safeloop-sembol-renkli.svg", width=64)}</div>
  <div class="cap"><b>Ana kesim</b> · 64 px ve üstü · lockup ≥ 250 px</div></div>
 <div class="tile paper"><div class="center" style="gap:5mm;align-items:flex-end;flex:1">
  {logo("safeloop-sembol-kucuk-renkli.svg", width=48)}{logo("safeloop-sembol-kucuk-renkli.svg", width=32)}{logo("safeloop-sembol-kucuk-renkli.svg", width=16)}</div>
  <div class="cap"><b>Küçük kesim</b> · 16–63 px · lockup 120–249 px</div></div>
</div>
<table><tr><th>Dosya</th><th>Ana kesim</th><th>Küçük kesim</th><th>En küçük</th></tr>
<tr><td>Yatay lockup</td><td>≥ 250 px genişlik</td><td>120–249 px</td><td>120 px (altında yalnız sembol)</td></tr>
<tr><td>Yatay imzalı</td><td>≥ 320 px</td><td>yok</td><td>320 px</td></tr>
<tr><td>Dikey lockup</td><td>≥ 200 px genişlik</td><td>80–199 px</td><td>80 px</td></tr>
<tr><td>Dikey imzalı</td><td>≥ 200 px</td><td>yok</td><td>200 px</td></tr>
<tr><td>Wordmark</td><td>tek kesim</td><td>—</td><td>80 px genişlik</td></tr>
<tr><td>Kutulu sembol</td><td>≥ 64 px</td><td>16–63 px</td><td>16 px</td></tr></table>
<p class="small muted">Baskıda 1 px ≈ 0,26 mm (96 dpi). Yatay lockup en az 32 mm, imzalı sürüm en az 85 mm.</p>
<h2>Boş alan</h2>
<div class="grid" style="grid-template-columns:auto 1fr;gap:8mm;align-items:center">
 <div style="padding:{clear:.1f}px;background:repeating-linear-gradient(45deg,#E6F7F5 0 4px,#fff 4px 8px);outline:1px dashed #0B7C71;position:relative">
  <div style="background:#fff">{logo("safeloop-yatay-renkli.svg", width=W)}</div>
  <div style="position:absolute;top:0;left:{clear+12:.1f}px;width:{clear:.1f}px;height:{clear:.1f}px;display:flex;align-items:center;justify-content:center;font:700 9pt 'Plus Jakarta Sans','PJS Local';color:#0B7C71">x</div>
 </div>
 <div><p><b>x = kutu yüksekliğinin yarısı</b> (wordmark'ın x-yüksekliğine, yani "o" harfinin boyuna eşit).</p>
 <p>Logonun dört yanında en az x kadar boşluk kalır. Bu alana metin, görsel ya da kenar giremez.</p></div>
</div>
<h2>Oranlar</h2>
<ul class="small">
<li>Yatay lockup'ta kutu yüksekliği x-yüksekliğinin 1,94 katı; kutu ile "s" arası kutunun 0,37'si.</li>
<li>Kutunun köşe yarıçapı kenarın %22,5'i; sembol kutu yüksekliğinin %66'sı.</li>
<li>Dikey lockup'ta kutu wordmark'a ortalanır; kutu ile harfler arası kutunun 0,28'i.</li>
<li>İmza (Plus Jakarta Sans SemiBold, path'e çevrildi) yatayda "s"nin sol kenarına hizalı, dikeyde ortalı.</li></ul>
"""))

# 5 — renk sürümleri
pages.append(page(5, f"""
<p class="kicker">02 · Logo</p><h1>Logo renk sürümleri</h1>
<div class="grid g3">
 <div class="tile white" style="height:44mm"><div class="center" style="flex:1">{logo("safeloop-yatay-renkli.svg", width=165)}</div><div class="cap"><b>renkli</b> · beyaz ve Kâğıt zemin</div></div>
 <div class="tile white" style="height:44mm"><div class="center" style="flex:1">{logo("safeloop-yatay-siyah.svg", width=165)}</div><div class="cap"><b>siyah</b> · tek renk baskı</div></div>
 <div class="tile navy" style="height:44mm"><div class="center" style="flex:1">{logo("safeloop-yatay-beyaz.svg", width=165)}</div><div class="cap"><b>beyaz</b> · koyu zemin, ters kutu</div></div>
 <div class="tile paper" style="height:44mm"><div class="center" style="flex:1">{logo("safeloop-yatay-imza-renkli.svg", width=165)}</div><div class="cap">Kâğıt #F5F7FA</div></div>
 <div class="tile" style="height:44mm;background:#0A1320"><div class="center" style="flex:1">{logo("safeloop-yatay-imza-beyaz.svg", width=165)}</div><div class="cap" style="color:#A9B4C3">Koyu tema #0A1320</div></div>
 <div class="tile white" style="height:44mm"><div class="center" style="flex:1">{logo("safeloop-yatay-imza-siyah.svg", width=165)}</div><div class="cap">İmzalı siyah · tek renk baskı</div></div>
</div>
<table style="margin-top:6mm"><tr><th>Sürüm</th><th>Kutu</th><th>Wordmark</th><th>İmza</th><th>Zemin</th></tr>
<tr><td><b>renkli</b></td><td>Lacivert #0F1B2D</td><td>Lacivert #0F1B2D</td><td>Arduvaz #566275</td><td>Beyaz, Kâğıt, açık görseller</td></tr>
<tr><td><b>siyah</b></td><td>#000000</td><td>#000000</td><td>#000000</td><td>Tek renk baskı, gazete, kabartma, lazer kesim</td></tr>
<tr><td><b>beyaz</b></td><td>#FFFFFF (sembol oyuk)</td><td>#FFFFFF</td><td>#FFFFFF</td><td>Lacivert, koyu tema, koyu fotoğraf</td></tr></table>
<ul class="small">
<li>Kutu her sürümde dolu, sembol oyuktur: zemin rengi sembolün içinden görünür. Beyaz sürüm bu yüzden ters kutudur.</li>
<li>Logo yalnız Lacivert, siyah ya da beyaz (ters kutu) kullanılır. Turkuaz ve durum renkleri logoda kullanılmaz.</li></ul>
"""))

# 6 — palet
sw = "".join(f"""<div class="sw"><div class="c" style="background:{h};color:{t}">{n}</div>
<div class="m"><b>{h}</b> · RGB {r}<br>{g}<br><span class="muted">{c}</span></div></div>""" for n, h, r, g, c, t in PALETTE)
st = "".join(f"""<div class="sw"><div class="m" style="background:{bg};color:{fg};display:flex;gap:2mm;align-items:center;font-weight:600;font-size:9pt">
<span style="width:3mm;height:3mm;border-radius:50%;background:{fg}"></span>{label}</div>
<div class="m"><b>{n}</b> · metin {fg} · zemin {bg}<br><span class="muted">Kendi zemininde {ratio}</span></div></div>""" for n, fg, bg, ratio, label in STATUS)
pages.append(page(6, f"""
<p class="kicker">03 · Renk</p><h1>Marka paleti</h1>
<div class="grid g3">{sw}</div>
<p class="small" style="margin-top:3mm"><b>Aksan gerekçesi:</b> Turkuaz temiz, dijital ve kurumsal bir his veriyor. İSG sektörünün sarı, turuncu ve kırmızı uyarı dilinden net biçimde ayrışıyor ve lacivertle güçlü kontrast kuruyor. Turkuaz Koyu, aynı tonun açık zeminde okunabilir sürümü.</p>
<h2>Uygulama durum renkleri (yalnız arayüz)</h2>
<div class="grid g3">{st}</div>
<ul class="small" style="margin-top:3mm">
<li>Uyarı rengi koyu kehribardır. Arayüzde gereklidir ama marka, pazarlama ve logo yüzeylerinde kullanılmaz; İSG sarısı gibi bir marka rengine dönüşmez.</li>
<li>Durum her zaman renk + ikon + metinle gösterilir. Bilgi mesajları için Lacivert ya da Turkuaz Koyu kullanılır.</li></ul>
<h2>Renk anlamı</h2>
<div class="grid g2">
 <div class="tile paper" style="flex-direction:row;align-items:center;gap:4mm;justify-content:flex-start"><span style="width:9mm;height:9mm;border-radius:2mm;background:#1FC7B4;flex:none"></span>
  <div><b>Turkuaz = aktif / devam eden / vurgu</b><div class="cap">"Çalışmada" adımı, aktif sekme, vurgu butonu</div></div></div>
 <div class="tile paper" style="flex-direction:row;align-items:center;gap:4mm;justify-content:flex-start"><span style="width:9mm;height:9mm;border-radius:2mm;background:#1B7741;flex:none"></span>
  <div><b>Başarılı yeşili = yalnız tamamlandı / kapandı</b><div class="cap">Devam eden iş yeşil, kapanmış iş turkuaz gösterilmez</div></div></div>
</div>
"""))

# 7 — tipografi
scale = "".join(f'<div style="display:flex;align-items:baseline;gap:5mm;border-bottom:1px solid #DDE3EA;padding:1.5mm 0">'
                f'<span class="cap" style="width:12mm">{s} px</span><span class="disp" style="font-size:{s}px;font-weight:{w};line-height:1.2">{t}</span></div>'
                for s, w, t in [(37, 800, "İş izni kapandı"), (29, 700, "Düzeltici faaliyetler"), (23, 700, "Saha bildirimleri"),
                                (19, 700, "Kök neden analizi"), (15, 500, "Gövde metni · Inter 15 px"), (12, 500, "Etiket · Inter 12 px")])
pages.append(page(7, f"""
<p class="kicker">04 · Tipografi</p><h1>Tipografi</h1>
<div class="grid g2">
 <div class="tile paper"><div class="cap">Başlık</div>
  <div class="disp" style="font-size:30pt;font-weight:800;line-height:1.1">Plus Jakarta Sans</div>
  <div class="disp" style="font-size:13pt;font-weight:700">Aa Bb Çç Ğğ Iı İi Öö Şş Üü 0123456789</div>
  <div class="cap">700 / 800 · SIL Open Font License · Google Fonts. Yuvarlak, geometrik formları wordmark'ın "o" ve "a" harfleriyle uyumlu.</div></div>
 <div class="tile paper"><div class="cap">Metin ve arayüz</div>
  <div style="font-size:30pt;font-weight:600;line-height:1.1;letter-spacing:-.01em">Inter</div>
  <div style="font-size:13pt;font-weight:500">Aa Bb Çç Ğğ Iı İi Öö Şş Üü 0123456789</div>
  <div class="cap">400 / 500 / 600 · SIL OFL. Küçük boyutta yüksek okunabilirlik, tablo rakamları.</div></div>
</div>
<h2>Ölçek · oran 1.25, gövde 15 px</h2>
{scale}
<h2>Yedek font sırası</h2>
<p><code>"Plus Jakarta Sans", Inter, system-ui, sans-serif</code> · <code>Inter, system-ui, sans-serif</code></p>
<p class="small muted">İki font da Türkçe karakterlerin tamamını destekliyor. Wordmark özel çizildiği için font lisansı gerekmez; "safeloop" yazısı fontla yeniden üretilmez.</p>
"""))

# 8 — kullanım ve yapılmayacaklar
L = lambda **kw: logo("safeloop-yatay-renkli.svg", width=118, **kw)
dont = [
    (L(style="transform:rotate(-12deg)"), "Döndürmek ya da eğmek"),
    (L(style="transform:scaleX(1.3);transform-origin:center"), "Orantısız ölçeklemek"),
    (L(recolor={"#0F1B2D": "#1FC7B4"}), "Turkuaz ya da durum renkleriyle boyamak"),
    (L(recolor={'fill="#0F1B2D"': 'fill="#0F1B2D" style="filter:drop-shadow(3px 3px 2px rgba(0,0,0,.45))"'}), "Gölge, degrade, kontur eklemek"),
    (f'<div style="display:flex;align-items:center;gap:10px">{devir_bare("#0F1B2D", 26)}{logo("safeloop-wordmark-renkli.svg", width=88)}</div>', "Sembolü kutusuz kullanmak"),
    (f'<div style="background:#F2C200;padding:10px">{logo("safeloop-yatay-siyah.svg", width=104)}</div>', "Sarı-siyah ya da İSG klişeleriyle"),
    (f'<div style="background:linear-gradient(120deg,#8aa 0,#d9c7a0 30%,#567 55%,#e3e0d6 80%);padding:8px">{logo("safeloop-yatay-renkli.svg", width=104)}</div>', "Karışık görselin üstünde zeminsiz"),
    (logo("safeloop-yatay-renkli.svg", width=118).replace('A27.9,27.9', 'A2,2'), "Kutunun köşe ya da oranını değiştirmek"),
]
dt = "".join(f'<div class="tile white" style="height:38mm;padding:4mm"><div class="center no" style="flex:1">{h}</div>'
             f'<div class="cap"><span class="x">✕</span> {t}</div></div>' for h, t in dont)
pages.append(page(8, f"""
<p class="kicker">05 · Kullanım</p><h1>Kullanım kuralları</h1>
<ul>
<li>Geniş alanlarda kutulu sembol + wordmark; dar alanlarda yalnız wordmark; ikon ve favicon'da yalnız kutulu sembol.</li>
<li>Ekranda tek bir Turkuaz vurgu butonu olur; birincil eylem Lacivert'tir.</li>
<li>Arka plan Kâğıt, kartlar Beyaz olur; renkli kart zemini kullanılmaz.</li>
<li>Turkuaz beyaz zeminde metin ya da ince ikon rengi olarak kullanılmaz; açık zeminde metin için Turkuaz Koyu kullanılır.</li>
<li>16–63 px'te ve 249 px'e kadar lockup'ta küçük kesim kullanılır.</li></ul>
<h2>Yapılmayacaklar</h2>
<div class="grid g4" style="gap:3mm">{dt}</div>
<p class="small muted" style="margin-top:3mm">Ayrıca: yarıların kayma yönünü değiştirmek, kutu ile wordmark arasındaki boşluğu değiştirmek, wordmark'taki "o" harflerini düz daireyle değiştirmek ya da wordmark'ı fontla yazmak.</p>
"""))

# 9 — dosyalar
pages.append(page(9, """
<p class="kicker">06 · Dosyalar</p><h1>Dosyalar ve web ikonları</h1>
<p>Vektör dosyalar <code>final/svg/</code> klasöründedir. Hepsi outline'dır (stroke ya da font yoktur) ve sıkı kırpılmıştır; boş alanı yerleşimde siz bırakın.</p>
<p>Adlandırma: <code>safeloop-{yatay|dikey|wordmark|sembol}[-kucuk|-imza]-{renkli|siyah|beyaz}.svg</code></p>
<table class="tight"><tr><th>Dosya</th><th>İçerik</th></tr>
<tr><td><code>safeloop-yatay-*.svg</code></td><td>Yatay lockup · <code>-kucuk</code> küçük kesim · <code>-imza</code> imzalı</td></tr>
<tr><td><code>safeloop-dikey-*.svg</code></td><td>Dikey lockup · <code>-kucuk</code> · <code>-imza</code></td></tr>
<tr><td><code>safeloop-wordmark-*.svg</code></td><td>Yalnız wordmark</td></tr>
<tr><td><code>safeloop-sembol-*.svg</code></td><td>Kutulu sembol · <code>-kucuk</code> 16–63 px için</td></tr>
<tr><td><code>safeloop-sembol-kare.svg</code></td><td>Köşesiz lacivert kare + beyaz sembol: Apple ikonu, maskable ikon, sosyal avatar</td></tr>
<tr><td><code>favicon.svg</code></td><td>Küçük kesim; tarayıcı koyu temadaysa beyaz kutuya geçer</td></tr></table>
<h2>Raster · final/png/</h2>
<table class="tight"><tr><th>Dosya</th><th>Kaynak</th><th>Kullanım</th></tr>
<tr><td><code>favicon.ico</code> (16/32/48)</td><td>küçük kesim</td><td>Eski tarayıcılar</td></tr>
<tr><td><code>favicon-16.png</code>, <code>favicon-32.png</code></td><td>küçük kesim</td><td>Sekme ikonu</td></tr>
<tr><td><code>apple-touch-icon.png</code> 180</td><td>tam kare</td><td>iOS ana ekran</td></tr>
<tr><td><code>icon-192.png</code>, <code>icon-512.png</code></td><td>kutulu, saydam köşe</td><td>PWA "any"</td></tr>
<tr><td><code>icon-maskable-512.png</code></td><td>tam kare</td><td>PWA "maskable" (sembol %80 güvenli alanda)</td></tr>
<tr><td><code>safeloop-*-1200.png</code> / <code>-800.png</code></td><td>lockup'lar</td><td>Saydam; yatay/wordmark 1200 px, dikey 800 px</td></tr>
<tr><td><code>site.webmanifest</code></td><td>—</td><td>PWA manifesti (tema Lacivert, arka plan Kâğıt)</td></tr></table>
<h2>Web &lt;head&gt;</h2>
<pre>&lt;link rel="icon" href="/favicon.ico" sizes="48x48"&gt;
&lt;link rel="icon" href="/favicon.svg" type="image/svg+xml"&gt;
&lt;link rel="apple-touch-icon" href="/apple-touch-icon.png"&gt;
&lt;link rel="manifest" href="/site.webmanifest"&gt;
&lt;meta name="theme-color" content="#0F1B2D"&gt;</pre>
<h2>Tasarım token'ları</h2>
<p class="small">Arayüz renkleri, tipografi ve boşluklar açık/koyu tema için token olarak tanımlıdır: <code>tokens/safeloop.tokens.css</code> (<code>--sl-</code> önekli) ve <code>tokens/safeloop.tokens.json</code> (W3C DTCG). Kontrast tablosu: <code>tokens/kontrast.md</code>.</p>
<h2>Açık konular</h2>
<ul class="small"><li>Marka tescil araştırması bir uzmana yaptırılmalı.</li>
<li>16–32 px'te sembolün "S"/"§" ya da senkron ikonu gibi okunma riski var; küçük kesim bu riski azaltır.</li>
<li>Slogan "Her açılan aksiyon kapanır." aday; İngilizce karşılığı ileride değerlendirilecek.</li></ul>
""", "compact"))

html = f"""<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>SafeLoop Marka Kılavuzu</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=block" rel="stylesheet">
<style>{CSS}</style></head><body>{"".join(pages)}</body></html>"""
open(OUT_HTML, "w", encoding="utf-8").write(html)

chrome = next(p for p in CHROME if os.path.exists(p))
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                "--virtual-time-budget=15000", f"--print-to-pdf={OUT_PDF}", "file:///" + OUT_HTML.replace("\\", "/")],
               check=True, capture_output=True)
print("ok", OUT_PDF, os.path.getsize(OUT_PDF))
