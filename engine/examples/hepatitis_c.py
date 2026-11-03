import sys as _s, os as _o; _s.path.insert(0, _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), ".."))
from eng import *
import eng

# ---------- own theme: dark umber background, amber accent, lime virus ----------
eng.BG = "#130B04"; eng.BGCMAP = LSC.from_list("g", [eng.BG, "#4A2C0C"]); eng.TEAL = "#F59E0B"; eng.MUTED = "#C9B79C"
BG = eng.BG; MUTED = eng.MUTED
AMB = "#F59E0B"; AMBL = "#FCD34D"; LIV = "#B45309"; LIVL = "#E7A15A"; LIME = "#A3E635"; SCAR = "#78716C"; CARDC = "#24170A"; LN = "#5A3A16"; OKC = "#34D399"; RED = "#F87171"
rng = np.random.default_rng(5)

def chaikin(P, n=4):
    P = np.asarray(P, float)
    for _ in range(n):
        Q = np.roll(P, -1, 0); P = np.stack([0.75 * P + 0.25 * Q, 0.25 * P + 0.75 * Q], 1).reshape(-1, 2)
    return P
LIVER = chaikin([(-0.5, 0.12), (-0.44, 0.3), (-0.22, 0.38), (0.08, 0.34), (0.34, 0.26), (0.52, 0.14), (0.47, 0.06), (0.24, 0.01), (0.04, -0.12), (-0.16, -0.3), (-0.36, -0.34), (-0.49, -0.16)])

def liver(ax, cx, cy, s, al, col=LIV, scar=0.0, t=0, z=8):
    al = min(al, 1)
    if al <= 0.01: return
    P = np.c_[cx + LIVER[:, 0] * s, cy + LIVER[:, 1] * s]
    c = mixc(col, SCAR, scar * 0.6)
    ax.add_patch(Polygon(P, closed=True, fc="none", ec=to_rgba(c, 0.18 * al), lw=26, zorder=z - 0.1))
    ax.add_patch(Polygon(P, closed=True, fc=to_rgba(c, 0.85 * al), ec=to_rgba(LIVL, al), lw=4, zorder=z))
    ax.add_patch(Ellipse((cx - 0.2 * s, cy + 0.16 * s), 0.38 * s, 0.12 * s, angle=8, fc=to_rgba(WHITE, 0.12 * al), ec="none", zorder=z + 0.1))
    ax.plot([cx + 0.02 * s, cx - 0.06 * s], [cy + 0.33 * s, cy - 0.08 * s], color=to_rgba("#7C2D12", 0.7 * al), lw=3, zorder=z + 0.1)
    if scar > 0:
        r = np.random.default_rng(3)
        for k in range(int(14 * scar)):
            x = cx + r.uniform(-0.38, 0.38) * s; y = cy + r.uniform(-0.15, 0.25) * s
            L = r.uniform(0.04, 0.09) * s; a = r.uniform(0, 3.14)
            xs = x + np.linspace(-L, L, 8) * np.cos(a); ys = y + np.linspace(-L, L, 8) * np.sin(a) + r.normal(0, 4, 8)
            ax.plot(xs, ys, color=to_rgba("#E7E5E4", 0.8 * al), lw=4, zorder=z + 0.2, solid_capstyle="round")

def virus(ax, x, y, r, al, t=0, col=LIME, z=12, rna=True):
    al = min(al, 1)
    if al <= 0.01 or r <= 1: return
    for k in range(12):
        a = k * np.pi / 6 + t * 0.4
        ax.plot([x + r * np.cos(a), x + r * 1.28 * np.cos(a)], [y + r * np.sin(a), y + r * 1.28 * np.sin(a)], color=col, lw=max(1, r / 14), alpha=al, zorder=z)
        ax.add_patch(Circle((x + r * 1.33 * np.cos(a), y + r * 1.33 * np.sin(a)), r * 0.11, fc=col, alpha=al, zorder=z))
    ax.add_patch(Circle((x, y), r, fc=to_rgba(col, 0.22 * al), ec=to_rgba(col, al), lw=max(1.5, r / 12), zorder=z + 0.1))
    ax.add_patch(Circle((x, y), r * 0.62, fc=to_rgba("#365314", 0.6 * al), ec=to_rgba(col, 0.6 * al), lw=max(1, r / 25), zorder=z + 0.2))
    if rna:
        u = np.linspace(0, 1, 120); th = u * 5 * np.pi + t
        rr = r * 0.45 * (0.3 + 0.7 * u)
        ax.plot(x + rr * np.cos(th), y + rr * np.sin(th), color=AMBL, lw=max(1, r / 22), alpha=al, zorder=z + 0.3)

