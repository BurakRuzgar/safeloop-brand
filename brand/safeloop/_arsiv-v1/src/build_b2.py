"""B2 · Sonsuz S, güçlendirilmiş döngü: uçlar omurgaya doğru daha çok kıvrılır (B'de 28°, B2'de k°),
S neredeyse kapanıp 8'e döner. Uç kesikleri omurgaya paralel değil radyal kalır (B ile aynı aile).
B dosyalarına dokunmaz. Çalıştır: python build_b2.py [k]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_concepts import arc, stroke, wordmark, svg

OUT = os.path.join(os.path.dirname(__file__), "..")


def sym_b2(k=44, w=34, r=46):
    cx = 128; c1 = 128 - r; c2 = 128 + r
    top = arc(cx, c1, r, k, 90, 0)
    bot = arc(cx, c2, r, -90, 180 + k, 1).split(" A", 1)[1]
    return stroke(top + " A" + bot, w)


if __name__ == "__main__":
    k = float(sys.argv[1]) if len(sys.argv) > 1 else 44
    b = sym_b2(k)
    open(os.path.join(OUT, "b2-sonsuz-s-symbol.svg"), "w", encoding="utf-8").write(
        svg(256, 256, b, "SafeLoop B2 Sonsuz S döngü"))
    wm, ww = wordmark(False)
    body = f'<g id="symbol">{b}</g>\n<g id="wordmark" transform="translate(312 180.5)">{wm}</g>'
    open(os.path.join(OUT, "b2-sonsuz-s-lockup.svg"), "w", encoding="utf-8").write(
        svg(312 + ww + 8, 256, body, "SafeLoop B2 yatay"))
    print("ok", k)
