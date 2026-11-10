import sys as _s, os as _o; _s.path.insert(0, _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), ".."))
from eng import *
import eng

# ---------- own theme: deep moss background, lime accent, coral bacteria ----------
eng.BG = "#06120B"; eng.BGCMAP = LSC.from_list("g", [eng.BG, "#173A22"]); eng.TEAL = "#A3E635"; eng.MUTED = "#B4C8B0"
BG = eng.BG; MUTED = eng.MUTED
LI = "#A3E635"; LIL = "#D9F99D"; CO = "#FB7185"; COL = "#FECDD3"; CARDC = "#0E2316"; LN = "#24502F"
SKYC = "#7DD3FC"; AMB = "#FBBF24"; OKC = "#4ADE80"; RED = "#F87171"; LUNG = "#F9A8D4"

def lbl(ax, x, y, s, al, col=WHITE, size=24, z=14, ec=LI, w=None):
    if al <= 0.01: return
    w = w or (wpx(s, size) * 1.08 + 64)
    pill(ax, x, y, w, size * 2.4, CARDC, al, ec=ec, lw=2, z=z)
    tx(ax, x, y, s, size, col, al, z=z + 1)

def cross(ax, x, y, s, al, z=15):
    for sg in (1, -1): ax.plot([x - s, x + s], [y - s * sg, y + s * sg], color=RED, lw=9, alpha=al, solid_capstyle="round", zorder=z)

def check(ax, x, y, s, al, col=OKC, z=15):
    ax.plot([x - s, x - 0.3 * s, x + s], [y, y - 0.7 * s, y + 0.8 * s], color=col, lw=9, alpha=al, solid_capstyle="round", zorder=z)

def rod(ax, x, y, L, ang, al, col=CO, z=12, lw=None):
    """rod-shaped bacterium"""
    al = min(al, 1)
    if al <= 0.01 or L <= 1: return
    dx, dy = np.cos(ang) * L / 2, np.sin(ang) * L / 2
    lw = lw or max(4, L * 0.33)
    ax.plot([x - dx, x + dx], [y - dy, y + dy], color=to_rgba(col, 0.25 * al), lw=lw * 1.9, solid_capstyle="round", zorder=z)
    ax.plot([x - dx, x + dx], [y - dy, y + dy], color=to_rgba(col, al), lw=lw, solid_capstyle="round", zorder=z + 0.1)
    ax.plot([x - dx * 0.6, x + dx * 0.6], [y - dy * 0.6 + lw * 0.12, y + dy * 0.6 + lw * 0.12], color=to_rgba(COL, 0.6 * al), lw=max(1, lw * 0.22), solid_capstyle="round", zorder=z + 0.2)

def person(ax, x, y, s, col, al, z=10, fill=0.35):
    al = min(al, 1)
    if al <= 0.01: return
    ax.add_patch(Circle((x, y + 40 * s), 24 * s, fc=to_rgba(col, fill * al), ec=to_rgba(col, al), lw=3, zorder=z))
    ax.add_patch(FancyBboxPatch((x - 36 * s, y - 45 * s), 72 * s, 62 * s, boxstyle=f"round,pad=0,rounding_size={26*s}", fc=to_rgba(col, fill * al), ec=to_rgba(col, al), lw=3, zorder=z))

def head(ax, x, y, s, al, face=1, col=SKYC, z=10):
    """side-profile head; face=+1 looks right, -1 looks left"""
    al = min(al, 1)
    if al <= 0.01: return
    ax.add_patch(Circle((x, y), 95 * s, fc=to_rgba(col, 0.22 * al), ec=to_rgba(col, al), lw=4, zorder=z))
    ax.add_patch(Polygon([(x + face * 80 * s, y + 10 * s), (x + face * 118 * s, y - 18 * s), (x + face * 85 * s, y - 30 * s)], closed=True, fc=to_rgba(col, 0.22 * al), ec=to_rgba(col, al), lw=4, zorder=z))
    ax.add_patch(Circle((x + face * 45 * s, y + 25 * s), 9 * s, fc=to_rgba(WHITE, al), zorder=z + 0.1))
    ax.add_patch(FancyBboxPatch((x - 60 * s, y - 230 * s), 120 * s, 150 * s, boxstyle=f"round,pad=0,rounding_size={40*s}", fc=to_rgba(col, 0.22 * al), ec=to_rgba(col, al), lw=4, zorder=z - 0.1))

