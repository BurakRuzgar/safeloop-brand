"""SafeLoop v2 kaba eskizler. Siyah, 256 tuval. Kullanım: python build_v2.py"""
import math, os

OUT = os.path.join(os.path.dirname(__file__), "..")
K = "#111"


def svg(body, vb="0 0 256 256", w=256, h=256):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}" height="{h}">\n'
            f'{body}\n</svg>\n')


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


# ---------- yuvarlak kare yolu: yay uzunluğuna göre örnekleme ----------
def rrect_pts(c=128, h=80, r=40, n=800, start=0.0):
    """Saat yönünde, üst kenarın ortasından başlayan yuvarlak kare merkez çizgisi."""
    segs = []
    L = 2 * h - 2 * r
    # kenarlar ve köşeler sırayla (üst-orta -> sağ üst köşe ...)
    def line(p0, p1):
        return ("l", p0, p1, math.dist(p0, p1))
    def arc(cx, cy, a0, a1):
        return ("a", (cx, cy, a0, a1), None, math.radians(abs(a1 - a0)) * r)
    x0, x1, y0, y1 = c - h, c + h, c - h, c + h
    segs = [
        line((c, y0), (x1 - r, y0)), arc(x1 - r, y0 + r, -90, 0),
        line((x1, y0 + r), (x1, y1 - r)), arc(x1 - r, y1 - r, 0, 90),
        line((x1 - r, y1), (x0 + r, y1)), arc(x0 + r, y1 - r, 90, 180),
        line((x0, y1 - r), (x0, y0 + r)), arc(x0 + r, y0 + r, 180, 270),
        line((x0 + r, y0), (c, y0)),
    ]
    total = sum(s[3] for s in segs)

    def at(d):
        d %= total
        for kind, a, b, ln in segs:
            if d <= ln:
                t = d / ln if ln else 0
                if kind == "l":
                    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
                cx, cy, a0, a1 = a
                ang = math.radians(a0 + (a1 - a0) * t)
                return (cx + r * math.cos(ang), cy + r * math.sin(ang))
            d -= ln
        return segs[-1][2]
    return at, total


def tapered(at, total, d0, d1, w0, w1, n=600, ease=1.0):
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        d = d0 + (d1 - d0) * t
        p = at(d)
        q = at(d + 0.5)
        tx, ty = q[0] - p[0], q[1] - p[1]
        m = math.hypot(tx, ty) or 1
        nx, ny = -ty / m, tx / m
        tt = min(t / 0.4, 1.0)
        w = (w0 + (w1 - w0) * (1 - (1 - tt) ** 2)) / 2
        left.append((p[0] + nx * w, p[1] + ny * w))
        right.append((p[0] - nx * w, p[1] - ny * w))
    pts = left + right[::-1]
    return "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts) + "Z"


# ======================= 1. Dört Adım (süreç) =======================
def dort_adim():
    # tek parça: üst çubuk, kuyruk düz, baş yuvarlak; 4 kez 90° döner
    piece = "M52,52 H136 A20,20 0 0 1 136,92 H52 Z"
    g = "".join(f'<path d="{piece}" transform="rotate({a} 128 128)"/>' for a in (0, 90, 180, 270))
    return svg(f'<g fill="{K}">{g}</g>')


# ======================= 2. İvme İzi (hareket) =======================
def ivme_izi(h=84, r=44, wmax=44, gap=14):
    at, total = rrect_pts(h=h, r=r)
    # başlangıç sol-üst köşeden biraz önce, bitiş aynı noktadan gap kadar önce
    s = total * 0.875
    d = tapered(at, total, s, s + total - gap - wmax * 0.15, 3, wmax, ease=0.85)
    return svg(f'<path fill="{K}" d="{d}"/>')


# ======================= 3. Yükselen Spiral (PDCA spirali) =======================
def spiral(sw=30):
    # dikdörtgen spiral, köşeler yuvarlak; dıştan içe 1¼ tur, iz aralığı 50
    pts = [(46, 214), (46, 42), (210, 42), (210, 214), (96, 214), (96, 92), (160, 92), (160, 160)]
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    return svg(f'<path d="{d}" fill="none" stroke="{K}" stroke-width="{sw}" '
               f'stroke-linejoin="round" stroke-linecap="round"/>')


# ======================= 4. Katman (iç içe, boşluklar döner) =======================
def katman(sw=22):
    out = []
    # 3 iç içe yuvarlak kare; her birinde bir köşe açık, açıklık katman başına 90° döner
    for i, (h, rot) in enumerate([(96, 0), (62, 90), (28, 180)]):
        r = max(h * 0.42, 10)
        at, total = rrect_pts(h=h, r=r)
        # köşe açıklığı: sağ-üst köşe çevresi (toplam uzunluğun ~%12,5'i)
        q = total / 8
        gap = sw * 2.6
        s, e = q + gap / 2, q + total - gap / 2
        pts = [at(s + (e - s) * k / 300) for k in range(301)]
        d = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts)
        out.append(f'<path d="{d}" transform="rotate({rot} 128 128)"/>')
    return svg(f'<g fill="none" stroke="{K}" stroke-width="{sw}" stroke-linecap="butt">{"".join(out)}</g>')


