"""E2 varyasyonları: "Z" okumasını kırıp S'yi öne çıkarmak.
- Üst çubuğun sol köşesi yarıçaplı bir kıvrım (S'nin üst kıvrımı) olur; keskin Z köşesi kalmaz.
- Omurga, üst kıvrım ile alt kâse arasındaki ortak (çapraz) teğettir: kıvrımlar büyüdükçe omurga yatışır.
- Kâse büyür. L gövdesi (sol alt -> sağ üst), L ayağı ve taban E2 ile aynı kalır.
Çalıştır: python build_e2v.py -> ../ altına e2a/e2b/e2c (+ -small, -lockup) yazar."""
import math, os, sys
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "..", "src"))
from build_concepts import wordmark  # wordmark değişmez, yalnız okunur

OUT = os.path.join(HERE, "..")
INK = "#111111"
# E2'den aynen: ızgara, L gövdesi, ayak ve taban
T, B, L, R, FOOT, LEFT = 58, 198, 70, 178, 232, 54


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def ang(c, p):
    return math.degrees(math.atan2(p[1] - c[1], p[0] - c[0]))


def symbol(rt, rb, cxb, ctx=None, w=28, T_=T, B=B, left=LEFT):
    ctx = L + rt if ctx is None else ctx
    Ct = (ctx, T_ + rt)               # üst kıvrım merkezi; sola taşabilir (eskizdeki gibi)
    assert math.hypot(cxb - ctx, (B - rb) - (T_ + rt)) > rt + rb + 4, 'kıvrımlar çakışıyor'
    Cb = (cxb, B - rb)                # kâse merkezi; alt teğeti = taban
    dx, dy = Cb[0] - Ct[0], Cb[1] - Ct[1]
    d = math.hypot(dx, dy); phi = math.atan2(dy, dx)
    best = None
    for sgn in (1, -1):               # iki çapraz teğetten doğru yöndekini seç
        a = phi + sgn * math.acos((rt + rb) / d)
        n = (math.cos(a), math.sin(a))
        Pt = (Ct[0] + rt * n[0], Ct[1] + rt * n[1])
        Pb = (Cb[0] - rb * n[0], Cb[1] - rb * n[1])
        rv = (Pt[0] - Ct[0], Pt[1] - Ct[1])
        tdir = (rv[1], -rv[0])        # saat tersi (sweep 0) hareket yönü
        if (Pb[0] - Pt[0]) * tdir[0] + (Pb[1] - Pt[1]) * tdir[1] > 0:
            best = (Pt, Pb)
    Pt, Pb = best
    span_t = (-90 - ang(Ct, Pt)) % 360          # tepe noktasından Pt'ye saat tersi
    span_b = (90 - ang(Cb, Pb)) % 360           # Pb'den kâse dibine saat yönü
    line = (f"M{L} {B} L{R} {T_} H{f(Ct[0])} "
            f"A{rt} {rt} 0 {1 if span_t > 180 else 0} 0 {f(Pt[0])} {f(Pt[1])} "
            f"L{f(Pb[0])} {f(Pb[1])} "
            f"A{rb} {rb} 0 {1 if span_b > 180 else 0} 1 {f(Cb[0])} {B}")
    base = f"M{left} {B} H{FOOT}"
    sw = (f'fill="none" stroke="{INK}" stroke-width="{w}" stroke-linejoin="round" '
          f'stroke-miterlimit="10" stroke-linecap="butt"')
    return f'<path d="{line}" {sw}/>\n<path d="{base}" {sw}/>'


VARIANTS = {
    # ad: (rt, rb, cxb, not)
    "e2a": dict(rt=28, ctx=98, rb=48, cxb=160),   # hafif: köşe yuvarlandı, kâse 44 -> 48
    "e2b": dict(rt=34, ctx=92, rb=50, cxb=164),   # dengeli: belirgin üst kıvrım, daha yatık omurga
    "e2c": dict(rt=42, ctx=88, rb=46, cxb=170),   # en S: büyük üst kıvrım, en yatık omurga, kâse 46
}


def svg(w, h, body, title, vb=None):
    vb = vb or f"0 0 {w:g} {h:g}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w:g}" height="{h:g}" '
            f'overflow="visible" role="img" aria-labelledby="t"><title id="t">{title}</title>\n{body}\n</svg>\n')


def write(name, body, title, w=256, h=256, vb=None):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(svg(w, h, body, title, vb))


if __name__ == "__main__":
    wm, ww = wordmark(False)
    for k, p in VARIANTS.items():
        write(f"{k}-symbol.svg", symbol(**p), f"SafeLoop {k.upper()}")
        # Küçük sürüm (16-32 px): ızgara 140 -> 184 birim yüksek (iç boşluklar açılır), kalınlık 34,
        # tabanın soldaki taşması kaldırıldı; viewBox çizime sıkı kırpılır
        write(f"{k}-small.svg", symbol(**p, w=34, T_=36, B=220, left=L - 17),
              f"SafeLoop {k.upper()} küçük (16-32 px)", vb="16 16 232 224")
        body = f'<g id="symbol">{symbol(**p)}</g>\n<g id="wordmark" transform="translate(312 180.5)">{wm}</g>'
        write(f"{k}-lockup.svg", body, f"SafeLoop {k.upper()} yatay", w=312 + ww + 8)
    print("ok")
