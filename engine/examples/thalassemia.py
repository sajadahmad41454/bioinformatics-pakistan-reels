import sys as _s, os as _o; _s.path.insert(0, _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), ".."))
from eng import *
import eng
from vids import monitor

# ---------- own theme: deep wine background, coral accent ----------
eng.BG = "#12060C"; eng.BGCMAP = LSC.from_list("g", [eng.BG, "#4A1226"])
BG = eng.BG
CORAL = "#FB7185"; RBC = "#E11D48"; RBCL = "#FDA4AF"; PALE = "#F9C9D3"; ALPHA = "#FBBF24"; ROSEC = "#2A0E1A"; LN = "#5B2338"
rng = np.random.default_rng(11)

def rbc(ax, x, y, r, al, ang=0, col=RBC, pale=0.0, z=8):
    """red blood cell seen at an angle: outer disc + lighter centre (biconcave look)"""
    al = min(al, 1)
    if al <= 0.01: return
    c = mixc(col, PALE, pale)
    sq = 0.55 + 0.45 * abs(np.cos(ang))
    ax.add_patch(Ellipse((x, y), 2 * r, 2 * r * sq, angle=np.degrees(ang) * 0.3, fc=to_rgba(c, 0.92 * al), ec=to_rgba(mixc(c, "#7F1D1D", 0.35), al), lw=2, zorder=z))
    ax.add_patch(Ellipse((x, y), r * (0.9 + 0.5 * pale), r * sq * (0.9 + 0.5 * pale), angle=np.degrees(ang) * 0.3, fc=to_rgba(mixc(c, WHITE, 0.35 + 0.3 * pale), 0.7 * al), ec="none", zorder=z + 0.05))

_FL = rng.uniform([0, 0], [1, 1], (26, 2)); _FS = rng.uniform(0.75, 1.15, 26); _FA = rng.uniform(0, 6.28, 26)
def s0(ax, t, lt, a, v):
    # vessel with flowing cells
    y0, y1 = 860, 1400
    ax.add_patch(FancyBboxPatch((40, y0), 1000, y1 - y0, boxstyle="round,pad=0,rounding_size=200", fc=to_rgba("#3B0A18", 0.5 * a), ec=to_rgba(CORAL, 0.5 * a), lw=4, zorder=6))
    for k in range(26):
        x = 80 + ((_FL[k, 0] * 1000 + t * 120 * _FS[k]) % 1000) - 40
        y = y0 + 70 + _FL[k, 1] * (y1 - y0 - 140) + 12 * np.sin(t + k)
        rbc(ax, x, y, 46 * _FS[k], a, ang=_FA[k] + t * 0.8 * _FS[k])
    q = ease(seg(lt, 2.4, 3.2))
    if q > 0:
        pill(ax, 540, 760, 560, 70, ROSEC, a * q, ec=CORAL, lw=2, z=12)
        tx(ax, 540, 760, "hemoglobin carries O₂", 26, WHITE, a * q, z=13)

def globin(ax, x, y, s, col, lab, al, t, ph=0, z=9):
    al = min(al, 1)
    th = np.linspace(0, 2 * np.pi, 120)
    r = s * (1 + 0.08 * np.sin(3 * th + ph) + 0.05 * np.sin(5 * th - t + ph))
    ax.add_patch(Polygon(np.c_[x + r * np.cos(th), y + r * np.sin(th)], closed=True, fc=to_rgba(col, 0.28 * al), ec=to_rgba(col, al), lw=3.5, zorder=z))
    # folded chain hint
    u = np.linspace(0, 1, 90)
    ax.plot(x + s * 0.55 * np.sin(u * 13 + ph) * (1 - u * 0.4), y - s * 0.6 + u * s * 1.2, color=col, lw=2.5, alpha=0.75 * al, zorder=z + 0.1)
    ax.add_patch(Polygon([(x + s * 0.35 + 18 * np.cos(k * np.pi / 3), y + 10 + 18 * np.sin(k * np.pi / 3)) for k in range(6)], closed=True, fc=to_rgba("#B91C1C", al), ec=WHITE, lw=1.5, alpha=al, zorder=z + 0.2))
    pill(ax, x, y, 110, 44, (0.07, 0.02, 0.05, 0.85), al, ec=col, lw=2, z=z + 0.9)
    tx(ax, x, y, lab, 22, col, al, z=z + 1)

