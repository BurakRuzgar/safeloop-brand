"""SafeLoop token üretici (Aşama 5).

Tek kaynak: bu dosya. Çıktılar (tokens/ altında):
  safeloop.tokens.json  W3C DTCG biçimi (primitive + semantic light/dark)
  safeloop.tokens.css   CSS değişkenleri (açık, koyu, sistem tercihi)
  kontrast.md           semantic çiftlerin WCAG kontrast raporu
Çalıştırma: python build_tokens.py
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- primitives
# Aşama 4'te onaylı renkler + koyu tema için türetilmiş tonlar.
P = {
    # onaylı marka
    "lacivert": "#0F1B2D",
    "turkuaz": "#1FC7B4",
    "turkuaz-koyu": "#0B7C71",
    "arduvaz": "#566275",
    "cizgi": "#DDE3EA",
    "kagit": "#F5F7FA",
    "beyaz": "#FFFFFF",
    # onaylı durum (açık tema)
    "basarili": "#1B7741", "basarili-zemin": "#E5F3EA",
    "uyari": "#A8570A", "uyari-zemin": "#FCF0E1",
    "hata": "#C0303C", "hata-zemin": "#FBE9EB",
    # türetilmiş: lacivert ailesi (koyu tema + hover/active)
    "lacivert-950": "#0A1320",  # koyu tema uygulama zemini
    "lacivert-800": "#17263B",  # koyu tema yükseltilmiş yüzey / açık tema hover
    "lacivert-700": "#22344D",  # koyu tema kenarlık
    "lacivert-600": "#2E4361",  # açık tema active
    # türetilmiş: nötr
    "sis": "#EEF1F5",           # açık tema input/kuyu zemini
    "duman": "#7A8699",         # açık tema placeholder (yalnız büyük/ikincil)
    "buz": "#E8EDF3",           # koyu tema ana metin (saf beyaz değil)
    "gri-mavi": "#A3AEBD",      # koyu tema ikincil metin
    "gri-mavi-koyu": "#7D8A9D", # koyu tema placeholder
    # türetilmiş: turkuaz hover/active
    "turkuaz-acik": "#4FD6C6",
    "turkuaz-hover": "#19B3A2",
    "turkuaz-koyu-hover": "#096A61",
    "turkuaz-zemin": "#E8F6F4",      # açık tema aktif etiket zemini
    # türetilmiş: koyu tema durum renkleri
    "basarili-acik": "#5CC98A", "basarili-zemin-koyu": "#10291C",
    "uyari-acik": "#F0A54E", "uyari-zemin-koyu": "#2E1F0D",
    "hata-acik": "#F27A84", "hata-zemin-koyu": "#2F1419",
}

def ref(name):
    return "{color." + name + "}"

# ----------------------------------------------------------- semantic colors
# (token adı, açık, koyu, açıklama)
SEM = [
    ("bg-app",            "kagit",        "lacivert-950", "Uygulama arka planı"),
    ("bg-surface",        "beyaz",        "lacivert",     "Kart, panel, tablo"),
    ("bg-surface-raised", "beyaz",        "lacivert-800", "Modal, menü, açılır pencere"),
    ("bg-subtle",         "sis",          "lacivert-800", "Input, kuyu, satır hover"),
    ("bg-inverse",        "lacivert",     "buz",          "Ters zemin (üst bar, tooltip)"),

    ("text-primary",      "lacivert",     "buz",          "Ana metin, başlık"),
    ("text-secondary",    "arduvaz",      "gri-mavi",     "İkincil metin, etiket"),
    ("text-tertiary",     "duman",        "gri-mavi-koyu","Placeholder, pasif (yalnız ≥ 3:1 gereken yerler)"),
    ("text-inverse",      "beyaz",        "lacivert",     "Ters zemin üstündeki metin"),
    ("text-link",         "turkuaz-koyu", "turkuaz",      "Bağlantı ve aksan metni"),
    ("text-link-hover",   "turkuaz-koyu-hover", "turkuaz-acik", "Bağlantı hover"),

    ("border-default",    "cizgi",        "lacivert-700", "Kenarlık, ayraç"),
    ("border-strong",     "arduvaz",      "gri-mavi-koyu","Input kenarlığı (≥ 3:1)"),
    ("border-focus",      "turkuaz-koyu", "turkuaz",      "Odak halkası"),

    # Birincil eylem: açıkta Lacivert, koyuda ters (logo ters kutu mantığı)
    ("action-primary-bg",        "lacivert",     "buz",       "Birincil buton zemini"),
    ("action-primary-bg-hover",  "lacivert-800", "beyaz",     "Birincil buton hover"),
    ("action-primary-bg-active", "lacivert-600", "cizgi",     "Birincil buton basılı"),
    ("action-primary-text",      "beyaz",        "lacivert",  "Birincil buton metni"),
    # Vurgu eylemi: ekranda tek; her iki temada Turkuaz + Lacivert metin
    ("action-accent-bg",         "turkuaz",       "turkuaz",       "Vurgu butonu (ekranda tek)"),
    ("action-accent-bg-hover",   "turkuaz-hover", "turkuaz-acik",  "Vurgu butonu hover"),
    ("action-accent-text",       "lacivert",      "lacivert",      "Vurgu butonu metni"),
    # İkincil eylem: çerçeveli
    ("action-secondary-bg",      "beyaz",        "lacivert",     "İkincil buton zemini"),
    ("action-secondary-border",  "cizgi",        "lacivert-700", "İkincil buton kenarı"),
    ("action-secondary-text",    "lacivert",     "buz",          "İkincil buton metni"),

    # Durum anlamı: AKTİF = Turkuaz, KAPANDI = Başarılı yeşili. Karıştırılmaz.
    ("state-active",      "turkuaz-koyu", "turkuaz",       "Aktif / devam eden (metin, ikon)"),
    ("state-active-mark", "turkuaz-koyu", "turkuaz",       "Aktif sekme çizgisi, ilerleme, nokta (beyazda 3:1 için açıkta Koyu)"),
    ("state-active-fill", "turkuaz",      "turkuaz",       "Geniş dolgu: grafik alanı, ilerleme çubuğu (yanında metin şart)"),
    ("state-active-bg",   "turkuaz-zemin",          "lacivert-800",  "Aktif etiket zemini"),
    ("state-done",        "basarili",     "basarili-acik", "Yalnız tamamlandı / kapandı"),
    ("state-done-bg",     "basarili-zemin","basarili-zemin-koyu", "Kapandı etiket zemini"),

    ("status-success",    "basarili",     "basarili-acik", "Başarılı mesaj (= state-done)"),
    ("status-success-bg", "basarili-zemin","basarili-zemin-koyu", ""),
    ("status-warning",    "uyari",        "uyari-acik",    "Uyarı (yalnız arayüz)"),
    ("status-warning-bg", "uyari-zemin",  "uyari-zemin-koyu", ""),
    ("status-error",      "hata",         "hata-acik",     "Hata"),
    ("status-error-bg",   "hata-zemin",   "hata-zemin-koyu", ""),
    ("status-info",       "lacivert",     "buz",           "Bilgi (ayrı mavi yok)"),
    ("status-info-bg",    "sis",          "lacivert-800",  ""),

    ("logo-fill",         "lacivert",     "beyaz",         "Logo rengi (koyuda ters kutu dosyaları)"),
]

OVERLAY = {"light": "rgba(15, 27, 45, 0.48)", "dark": "rgba(4, 8, 14, 0.64)"}

# -------------------------------------------------------- non-color scales
SPACE = {"0": 0, "1": 2, "2": 4, "3": 8, "4": 12, "5": 16, "6": 20, "7": 24,
         "8": 32, "9": 40, "10": 48, "11": 64, "12": 80}
FONT_FAMILY = {
    "display": '"Plus Jakarta Sans", Inter, system-ui, sans-serif',
    "body": "Inter, system-ui, sans-serif",
    "mono": '"JetBrains Mono", ui-monospace, "SFMono-Regular", Consolas, monospace',
}
FONT_SIZE = {"xs": 12, "base": 15, "md": 19, "lg": 23, "xl": 29, "2xl": 37, "3xl": 46}
FONT_WEIGHT = {"normal": 400, "medium": 500, "semibold": 600, "bold": 700, "extrabold": 800}
LINE_HEIGHT = {"tight": 1.2, "snug": 1.35, "normal": 1.5, "relaxed": 1.65}
LETTER_SPACING = {"tight": "-0.02em", "normal": "0", "wide": "0.06em"}
RADIUS = {"sm": "4px", "md": "8px", "lg": "12px", "xl": "16px", "full": "9999px"}
SHADOW = {
    "light": {
        "sm": "0 1px 2px rgba(15, 27, 45, 0.06)",
        "md": "0 2px 8px rgba(15, 27, 45, 0.08), 0 1px 2px rgba(15, 27, 45, 0.04)",
        "lg": "0 12px 32px rgba(15, 27, 45, 0.12), 0 2px 6px rgba(15, 27, 45, 0.06)",
        "focus": "0 0 0 2px #FFFFFF, 0 0 0 4px #0B7C71",
    },
    "dark": {
        "sm": "0 1px 2px rgba(0, 0, 0, 0.40)",
        "md": "0 2px 8px rgba(0, 0, 0, 0.45)",
        "lg": "0 12px 32px rgba(0, 0, 0, 0.55)",
        "focus": "0 0 0 2px #0F1B2D, 0 0 0 4px #1FC7B4",
    },
}
DURATION = {"instant": "50ms", "fast": "150ms", "normal": "250ms", "slow": "400ms"}
EASING = {"default": "cubic-bezier(0.4, 0, 0.2, 1)", "in": "cubic-bezier(0.4, 0, 1, 1)",
          "out": "cubic-bezier(0, 0, 0.2, 1)"}
BREAKPOINT = {"sm": "375px", "md": "768px", "lg": "1024px", "xl": "1280px", "2xl": "1536px"}
LAYOUT = {"content": "720px", "wide": "1120px", "page": "1440px", "sidebar": "264px", "topbar": "56px"}

# ------------------------------------------------------------- contrast
def lum(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)

# (ön, zemin, gereken, not)
CHECKS = [
    ("text-primary", "bg-app", 4.5, "metin"),
    ("text-primary", "bg-surface", 4.5, "metin"),
    ("text-secondary", "bg-app", 4.5, "metin"),
    ("text-secondary", "bg-surface", 4.5, "metin"),
    ("text-secondary", "bg-subtle", 4.5, "metin"),
    ("text-tertiary", "bg-surface", 3.0, "placeholder / pasif"),
    ("text-link", "bg-app", 4.5, "metin"),
    ("text-link", "bg-surface", 4.5, "metin"),
    ("text-inverse", "bg-inverse", 4.5, "metin"),
    ("border-strong", "bg-surface", 3.0, "UI kenarı"),
    ("border-focus", "bg-surface", 3.0, "odak halkası"),
    ("action-primary-text", "action-primary-bg", 4.5, "buton"),
    ("action-primary-text", "action-primary-bg-hover", 4.5, "buton"),
    ("action-accent-text", "action-accent-bg", 4.5, "buton"),
    ("action-accent-text", "action-accent-bg-hover", 4.5, "buton"),
    ("action-secondary-text", "action-secondary-bg", 4.5, "buton"),
    ("state-active", "bg-surface", 4.5, "metin"),
    ("state-active", "state-active-bg", 4.5, "etiket"),
    ("state-active-mark", "bg-surface", 3.0, "grafik"),
    ("state-done", "bg-surface", 4.5, "metin"),
    ("state-done", "state-done-bg", 4.5, "etiket"),
    ("status-warning", "status-warning-bg", 4.5, "etiket"),
    ("status-warning", "bg-surface", 4.5, "metin"),
    ("status-error", "status-error-bg", 4.5, "etiket"),
    ("status-error", "bg-surface", 4.5, "metin"),
    ("status-info", "status-info-bg", 4.5, "etiket"),
]

# ---------------------------------------------------------------- build
def resolve(theme):
    i = 1 if theme == "light" else 2
    return {s[0]: P[s[i]] for s in SEM}

def build_json():
    def dim(v): return {"$type": "dimension", "$value": f"{v}px"}
    doc = {
        "$description": "SafeLoop design tokens (W3C DTCG). Kaynak: tokens/src/build_tokens.py",
        "color": {k: {"$type": "color", "$value": v} for k, v in P.items()},
        "space": {k: dim(v) for k, v in SPACE.items()},
        "font": {
            "family": {k: {"$type": "fontFamily", "$value": v} for k, v in FONT_FAMILY.items()},
            "size": {k: dim(v) for k, v in FONT_SIZE.items()},
            "weight": {k: {"$type": "fontWeight", "$value": v} for k, v in FONT_WEIGHT.items()},
            "line-height": {k: {"$type": "number", "$value": v} for k, v in LINE_HEIGHT.items()},
            "letter-spacing": {k: {"$type": "dimension", "$value": v} for k, v in LETTER_SPACING.items()},
        },
        "radius": {k: {"$type": "dimension", "$value": v} for k, v in RADIUS.items()},
        "duration": {k: {"$type": "duration", "$value": v} for k, v in DURATION.items()},
        "easing": {k: {"$type": "cubicBezier", "$value": v} for k, v in EASING.items()},
        "breakpoint": {k: {"$type": "dimension", "$value": v} for k, v in BREAKPOINT.items()},
        "layout": {k: {"$type": "dimension", "$value": v} for k, v in LAYOUT.items()},
        "theme": {},
    }
    for t, i in (("light", 1), ("dark", 2)):
        sem = {}
        for s in SEM:
            e = {"$type": "color", "$value": ref(s[i])}
            if s[3]:
                e["$description"] = s[3]
            sem[s[0]] = e
        sem["overlay"] = {"$type": "color", "$value": OVERLAY[t]}
        doc["theme"][t] = {"color": sem,
                           "shadow": {k: {"$type": "shadow", "$value": v} for k, v in SHADOW[t].items()}}
    (OUT / "safeloop.tokens.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def theme_block(theme, indent):
    pad = " " * indent
    lines = [f"{pad}color-scheme: {theme};"]
    i = 1 if theme == "light" else 2
    for s in SEM:
        lines.append(f"{pad}--sl-color-{s[0]}: var(--sl-{s[i]});")
    lines.append(f"{pad}--sl-color-overlay: {OVERLAY[theme]};")
    for k, v in SHADOW[theme].items():
        lines.append(f"{pad}--sl-shadow-{k}: {v};")
    return "\n".join(lines)

def build_css():
    o = ["/* SafeLoop design tokens — Aşama 5",
         "   Üretici: tokens/src/build_tokens.py (elle düzenlemeyin)",
         "   Önek: --sl-  ·  Bileşenler yalnız --sl-color-* semantic token'larını kullanır;",
         "   primitive (--sl-lacivert vb.) doğrudan kullanılmaz.",
         "   Tema: <html data-theme=\"dark\"> ya da sistem tercihi. */", "",
         ":root {", "  /* primitive renkler */"]
    o += [f"  --sl-{k}: {v};" for k, v in P.items()]
    o += ["", "  /* boşluk (4 px taban) */"]
    o += [f"  --sl-space-{k}: {v}{'px' if v else ''};" for k, v in SPACE.items()]
    o += ["", "  /* tipografi */"]
    o += [f"  --sl-font-family-{k}: {v};" for k, v in FONT_FAMILY.items()]
    o += [f"  --sl-font-size-{k}: {v / 16:.4g}rem; /* {v}px */" for k, v in FONT_SIZE.items()]
    o += [f"  --sl-font-weight-{k}: {v};" for k, v in FONT_WEIGHT.items()]
    o += [f"  --sl-line-height-{k}: {v};" for k, v in LINE_HEIGHT.items()]
    o += [f"  --sl-letter-spacing-{k}: {v};" for k, v in LETTER_SPACING.items()]
    o += ["", "  /* biçim, hareket, yerleşim */"]
    o += [f"  --sl-radius-{k}: {v};" for k, v in RADIUS.items()]
    o += [f"  --sl-duration-{k}: {v};" for k, v in DURATION.items()]
    o += [f"  --sl-easing-{k}: {v};" for k, v in EASING.items()]
    o += [f"  --sl-max-width-{k}: {v};" for k, v in LAYOUT.items() if k in ("content", "wide", "page")]
    o += [f"  --sl-size-{k}: {v};" for k, v in LAYOUT.items() if k in ("sidebar", "topbar")]
    o += ["  /* kırılım noktaları CSS değişkeniyle media query'de çalışmaz; referans: */"]
    o += ["  /* " + " · ".join(f"{k} {v}" for k, v in BREAKPOINT.items()) + " */"]
    o += ["", "  /* açık tema (varsayılan) */", theme_block("light", 2), "}", ""]
    o += ['[data-theme="light"] {', theme_block("light", 2), "}", ""]
    o += ['[data-theme="dark"] {', theme_block("dark", 2), "}", ""]
    o += ["@media (prefers-color-scheme: dark) {", '  :root:not([data-theme="light"]) {',
          theme_block("dark", 4), "  }", "}", ""]
    o += ["@media (prefers-reduced-motion: reduce) {", "  :root {"]
    o += [f"    --sl-duration-{k}: 0ms;" for k in DURATION]
    o += ["  }", "}", ""]
    (OUT / "safeloop.tokens.css").write_text("\n".join(o), encoding="utf-8")

def build_report():
    fails = []
    o = ["# SafeLoop · Token kontrast raporu", "",
         "Üretici: `src/build_tokens.py`. WCAG 2.1: metin 4.5:1, UI/grafik 3:1.", "",
         "| Ön | Zemin | Açık | Koyu | Gereken | Tür |", "|---|---|---|---|---|---|"]
    L, D = resolve("light"), resolve("dark")
    for fg, bg, need, kind in CHECKS:
        cells = []
        for t, m in (("açık", L), ("koyu", D)):
            r = ratio(m[fg], m[bg])
            ok = r >= need
            if not ok:
                fails.append(f"{t}: {fg} / {bg} = {r:.2f}")
            cells.append(f"{r:.1f}:1 {'✓' if ok else '✗'}")
        o.append(f"| {fg} | {bg} | {cells[0]} | {cells[1]} | {need}:1 | {kind} |")
    o += ["", "**Sonuç:** " + ("tüm çiftler geçti." if not fails else "KALAN: " + "; ".join(fails)), ""]
    (OUT / "kontrast.md").write_text("\n".join(o), encoding="utf-8")
    return fails

if __name__ == "__main__":
    build_json()
    build_css()
    fails = build_report()
    print("FAIL:" if fails else "OK", *fails, sep="\n  ")