def lbl(ax, x, y, s, al, col=WHITE, size=24, z=14, ec=AMB, w=None):
    if al <= 0.01: return
    w = w or (wpx(s, size) * 1.08 + 64)
    pill(ax, x, y, w, size * 2.4, CARDC, al, ec=ec, lw=2, z=z)
    tx(ax, x, y, s, size, col, al, z=z + 1)

def cross(ax, x, y, s, al, z=15):
    for sg in (1, -1): ax.plot([x - s, x + s], [y - s * sg, y + s * sg], color=RED, lw=9, alpha=al, solid_capstyle="round", zorder=z)

def person(ax, x, y, s, col, al, z=10):
    al = min(al, 1)
    if al <= 0.01: return
    ax.add_patch(Circle((x, y + 40 * s), 24 * s, fc=to_rgba(col, 0.35 * al), ec=col, lw=3, alpha=al, zorder=z))
    ax.add_patch(FancyBboxPatch((x - 36 * s, y - 45 * s), 72 * s, 62 * s, boxstyle=f"round,pad=0,rounding_size={26*s}", fc=to_rgba(col, 0.35 * al), ec=col, lw=3, alpha=al, zorder=z))

def syringe(ax, x, y, s, al, ang=0, z=10, fill=0.6, col=RED):
    al = min(al, 1)
    if al <= 0.01: return
    ca, sa = np.cos(ang), np.sin(ang)
    T = lambda px, py: (x + (px * ca - py * sa) * s, y + (px * sa + py * ca) * s)
    body = [T(-120, -26), T(80, -26), T(80, 26), T(-120, 26)]
    ax.add_patch(Polygon(body, closed=True, fc=to_rgba(WHITE, 0.08 * al), ec=to_rgba(WHITE, 0.9 * al), lw=3, zorder=z))
    fl = [T(80 - 190 * fill, -20), T(76, -20), T(76, 20), T(80 - 190 * fill, 20)]
    ax.add_patch(Polygon(fl, closed=True, fc=to_rgba(col, 0.8 * al), ec="none", zorder=z + 0.1))
    ax.plot(*zip(T(80, 0), T(150, 0)), color=WHITE, lw=3, alpha=al, zorder=z)
    ax.plot(*zip(T(-120, 0), T(-180, 0)), color=WHITE, lw=6, alpha=al, zorder=z)
    ax.plot(*zip(T(-180, -34), T(-180, 34)), color=WHITE, lw=6, alpha=al, zorder=z, solid_capstyle="round")
    for k in range(4): ax.plot(*zip(T(-90 + k * 40, 26), T(-90 + k * 40, 12)), color=WHITE, lw=2, alpha=al * 0.7, zorder=z + 0.2)

# ---------------- scenes ----------------
def s0(ax, t, lt, a, v):
    q = pop(lt, 0.1)
    liver(ax, 540, 1110, 760 * max(q, 0.01), a * min(1, q * 2))
    for k in range(5):
        p = ease(seg(lt, 1.0 + k * 0.25, 1.6 + k * 0.25))
        an = k * 1.26 + t * 0.35
        virus(ax, 540 + 330 * np.cos(an), 1110 + 250 * np.sin(an), 28 * p, a * p, t)
    tx(ax, 540, 800, "the liver", 26, MUTED, a * ease(seg(lt, 2.4, 3.0)), w="semibold")

def s1(ax, t, lt, a, v):
    q = pop(lt, 0.1)
    virus(ax, 540, 1120, 190 * q, a, t * 0.5)
    p = ease(seg(lt, 1.0, 1.6))
    if p > 0:
        ax.plot([640, 800], [1150, 1300], color=AMBL, lw=2, alpha=a * p, zorder=13)
        lbl(ax, 860, 1330, "RNA genome", a * p, AMBL, 22, ec=AMBL)
    p2 = ease(seg(lt, 2.6, 3.2))
    lbl(ax, 540, 820, "spreads through infected blood", a * p2, WHITE, 26)