def s1(ax, t, lt, a, v):
    cx, cy = 540, 1100; d = 125
    pos = [(-1, 1, ALPHA, "alpha"), (1, -1, ALPHA, "alpha"), (1, 1, CORAL, "beta"), (-1, -1, CORAL, "beta")]
    for k, (sx, sy, c, lab) in enumerate(pos):
        q = pop(lt, 0.3 + k * 0.35 if k < 2 else 3.0 + (k - 2) * 0.35)
        if q <= 0: continue
        globin(ax, cx + sx * d, cy + sy * d * 0.95, 105 * q, c, lab, a, t, ph=k * 1.7)
    tx(ax, 540, 760, "4 chains = 1 hemoglobin", 24, MUTED, a * ease(seg(lt, 3.6, 4.2)), w="semibold")

def chromo(ax, x, y, h, al, z=8):
    al = min(al, 1)
    for dx in (-26, 26):
        ax.add_patch(FancyBboxPatch((x + dx - 22, y - h / 2), 44, h, boxstyle="round,pad=0,rounding_size=22", fc=to_rgba(VIO, 0.35 * al), ec=VIO, lw=3, alpha=al, zorder=z))
    ax.add_patch(Ellipse((x, y + h * 0.18), 70, 26, fc=to_rgba(BG, al), ec="none", zorder=z + 0.1))
    for k, yy in enumerate(np.linspace(y - h / 2 + 30, y + h / 2 - 30, 9)):
        ax.plot([x - 46, x + 46], [yy, yy], color=VIO, lw=3, alpha=al * 0.5, zorder=z + 0.2)

def hbb_gene(ax, x0, y, w, al, t, bad=0.0, z=9):
    ax.plot([x0, x0 + w], [y, y], color=MUTED, lw=4, alpha=al, zorder=z)
    ex = [(0.04, 0.16), (0.36, 0.52), (0.78, 0.96)]
    for k, (f0, f1) in enumerate(ex):
        c = mixc(CORAL, "#7F1D1D", bad) if k == 0 else CORAL
        ax.add_patch(FancyBboxPatch((x0 + f0 * w, y - 34), (f1 - f0) * w, 68, boxstyle="round,pad=0,rounding_size=10", fc=to_rgba(c, 0.55 * al), ec=c, lw=2.5, alpha=al, zorder=z + 0.1))
    tx(ax, x0 + w / 2, y + 70, "HBB gene", 28, WHITE, al, z=z + 1)

def s2(ax, t, lt, a, v):
    chromo(ax, 170, 1090, 420, a * pop(lt, 0.0))
    q = ease(seg(lt, 0.6, 1.4))
    ax.plot([215, 330], [1150, 1150], color=CORAL, lw=2, alpha=a * q, ls="--", zorder=8)
    hbb_gene(ax, 330, 1150, 650 * q + 1, a * q, t)
    p = ease(seg(lt, 1.8, 3.2))
    arrow(ax, 655, 1080, 655, 990, CORAL, a * p, lw=4)
    # chain coming out
    n = int(28 * p)
    for k in range(n):
        x = 380 + k * 20; y = 900 + 26 * np.sin(k * 0.7 + t * 2)
        ax.add_patch(Circle((x, y), 11, fc=to_rgba(CORAL, 0.8 * a), ec=WHITE, lw=1, zorder=10))
    tx(ax, 655, 810, "beta globin", 24, CORAL, a * ease(seg(lt, 2.8, 3.4)), w="semibold")