def lungs(ax, x, y, s, al, t, spots=0.0, z=9):
    al = min(al, 1)
    if al <= 0.01: return
    br = 1 + 0.03 * np.sin(t * 2.2)
    for sg in (-1, 1):
        cx = x + sg * 120 * s
        ax.add_patch(Ellipse((cx, y - 20 * s), 190 * s * br, 330 * s * br, angle=sg * 8, fc=to_rgba(LUNG, 0.28 * al), ec=to_rgba(LUNG, al), lw=4, zorder=z))
        # bronchi
        ax.plot([x, cx - sg * 20 * s], [y + 120 * s, y + 40 * s], color=to_rgba(COL, al), lw=6, zorder=z + 0.2, solid_capstyle="round")
        ax.plot([cx - sg * 20 * s, cx + sg * 30 * s], [y + 40 * s, y - 60 * s], color=to_rgba(COL, 0.8 * al), lw=4, zorder=z + 0.2, solid_capstyle="round")
        ax.plot([cx - sg * 20 * s, cx - sg * 10 * s], [y + 40 * s, y - 100 * s], color=to_rgba(COL, 0.8 * al), lw=4, zorder=z + 0.2, solid_capstyle="round")
    ax.plot([x, x], [y + 120 * s, y + 230 * s], color=to_rgba(COL, al), lw=10, zorder=z + 0.2, solid_capstyle="round")
    if spots > 0:
        for (dx, dy, r) in [(-150, 60, 22), (140, 80, 18), (-110, -90, 16), (170, -40, 14)]:
            ax.add_patch(Circle((x + dx * s, y + dy * s), r * s * spots, fc=to_rgba(CO, 0.75 * al), ec=to_rgba(WHITE, 0.4 * al), lw=1, zorder=z + 0.3))

# ---------------- scenes ----------------
R0 = np.random.default_rng(4)
CL = [(R0.uniform(-230, 230), R0.uniform(-180, 180), R0.uniform(0, np.pi), R0.uniform(70, 120)) for _ in range(16)]

def s0(ax, t, lt, a, v):
    for k, (dx, dy, an, L) in enumerate(CL):
        q = pop(lt, 0.1 + k * 0.06)
        if q <= 0: continue
        rod(ax, 540 + dx + 6 * np.sin(t * 1.3 + k), 1120 + dy + 6 * np.cos(t * 1.1 + k), L * q, an + 0.15 * np.sin(t * 0.7 + k), a)
    lbl(ax, 540, 820, "Mycobacterium tuberculosis", a * ease(seg(lt, 1.8, 2.4)), COL, 28, ec=CO)

def s1(ax, t, lt, a, v):
    # simple globe with meridians (no map outline) and a highlighted pin
    q = pop(lt, 0.1)
    if q > 0:
        r = 250 * q
        ax.add_patch(Circle((540, 1130), r, fc=to_rgba("#0F2E1D", a), ec=to_rgba(LI, 0.7 * a), lw=3, zorder=8))
        for k in range(-2, 3):
            ax.add_patch(Ellipse((540, 1130), 2 * r * abs(np.cos((k / 3 + t * 0.05) * np.pi / 2 + 0.3)), 2 * r, fc="none", ec=to_rgba(LI, 0.25 * a), lw=1.5, zorder=8.1))
            ax.plot([540 - r * np.sqrt(1 - (k / 3) ** 2), 540 + r * np.sqrt(1 - (k / 3) ** 2)], [1130 + k * r / 3] * 2, color=LI, alpha=0.25 * a, lw=1.5, zorder=8.1)
    p = pop(lt, 1.0)
    if p > 0:
        px, py = 600, 1200
        for m in range(3):
            ph = (t * 0.7 + m / 3) % 1
            ax.add_patch(Circle((px, py), 20 + 70 * ph, fc="none", ec=to_rgba(CO, a * (1 - ph)), lw=3, zorder=9))
        ax.add_patch(Circle((px, py), 18 * p, fc=to_rgba(CO, a), ec=to_rgba(WHITE, a), lw=2, zorder=9.5))
        lbl(ax, 760, 1330, "Pakistan", a * ease(seg(lt, 1.3, 1.8)), WHITE, 30, ec=CO)
    tx(ax, 540, 800, "among the countries with the most TB cases", 25, MUTED, a * ease(seg(lt, 2.0, 2.6)), w="semibold")

