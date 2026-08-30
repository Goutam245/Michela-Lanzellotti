# -*- coding: utf-8 -*-
"""Genera i motivi SVG del sito: rosone, merletto (orlo), trine per le schede."""
import math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg")
os.makedirs(OUT, exist_ok=True)


def P(x, y):
    return f"{x:.2f} {y:.2f}"


def pol(cx, cy, r, a):
    return (cx + r * math.cos(a), cy + r * math.sin(a))


# ---------------------------------------------------------------- ROSONE 400x400
CX = CY = 200.0


def rosone():
    p = []
    # cornice esterna: 36 archetti (merlatura)
    n, r1, r2 = 36, 190.0, 180.0
    d = []
    for i in range(n):
        a0 = 2 * math.pi * i / n - math.pi / 2
        a1 = 2 * math.pi * (i + 1) / n - math.pi / 2
        x0, y0 = pol(CX, CY, r2, a0)
        x1, y1 = pol(CX, CY, r2, a1)
        am = (a0 + a1) / 2
        xm, ym = pol(CX, CY, r1, am)
        if i == 0:
            d.append(f"M{P(x0, y0)}")
        d.append(f"Q{P(xm, ym)} {P(x1, y1)}")
    d.append("Z")
    p.append(f'<path class="rw-scallop" d="{" ".join(d)}"/>')
    # cerchi concentrici
    for r in (168.0, 150.0, 96.0, 54.0, 26.0):
        p.append(f'<circle class="rw-ring" cx="200" cy="200" r="{r:.0f}"/>')
    # 12 colonnine radiali (solo la ghiera esterna, 96 -> 150)
    N = 12
    for i in range(N):
        a = 2 * math.pi * i / N - math.pi / 2
        x0, y0 = pol(CX, CY, 96.0, a)
        x1, y1 = pol(CX, CY, 150.0, a)
        p.append(f'<line class="rw-spoke" x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}"/>')
    # petali a sesto acuto fra le colonnine
    for i in range(N):
        a0 = 2 * math.pi * i / N - math.pi / 2
        a1 = 2 * math.pi * (i + 1) / N - math.pi / 2
        am = (a0 + a1) / 2
        bx0, by0 = pol(CX, CY, 96.0, a0)
        bx1, by1 = pol(CX, CY, 96.0, a1)
        tx, ty = pol(CX, CY, 150.0, am)
        c0x, c0y = pol(CX, CY, 138.0, a0 + (am - a0) * 0.10)
        c1x, c1y = pol(CX, CY, 138.0, a1 - (a1 - am) * 0.10)
        p.append(f'<path class="rw-petal" d="M{P(bx0, by0)} Q{P(c0x, c0y)} {P(tx, ty)} Q{P(c1x, c1y)} {P(bx1, by1)}"/>')
        mx, my = pol(CX, CY, 118.0, am)
        p.append(f'<circle class="rw-dot" cx="{mx:.2f}" cy="{my:.2f}" r="5.4"/>')
    # rosetta interna: 6 petali tondi nella fascia 54 -> 96
    M = 6
    for i in range(M):
        a0 = 2 * math.pi * i / M - math.pi / 2
        a1 = 2 * math.pi * (i + 1) / M - math.pi / 2
        am = (a0 + a1) / 2
        x0, y0 = pol(CX, CY, 54.0, a0)
        x1, y1 = pol(CX, CY, 54.0, a1)
        tx, ty = pol(CX, CY, 96.0, am)
        c0x, c0y = pol(CX, CY, 92.0, a0 + (am - a0) * 0.30)
        c1x, c1y = pol(CX, CY, 92.0, a1 - (a1 - am) * 0.30)
        p.append(f'<path class="rw-inner" d="M{P(x0, y0)} Q{P(c0x, c0y)} {P(tx, ty)} Q{P(c1x, c1y)} {P(x1, y1)}"/>')
        # occhiello fra i petali
        ex, ey = pol(CX, CY, 72.0, a0)
        p.append(f'<circle class="rw-dot" cx="{ex:.2f}" cy="{ey:.2f}" r="4.2"/>')
    # fiore centrale: 6 piccoli petali entro r=26
    for i in range(6):
        a0 = 2 * math.pi * i / 6 - math.pi / 2
        a1 = 2 * math.pi * (i + 1) / 6 - math.pi / 2
        am = (a0 + a1) / 2
        tx, ty = pol(CX, CY, 26.0, am)
        c0x, c0y = pol(CX, CY, 21.0, am - 0.46)
        c1x, c1y = pol(CX, CY, 21.0, am + 0.46)
        p.append(f'<path class="rw-star" d="M{P(CX, CY)} Q{P(c0x, c0y)} {P(tx, ty)} Q{P(c1x, c1y)} {P(CX, CY)} Z"/>')
    return "\n".join(p)