SEQ = "CCTGTGGGGCAAGG"
def s3(ax, t, lt, a, v):
    m = ease(seg(lt, 0.8, 1.5))
    x0 = 540 - len(SEQ) * 62 / 2 + 31
    for k, b in enumerate(SEQ):
        x = x0 + k * 62; isM = k == 6
        ch = ("A" if m > 0.5 else b) if isM else b
        c = mixc(BCOL[b], CORAL, m) if isM else BCOL[b]
        sc = pop(lt, 0.8) if isM and m > 0 else 1
        card(ax, x - 27 * sc, 1290 - 32 * sc, 54 * sc, 64 * sc, a, ec=c, lw=2.5 if isM else 1.2, z=9, r=10, fc=to_rgba(c, 0.15) if isM else ROSEC)
        tx(ax, x, 1290, ch, 28 * sc, WHITE if (isM and m > 0) else c, a, fam=MONO, z=10)
    tx(ax, 540, 1210, "a change in HBB", 20, CORAL, a * m, w="semibold")
    # production meters: normal vs reduced
    drop = ease(seg(lt, 1.8, 3.2))
    for k, (lab, lev, c) in enumerate([("alpha globin", 1.0, ALPHA), ("beta globin", 1.0 - 0.8 * drop, CORAL)]):
        y = 1040 - k * 150
        tx(ax, 120, y + 45, lab, 22, c, a, ha="left", w="semibold")
        pill(ax, 540, y, 840, 44, LN, a, z=9)
        L = 840 * lev
        if L > 44: pill(ax, 120 + L / 2, y, L, 44, c, a, z=10)
    tx(ax, 540, 730, "less (or no) beta globin made", 24, WHITE, a * ease(seg(lt, 3.0, 3.6)))

_P = rng.uniform(-1, 1, (12, 2)); _PA = rng.uniform(0, 6.28, 12)
def s4(ax, t, lt, a, v):
    for side, (cx, pale, sz, lab) in enumerate([(290, 0.0, 1.0, "typical"), (790, 0.75, 0.66, "thalassemia")]):
        q = ease(seg(lt, 0.2 + side * 1.2, 0.9 + side * 1.2))
        if q <= 0: continue
        card(ax, cx - 230, 820, 460, 560, a * q, ec=LN, z=7, fc=ROSEC)
        for k in range(9):
            x = cx + _P[k, 0] * 140; y = 1070 + _P[k, 1] * 170
            rbc(ax, x, y, 52 * sz, a * q, ang=_PA[k] + 0.4 * np.sin(t * 0.6 + k), pale=pale)
        tx(ax, cx, 1335, lab, 24, CORAL if side else WHITE, a * q, z=10)
    tx(ax, 790, 780, "smaller, paler", 20, CORAL, a * ease(seg(lt, 2.4, 3.0)), w="semibold")

def person(ax, x, y, s, col, al, z=10):
    al = min(al, 1)
    if al <= 0.01: return
    ax.add_patch(Circle((x, y + 40 * s), 26 * s, fc=to_rgba(col, 0.3 * al), ec=col, lw=3, alpha=al, zorder=z))
    ax.add_patch(FancyBboxPatch((x - 40 * s, y - 50 * s), 80 * s, 70 * s, boxstyle=f"round,pad=0,rounding_size={30*s}", fc=to_rgba(col, 0.3 * al), ec=col, lw=3, alpha=al, zorder=z))

def copies(ax, x, y, c1, c2, al, z=11):
    for k, c in enumerate((c1, c2)):
        ax.add_patch(FancyBboxPatch((x - 46 + k * 52, y - 14), 40, 28, boxstyle="round,pad=0,rounding_size=8", fc=to_rgba(c, 0.85 * al), ec=WHITE, lw=1.2, alpha=al, zorder=z))

