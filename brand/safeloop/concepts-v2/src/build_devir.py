"""SafeLoop · Devir geliştirme. Çıktı: concepts-v2/devir/
Kayma yönü her yerde aynı: sol yarı YUKARI, sağ yarı AŞAĞI.
"""
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "devir")
os.makedirs(OUT, exist_ok=True)
K = "#0F1B2D"   # Lacivert (Aşama 4 ana renk)
WHITE = "#FFFFFF"


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def devir_d(cx, cy, ro, sw, dy, gap):
    """Devir yolu. ro: dış yarıçap, sw: kalınlık, dy: kayma, gap: orta boşluk."""
    ri = ro - sw

    def half(hcy, left):
        x = cx - gap / 2 if left else cx + gap / 2
        so, si = (0, 1) if left else (1, 0)
        return (f"M{f(x)},{f(hcy-ro)} A{f(ro)},{f(ro)} 0 0 {so} {f(x)},{f(hcy+ro)} "
                f"L{f(x)},{f(hcy+ri)} A{f(ri)},{f(ri)} 0 0 {si} {f(x)},{f(hcy-ri)} Z")
    return half(cy - dy, True) + " " + half(cy + dy, False)


# Üç kesim — oranlar: dy/sw ≈ 0.45–0.5, kayma küçükte de görünür kalsın diye büyütüldü
MAIN = dict(ro=94, sw=40, dy=18, gap=10)     # 64 px ve üstü
SMALL = dict(ro=90, sw=46, dy=24, gap=20)    # 16–32 px (favicon)
WORD = dict(ro=30.5, sw=14.5, dy=6, gap=5)   # kelime içi: x-yüksekliği 64, harf kalınlığı 14


def svg(body, vb, w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{f(w)}" height="{f(h)}">\n'
            f'{body}\n</svg>\n')


def save(name, s):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(s)


def symbol(cut):
    return svg(f'<path fill="{K}" d="{devir_d(128, 128, **cut)}"/>', "0 0 256 256", 256, 256)


# ---------- wordmark (v2 harfleri, monoline kalınlık 14, x-yüksekliği 76..140) ----------
SW, T, B, M = 14, 76, 140, 108
O_CX = (321, 397)


def letter_paths(devir_o, col=K):
    p = [
        f"M42.1,87 A14,14 0 1 0 30,108 A14,14 0 1 1 17.9,129",                       # s
        f"M120,{M} A25,25 0 1 0 70,{M} A25,25 0 1 0 120,{M} M120,{T} V{B}",           # a
        f"M151,{B} V60 A18,18 0 0 1 169,42 H175 M137,83 H171",                         # f
        f"M190,{M} H240 A25,25 0 1 0 232.7,125.7",                                     # e
        f"M268,40 V{B}",                                                                # l
        f"M498,{M} A25,25 0 1 0 448,{M} A25,25 0 1 0 498,{M} M448,76 V176",            # p
    ]
    fills = []
    for i, cx in enumerate(O_CX):
        if i in devir_o:
            fills.append(devir_d(cx, M, **WORD))
        else:
            p.append(f"M{cx+25},{M} A25,25 0 1 0 {cx-25},{M} A25,25 0 1 0 {cx+25},{M}")
    g = (f'<path d="{" ".join(p)}" fill="none" stroke="{col}" stroke-width="{SW}" '
         f'stroke-linecap="butt" stroke-linejoin="round"/>')
    if fills:
        g += f'<path fill="{col}" d="{" ".join(fills)}"/>'
    return g


def wordmark(devir_o, col=K):
    return svg(letter_paths(devir_o, col), "0 30 520 156", 520, 156)


def lockup(devir_o):
    # sembol yüksekliği = çıkıntı üstü (40) .. iniş altı (176); merkez x-yüksekliği ortası (108)
    half_h = MAIN["ro"] + MAIN["dy"]
    s = 68 / half_h
    half_w = (MAIN["ro"] + MAIN["gap"] / 2) * s
    cx = -(44 + half_w)
    sym = (f'<path fill="{K}" d="{devir_d(128, 128, **MAIN)}" '
           f'transform="translate({f(cx)},{M}) scale({f(s)}) translate(-128,-128)"/>')
    x0 = cx - half_w - 6
    return svg(sym + letter_paths(devir_o), f"{f(x0)} 30 {f(520 - x0)} 156", 520 - x0, 156)