def s2(ax, t, lt, a, v):
    head(ax, 260, 1180, 1.0, a * pop(lt, 0.1), face=1, col=CO)
    head(ax, 830, 1180, 1.0, a * pop(lt, 0.4), face=-1, col=SKYC)
    d = ease(seg(lt, 0.9, 3.4))
    rng = np.random.default_rng(7)
    for k in range(14):
        u = d - k * 0.04
        if u <= 0: continue
        u = min(u, 1)
        y0 = 1160 + rng.uniform(-40, 40); y1 = 1170 + rng.uniform(-80, 80)
        xx_ = 390 + (690 - 390) * u; yy_ = y0 + (y1 - y0) * u + 30 * np.sin(u * np.pi) * (1 if k % 2 else -1)
        ax.add_patch(Circle((xx_, yy_), 16, fc=to_rgba(SKYC, 0.12 * a), ec=to_rgba(SKYC, 0.35 * a), lw=1, zorder=11))
        rod(ax, xx_, yy_, 22, k, a, z=12, lw=6)
    tx(ax, 540, 1400, "airborne", 34, LIL, a * ease(seg(lt, 0.8, 1.3)))
    for k, (s, st) in enumerate([("cough", 1.2), ("sneeze", 1.9), ("spit", 2.6)]):
        q = ease(seg(lt, st, st + 0.4))
        lbl(ax, 300 + k * 240, 850, s, a * q, WHITE, 26, ec=CO)

def s3(ax, t, lt, a, v):
    n = 0
    for r_ in range(4):
        for c in range(5):
            q = pop(lt, 0.1 + n * 0.05)
            hit = c == r_ or (r_ == 0 and c == 4)   # 5 of 20 = one quarter
            col = CO if (hit and lt > 1.6) else MUTED
            person(ax, 220 + c * 160, 1400 - r_ * 150, 0.95 * q, col, a, fill=0.5 if hit and lt > 1.6 else 0.15)
            n += 1
    lbl(ax, 540, 790, "about 1 in 4 people worldwide", a * ease(seg(lt, 1.8, 2.4)), WHITE, 27, ec=CO)

def s4(ax, t, lt, a, v):
    cx, cy = 540, 1130
    for k, (dx, dy, an, L) in enumerate(CL[:7]):
        rod(ax, cx + dx * 0.32, cy + dy * 0.32, L * 0.6, an, a * 0.95)
    p = ease(seg(lt, 0.4, 2.0))
    for k in range(14):
        an = k * 2 * np.pi / 14 + t * 0.15
        rr = 330 - 140 * p
        x, y = cx + rr * np.cos(an), cy + rr * np.sin(an)
        ax.add_patch(Circle((x, y), 46, fc=to_rgba(LI, 0.25 * a * min(1, p * 3)), ec=to_rgba(LI, a * min(1, p * 3)), lw=3, zorder=13))
        ax.add_patch(Circle((x + 8, y + 6), 15, fc=to_rgba(LIL, 0.7 * a * min(1, p * 3)), zorder=13.1))
    tx(ax, 540, 1420, "immune cells keep the bacteria in check", 25, LIL, a * ease(seg(lt, 1.6, 2.2)), w="semibold")
    for k, (s, st) in enumerate([("latent TB", 4.2), ("no symptoms · not contagious", 5.6)]):
        q = ease(seg(lt, st, st + 0.5))
        lbl(ax, 540, 850 - k * 105, s, a * q, WHITE if k else LIL, 28 if k == 0 else 25, ec=LI)

def s5(ax, t, lt, a, v):
    x0, x1, y = 140, 940, 1150
    card(ax, 90, 1000, 900, 330, a, ec=LN, fc=CARDC, z=8)
    tx(ax, 540, 1270, "lifetime risk of TB disease", 25, MUTED, a, w="semibold", z=10)
    ax.add_patch(Rectangle((140, 1120), 800, 60, fc=to_rgba("#1C3A25", a), zorder=9))
    p = ease(seg(lt, 0.5, 1.8))
    w0 = 800 * 0.05; w1 = 800 * 0.10
    if p > 0:
        ax.add_patch(Rectangle((x0, y - 30), w0 * p, 60, fc=to_rgba(CO, a), ec="none", zorder=10))
        ax.add_patch(Rectangle((x0 + w0 * p, y - 30), (w1 - w0) * p, 60, fc=to_rgba(CO, 0.45 * a), ec="none", zorder=10))
    tx(ax, x0 + 40, 1060, "5–10%", 34, COL, a * ease(seg(lt, 1.4, 1.9)), ha="left", z=10)
    tx(ax, 940, 1060, "most never fall ill", 22, MUTED, a * ease(seg(lt, 1.8, 2.3)), ha="right", w="normal", z=10)
    lbl(ax, 540, 850, "higher if the immune system is weak", a * ease(seg(lt, 3.6, 4.2)), WHITE, 25, ec=AMB)