def s2(ax, t, lt, a, v):
    xs = [210, 540, 870]
    for k, x in enumerate(xs):
        q = pop(lt, 0.1 + k * 0.5)
        if q <= 0: continue
        card(ax, x - 140, 960, 280, 330, a, ec=LN, z=8, fc=CARDC)
        y = 1150
        if k == 0:   # plate
            ax.add_patch(Circle((x, y), 80 * q, fc=to_rgba(WHITE, 0.1 * a), ec=WHITE, lw=3, alpha=a, zorder=10))
            ax.add_patch(Circle((x, y), 50 * q, fc="none", ec=MUTED, lw=2, alpha=a, zorder=10))
            lab = "food"
        elif k == 1:  # water drop
            th = np.linspace(0, 2 * np.pi, 120)
            P = np.c_[x + 70 * q * np.sin(th) * np.sin(th / 2), y + 90 * q * np.cos(th)]
            ax.add_patch(Polygon(P, closed=True, fc=to_rgba("#38BDF8", 0.5 * a), ec="#7DD3FC", lw=3, alpha=a, zorder=10))
            lab = "water"
        else:
            person(ax, x - 35, y - 10, 1.1 * q, AMB, a); person(ax, x + 35, y - 10, 1.1 * q, LIVL, a)
            lab = "hugging"
        tx(ax, x, 1010, lab, 24, WHITE, a, w="semibold", z=11)
        c = ease(seg(lt, 0.5 + k * 0.5, 0.8 + k * 0.5))
        cross(ax, x, y, 95 * c + 1, a * c)
    tx(ax, 540, 880, "casual contact does not spread it", 24, MUTED, a * ease(seg(lt, 2.0, 2.6)), w="semibold")

def s3(ax, t, lt, a, v):
    syringe(ax, 540, 1260, 1.5, a * pop(lt, 0.1), ang=-0.15, fill=0.55 + 0.1 * np.sin(t * 2))
    items = [("unsafe injections", 0.6), ("reused needles", 1.6), ("unscreened blood transfusions", 2.9)]
    for k, (s, st) in enumerate(items):
        p = ease(seg(lt, st, st + 0.5))
        if p <= 0: continue
        y = 1060 - k * 95; xo = (1 - p) * 60
        ax.add_patch(Circle((140 + xo, y), 12, fc=RED, alpha=a * p, zorder=12))
        tx(ax, 175 + xo, y, s, 30, WHITE, a * p, ha="left", w="semibold")

HX = [(i, j) for i in range(-3, 4) for j in range(-2, 3)]
def s4(ax, t, lt, a, v):
    S = 82
    for k, (i, j) in enumerate(HX):
        x = 540 + i * S * 1.5; y = 1100 + j * S * 1.732 + (S * 0.866 if i % 2 else 0)
        if not (60 < x < 1020 and 760 < y < 1440): continue
        hexa = [(x + S * 0.95 * np.cos(m * np.pi / 3), y + S * 0.95 * np.sin(m * np.pi / 3)) for m in range(6)]
        inf = ease(seg(lt, 0.8 + 0.12 * ((k * 7) % 13), 1.6 + 0.12 * ((k * 7) % 13)))
        ax.add_patch(Polygon(hexa, closed=True, fc=to_rgba(mixc(LIV, "#4D7C0F", 0.5 * inf), 0.55 * a), ec=to_rgba(LIVL, 0.8 * a), lw=2.5, zorder=8))
        ax.add_patch(Circle((x, y), 16, fc=to_rgba("#7C2D12", 0.9 * a), zorder=8.1))
        if inf > 0:
            n = 1 + int(inf * 3)
            for m in range(n):
                an = m * 2.1 + t * 0.8 + k
                virus(ax, x + 42 * np.cos(an), y + 42 * np.sin(an), 11 * inf, a, t, rna=False, z=9)
    tx(ax, 540, 690, "liver cells", 24, MUTED, a, w="semibold")

def s5(ax, t, lt, a, v):
    L6 = v.T[6] - v.T[5]
    sp = ease(seg(lt, L6 - 0.6, L6 + 0.4))
    for k in range(10):
        q = pop(lt, 0.1 + k * 0.08)
        if q <= 0: continue
        clear = k < 3
        col = mixc(MUTED, OKC if clear else AMB, ease(seg(lt, 1.2, 2.0)) if clear else sp)
        x = 150 + (k % 5) * 195 + (0 if clear else 0); y = 1270 if k < 5 else 1020
        person(ax, x, y, 1.25 * q, col, a)
    tx(ax, 345, 1395, "3 in 10 clear it", 26, OKC, a * ease(seg(lt, 1.6, 2.2)), w="bold")
    tx(ax, 540, 870, "~7 in 10: long-term (chronic) infection", 26, AMB, a * sp, w="bold")