# ======================= 4. Devir (iki yarım yay, kaydırılmış) =======================
def devir(r=76, sw=38, dy=11, gap=7):
    o, i = r + sw / 2, r - sw / 2
    def half(cy, left):
        sx = -1 if left else 1
        # üstten alta yarım halka dolgu (dış yay + iç yay)
        x = 128 - gap / 2 if left else 128 + gap / 2
        sweep_o = 0 if left else 1
        sweep_i = 1 if left else 0
        return (f"M{f(x)},{f(cy-o)} A{f(o)},{f(o)} 0 0 {sweep_o} {f(x)},{f(cy+o)} "
                f"L{f(x)},{f(cy+i)} A{f(i)},{f(i)} 0 0 {sweep_i} {f(x)},{f(cy-i)} Z")
    d = half(128 - dy, True) + " " + half(128 + dy, False)
    return svg(f'<path fill="{K}" d="{d}"/>')


# ======================= Wordmark (sıfırdan, monoline) =======================
SW = 14
T, B, M = 76, 140, 108


def letters():
    p = []
    # s
    cx = 30
    p.append(f"M{f(cx+12.1)},{94-7} A14,14 0 1 0 {cx},108 A14,14 0 1 1 {f(cx-12.1)},129")
    # a
    cx = 95
    p.append(f"M{cx+25},{M} A25,25 0 1 0 {cx-25},{M} A25,25 0 1 0 {cx+25},{M} M{cx+25},{T} V{B}")
    # f
    fx = 151
    p.append(f"M{fx},{B} V60 A18,18 0 0 1 {fx+18},42 H{fx+24} M{fx-14},{T+7} H{fx+20}")
    # e
    cx = 215
    p.append(f"M{cx-25},{M} H{cx+25} A25,25 0 1 0 {f(cx+17.7)},{f(M+17.7)}")
    # l
    p.append(f"M268,40 V{B}")
    # o o
    for cx in (321, 397):
        p.append(f"M{cx+25},{M} A25,25 0 1 0 {cx-25},{M} A25,25 0 1 0 {cx+25},{M}")
    # p bowl
    cx = 473
    p.append(f"M{cx+25},{M} A25,25 0 1 0 {cx-25},{M} A25,25 0 1 0 {cx+25},{M}")
    return p


def wordmark(close_line=False):
    p = letters()
    if close_line:
        # p'nin inişi sola döner, kelimenin altından s'ye kadar geri gelir, yukarı kıvrılır
        p.append("M448,76 V170 A16,16 0 0 1 432,186 H30 A16,16 0 0 1 14,170 V156")
    else:
        p.append("M448,76 V176")
    body = (f'<path d="{" ".join(p)}" fill="none" stroke="{K}" stroke-width="{SW}" '
            f'stroke-linecap="butt" stroke-linejoin="round"/>')
    return body


def wordmark_svg(close_line=False):
    return svg(wordmark(close_line), vb="0 20 520 190", w=520, h=190)


def lockup(sym_svg_body, close_line=False):
    # sembol 256 + boşluk + wordmark (yükseklik 256)
    word = wordmark(close_line)
    return svg(f'<g>{sym_svg_body}</g><g transform="translate(300,10) scale(1.15)">{word}</g>',
               vb="0 0 920 256", w=920, h=256)


def body_of(s):
    return s.split("\n", 1)[1].rsplit("</svg>", 1)[0]


# ---- 4. konseptin sembolü: p + geri dönen iniş (tek harf) ----
def kapanan_cizgi_symbol():
    sp = ("M{a},87 A14,14 0 1 0 30,108 A14,14 0 1 1 17.9,129 ".format(a=42.1) +
          "M128,108 A25,25 0 1 0 78,108 A25,25 0 1 0 128,108 "
          "M78,76 V170 A16,16 0 0 1 62,186 H30 A16,16 0 0 1 14,170 V156")
    return svg(f'<path d="{sp}" fill="none" stroke="{K}" stroke-width="16" stroke-linejoin="round" '
               f'transform="translate(128,128) scale(1.55) translate(-71,-116)"/>')
    d = ("M154,104 A34,34 0 1 0 86,104 A34,34 0 1 0 154,104 "
         "M86,70 V194 A22,22 0 0 1 64,216 H8 A22,22 0 0 1 -14,194 V186")
    return svg(f'<path d="{d}" fill="none" stroke="{K}" stroke-width="28" transform="translate(44,-12)"/>')


if __name__ == "__main__":
    concepts = {
        "1-dort-adim": dort_adim(),
        "2-ivme-izi": ivme_izi(),
        "3-yukselen-spiral": spiral(),
        "4-devir": devir(),
        "5-kapanan-cizgi": kapanan_cizgi_symbol(),
    }
    for k, s in concepts.items():
        save(f"{k}-symbol.svg", s)
        save(f"{k}-lockup.svg", lockup(body_of(s), close_line=(k == "5-kapanan-cizgi")))
    save("wordmark-v2.svg", wordmark_svg(False))
    save("5-kapanan-cizgi-wordmark.svg", wordmark_svg(True))
    print("ok")
