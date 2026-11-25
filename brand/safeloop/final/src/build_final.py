"""SafeLoop · Aşama 6 teslim dosyaları. Çıktı: final/svg/ (+ PNG'ler render_final.py ile).
Geometri tek kaynaktan gelir: concepts-v2/src/build_devir.py. Burada wordmark stroke'u outline'a çevrilir,
alt imza (Plus Jakarta Sans SemiBold) path'e çevrilir, lockup'lar kurulur.
"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "concepts-v2", "src"))
sys.dont_write_bytecode = True
import build_devir as D  # noqa: E402
from ttf import TTF  # noqa: E402

OUT = os.path.join(HERE, "..", "svg")
os.makedirs(OUT, exist_ok=True)

NAVY, BLACK, WHITE, SLATE = "#0F1B2D", "#000000", "#FFFFFF", "#566275"
# renk seti: (kutu, wordmark, imza)
COLORS = {
    "renkli": (NAVY, NAVY, SLATE),
    "siyah": (BLACK, BLACK, BLACK),
    "beyaz": (WHITE, WHITE, WHITE),   # koyu zemin: ters kutu, sembol oyuk
}
f = D.f
TAU = 2 * math.pi


# ---------------------------------------------------------------- stroke → outline
def parse(d):
    toks = re.findall(r"[MAVHLZ]|-?\d*\.?\d+", d)
    i, cmd, subs, cur, pos = 0, None, [], None, (0.0, 0.0)
    num = lambda: float(toks[i])
    while i < len(toks):
        if toks[i] in "MAVHLZ":
            cmd = toks[i]; i += 1
            continue
        if cmd == "M":
            pos = (float(toks[i]), float(toks[i + 1])); i += 2
            cur = []; subs.append(cur)
            cmd = "L"
        elif cmd == "L":
            p = (float(toks[i]), float(toks[i + 1])); i += 2
            cur.append(("L", pos, p)); pos = p
        elif cmd == "H":
            p = (num(), pos[1]); i += 1
            cur.append(("L", pos, p)); pos = p
        elif cmd == "V":
            p = (pos[0], num()); i += 1
            cur.append(("L", pos, p)); pos = p
        elif cmd == "A":
            r, _, _, la, sw, x, y = (float(t) for t in toks[i:i + 7]); i += 7
            p = (x, y)
            cur.append(("A", pos, p, r, int(la), int(sw))); pos = p
    return subs


def arc_center(p0, p1, r, la, sw):
    """SVG uç-nokta → merkez (rx=ry, döndürme yok). Dönüş: c, θ1, Δθ (y aşağı koordinat)."""
    x1, y1 = (p0[0] - p1[0]) / 2, (p0[1] - p1[1]) / 2
    d2 = x1 * x1 + y1 * y1
    r = max(r, math.sqrt(d2))
    k = math.sqrt(max(0.0, (r * r - d2) / d2))
    if la == sw:
        k = -k
    cxp, cyp = k * y1, -k * x1
    c = (cxp + (p0[0] + p1[0]) / 2, cyp + (p0[1] + p1[1]) / 2)
    t1 = math.atan2(p0[1] - c[1], p0[0] - c[0])
    t2 = math.atan2(p1[1] - c[1], p1[0] - c[0])
    dt = (t2 - t1) % TAU
    if not sw:
        dt -= TAU
    if abs(abs(dt) - TAU) < 1e-9:
        dt = 0.0
    return c, r, t1, dt


def pt(c, r, t):
    return (c[0] + r * math.cos(t), c[1] + r * math.sin(t))


class Outline:
    def __init__(self, w):
        self.h = w / 2
        self.parts, self.samples = [], []

    def line(self, a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        nx, ny = -dy / L * self.h, dx / L * self.h
        q = [(a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny), (b[0] - nx, b[1] - ny), (a[0] - nx, a[1] - ny)]
        area = sum(q[i][0] * q[(i + 1) % 4][1] - q[(i + 1) % 4][0] * q[i][1] for i in range(4))
        if area < 0:
            q.reverse()
        self.parts.append("M" + " L".join(f"{f(x)},{f(y)}" for x, y in q) + " Z")
        self.samples += q

    def arc(self, c, r, t1, dt):
        if dt < 0:                       # hep saat yönü (y aşağı, açı artan) → nonzero birleşim
            t1, dt = t1 + dt, -dt
        R, ri, la = r + self.h, r - self.h, 1 if dt > math.pi + 1e-9 else 0
        o0, o1, i1, i0 = pt(c, R, t1), pt(c, R, t1 + dt), pt(c, ri, t1 + dt), pt(c, ri, t1)
        self.parts.append(
            f"M{f(o0[0])},{f(o0[1])} A{f(R)},{f(R)} 0 {la} 1 {f(o1[0])},{f(o1[1])} "
            f"L{f(i1[0])},{f(i1[1])} A{f(ri)},{f(ri)} 0 {la} 0 {f(i0[0])},{f(i0[1])} Z")
        n = 64
        for k in range(n + 1):
            t = t1 + dt * k / n
            self.samples += [pt(c, R, t), pt(c, ri, t)]

    def disk(self, p):
        h = self.h
        self.parts.append(f"M{f(p[0]-h)},{f(p[1])} A{f(h)},{f(h)} 0 0 1 {f(p[0]+h)},{f(p[1])} "
                          f"A{f(h)},{f(h)} 0 0 1 {f(p[0]-h)},{f(p[1])} Z")
        self.samples += [(p[0] - h, p[1] - h), (p[0] + h, p[1] + h)]


def tangents(seg):
    """(başlangıç yönü, bitiş yönü) birim vektör."""
    if seg[0] == "L":
        a, b = seg[1], seg[2]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        v = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        return v, v
    c, r, t1, dt = arc_center(*seg[1:3], seg[3], seg[4], seg[5])
    s = 1 if dt > 0 else -1
    tan = lambda t: (-math.sin(t) * s, math.cos(t) * s)
    return tan(t1), tan(t1 + dt)


def outline_stroke(d, w):
    o = Outline(w)
    for sub in parse(d):
        for j, seg in enumerate(sub):
            if seg[0] == "L":
                o.line(seg[1], seg[2])
            else:
                c, r, t1, dt = arc_center(seg[1], seg[2], seg[3], seg[4], seg[5])
                o.arc(c, r, t1, dt)
            if j:                         # round join: yalnız köşede (teğet kırılıyorsa) disk
                v0, v1 = tangents(sub[j - 1])[1], tangents(seg)[0]
                if v0[0] * v1[0] + v0[1] * v1[1] < 0.9998:
                    o.disk(seg[1])
    return o


def word_parts():
    """(outline path d, dolgu path d, örnek noktalar) — kelime içi iki Devir 'o' dahil."""
    g = D.letter_paths({0, 1})
    stroke_d = re.search(r'<path d="([^"]+)" fill="none"', g).group(1)
    fill_d = re.search(r'<path fill="[^"]+" d="([^"]+)"', g).group(1)
    o = outline_stroke(stroke_d, D.SW)
    return " ".join(o.parts), fill_d, o.samples, stroke_d


WORD_D, DEVIR_D, WORD_SAMPLES, STROKE_D = word_parts()


def bbox(points):
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    return min(xs), min(ys), max(xs), max(ys)


WB = bbox(WORD_SAMPLES)          # wordmark sınırları (s sol kenarı 9 .. p sağ 505, 35 .. 176)

# ---------------------------------------------------------------- alt imza
FONT = TTF(os.path.join(HERE, "fonts", "PlusJakartaSans-SemiBold.ttf"))
SIG_TEXT = "by Rüzgar Safety"
SIG_SIZE = 30            # wordmark birimi (x-yüksekliği 64 → imza büyük harfi ≈ 22)
SIG_TRACK = 0.02
SIG_BASE = 190           # yatay: wordmark taban çizgisi 140, iniş 176


def sig_path(x_left=None, x_center=None, baseline=SIG_BASE):
    _, w = FONT.text_path(SIG_TEXT, 0, 0, SIG_SIZE, SIG_TRACK)
    x = x_left if x_left is not None else x_center - w / 2
    d, _ = FONT.text_path(SIG_TEXT, x, baseline, SIG_SIZE, SIG_TRACK)
    desc = 0.25 * SIG_SIZE
    return d, (x, baseline - FONT.cap / FONT.upm * SIG_SIZE, x + w, baseline + desc)


# ---------------------------------------------------------------- kompozisyon
def doc(body, box, title, pad=0):
    x0, y0, x1, y1 = box
    x0, y0, x1, y1 = math.floor(x0) - pad, math.floor(y0) - pad, math.ceil(x1) + pad, math.ceil(y1) + pad
    w, h = x1 - x0, y1 - y0
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{title}">\n<title>{title}</title>\n{body}\n</svg>\n'), (w, h)


def word_body(col):
    return f'<path fill="{col}" d="{WORD_D} {DEVIR_D}"/>'


def horizontal(cut, colors, sig=False):
    box_c, word_c, sig_c = colors
    bx, by = 9 - D.BOX_GAP - D.BOX, D.M - D.BOX / 2      # build_devir.lockup_box ile aynı
    body = D.boxed(bx, by, D.BOX, cut, "solid", box_c) + word_body(word_c)
    bb = [bx, min(by, WB[1]), WB[2], max(by + D.BOX, WB[3])]
    if sig:
        d, sb = sig_path(x_left=WB[0])
        body += f'<path fill="{sig_c}" d="{d}"/>'
        bb[3] = max(bb[3], sb[3])
    return body, bb


V_BOX, V_GAP = 200, 56   # dikey: kutu kenarı ve kutu–yükselen harf arası


def vertical(cut, colors, sig=False):
    box_c, word_c, sig_c = colors
    cx = (WB[0] + WB[2]) / 2
    bx, by = cx - V_BOX / 2, WB[1] - V_GAP - V_BOX
    body = D.boxed(bx, by, V_BOX, cut, "solid", box_c) + word_body(word_c)
    bb = [WB[0], by, WB[2], WB[3]]
    if sig:
        d, sb = sig_path(x_center=cx, baseline=WB[3] + 44)
        body += f'<path fill="{sig_c}" d="{d}"/>'
        bb[3] = max(bb[3], sb[3])
    return body, bb


def symbol(cut, col):
    return D.boxed(0, 0, 256, cut, "solid", col), (0, 0, 256, 256)


def square(cut, bg=NAVY, fg=WHITE):
    """Tam kare (köşesiz) zemin + dolu sembol: apple-touch, maskable, sosyal avatar."""
    k = (256 * D.SYM_FILL / 2) / (cut["ro"] + cut["dy"])
    c = {key: v * k for key, v in cut.items()}
    return (f'<rect width="256" height="256" fill="{bg}"/><path fill="{fg}" d="{D.devir_d(128, 128, **c)}"/>',
            (0, 0, 256, 256))


MANIFEST = []


def save(name, body_box, title):
    s, size = doc(*body_box, title)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(s)
    MANIFEST.append({"file": name, "w": size[0], "h": size[1]})


if __name__ == "__main__":
    T, TS = "SafeLoop", "SafeLoop by Rüzgar Safety"
    for cname, cols in COLORS.items():
        save(f"safeloop-yatay-{cname}.svg", horizontal(D.MAIN, cols), T)
        save(f"safeloop-yatay-kucuk-{cname}.svg", horizontal(D.SMALL, cols), T)
        save(f"safeloop-yatay-imza-{cname}.svg", horizontal(D.MAIN, cols, sig=True), TS)
        save(f"safeloop-dikey-{cname}.svg", vertical(D.MAIN, cols), T)
        save(f"safeloop-dikey-kucuk-{cname}.svg", vertical(D.SMALL, cols), T)
        save(f"safeloop-dikey-imza-{cname}.svg", vertical(D.MAIN, cols, sig=True), TS)
        save(f"safeloop-wordmark-{cname}.svg", (word_body(cols[1]), WB), T)
        save(f"safeloop-sembol-{cname}.svg", symbol(D.MAIN, cols[0]), T)
        save(f"safeloop-sembol-kucuk-{cname}.svg", symbol(D.SMALL, cols[0]), T)
    save("safeloop-sembol-kare.svg", square(D.MAIN), T)
    # koyu tarayıcı temasında beyaz kutu (sembol oyuk → sekme rengi görünür)
    fav_body, fav_box = symbol(D.SMALL, NAVY)
    fav_body = "<style>@media (prefers-color-scheme: dark){path{fill:#FFFFFF}}</style>" + fav_body
    save("favicon.svg", (fav_body, fav_box), T)
    with open(os.path.join(HERE, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump({"files": MANIFEST, "stroke_d": STROKE_D, "word_bbox": WB}, fh, indent=1)
    print(len(MANIFEST), "svg · wordmark bbox", [round(v, 2) for v in WB])