def s7(ax, t, lt, a, v):
    sc = ease(seg(lt, 0.4, 3.6))
    liver(ax, 540, 1150, 680, a, scar=sc)
    p = ease(seg(lt, 2.0, 2.6))
    pill(ax, 540, 860, 760, 84, CARDC, a * p, ec=AMB, lw=2.5, z=12)
    tx(ax, 540, 860, "15–30% develop cirrhosis in 20 years", 27, WHITE, a * p, z=13)
    tx(ax, 540, 780, "among those with chronic infection (WHO)", 19, MUTED, a * p, w="normal")

def s8(ax, t, lt, a, v):
    q = pop(lt, 0.1)
    card(ax, 120, 1130, 840, 250, a * min(1, q * 2), ec=AMB, z=8, fc=CARDC, lw=2.5)
    tx(ax, 540, 1300, "PAKISTAN", 44, AMB, a * min(1, q * 2), z=10)
    tx(ax, 540, 1205, "one of the highest HCV burdens", 28, WHITE, a * min(1, q * 2), z=10)
    p = ease(seg(lt, 2.6, 3.2))
    for k in range(10):
        x = 175 + k * 81; lit = k < 3
        c = AMB if lit else "#3A2A18"
        ax.add_patch(Circle((x, 990), 30, fc=to_rgba(c, a * p), ec=to_rgba(AMBL if lit else LN, a * p), lw=2, zorder=10))
    tx(ax, 540, 900, "only ~3 in 10 know they have it", 26, MUTED, a * ease(seg(lt, 3.2, 3.8)), w="semibold")

def tube(ax, x, y, s, al, col, fill=0.6, z=9):
    al = min(al, 1)
    if al <= 0.01: return
    ax.add_patch(FancyBboxPatch((x - 30 * s, y - 120 * s), 60 * s, 240 * s, boxstyle=f"round,pad=0,rounding_size={30*s}", fc=to_rgba(WHITE, 0.06 * al), ec=to_rgba(WHITE, 0.8 * al), lw=3, zorder=z))
    ax.add_patch(FancyBboxPatch((x - 22 * s, y - 112 * s), 44 * s, 200 * s * fill, boxstyle=f"round,pad=0,rounding_size={20*s}", fc=to_rgba("#DC2626", 0.85 * al), ec="none", zorder=z + 0.1))
    ax.add_patch(Rectangle((x - 36 * s, y + 120 * s), 72 * s, 26 * s, fc=to_rgba(col, al), zorder=z + 0.2))

def s9(ax, t, lt, a, v):
    for k, (x, n, title, res, col, st) in enumerate([(290, "1", "antibody test", "exposure?", AMB, 0.1), (790, "2", "HCV RNA test", "active infection?", LIME, 2.2)]):
        q = ease(seg(lt, st, st + 0.6))
        if q <= 0: continue
        card(ax, x - 220, 800, 440, 600, a * q, ec=col, z=8, fc=CARDC, lw=2.5)
        pill(ax, x, 1340, 80, 80, col, a * q, z=10); tx(ax, x, 1340, n, 32, BG, a * q, z=11)
        tube(ax, x, 1110, 0.9, a * q, col)
        tx(ax, x, 930, title, 28, WHITE, a * q, z=10)
        tx(ax, x, 865, res, 24, col, a * q, z=10, w="semibold")
    if lt > 2.0: arrow(ax, 520, 1110, 560, 1110, MUTED, a * ease(seg(lt, 2.0, 2.4)), lw=3)

GT = [("1", "#60A5FA"), ("2", "#F472B6"), ("3", AMB), ("4", "#34D399"), ("5", "#A78BFA"), ("6", "#F87171"), ("7", "#2DD4BF")]
SEQ = "AGCCATGGCGTTAGTATGAGTGTCGTGCAGCCTCCAGG"
def s10(ax, t, lt, a, v):
    card(ax, 60, 1240, 960, 150, a, ec=LN, z=8, fc=CARDC)
    sh = int(t * 6)
    for j in range(26):
        b = SEQ[(j + sh) % len(SEQ)]
        tx(ax, 110 + j * 33.5, 1315, b, 22, BCOL[b], a, fam=MONO, z=10)
    tx(ax, 540, 1215, "viral genome sequence", 18, MUTED, a, w="normal")
    # tree: root at (540, 1150) to 7 leaves
    p = ease(seg(lt, 1.2, 3.4))
    if p > 0:
        rx, ry = 540, 1140
        ax.plot([rx, rx], [ry, ry - 60 * p], color=MUTED, lw=3, alpha=a, zorder=9)
        xs = [110 + k * 143 for k in range(7)]
        ax.plot([xs[0] + (rx - xs[0]) * (1 - p), xs[-1] - (xs[-1] - rx) * (1 - p)], [ry - 60] * 2, color=MUTED, lw=3, alpha=a * (p > 0.05), zorder=9)
        for k, (g, c) in enumerate(GT):
            q = pop(lt, 2.2 + k * 0.15)
            if q <= 0: continue
            ax.plot([xs[k], xs[k]], [ry - 60, 950], color=c, lw=3, alpha=a, zorder=9)
            pill(ax, xs[k], 900, 96 * q, 96 * q, c, a, z=10)
            tx(ax, xs[k], 900, g, 34 * q, BG, a, z=11)
    tx(ax, 540, 790, "7 major genotypes", 26, WHITE, a * ease(seg(lt, 3.6, 4.2)))

