"""SafeLoop Aşama 2 konseptleri: elle kurulmuş geometrik SVG üretir (siyah, greyscale).
Çalıştır: python build_concepts.py  -> ../ altına SVG yazar.
Not: konsept aşamasında çizgiler stroke olarak duruyor; final aşamasında outline'a çevrilecek."""
import math, os

OUT = os.path.join(os.path.dirname(__file__), "..")
INK = "#111111"


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" '
            f'overflow="visible" role="img" aria-labelledby="t"><title id="t">{title}</title>\n{body}\n</svg>\n')


def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)  # ekran açısı: 0=doğu, 90=güney


def arc(cx, cy, r, a0, a1, sweep):
    """a0'dan a1'e yay. sweep=1 saat yönü (ekranda)."""
    x0, y0 = pt(cx, cy, r, a0)
    x1, y1 = pt(cx, cy, r, a1)
    span = (a1 - a0) % 360 if sweep else (a0 - a1) % 360
    large = 1 if span > 180 else 0
    return f"M{x0:.2f} {y0:.2f} A{r:g} {r:g} 0 {large} {sweep} {x1:.2f} {y1:.2f}"


def stroke(d, w, cap="butt", join="round"):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w:g}" '
            f'stroke-linecap="{cap}" stroke-linejoin="{join}"/>')


# ---------------- Semboller (256x256) ----------------

def sym_a():
    """A: Kapanan Halka. Halka r=84, kalınlık 36; sağ üstte boşluğa oturan düğüm (d=44)."""
    cx = cy = 128; r = 84; w = 36; node = 22; gap = 12
    half = math.degrees((node + gap) / r)
    a_node = -45
    ring = arc(cx, cy, r, a_node + half, a_node - half + 360, 1)
    nx, ny = pt(cx, cy, r, a_node)
    return stroke(ring, w) + f'\n<circle cx="{nx:.2f}" cy="{ny:.2f}" r="{node}" fill="{INK}"/>'


def sym_b():
    """B: Sonsuz S. Üst üste iki daire (r=46), 270°'lik iki yay: S kendi içine kıvrılır."""
    w = 34; r = 46; cx = 128
    c1 = 128 - r; c2 = 128 + r
    k = 28  # uçlar omurgaya doğru kıvrılır: S neredeyse kapanıp 8 olur
    top = arc(cx, c1, r, k, 90, 0)          # sağ-alt -> kuzey -> batı -> güney (saat tersi)
    bot = arc(cx, c2, r, -90, 180 + k, 1).split(" A", 1)[1]  # kuzey -> doğu -> güney -> sol-üst
    return stroke(top + " A" + bot, w)


def sym_d():
    """D: L-Döngü. Yuvarlak köşeli kare döngü; tek keskin köşe (sol-alt) L'yi verir, üstte tek boşluk."""
    w = 36; x0 = y0 = 28 + w / 2; s = 256 - 2 * x0; rr = 48; gap = 24
    xs = 128 + gap / 2  # başlangıç: üst kenar ortasının sağı
    d = (f"M{xs:g} {y0:g} H{x0 + rr:g} A{rr} {rr} 0 0 0 {x0:g} {y0 + rr:g} V{y0 + s:g} "
         f"H{x0 + s - rr:g} A{rr} {rr} 0 0 0 {x0 + s:g} {y0 + s - rr:g} "
         f"V{y0 + rr:g} A{rr} {rr} 0 0 0 {x0 + s - rr:g} {y0:g} H{xs + gap:g}")
    return stroke(d, w, join="miter")


# ---------------- Wordmark (geometrik monoline, küçük harf) ----------------
SW = 22; XH = 100; RO = (XH - SW) / 2  # o merkez hattı yarıçapı 39
YC = -XH / 2  # x-yüksekliği ortası (baseline=0)


def g_s(x):
    rx, ry = 26, (XH - SW) / 4
    cx = x + SW / 2 + rx; t = YC - ry; b = YC + ry
    d = (f"M{cx + rx:g} {t:g} A{rx} {ry} 0 1 0 {cx:g} {YC:g} "
         f"A{rx} {ry} 0 1 1 {cx - rx:g} {b:g}")
    return stroke(d, SW), 2 * rx + SW