OK_ = "#34D399"
def s5(ax, t, lt, a, v):
    # lines 5..8
    L6 = v.T[6] - v.T[5]; L7 = v.T[7] - v.T[5]; L8 = v.T[8] - v.T[5]
    carr = ease(seg(lt, L6, L6 + 0.8))
    for k, x in enumerate((300, 780)):
        q = pop(lt, 0.3 + k * 0.3)
        if q <= 0: continue
        person(ax, x, 1280, 1.4 * q, mixc(SKY, GOLD, carr), a)
        copies(ax, x, 1150, OK_, mixc(OK_, CORAL, carr), a)
        tx(ax, x, 1405, "parent", 20, MUTED, a, w="normal")
    tx(ax, 540, 1150, "+", 40, MUTED, a)
    tx(ax, 540, 1080, "carriers", 22, GOLD, a * carr * (1 - ease(seg(lt, L7, L7 + 0.4))), w="semibold")
    kids = [(CORAL, CORAL, "thalassemia major", "1 in 4", CORAL), (OK_, CORAL, "carrier", "1 in 2", GOLD), (CORAL, OK_, "carrier", "", GOLD), (OK_, OK_, "neither", "1 in 4", OK_)]
    for k, (c1, c2, lab, odds, col) in enumerate(kids):
        st = L7 + 0.3 if k == 0 else (L8 + 0.1 + (k - 1) * 0.35 if k < 3 else L8 + 2.6)
        q = pop(lt, st)
        if q <= 0: continue
        x = 165 + k * 250; y = 860
        person(ax, x, y, 0.95 * q, col, a)
        copies(ax, x, y - 85, c1, c2, a)
        tx(ax, x, y - 135, lab, 17 if k == 0 else 19, col, a, w="semibold")
        if odds: tx(ax, x + (125 if k == 1 else 0), y - 180, odds, 26, WHITE, a)
    # connector lines
    q = ease(seg(lt, L7, L7 + 0.6))
    if q > 0:
        ax.plot([300, 780], [1010, 1010], color=LN, lw=3, alpha=a * q, zorder=8)
        ax.plot([540, 540], [1010, 1050], color=LN, lw=3, alpha=a * q, zorder=8)

def s9(ax, t, lt, a, v):
    # blood drop + Pakistan card
    q = pop(lt, 0.2)
    if q > 0:
        th = np.linspace(0, 2 * np.pi, 160)
        r = 1 - 0.0 * th; xs = 140 * q * np.sin(th) * (1 - 0.0); ys = 140 * q * (np.cos(th))
        # teardrop
        P = np.c_[540 + 130 * q * np.sin(th) * np.sin(th / 2) ** 1.0, 1150 + 170 * q * np.cos(th)]
        ax.add_patch(Polygon(P, closed=True, fc=to_rgba(RBC, 0.85 * a), ec=RBCL, lw=3, zorder=9))
        ax.add_patch(Ellipse((500, 1080), 40 * q, 70 * q, angle=20, fc=to_rgba(WHITE, 0.35 * a), ec="none", zorder=9.1))
    p = ease(seg(lt, 1.0, 1.6))
    pill(ax, 540, 880, 640, 84, ROSEC, a * p, ec=CORAL, lw=2.5, z=10)
    tx(ax, 540, 880, "common in Pakistan", 32, WHITE, a * p, z=11)
    tx(ax, 540, 790, "inherited blood disorder", 22, MUTED, a * p, w="normal")

REF = "GGTTGGTATCAAGGTTACAAG"
def s10(ax, t, lt, a, v):
    monitor(ax, 90, 790, 900, 640, a, title="HBB_sample.bam", z=8)
    col_ = 10; x0 = 150; dx = 37.5
    tx(ax, x0 - 20, 1320, "ref", 16, MUTED, a, ha="right", w="normal", fam=MONO, z=10)
    for j, b in enumerate(REF):
        tx(ax, x0 + j * dx, 1320, b, 22, BCOL[b], a, fam=MONO, z=10)
    reads = [(0, 14), (3, 20), (6, 21), (1, 12), (8, 21), (4, 17)]
    for i, (s, e) in enumerate(reads):
        q = ease(seg(lt, 0.3 + i * 0.3, 0.8 + i * 0.3))
        if q <= 0: continue
        y = 1250 - i * 52; xo = (1 - q) * 300
        for j in range(s, e):
            b = REF[j]; mm = (j == col_ and i % 2 == 0)
            b = "C" if mm else b
            tx(ax, x0 + j * dx + xo, y, b, 22, CORAL if mm else mixc(BCOL[b], MUTED, 0.45), a * q, fam=MONO, z=10)
    h = ease(seg(lt, 3.2, 3.8))
    if h > 0:
        X = x0 + col_ * dx
        ax.add_patch(FancyBboxPatch((X - 18, 950), 36, 400, boxstyle="round,pad=0,rounding_size=14", fc=to_rgba(CORAL, 0.15 * a * h), ec=to_rgba(CORAL, a * h), lw=2.5, zorder=9))
        pill(ax, 540, 880, 380, 56, CORAL, a * h, z=11)
        tx(ax, 540, 880, "variant found", 24, BG, a * h, z=12)

