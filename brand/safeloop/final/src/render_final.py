"""SafeLoop · Aşama 6 PNG/ICO seti. Önce build_final.py çalıştırılır.
Render: logo-design skill'inin render_png.py'si (headless Chrome).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SVG = os.path.join(HERE, "..", "svg")
PNG = os.path.join(HERE, "..", "png")
os.makedirs(PNG, exist_ok=True)
RENDER = os.path.expanduser("~/.claude/skills/logo-design/scripts/render_png.py")


def run(*args):
    subprocess.run([sys.executable, RENDER, *args], check=True)


def png(src, out, w, h=None):
    run(os.path.join(SVG, src), "-o", os.path.join(PNG, out), "--width", str(w), "--height", str(h or w))


man = {m["file"]: (m["w"], m["h"]) for m in json.load(open(os.path.join(HERE, "manifest.json")))["files"]}

# --- web ikonları: 16–48 px küçük kesim, 64 px+ ana kesim
png("safeloop-sembol-kucuk-renkli.svg", "favicon-16.png", 16)
png("safeloop-sembol-kucuk-renkli.svg", "favicon-32.png", 32)
run(os.path.join(SVG, "favicon.svg"), "--ico", os.path.join(PNG, "favicon.ico"), "--ico-sizes", "16", "32", "48")
png("safeloop-sembol-kare.svg", "apple-touch-icon.png", 180)          # iOS köşeyi kendisi yuvarlar
png("safeloop-sembol-renkli.svg", "icon-192.png", 192)                 # PWA "any"
png("safeloop-sembol-renkli.svg", "icon-512.png", 512)
png("safeloop-sembol-kare.svg", "icon-maskable-512.png", 512)          # PWA "maskable" (güvenli alan %80)

# --- lockup PNG'leri (saydam, sıkı kırpım)
for name in ["yatay", "yatay-imza", "dikey", "dikey-imza", "wordmark"]:
    for col in ["renkli", "siyah", "beyaz"]:
        f = f"safeloop-{name}-{col}.svg"
        w, h = man[f]
        W = 1200 if name.startswith(("yatay", "wordmark")) else 800
        png(f, f.replace(".svg", f"-{W}.png"), W, round(W * h / w))

with open(os.path.join(PNG, "site.webmanifest"), "w", encoding="utf-8") as fh:
    json.dump({
        "name": "SafeLoop", "short_name": "SafeLoop",
        "icons": [
            {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
        "theme_color": "#0F1B2D", "background_color": "#F5F7FA", "display": "standalone",
    }, fh, indent=2, ensure_ascii=False)
print("ok")
