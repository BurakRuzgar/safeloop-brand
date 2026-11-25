"""Konsept E: kullanıcının S+L eskizinin geometrik yorumları.
Okuma: S açısal çizildiğinde (üst bar -> çapraz omurga -> alt) ve L'nin gövdesi sağ üstten sol alta
çapraz indiğinde, ikisi birlikte kapalı bir "8 / kum saati" döngüsü oluşturur. L'nin ayağı taban çizgisi
olarak sağa uzar. Çalıştır: python build_e.py -> ../ altına e-*.svg yazar."""
import math, os, sys
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "..", "src"))
from build_concepts import wordmark  # yalnız okunur, A dosyalarına dokunulmaz

OUT = os.path.join(HERE, "..")
INK = "#111111"; W = 28


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" '
            f'overflow="visible" role="img" aria-labelledby="t"><title id="t">{title}</title>\n{body}\n</svg>\n')


def st(d, join="miter", cap="butt"):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{W}" stroke-linejoin="{join}" '
            f'stroke-miterlimit="10" stroke-linecap="{cap}"/>')


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


# Ortak ızgara: üst y=58, taban y=198, sol x=70, sağ x=178; ayak x=232'ye uzar
T, B, L, R, FOOT = 58, 198, 70, 178, 232


def e1():
    """E1 Açısal: kapalı kum saati döngüsü + sağa uzayan L ayağı."""
    loop = f"M{R} {T} H{L} L{R} {B} H{L} Z"      # S: üst bar, omurga, alt bar; Z = L gövdesi (sol alt -> sağ üst)
    foot = f"M{R - 1} {B} H{FOOT}"
    return st(loop) + "\n" + st(foot)


def e2():
    """E2 Eskize sadık: omurga sağ altta yuvarlak bir kâseye döner; taban çizgisi kâseye teğet geçip sağa uzar."""
    r = 44; cx, cy = R - r + 8, B - r             # kâse çemberi, alt teğeti = taban çizgisi
    # TL'den kâse çemberine teğet noktası (dış teğet, sağ taraf)
    dx, dy = cx - L, cy - T; dist = math.hypot(dx, dy)
    a = math.atan2(dy, dx) - math.asin(r / dist)  # teğet doğrultusu
    # teğet noktası: merkezden doğrultuya dik
    tx, ty = cx + r * math.sin(a), cy - r * math.cos(a)
    # Tek kesintisiz çizgi (eskizdeki gibi): sol alt -> L gövdesi -> sağ üst -> üst bar -> omurga -> kâse
    line = f"M{L} {B} L{R} {T} H{L} L{f(tx)} {f(ty)} A{r} {r} 0 0 1 {f(cx)} {B}"
    base = f"M{L - 16} {B} H{FOOT}"               # taban: L ayağı (sola kısa, sağa uzun)
    return st(line, join="round") + "\n" + st(base)


def write(name, w, h, body, title):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(svg(w, h, body, title))


def lockup(name, sym, title):
    wm, ww = wordmark(False)
    body = f'<g id="symbol">{sym}</g>\n<g id="wordmark" transform="translate(312 180.5)">{wm}</g>'
    write(name, 312 + ww + 8, 256, body, title)


if __name__ == "__main__":
    write("e1-acisal-symbol.svg", 256, 256, e1(), "SafeLoop E1 açısal SL döngü")
    write("e2-eskiz-symbol.svg", 256, 256, e2(), "SafeLoop E2 eskize sadık SL")
    lockup("e1-acisal-lockup.svg", e1(), "SafeLoop E1 lockup")
    lockup("e2-eskiz-lockup.svg", e2(), "SafeLoop E2 lockup")
    print("ok")