def g_o(x):
    return f'<circle cx="{x + 50:g}" cy="{YC:g}" r="{RO:g}" fill="none" stroke="{INK}" stroke-width="{SW}"/>', 100


def g_a(x):
    c, _ = g_o(x)
    return c + "\n" + stroke(f"M{x + 89:g} {-XH:g} V0", SW), 100


def g_p(x):
    c, _ = g_o(x)
    return c + "\n" + stroke(f"M{x + 11:g} {-XH:g} V45", SW), 100


def g_e(x):
    cx = x + 50
    d = arc(cx, YC, RO, 0, 40, 0) + f" M{x + 11:g} {YC:g} H{x + 89:g}"
    return stroke(d, SW), 100


def g_l(x):
    return stroke(f"M{x + 11:g} -150 V0", SW), 22


def g_f(x):
    sx = x + 24; r = 22; top = -150 + SW / 2
    d = (f"M{sx:g} 0 V{top + r:g} A{r} {r} 0 0 1 {sx + r:g} {top:g} H{sx + 36:g} "
         f"M{x:g} {-XH + SW / 2:g} H{sx + 30:g}")
    return stroke(d, SW), 60


def g_oo(x):
    """C'nin imzası: iki o tek bir kapalı döngüde birleşir (ortak orta çubuk)."""
    c1 = x + 50; c2 = c1 + 2 * RO; t = YC - RO; b = YC + RO
    d = (f"M{c1:g} {t:g} H{c2:g} A{RO} {RO} 0 0 1 {c2:g} {b:g} H{c1:g} A{RO} {RO} 0 0 1 {c1:g} {t:g} Z "
         f"M{c1 + RO:g} {t:g} V{b:g}")
    return stroke(d, SW), 100 + 2 * RO


def wordmark(ligature=False):
    seq = [g_s, g_a, g_f, g_e, g_l] + ([g_oo] if ligature else [g_o, g_o]) + [g_p]
    gaps = {"g_l": 14}
    x = 0; parts = []
    for i, g in enumerate(seq):
        p, wd = g(x)
        parts.append(p)
        x += wd + (16 if i < len(seq) - 1 else 0)
    return "\n".join(parts), x  # genişlik


def write(name, w, h, body, title):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg(w, h, body, title))


def lockup(name, sym_body, ligature=False, title=""):
    wm, ww = wordmark(ligature)
    # wordmark yüksekliği -150..45 (195). Lockup yüksekliği 256; wordmark x-yüksekliği sembolün ~%40'ı
    k = 1.0
    sym_h = 256; pad = 56
    wm_top = 128 - (-150 + 45) / 2 * k  # dikey ortala
    body = (f'<g id="symbol">{sym_body}</g>\n'
            f'<g id="wordmark" transform="translate({sym_h + pad} {128 + 52.5 * k:g}) scale({k})">{wm}</g>')
    write(name, sym_h + pad + ww * k + 8, 256, body, title)


if __name__ == "__main__":
    A, B, D = sym_a(), sym_b(), sym_d()
    write("a-halka-symbol.svg", 256, 256, A, "SafeLoop A Kapanan Halka")
    write("b-sonsuz-s-symbol.svg", 256, 256, B, "SafeLoop B Sonsuz S")
    write("d-l-dongu-symbol.svg", 256, 256, D, "SafeLoop D L-Dongu")
    wm, ww = wordmark(True)
    write("c-oo-wordmark.svg", ww + 16, 256, f'<g transform="translate(8 {128 + 52.5:g})">{wm}</g>',
          "SafeLoop C oo wordmark")
    # C için favicon/sembol: birleşik oo
    oo, _ = g_oo(0)
    write("c-oo-symbol.svg", 256, 256, f'<g transform="translate(23 187) scale(1.18)">{oo}</g>',
          "SafeLoop C oo sembol")
    lockup("a-halka-lockup.svg", A, title="SafeLoop A lockup")
    lockup("b-sonsuz-s-lockup.svg", B, title="SafeLoop B lockup")
    lockup("d-l-dongu-lockup.svg", D, title="SafeLoop D lockup")
    print("ok")