def s6(ax, t, lt, a, v):
    lungs(ax, 300, 1120, 0.95, a * pop(lt, 0.1), t, spots=ease(seg(lt, 0.8, 1.6)))
    for k, (s, st) in enumerate([("long-lasting cough", 1.6), ("fever", 2.6), ("night sweats", 3.2), ("weight loss", 4.0)]):
        q = ease(seg(lt, st, st + 0.5))
        if q <= 0: continue
        yy_ = 1310 - k * 130; xo = (1 - q) * 60
        pill(ax, 790 + xo, yy_, 440, 86, CARDC, a * q, ec=CO, lw=2, z=10)
        tx(ax, 790 + xo, yy_, s, 27, WHITE, a * q, z=11)

def s7(ax, t, lt, a, v):
    q = pop(lt, 0.1)
    card(ax, 300, 820, 480, 560, a, ec=LI, fc=CARDC, z=8, lw=2.5)
    if q > 0:
        # cartridge-style molecular test
        ax.add_patch(FancyBboxPatch((440, 980), 200 * q, 320 * q, boxstyle="round,pad=0,rounding_size=26", fc=to_rgba("#E5E7EB", 0.9 * a), ec=to_rgba(WHITE, a), lw=3, zorder=9))
        ax.add_patch(Rectangle((470, 1180), 140 * q, 70 * q, fc=to_rgba(LI, 0.8 * a), zorder=9.5))
        for k in range(4):
            on = seg(lt, 0.8 + k * 0.3, 1.0 + k * 0.3)
            ax.add_patch(Circle((480 + k * 40, 1040), 12, fc=to_rgba(LI if on > 0.5 else "#6B7280", a), zorder=9.6))
    tx(ax, 540, 920, "rapid molecular test", 28, WHITE, a * ease(seg(lt, 0.6, 1.1)), z=10)
    tx(ax, 540, 865, "recommended first test (WHO)", 21, LIL, a * ease(seg(lt, 1.4, 1.9)), w="semibold", z=10)

def capsule(ax, x, y, s, al, z=10):
    al = min(al, 1)
    if al <= 0.01: return
    ax.add_patch(FancyBboxPatch((x - 70 * s, y - 28 * s), 70 * s, 56 * s, boxstyle=f"round,pad=0,rounding_size={28*s}", fc=to_rgba(AMB, al), ec="none", zorder=z))
    ax.add_patch(FancyBboxPatch((x, y - 28 * s), 70 * s, 56 * s, boxstyle=f"round,pad=0,rounding_size={28*s}", fc=to_rgba(WHITE, al), ec="none", zorder=z))