def tube(ax, x, y, s, al, fill, z=9):
    al = min(al, 1)
    ax.add_patch(FancyBboxPatch((x - 34 * s, y - 150 * s), 68 * s, 300 * s, boxstyle=f"round,pad=0,rounding_size={34*s}", fc=to_rgba(WHITE, 0.06 * al), ec=to_rgba(WHITE, 0.8 * al), lw=3, zorder=z))
    hh = 260 * s * fill
    if hh > 10: ax.add_patch(FancyBboxPatch((x - 26 * s, y - 142 * s), 52 * s, hh, boxstyle=f"round,pad=0,rounding_size={24*s}", fc=to_rgba(RBC, 0.9 * al), ec="none", zorder=z + 0.1))
    ax.add_patch(Rectangle((x - 40 * s, y + 150 * s), 80 * s, 30 * s, fc=to_rgba(VIO, al), zorder=z + 0.2))

def s11(ax, t, lt, a, v):
    tube(ax, 330, 1110, 1.0, a, ease(seg(lt, 0.1, 1.0)))
    q = pop(lt, 1.2)
    if q > 0:
        arrow(ax, 420, 1110, 540, 1110, CORAL, a, lw=4)
        card(ax, 580, 960, 380, 300, a, ec=CORAL, z=9, fc=ROSEC, lw=2.5)
        tx(ax, 770, 1200, "blood test", 22, MUTED, a, w="normal", z=10)
        tx(ax, 770, 1110, "carrier?", 34, WHITE, a, z=10)
        tx(ax, 770, 1020, "yes  /  no", 26, GOLD, a, z=10, w="semibold")

def s12(ax, t, lt, a, v):
    for k, x in enumerate((420, 660)):
        person(ax, x, 1200, 1.5, [SKY, CORAL][k], a * pop(lt, 0.1 + 0.2 * k))
    q = ease(seg(lt, 0.8, 1.6))
    tx(ax, 540, 940, "Know your", 48, WHITE, a * q)
    tx(ax, 540, 860, "carrier status.", 54, CORAL, a * ease(seg(lt, 1.2, 2.0)))
    tx(ax, 540, 770, "ask a doctor or genetic counselor", 22, MUTED, a * ease(seg(lt, 2.0, 2.6)), w="normal")

def V():
    return Video("v_thal", "GENETICS", CORAL,
                 [(s0, 0, 0), (s1, 1, 1), (s2, 2, 2), (s3, 3, 3), (s4, 4, 4), (s5, 5, 8), (s9, 9, 9), (s10, 10, 10), (s11, 11, 11), (s12, 12, 12)],
                 [(0, 0, "INSIDE YOUR BLOOD", "Hemoglobin"), (1, 1, "ONE MOLECULE", "Four chains"), (2, 2, "THE BLUEPRINT", "The HBB gene"),
                  (3, 3, "WHAT GOES WRONG", "Beta thalassemia"), (4, 4, "THE RESULT", "Anemia"), (5, 6, "HOW IT'S INHERITED", "Two copies"),
                  (7, 8, "TWO CARRIERS", "Each pregnancy"), (9, 9, "CLOSE TO HOME", "Pakistan"), (10, 10, "BIOINFORMATICS", "Reading the gene"),
                  (11, 11, "SIMPLE STEP", "Carrier screening"), (12, 12, "THE TAKEAWAY", "Plan ahead")], gap=0.35, start=0.4, outro=2.8)

if __name__ == "__main__":
    V().main(sys.argv, seed=1)