# ---------- kutulu sembol ----------
BOX_R = 0.225        # köşe yarıçapı / kutu kenarı (uygulama ikonu oranı)
SYM_FILL = 0.66      # sembolün kutu içindeki yükseklik payı
FRAME_SW = 14        # çerçeve kalınlığı = harf kalınlığı


def rrect(x, y, w, r):
    return (f"M{f(x+r)},{f(y)} H{f(x+w-r)} A{f(r)},{f(r)} 0 0 1 {f(x+w)},{f(y+r)} V{f(y+w-r)} "
            f"A{f(r)},{f(r)} 0 0 1 {f(x+w-r)},{f(y+w)} H{f(x+r)} A{f(r)},{f(r)} 0 0 1 {f(x)},{f(y+w-r)} "
            f"V{f(y+r)} A{f(r)},{f(r)} 0 0 1 {f(x+r)},{f(y)} Z")


def boxed(x, y, w, cut, mode, col):
    """mode: 'solid' = dolu kutu, sembol oyuk (zemin görünür) · 'frame' = çerçeve + dolu sembol."""
    k = (w * SYM_FILL / 2) / (cut["ro"] + cut["dy"])
    c = dict(ro=cut["ro"] * k, sw=cut["sw"] * k, dy=cut["dy"] * k, gap=cut["gap"] * k)
    sym = devir_d(x + w / 2, y + w / 2, **c)
    if mode == "solid":
        return f'<path fill="{col}" fill-rule="evenodd" d="{rrect(x, y, w, w*BOX_R)} {sym}"/>'
    h = FRAME_SW / 2
    return (f'<path fill="none" stroke="{col}" stroke-width="{FRAME_SW}" d="{rrect(x+h, y+h, w-FRAME_SW, w*BOX_R-h)}"/>'
            f'<path fill="{col}" d="{sym}"/>')


BOX = 124            # kutu yüksekliği (wordmark birimi): çıkıntı 40 .. iniş 176 arası, x-ortası 108'e merkezli
BOX_GAP = 46         # kutu ile "s" arası (~ 0.37 kutu, ~ s genişliği)


NAVY = "#0F1B2D"     # KARAR: kutu ve wordmark rengi


def lockup_box(cut=MAIN, mode="solid", box_col=NAVY, word_col=NAVY, bg=None):
    x = 9 - BOX_GAP - BOX           # s'nin sol kenarı ≈ 9
    y = M - BOX / 2
    body = boxed(x, y, BOX, cut, mode, box_col) + letter_paths({0, 1}, word_col)
    x0, y0, w, h = x - 8, 30, 520 - x + 8, 156
    if bg:
        pad = 26
        x0, y0, w, h = x0 - pad, y0 - pad, w + 2 * pad, h + 2 * pad
        body = f'<rect x="{f(x0)}" y="{y0}" width="{f(w)}" height="{h}" fill="{bg}"/>' + body
    return svg(body, f"{f(x0)} {y0} {f(w)} {h}", w, h)


def icon(cut, mode="solid", col=NAVY):
    return svg(boxed(0, 0, 256, cut, mode, col), "0 0 256 256", 256, 256)


if __name__ == "__main__":
    save("devir-symbol.svg", symbol(MAIN))
    save("devir-small.svg", symbol(SMALL))
    save("wordmark-oo.svg", wordmark({0, 1}))
    save("lockup-oo.svg", lockup({0, 1}))
    # yeni: kutulu sembol
    save("icon-box.svg", icon(MAIN))                  # uygulama ikonu 64 px+
    save("icon-box-small.svg", icon(SMALL))           # favicon 16–32 px
    save("lockup-box.svg", lockup_box(MAIN))          # açık zemin, ~250 px genişlik ve üstü
    save("lockup-box-small.svg", lockup_box(SMALL))   # açık zemin, ≤ 200 px genişlik
    # koyu zemin = ters kutu: beyaz kutu, sembol oyuk (zemin görünür), beyaz wordmark; saydam
    save("lockup-box-ters.svg", lockup_box(MAIN, "solid", WHITE, WHITE))
    save("lockup-box-ters-small.svg", lockup_box(SMALL, "solid", WHITE, WHITE))
    save("wordmark-oo-beyaz.svg", wordmark({0, 1}, WHITE))
    save("icon-box-ters.svg", icon(MAIN, col=WHITE))
    print("ok")