# ---------------------------------------------------------------- MERLETTO / ORLO
def merletto(w=720.0, unit=72.0, h=56.0):
    """Bordo a festone con archetti e nodi: l'orlo dell'abito."""
    n = int(w / unit)
    out = []
    top = []
    for i in range(n):
        x0 = i * unit
        x1 = x0 + unit
        if i == 0:
            top.append(f"M{P(x0, 4.0)}")
        top.append(f"C{P(x0 + unit * 0.22, h * 0.92)} {P(x1 - unit * 0.22, h * 0.92)} {P(x1, 4.0)}")
    out.append(f'<path class="lc-arc" d="{" ".join(top)}"/>')
    out.append(f'<line class="lc-line" x1="0" y1="4" x2="{w:.0f}" y2="4"/>')
    for i in range(n + 1):
        out.append(f'<circle class="lc-knot" cx="{i * unit:.0f}" cy="4" r="2.6"/>')
    for i in range(n):
        cx = i * unit + unit / 2
        out.append(f'<circle class="lc-drop" cx="{cx:.1f}" cy="{h * 0.60:.1f}" r="3.4"/>')
        out.append(
            f'<path class="lc-leaf" d="M{P(cx, h * 0.60 + 4)} Q{P(cx - 5.5, h * 0.80)} {P(cx, h * 0.97)} '
            f'Q{P(cx + 5.5, h * 0.80)} {P(cx, h * 0.60 + 4)} Z"/>'
        )
    return "\n".join(out)


# ---------------------------------------------------------------- TRINE (schede)
def trina(petals, r_out=86.0, style=0):
    """Piccolo motivo di merletto per le schede senza fotografia."""
    cx = cy = 100.0
    p = []
    p.append(f'<circle class="tr-ring" cx="100" cy="100" r="{r_out:.0f}"/>')
    p.append(f'<circle class="tr-ring" cx="100" cy="100" r="{r_out - 11:.0f}"/>')
    for i in range(petals):
        a0 = 2 * math.pi * i / petals - math.pi / 2
        a1 = 2 * math.pi * (i + 1) / petals - math.pi / 2
        am = (a0 + a1) / 2
        inner = (26.0 if style == 0 else 34.0) if petals >= 8 else 42.0
        x0, y0 = pol(cx, cy, inner, a0)
        x1, y1 = pol(cx, cy, inner, a1)
        tx, ty = pol(cx, cy, r_out - 11, am)
        c0x, c0y = pol(cx, cy, (r_out - 11) * 0.86, a0 + (am - a0) * 0.34)
        c1x, c1y = pol(cx, cy, (r_out - 11) * 0.86, a1 - (a1 - am) * 0.34)
        p.append(f'<path class="tr-petal" d="M{P(x0, y0)} Q{P(c0x, c0y)} {P(tx, ty)} Q{P(c1x, c1y)} {P(x1, y1)} Z"/>')
        sx, sy = pol(cx, cy, r_out - 5.5, am)
        p.append(f'<circle class="tr-dot" cx="{sx:.2f}" cy="{sy:.2f}" r="2.6"/>')
    core = (18.0 if style == 0 else 24.0) if petals >= 8 else 30.0
    p.append(f'<circle class="tr-core" cx="100" cy="100" r="{core:.0f}"/>')
    for i in range(petals * 2):
        a = 2 * math.pi * i / (petals * 2) - math.pi / 2
        x0, y0 = pol(cx, cy, r_out, a)
        x1, y1 = pol(cx, cy, r_out + 9, a)
        p.append(f'<line class="tr-ray" x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}"/>')
    return "\n".join(p)


import re

# normalizza la lunghezza dei tracciati: permette di "accendere" il rosone
# con una sola animazione, identica per ogni elemento.
DRAWN = ("rw-scallop", "rw-ring", "rw-spoke", "rw-petal", "rw-inner", "rw-star",
         "lc-arc", "lc-line", "lc-leaf")


def normalize(svg_markup):
    def add(m):
        tag = m.group(0)
        return tag if 'pathLength' in tag else tag[:-1] + ' pathLength="1"/>'
    return re.sub(r'<(?:path|circle|line)[^>]*class="(?:%s)"[^>]*/>' % "|".join(DRAWN), add, svg_markup)


open(os.path.join(OUT, "rosone.svg"), "w", encoding="utf-8").write(normalize(rosone()))
open(os.path.join(OUT, "merletto.svg"), "w", encoding="utf-8").write(normalize(merletto()))
for i, (n, st) in enumerate([(8, 0), (12, 1), (6, 0), (10, 1)], start=1):
    open(os.path.join(OUT, f"trina{i}.svg"), "w", encoding="utf-8").write(trina(n, style=st))
print("fatto:", sorted(os.listdir(OUT)))
