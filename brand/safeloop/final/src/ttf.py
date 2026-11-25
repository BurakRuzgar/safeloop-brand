"""Bağımlılıksız küçük TrueType okuyucu: metni SVG path'e çevirir (glyf + cmap + hmtx + GPOS kerning).
Yalnız "by Rüzgar Safety" alt imzasını outline'a çevirmek için.
"""
import struct


class TTF:
    def __init__(self, path):
        self.b = open(path, "rb").read()
        n = struct.unpack(">H", self.b[4:6])[0]
        self.t = {}
        for i in range(n):
            tag, _, off, ln = struct.unpack(">4sIII", self.b[12 + 16 * i: 28 + 16 * i])
            self.t[tag.decode()] = (off, ln)
        h = self.t["head"][0]
        self.upm = self.u16(h + 18)
        self.loc_long = self.i16(h + 50) == 1
        self.num_glyphs = self.u16(self.t["maxp"][0] + 4)
        self.num_hm = self.u16(self.t["hhea"][0] + 34)
        os2 = self.t.get("OS/2")
        self.cap = self.i16(os2[0] + 88) if os2 and self.u16(os2[0]) >= 2 else int(self.upm * 0.7)
        self.cmap = self._cmap()
        self.kern = self._gpos_kern()

    def u16(self, o): return struct.unpack(">H", self.b[o:o + 2])[0]
    def i16(self, o): return struct.unpack(">h", self.b[o:o + 2])[0]
    def u32(self, o): return struct.unpack(">I", self.b[o:o + 4])[0]

    # ---------- cmap ----------
    def _cmap(self):
        c = self.t["cmap"][0]
        best = None
        for i in range(self.u16(c + 2)):
            pid, eid, off = struct.unpack(">HHI", self.b[c + 4 + 8 * i: c + 12 + 8 * i])
            fmt = self.u16(c + off)
            if fmt == 12:
                best = (12, c + off)
            elif fmt == 4 and best is None and pid in (0, 3):
                best = (4, c + off)
        fmt, o = best
        m = {}
        if fmt == 4:
            seg = self.u16(o + 6) // 2
            ends, starts = o + 14, o + 16 + 2 * seg
            deltas, ranges = starts + 2 * seg, starts + 4 * seg
            for s in range(seg):
                e, st = self.u16(ends + 2 * s), self.u16(starts + 2 * s)
                d, ro = self.i16(deltas + 2 * s), self.u16(ranges + 2 * s)
                for ch in range(st, e + 1):
                    if ch == 0xFFFF:
                        continue
                    if ro == 0:
                        g = (ch + d) & 0xFFFF
                    else:
                        g = self.u16(ranges + 2 * s + ro + 2 * (ch - st))
                        g = (g + d) & 0xFFFF if g else 0
                    m[ch] = g
        else:
            for i in range(self.u32(o + 12)):
                st, e, g = struct.unpack(">III", self.b[o + 16 + 12 * i: o + 28 + 12 * i])
                for ch in range(st, e + 1):
                    m[ch] = g + ch - st
        return m

    def adv(self, g):
        h = self.t["hmtx"][0]
        return self.u16(h + 4 * min(g, self.num_hm - 1))

    # ---------- glyf ----------
    def _gloc(self, g):
        l = self.t["loca"][0]
        if self.loc_long:
            a, b = self.u32(l + 4 * g), self.u32(l + 4 * g + 4)
        else:
            a, b = 2 * self.u16(l + 2 * g), 2 * self.u16(l + 2 * g + 2)
        return self.t["glyf"][0] + a, b - a

    def contours(self, g):
        """[(x, y, on_curve), ...] listeleri; font koordinatı (y yukarı)."""
        o, ln = self._gloc(g)
        if ln == 0:
            return []
        nc = self.i16(o)
        if nc < 0:
            return self._composite(o)
        p = o + 10
        ends = [self.u16(p + 2 * i) for i in range(nc)]
        p += 2 * nc
        p += 2 + self.u16(p)
        npts = ends[-1] + 1
        flags = []
        while len(flags) < npts:
            fl = self.b[p]; p += 1
            flags.append(fl)
            if fl & 8:
                r = self.b[p]; p += 1
                flags += [fl] * r
        def coords(short, same):
            nonlocal p
            v, out = 0, []
            for fl in flags:
                if fl & short:
                    d = self.b[p]; p += 1
                    v += d if fl & same else -d
                elif not fl & same:
                    v += self.i16(p); p += 2
                out.append(v)
            return out
        xs = coords(2, 16)
        ys = coords(4, 32)
        res, s = [], 0
        for e in ends:
            res.append([(xs[i], ys[i], bool(flags[i] & 1)) for i in range(s, e + 1)])
            s = e + 1
        return res

    def _composite(self, o):
        p, res = o + 10, []
        while True:
            fl, gi = self.u16(p), self.u16(p + 2); p += 4
            if fl & 1:
                dx, dy = self.i16(p), self.i16(p + 2); p += 4
            else:
                dx, dy = struct.unpack(">bb", self.b[p:p + 2]); p += 2
            a, b, c, d = 1, 0, 0, 1
            f2 = lambda q: self.i16(q) / 16384
            if fl & 8:
                a = d = f2(p); p += 2
            elif fl & 0x40:
                a, d = f2(p), f2(p + 2); p += 4
            elif fl & 0x80:
                a, b, c, d = f2(p), f2(p + 2), f2(p + 4), f2(p + 6); p += 8
            for ct in self.contours(gi):
                res.append([(a * x + c * y + dx, b * x + d * y + dy, on) for x, y, on in ct])
            if not fl & 0x20:
                break
        return res

    # ---------- GPOS pair kerning (lookup 2, uzantı 9) ----------
    def _coverage(self, o):
        fmt, m = self.u16(o), {}
        if fmt == 1:
            for i in range(self.u16(o + 2)):
                m[self.u16(o + 4 + 2 * i)] = i
        else:
            for i in range(self.u16(o + 2)):
                s, e, si = struct.unpack(">HHH", self.b[o + 4 + 6 * i: o + 10 + 6 * i])
                for g in range(s, e + 1):
                    m[g] = si + g - s
        return m

    def _classdef(self, o):
        fmt, m = self.u16(o), {}
        if fmt == 1:
            st = self.u16(o + 2)
            for i in range(self.u16(o + 4)):
                m[st + i] = self.u16(o + 6 + 2 * i)
        else:
            for i in range(self.u16(o + 2)):
                s, e, c = struct.unpack(">HHH", self.b[o + 4 + 6 * i: o + 10 + 6 * i])
                for g in range(s, e + 1):
                    m[g] = c
        return m

    def _vr_len(self, vf):
        return 2 * bin(vf & 0xFF).count("1")

    def _xadv(self, o, vf):
        """ValueRecord içinden XAdvance (bit 2)."""
        if not vf & 4:
            return 0
        q = o + 2 * bin(vf & 3).count("1")
        return self.i16(q)

    def _gpos_kern(self):
        pairs, cls = {}, []
        if "GPOS" not in self.t:
            return (pairs, cls)
        g = self.t["GPOS"][0]
        ll = g + self.u16(g + 8)
        for i in range(self.u16(ll)):
            lk = ll + self.u16(ll + 2 + 2 * i)
            typ = self.u16(lk)
            for j in range(self.u16(lk + 4)):
                st = lk + self.u16(lk + 6 + 2 * j)
                t = typ
                if t == 9:
                    t, st = self.u16(st + 2), st + self.u32(st + 4)
                if t != 2:
                    continue
                fmt, cov = self.u16(st), self._coverage(st + self.u16(st + 2))
                vf1, vf2 = self.u16(st + 4), self.u16(st + 6)
                l1, l2 = self._vr_len(vf1), self._vr_len(vf2)
                if fmt == 1:
                    for g1, ci in cov.items():
                        ps = st + self.u16(st + 10 + 2 * ci)
                        for k in range(self.u16(ps)):
                            r = ps + 2 + k * (2 + l1 + l2)
                            pairs.setdefault((g1, self.u16(r)), self._xadv(r + 2, vf1))
                else:
                    c1 = self._classdef(st + self.u16(st + 8))
                    c2 = self._classdef(st + self.u16(st + 10))
                    n2 = self.u16(st + 14)
                    rec = l1 + l2
                    cls.append((cov, c1, c2, n2, st + 16, rec, vf1))
        return (pairs, cls)

    def kern_pair(self, a, b):
        pairs, cls = self.kern
        if (a, b) in pairs:
            return pairs[(a, b)]
        for cov, c1, c2, n2, base, rec, vf1 in cls:
            if a in cov:
                r = base + (c1.get(a, 0) * n2 + c2.get(b, 0)) * rec
                return self._xadv(r, vf1)
        return 0

    # ---------- metin → path ----------
    def text_path(self, text, x, baseline, size, tracking=0.0):
        """SVG path d (y aşağı). tracking: em cinsinden harf arası. Dönüş: (d, genişlik)."""
        s = size / self.upm
        pen, out, prev = 0.0, [], None
        F = lambda v: f"{v:.2f}".rstrip("0").rstrip(".")
        for i, ch in enumerate(text):
            g = self.cmap.get(ord(ch), 0)
            if prev is not None:
                pen += self.kern_pair(prev, g)
            for ct in self.contours(g):
                pts = [(x + (pen + px) * s, baseline - py * s, on) for px, py, on in ct]
                out.append(_contour_d(pts, F))
            pen += self.adv(g) + (tracking * self.upm if i < len(text) - 1 else 0)
            prev = g
        return " ".join(out), pen * s


def _contour_d(pts, F):
    n = len(pts)
    # başlangıç: bir on-curve nokta (yoksa iki off-curve ortası)
    k = next((i for i, p in enumerate(pts) if p[2]), None)
    if k is None:
        a, b = pts[0], pts[1]
        pts = [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, True)] + pts[1:] + pts[:1]
        k, n = 0, len(pts)
    seq = pts[k:] + pts[:k]
    d = [f"M{F(seq[0][0])},{F(seq[0][1])}"]
    i, ctrl = 1, None
    seq = seq + [seq[0]]
    for p in seq[1:]:
        if p[2]:
            if ctrl:
                d.append(f"Q{F(ctrl[0])},{F(ctrl[1])} {F(p[0])},{F(p[1])}")
                ctrl = None
            else:
                d.append(f"L{F(p[0])},{F(p[1])}")
        else:
            if ctrl:
                mx, my = (ctrl[0] + p[0]) / 2, (ctrl[1] + p[1]) / 2
                d.append(f"Q{F(ctrl[0])},{F(ctrl[1])} {F(mx)},{F(my)}")
            ctrl = p
    return "".join(d) + "Z"