def s8(ax, t, lt, a, v):
    capsule(ax, 540, 1350, 1.4, a * pop(lt, 0.1))
    tx(ax, 540, 1255, "standard drugs", 22, MUTED, a * ease(seg(lt, 0.3, 0.8)), w="semibold")
    rng = np.random.default_rng(3)
    for k in range(10):
        x = 200 + (k % 5) * 170; y = 1100 - (k // 5) * 130
        res = k in (3, 7)
        fade = ease(seg(lt, 1.2 + k * 0.08, 1.8 + k * 0.08))
        al = a * (1 - 0.85 * fade) if not res else a
        rod(ax, x, y, 80, 0.4 + rng.uniform(-0.4, 0.4), al, col=(AMB if res and fade > 0.5 else CO))
        if res and fade > 0.5:
            ax.add_patch(Circle((x, y), 62, fc="none", ec=to_rgba(AMB, a), lw=3, zorder=13))
    lbl(ax, 540, 830, "drug-resistant TB: longer, more complex treatment", a * ease(seg(lt, 3.2, 3.8)), WHITE, 23, ec=AMB)

SEQ = "GGCCAGCTGAGCCAATTCATGGACCAGAACAACCCGCTGTCGGGGTTGACCCACAAGCGCCGACTGTC"
SCOL = {"A": "#A3E635", "T": "#7DD3FC", "G": "#F9A8D4", "C": "#FBBF24"}
def s9(ax, t, lt, a, v):
    card(ax, 60, 1180, 960, 170, a, ec=LN, z=8, fc=CARDC)
    tx(ax, 540, 1395, "bacterial genome  →  sequencing reads", 20, MUTED, a, w="normal")
    sh = int(min(lt, 2.5) * 6)
    for j in range(26):
        b = SEQ[(j + sh) % len(SEQ)]
        hl = j == 13 and lt > 3.0
        if hl:
            pill(ax, 110 + j * 33.5, 1265, 40, 64, RED, a, z=9)
            b = "T"
        tx(ax, 110 + j * 33.5, 1265, b, 24, WHITE if hl else SCOL[b], a, fam=MONO, z=10)
    p = ease(seg(lt, 3.2, 3.8))
    if p > 0:
        ax.plot([110 + 13 * 33.5, 110 + 13 * 33.5], [1225, 1070], color=RED, lw=3, alpha=a * p, zorder=9)
        lbl(ax, 540, 1010, "mutation linked to drug resistance", a * p, WHITE, 26, ec=RED)
    rod(ax, 540, 820, 140 * pop(lt, 0.2), 0.3 + 0.05 * np.sin(t), a)

def s10(ax, t, lt, a, v):
    q = ease(seg(lt, 0.1, 0.7))
    card(ax, 170, 760, 740, 650, a * q, ec=LI, fc=CARDC, z=8, lw=2.5)
    tx(ax, 540, 1340, "WHO catalogue of mutations", 28, WHITE, a * q, z=10)
    tx(ax, 540, 1290, "reference for interpreting sequencing results", 20, MUTED, a * q, w="normal", z=10)
    rows = [("variant 1", "resistance"), ("variant 2", "no resistance"), ("variant 3", "resistance"), ("variant 4", "no resistance")]
    for k, (vn, lab) in enumerate(rows):
        p = ease(seg(lt, 0.8 + k * 0.35, 1.2 + k * 0.35))
        if p <= 0: continue
        y = 1200 - k * 80
        ax.plot([220, 860], [y - 45, y - 45], color=LN, lw=1.5, alpha=a * p, zorder=9)
        tx(ax, 240, y, vn, 22, LIL, a * p, ha="left", fam=MONO, z=10)
        tx(ax, 840, y, lab, 22, RED if lab == "resistance" else OKC, a * p, ha="right", w="semibold", z=10)
    lbl(ax, 540, 850, "covers 13 TB medicines", a * ease(seg(lt, 2.8, 3.4)), WHITE, 26, ec=LI)

def s11(ax, t, lt, a, v):
    acts = [("cough for 3 weeks or more?", CO, 0.1), ("get tested", LI, 1.4), ("see a doctor", SKYC, 2.6)]
    for k, (s, col, st) in enumerate(acts):
        q = ease(seg(lt, st, st + 0.5))
        if q <= 0: continue
        y = 1340 - k * 200; xo = (1 - q) * 80
        card(ax, 110 + xo, y - 80, 860, 160, a * q, ec=col, fc=CARDC, z=8, lw=2.5)
        ax.add_patch(Circle((210 + xo, y), 50, fc=to_rgba(col, 0.25 * a * q), ec=to_rgba(col, a * q), lw=3, zorder=9))
        if k == 0: tx(ax, 210 + xo, y, "?", 40, col, a * q, z=10)
        else: check(ax, 210 + xo, y + 4, 24, a * q, col=col, z=10)
        tx(ax, 300 + xo, y, s, 30, WHITE, a * q, ha="left", z=10)

def V():
    return Video("v_tb", "DISEASE EXPLAINER", LI,
                 [(s0, 0, 0), (s1, 1, 1), (s2, 2, 2), (s3, 3, 3), (s4, 4, 4), (s5, 5, 5), (s6, 6, 6), (s7, 7, 7), (s8, 8, 8),
                  (s9, 9, 9), (s10, 10, 10), (s11, 11, 11)],
                 [(0, 0, "BACTERIAL INFECTION", "Tuberculosis (TB)"), (1, 1, "CLOSE TO HOME", "A major burden"), (2, 2, "HOW IT SPREADS", "Through the air"),
                  (3, 3, "HOW COMMON", "A quarter of people"), (4, 4, "LATENT TB", "Infected, not ill"), (5, 5, "FROM INFECTION TO DISEASE", "Who falls ill"),
                  (6, 6, "TB DISEASE", "Mostly the lungs"), (7, 7, "DIAGNOSIS", "Rapid molecular tests"), (8, 8, "A GROWING PROBLEM", "Drug resistance"),
                  (9, 9, "BIOINFORMATICS", "Reading the genome"), (10, 10, "BIOINFORMATICS", "Interpreting mutations"), (11, 11, "DON'T WAIT", "Get tested")],
                 gap=0.3, start=0.4, outro=2.6)

if __name__ == "__main__":
    V().main(sys.argv, seed=2)
