"""Aşama 3: A · Kapanan Halka v2 (optik düzeltilmiş, dolgu/outline) + 16/32 px küçük boyut kesimi.
Çalıştır: python build_a_v2.py  -> ../ altına a-halka-v2-*.svg yazar.

Optik düzeltme fikri: v1'de halka uçları radyal kesikti; boşluk iç kenarda ~13, dış kenarda ~19 birimdi
(kama gibi). v2'de uçlar noktayla eş merkezli bir "yuva" yayıyla kesilir: nokta ile halka arasındaki
boşluk her yerde eşit kalır.
"""
import math, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from build_concepts import wordmark, INK  # ortak wordmark

OUT = os.path.join(os.path.dirname(__file__), "..")
C = 128.0


def P(r, deg, cx=C, cy=C):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def halka(R_o, R_i, rc, node_r, clr, theta=-45.0):
    """Halka (dolgu path, yuva kesikli) + nokta (circle). Açılar ekran açısı (0=doğu, -90=kuzey)."""
    Rb = node_r + clr  # yuva yarıçapı
    nx, ny = P(rc, theta)

    def delta(R):  # yuva çemberinin R yarıçaplı çemberi kestiği açı farkı
        return math.degrees(math.acos((R * R + rc * rc - Rb * Rb) / (2 * R * rc)))

    do, di = delta(R_o), delta(R_i)
    o1, o2 = P(R_o, theta + do), P(R_o, theta - do)  # o1: saat yönü tarafı, o2: saat tersi tarafı
    i1, i2 = P(R_i, theta + di), P(R_i, theta - di)

    def bite(a, b):  # a->b yuva yayı (küçük yay, doğru yön)
        aa = math.degrees(math.atan2(a[1] - ny, a[0] - nx))
        bb = math.degrees(math.atan2(b[1] - ny, b[0] - nx))
        d = (bb - aa + 540) % 360 - 180
        return f"A{f(Rb)} {f(Rb)} 0 0 {1 if d > 0 else 0} {f(b[0])} {f(b[1])}"

    d = (f"M{f(o1[0])} {f(o1[1])} "
         f"A{f(R_o)} {f(R_o)} 0 1 1 {f(o2[0])} {f(o2[1])} "
         + bite(o2, i2) +
         f" A{f(R_i)} {f(R_i)} 0 1 0 {f(i1[0])} {f(i1[1])} "
         + bite(i1, o1) + " Z")
    return (f'<path d="{d}" fill="{INK}"/>\n'
            f'<circle cx="{f(nx)}" cy="{f(ny)}" r="{f(node_r)}" fill="{INK}"/>')


# Ana sürüm (>= 48 px): kalınlık 36, nokta Ø48 = 1.33 × kalınlık, eşit boşluk 12
MASTER = dict(R_o=102, R_i=66, rc=84, node_r=24, clr=12)
# Küçük kesim (16-32 px): kalınlık 44 (16px'te 2.75 px), nokta Ø64 (4 px), boşluk 30 (~1.9 px)
SMALL = dict(R_o=106, R_i=62, rc=84, node_r=32, clr=30)


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" '
            f'role="img" aria-labelledby="t"><title id="t">{title}</title>\n{body}\n</svg>\n')


def write(name, w, h, body, title):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(svg(w, h, body, title))


if __name__ == "__main__":
    m = halka(**MASTER)
    s = halka(**SMALL)
    write("a-halka-v2-symbol.svg", 256, 256, f'<g id="symbol">{m}</g>', "SafeLoop sembol v2")
    write("a-halka-v2-small.svg", 256, 256, f'<g id="symbol-small">{s}</g>', "SafeLoop sembol küçük boyut (16-32 px)")
    wm, ww = wordmark(False)
    body = (f'<g id="symbol">{m}</g>\n'
            f'<g id="wordmark" transform="translate(312 180.5)" overflow="visible">{wm}</g>')
    write("a-halka-v2-lockup.svg", 312 + ww + 8, 256, body, "SafeLoop yatay logo v2")
    print("ok")