def s11(ax, t, lt, a, v):
    g = ease(seg(lt, 0.3, 1.8))
    card(ax, 100, 820, 880, 560, a, ec=LN, z=8, fc=CARDC)
    tx(ax, 540, 1330, "HCV genotypes in Pakistan", 24, MUTED, a, w="semibold", z=10)
    # single stacked bar: genotype 3 = 65.35%, others = rest
    x0, x1, y = 160, 920, 1150
    pill(ax, (x0 + x1) / 2, y, x1 - x0, 90, "#3A2A18", a, z=9)
    w3 = (x1 - x0) * 0.6535 * g
    if w3 > 90: pill(ax, x0 + w3 / 2, y, w3, 90, AMB, a, z=10)
    tx(ax, x0 + 30, y, "genotype 3", 26, BG, a * ease(seg(lt, 1.2, 1.7)), ha="left", z=11)
    tx(ax, 540, 990, f"{65.35 * g:.0f}%", 72, AMB, a * ease(seg(lt, 0.6, 1.0)), z=10)
    tx(ax, 540, 880, "of isolates · 2023 meta-analysis", 19, MUTED, a * ease(seg(lt, 1.6, 2.2)), w="normal", z=10)

def s12(ax, t, lt, a, v):
    q = pop(lt, 0.1)
    if q > 0:
        lbl(ax, 540, 1340, "no vaccine for hepatitis C", a, WHITE, 26)
    p = ease(seg(lt, 1.2, 1.8))
    if p > 0:
        card(ax, 140, 980, 520, 220, a * p, ec=OKC, z=8, fc=CARDC, lw=2.5)
        syringe(ax, 410, 1090, 1.0, a * p, fill=0.0)
        tx(ax, 400, 1015, "new, sealed syringe", 22, OKC, a * p, w="semibold", z=11)
        ax.add_patch(Circle((800, 1090), 90 * p, fc=to_rgba(OKC, 0.2 * a * p), ec=to_rgba(OKC, a * p), lw=4, zorder=10))
        ax.plot([755, 790, 850], [1090, 1055, 1130], color=WHITE, lw=9, alpha=a * p, solid_capstyle="round", zorder=11)
    r = ease(seg(lt, 3.0, 3.6))
    lbl(ax, 540, 860, "ask a doctor about testing", a * r, AMB, 28, ec=AMB)

def V():
    return Video("v_hcv", "DISEASE EXPLAINER", AMB,
                 [(s0, 0, 0), (s1, 1, 1), (s2, 2, 2), (s3, 3, 3), (s4, 4, 4), (s5, 5, 6), (s7, 7, 7), (s8, 8, 8), (s9, 9, 9), (s10, 10, 10), (s11, 11, 11), (s12, 12, 12)],
                 [(0, 0, "THE SILENT VIRUS", "Hepatitis C"), (1, 1, "MEET THE VIRUS", "HCV"), (2, 2, "MYTH CHECK", "Not spread by"),
                  (3, 3, "HOW IT SPREADS", "Through blood"), (4, 4, "INSIDE THE BODY", "Liver infection"), (5, 6, "AFTER INFECTION", "Two paths"),
                  (7, 7, "OVER TIME", "Liver damage"), (8, 8, "CLOSE TO HOME", "Pakistan"), (9, 9, "DIAGNOSIS", "Two tests"),
                  (10, 10, "BIOINFORMATICS", "Reading the genome"), (11, 11, "IN PAKISTAN", "Genotype 3"), (12, 12, "PROTECT YOURSELF", "Prevent & test")],
                 gap=0.3, start=0.4, outro=2.6)

if __name__ == "__main__":
    V().main(sys.argv, seed=2)
