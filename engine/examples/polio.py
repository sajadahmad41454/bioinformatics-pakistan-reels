import sys as _s, os as _o; _s.path.insert(0, _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), ".."))
from eng import *
import eng

# ---------- own theme: graphite background, rose virus, mint vaccine ----------
eng.BG = "#0C0E13"; eng.BGCMAP = LSC.from_list("g", [eng.BG, "#2B303D"]); eng.TEAL = "#FB7185"; eng.MUTED = "#B3B9C6"
BG = eng.BG; MUTED = eng.MUTED
RO = "#FB7185"; ROL = "#FECDD3"; MI = "#5EEAD4"; MIL = "#CCFBF1"; CARDC = "#171A22"; LN = "#343A48"
AMB = "#FBBF24"; OKC = "#4ADE80"; RED = "#F87171"; SKYC = "#7DD3FC"; GR = "#6B7280"

def lbl(ax, x, y, s, al, col=WHITE, size=24, z=14, ec=RO, w=None):
    if al <= 0.01: return
    w = w or (wpx(s, size) * 1.08 + 64)
    pill(ax, x, y, w, size * 2.4, CARDC, al, ec=ec, lw=2, z=z)
    tx(ax, x, y, s, size, col, al, z=z + 1)

def cross(ax, x, y, s, al, z=15):
    if al <= 0.01: return
    for sg in (1, -1): ax.plot([x - s, x + s], [y - s * sg, y + s * sg], color=RED, lw=8, alpha=min(al, 1), solid_capstyle="round", zorder=z)

def check(ax, x, y, s, al, col=OKC, z=15):
    if al <= 0.01: return
    ax.plot([x - s, x - 0.3 * s, x + s], [y, y - 0.7 * s, y + 0.8 * s], color=col, lw=9, alpha=min(al, 1), solid_capstyle="round", zorder=z)

def virus(ax, x, y, r, al, t=0, col=RO, z=12, rot=0.0):
    """icosahedral capsid: hexagon outline with facet lines and knobs"""
    al = min(al, 1)
    if al <= 0.01 or r <= 1: return
    ang = rot + np.arange(6) * np.pi / 3 + np.pi / 6
    P = np.stack([x + r * np.cos(ang), y + r * np.sin(ang)], 1)
    ax.add_patch(Circle((x, y), r * 1.35, fc=to_rgba(col, 0.10 * al), ec="none", zorder=z - 0.2))
    ax.add_patch(Polygon(P, closed=True, fc=to_rgba(col, 0.55 * al), ec=to_rgba(ROL if col == RO else WHITE, al), lw=max(1, r * 0.06), zorder=z))
    c = np.array([x + r * 0.12 * np.cos(rot), y + r * 0.12 * np.sin(rot)])
    for p in P:
        ax.plot([c[0], p[0]], [c[1], p[1]], color=to_rgba(WHITE, 0.35 * al), lw=max(0.8, r * 0.03), zorder=z + 0.1)
    for k in range(6):
        m = (P[k] + P[(k + 1) % 6]) / 2
        ax.plot([c[0], m[0]], [c[1], m[1]], color=to_rgba(WHITE, 0.18 * al), lw=max(0.6, r * 0.02), zorder=z + 0.1)
    for p in P:
        ax.add_patch(Circle(p, r * 0.11, fc=to_rgba(ROL if col == RO else WHITE, al), ec="none", zorder=z + 0.2))

def person(ax, x, y, s, col, al, z=10, fill=0.35):
    al = min(al, 1)
    if al <= 0.01 or s <= 0.01: return
    ax.add_patch(Circle((x, y + 40 * s), 24 * s, fc=to_rgba(col, fill * al), ec=to_rgba(col, al), lw=3, zorder=z))
    ax.add_patch(FancyBboxPatch((x - 36 * s, y - 45 * s), 72 * s, 62 * s, boxstyle=f"round,pad=0,rounding_size={26*s}", fc=to_rgba(col, fill * al), ec=to_rgba(col, al), lw=3, zorder=z))

R0 = np.random.default_rng(7)
VP = [(R0.uniform(-280, 280), R0.uniform(-200, 200), R0.uniform(30, 55), R0.uniform(0, 1)) for _ in range(8)]

# ---------------- scenes ----------------
def s0(ax, t, lt, a, v):
    q = pop(lt, 0.1, 0.6)
    virus(ax, 540, 1130, 150 * q, a, t, rot=0.15 * t)
    for k, (dx, dy, r, ph) in enumerate(VP):
        qq = pop(lt, 0.8 + k * 0.12)
        if qq <= 0: continue
        dd = 1 + 0.25 * qq
        virus(ax, 540 + dx * dd + 10 * np.sin(t + k), 1130 + dy * dd + 10 * np.cos(t * 0.8 + k), r * qq * 0.7, a * 0.7, t, rot=t * 0.3 + k, z=10)
    lbl(ax, 540, 860, "poliovirus", a * ease(seg(lt, 1.6, 2.1)), ROL, 30, ec=RO)

def glass(ax, x, y, s, al, z=9):
    al = min(al, 1)
    if al <= 0.01: return
    ax.add_patch(Polygon([(x - 70 * s, y + 110 * s), (x + 70 * s, y + 110 * s), (x + 55 * s, y - 110 * s), (x - 55 * s, y - 110 * s)], closed=True, fc=to_rgba(WHITE, 0.06 * al), ec=to_rgba(SKYC, al), lw=4, zorder=z))
    ax.add_patch(Polygon([(x - 66 * s, y + 60 * s), (x + 66 * s, y + 60 * s), (x + 56 * s, y - 106 * s), (x - 56 * s, y - 106 * s)], closed=True, fc=to_rgba(SKYC, 0.3 * al), ec="none", zorder=z - 0.1))

def s1(ax, t, lt, a, v):
    person(ax, 230, 1180, 1.8 * pop(lt, 0.1), GR, a, fill=0.25)
    person(ax, 850, 1180, 1.8 * pop(lt, 0.3), MI, a, fill=0.25)
    d = ease(seg(lt, 0.6, 2.4))
    for k in range(5):
        u = np.clip(d * 1.4 - k * 0.1, 0, 1)
        if u <= 0 or u >= 1: continue
        xx_ = 330 + (750 - 330) * u; yy_ = 1240 + 120 * np.sin(np.pi * u)
        virus(ax, xx_, yy_, 22, a, t, rot=t + k, z=12)
    lbl(ax, 540, 1430, "faecal-oral route", a * ease(seg(lt, 1.0, 1.5)), WHITE, 26, ec=RO)
    q = ease(seg(lt, 3.0, 3.5))
    glass(ax, 540, 1010, 0.8, a * q)
    lbl(ax, 540, 840, "less often: contaminated water or food", a * ease(seg(lt, 3.4, 3.9)), MUTED, 22, ec=LN)

def s2(ax, t, lt, a, v):
    # intestine: winding tube
    p = ease(seg(lt, 0.0, 1.0))
    u = np.linspace(0, 1, 400)
    xs = 200 + 680 * u; ys = 1170 + 150 * np.sin(u * 2 * np.pi * 2.5)
    n = max(2, int(400 * p))
    ax.plot(xs[:n], ys[:n], color=to_rgba("#F9A8D4", 0.22 * a), lw=70, solid_capstyle="round", zorder=8)
    ax.plot(xs[:n], ys[:n], color=to_rgba("#F9A8D4", 0.55 * a), lw=4, solid_capstyle="round", zorder=8.1)
    m = int(np.clip(1 + 22 * ease(seg(lt, 0.8, 2.4)), 0, 23))
    for k in range(m):
        uu = (k * 0.0437 + 0.02 + 0.01 * np.sin(t + k)) % 1
        virus(ax, 200 + 680 * uu, 1170 + 150 * np.sin(uu * 2 * np.pi * 2.5) + 12 * np.sin(k * 2.1), 15, a, t, rot=t + k, z=9)
    lbl(ax, 540, 1445, "multiplies in the intestine", a * ease(seg(lt, 1.0, 1.5)), WHITE, 25, ec=RO)
    q = ease(seg(lt, 2.8, 3.3))
    if q > 0:
        for k in range(10):
            person(ax, 135 + k * 90, 880, 0.75 * pop(lt, 2.8 + k * 0.05), OKC if k < 7 else GR, a, fill=0.35)
        tx(ax, 540, 790, "most infected people: no symptoms", 24, OKC, a * q, w="semibold")

def neuron(ax, x, y, al, sick=0, z=9):
    al = min(al, 1)
    if al <= 0.01: return
    col = mixc(MI, RED, sick)
    for k in range(7):
        th = np.pi / 2 + (k - 3) * 0.32
        L = 120 + 25 * (k % 2)
        ax.plot([x, x + L * np.cos(th + np.pi / 2 * 0)], [y, y + L * np.sin(th)], color=to_rgba(col, al), lw=5, solid_capstyle="round", zorder=z)
    ax.add_patch(Circle((x, y), 55, fc=to_rgba(col, 0.35 * al), ec=to_rgba(col, al), lw=4, zorder=z + 0.1))
    ax.add_patch(Circle((x, y), 18, fc=to_rgba(col, al), zorder=z + 0.2))
    ax.plot([x, x], [y - 55, y - 330], color=to_rgba(col, al), lw=8, solid_capstyle="round", zorder=z)
    for k in range(4):
        ax.add_patch(FancyBboxPatch((x - 16, y - 100 - k * 60), 32, 46, boxstyle="round,pad=0,rounding_size=14", fc=to_rgba(col, 0.25 * al), ec=to_rgba(col, 0.8 * al), lw=2, zorder=z + 0.1))
    for k in range(5):
        th = -np.pi / 2 + (k - 2) * 0.35
        ax.plot([x, x + 60 * np.cos(th)], [y - 330, y - 330 + 60 * np.sin(th)], color=to_rgba(col, al), lw=4, solid_capstyle="round", zorder=z)

def s3(ax, t, lt, a, v):
    sick = ease(seg(lt, 2.4, 3.6))
    neuron(ax, 380, 1250, a * pop(lt, 0.1), sick)
    for k in range(4):
        u = ease(seg(lt, 0.8 + k * 0.25, 2.2 + k * 0.25))
        if u <= 0: continue
        virus(ax, 820 - (820 - 430) * u, 1350 - 80 * u + 30 * np.sin(k + t), 20, a * (1 - 0.6 * ease(seg(lt, 3.6, 4.2))), t, rot=t + k, z=12)
    lbl(ax, 720, 1100, "motor neuron", a * ease(seg(lt, 0.6, 1.1)), MIL, 24, ec=MI)
    # muscle
    q = ease(seg(lt, 0.4, 0.9))
    if q > 0:
        mc = mixc("#F472B6", GR, sick)
        ax.add_patch(Ellipse((380, 830), 300, 110, fc=to_rgba(mc, 0.4 * a * q), ec=to_rgba(mc, a * q), lw=3, zorder=8))
        for k in range(5): ax.plot([260 + k * 60, 260 + k * 60], [800, 860], color=to_rgba(mc, 0.6 * a * q), lw=2, zorder=8.1)
    lbl(ax, 770, 830, "paralysis within hours", a * ease(seg(lt, 3.8, 4.4)), WHITE, 24, ec=RED)

def s4(ax, t, lt, a, v):
    card(ax, 90, 760, 900, 680, a, ec=LN, fc=CARDC, z=8)
    shown = int(200 * ease(seg(lt, 0.1, 2.0)))
    for k in range(shown):
        r_, c_ = divmod(k, 20)
        x = 160 + c_ * 40; y = 1370 - r_ * 40
        hl = (k == 137)
        if hl and lt > 2.3:
            ax.add_patch(Circle((x, y), 16 + 4 * np.sin(t * 4), fc=to_rgba(RO, a), ec=to_rgba(WHITE, a), lw=2, zorder=10))
        else:
            ax.add_patch(Circle((x, y), 11, fc=to_rgba(GR, 0.55 * a), zorder=9))
    tx(ax, 540, 900, "1 in 200 infections", 44, ROL, a * ease(seg(lt, 2.4, 2.9)), z=11)
    tx(ax, 540, 830, "irreversible paralysis, usually in the legs", 24, WHITE, a * ease(seg(lt, 3.2, 3.7)), w="semibold", z=11)

def s5(ax, t, lt, a, v):
    q = pop(lt, 0.1)
    person(ax, 540, 1100, 2.4 * q, AMB, a, fill=0.25)
    tx(ax, 540, 850, "under 5", 64, AMB, a * ease(seg(lt, 0.5, 1.0)), z=11)
    ring(ax, 540, 1150, 230 + 10 * np.sin(t * 3), AMB, a * 0.5 * ease(seg(lt, 0.3, 0.8)), lw=3)

def shield(ax, x, y, s, al, col=MI, z=9):
    al = min(al, 1)
    if al <= 0.01 or s <= 0.01: return
    pts = [(x - 120 * s, y + 130 * s), (x, y + 170 * s), (x + 120 * s, y + 130 * s), (x + 110 * s, y - 20 * s), (x, y - 160 * s), (x - 110 * s, y - 20 * s)]
    ax.add_patch(Polygon(pts, closed=True, fc=to_rgba(col, 0.2 * al), ec=to_rgba(col, al), lw=5, zorder=z))

def s6(ax, t, lt, a, v):
    q = ease(seg(lt, 0.1, 0.5))
    card(ax, 140, 1180, 800, 200, a * q, ec=RED, fc=CARDC, z=8, lw=2.5)
    cross(ax, 260, 1280, 34, a * q)
    tx(ax, 340, 1280, "no cure", 46, WHITE, a * q, ha="left", z=10)
    q2 = ease(seg(lt, 1.6, 2.1))
    shield(ax, 540, 930, 0.95 * pop(lt, 1.6), a)
    check(ax, 540, 940, 50, a * q2, col=MI)
    tx(ax, 540, 740, "it can only be prevented", 28, MIL, a * q2, w="semibold")

def dropper(ax, x, y, s, al, z=10):
    al = min(al, 1)
    if al <= 0.01: return
    ax.add_patch(FancyBboxPatch((x - 30 * s, y), 60 * s, 160 * s, boxstyle=f"round,pad=0,rounding_size={20*s}", fc=to_rgba(WHITE, 0.10 * al), ec=to_rgba(MIL, al), lw=3, zorder=z))
    ax.add_patch(FancyBboxPatch((x - 40 * s, y + 150 * s), 80 * s, 70 * s, boxstyle=f"round,pad=0,rounding_size={30*s}", fc=to_rgba(MI, 0.8 * al), ec="none", zorder=z))
    ax.add_patch(Polygon([(x - 18 * s, y), (x + 18 * s, y), (x, y - 50 * s)], closed=True, fc=to_rgba(MIL, al), zorder=z))

def s7(ax, t, lt, a, v):
    dropper(ax, 540, 1240, 1.0, a * pop(lt, 0.1))
    ph = (lt * 1.2) % 1
    if lt > 0.5:
        ax.add_patch(Circle((540, 1180 - 120 * ph), 12, fc=to_rgba(MI, a * (1 - ph)), zorder=11))
    for k in range(4):
        q = pop(lt, 0.9 + k * 0.45)
        x = 225 + k * 210
        if q <= 0: continue
        ax.add_patch(Circle((x, 1000), 62 * q, fc=to_rgba(MI, 0.15 * a), ec=to_rgba(MI, a), lw=3, zorder=9))
        tx(ax, x, 1000, f"dose {k+1}", 22, MIL, a, z=10)
        if k < 3: arrow(ax, x + 70, 1000, x + 140, 1000, MUTED, a * min(1, q), lw=2.5)
    lbl(ax, 540, 830, "multiple doses: protection for life", a * ease(seg(lt, 2.9, 3.4)), WHITE, 25, ec=MI)

def s8(ax, t, lt, a, v):
    v_ = v
    rows = [("Type 2", "eradicated · declared 2015", MI, 0.1), ("Type 3", "eradicated · declared 2019", MI, 0.9), ("Type 1", "still circulating", RO, 4.3)]
    for k, (n, s, col, st) in enumerate(rows):
        q = ease(seg(lt, st, st + 0.5))
        if q <= 0: continue
        y = 1380 - k * 175; xo = (1 - q) * 60
        card(ax, 110 + xo, y - 70, 860, 140, a * q, ec=col, fc=CARDC, z=8, lw=2.5)
        virus(ax, 200 + xo, y, 38, a * q, t, col=GR if k < 2 else RO, rot=t * 0.5, z=9)
        tx(ax, 280 + xo, y + 22, n, 34, WHITE, a * q, ha="left", z=10)
        tx(ax, 280 + xo, y - 26, s, 22, MUTED, a * q, w="semibold", ha="left", z=10)
        if k < 2: check(ax, 900 + xo, y, 26, a * q, col=MI)
        else:
            ax.add_patch(Circle((900 + xo, y), 16 + 5 * np.sin(t * 5), fc=to_rgba(RO, a * q), zorder=10))
    q = ease(seg(lt, 5.2, 5.7))
    if q > 0:
        lbl(ax, 330, 820, "Pakistan", a * q, WHITE, 30, ec=RO)
        lbl(ax, 750, 820, "Afghanistan", a * ease(seg(lt, 5.6, 6.1)), WHITE, 30, ec=RO)
        tx(ax, 540, 730, "the only two endemic countries", 22, ROL, a * ease(seg(lt, 6.4, 6.9)), w="semibold")

def s10(ax, t, lt, a, v):
    # sewage pipe
    q = ease(seg(lt, 0.1, 0.6))
    if q > 0:
        ax.add_patch(FancyBboxPatch((60, 1080), 960 * q, 170, boxstyle="round,pad=0,rounding_size=40", fc=to_rgba("#3F3A2E", 0.6 * a), ec=to_rgba(MUTED, a), lw=4, zorder=8))
        for k in range(14):
            xx_ = (60 + ((k * 75 + t * 90) % 960))
            if xx_ < 60 + 960 * q - 20:
                ax.plot([xx_, xx_ + 40], [1130 + 30 * (k % 3), 1130 + 30 * (k % 3)], color=to_rgba("#A3A08A", 0.6 * a), lw=3, zorder=8.5)
        for k in range(3):
            xx_ = 60 + ((k * 320 + t * 90) % 960)
            if xx_ < 60 + 960 * q - 30: virus(ax, xx_, 1165, 20, a, t, rot=t + k, z=9)
    # sample tube
    tq = pop(lt, 1.6)
    if tq > 0:
        ax.add_patch(FancyBboxPatch((500, 820), 80 * tq, 190 * tq, boxstyle="round,pad=0,rounding_size=36", fc=to_rgba(WHITE, 0.08 * a), ec=to_rgba(MIL, a), lw=4, zorder=9))
        ax.add_patch(FancyBboxPatch((505, 825), 70 * tq, 90 * tq, boxstyle="round,pad=0,rounding_size=32", fc=to_rgba("#A3A08A", 0.6 * a), ec="none", zorder=9.1))
        arrow(ax, 540, 1070, 540, 1025, MIL, a * ease(seg(lt, 1.8, 2.1)), lw=3)
    d = ease(seg(lt, 3.0, 3.5))
    if d > 0:
        ring(ax, 760, 920, 70, RO, a * d, lw=4)
        virus(ax, 760, 920, 34 * d, a, t, rot=t)
        ax.plot([810, 850], [870, 830], color=to_rgba(RO, a * d), lw=8, solid_capstyle="round", zorder=10)
    lbl(ax, 540, 1400, "environmental surveillance", a * ease(seg(lt, 0.8, 1.3)), WHITE, 25, ec=MI)
    lbl(ax, 300, 760, "found early", a * ease(seg(lt, 4.2, 4.7)), ROL, 22, ec=RO)

SEQ = "TTAGACACAACCAGGCTGTTGGCAATAATGCAATACGCAATGCTCGTCGAGGATCATCAGTAAACCTAGTCTTG"
SCOL = {"A": "#5EEAD4", "T": "#FB7185", "G": "#FBBF24", "C": "#7DD3FC"}
MUT = {5, 13, 19}
def s11(ax, t, lt, a, v):
    for row, (name, y, st, col) in enumerate([("sewage", 1280, 0.2, MUTED), ("patient", 1060, 1.2, AMB)]):
        q = ease(seg(lt, st, st + 0.5))
        if q <= 0: continue
        card(ax, 60, y - 85, 960, 170, a * q, ec=LN, fc=CARDC, z=8)
        tx(ax, 100, y + 50, name, 20, col, a * q, w="semibold", ha="left", z=10)
        for j in range(24):
            b = SEQ[j + 10]
            if row == 1 and j in MUT: b = {"A": "G", "G": "A", "C": "T", "T": "C"}[b]
            tx(ax, 120 + j * 36.5, y - 15, b, 26, SCOL[b], a * ease(seg(lt, st + 0.2 + j * 0.02, st + 0.6 + j * 0.02)), fam=MONO, z=10)
    c = ease(seg(lt, 2.4, 2.9))
    if c > 0:
        for j in range(24):
            x = 120 + j * 36.5
            same = j not in MUT
            ax.plot([x, x], [1225, 1100], color=to_rgba(MI if same else RO, (0.35 if same else 0.9) * a * c), lw=2 if same else 4, zorder=9)
    lbl(ax, 540, 830, "compare: how closely related?", a * ease(seg(lt, 3.0, 3.5)), WHITE, 25, ec=MI)

def s12(ax, t, lt, a, v):
    p = ease(seg(lt, 0.1, 1.6))
    segs = [((130, 1120), (260, 1120)), ((260, 1330), (260, 900)), ((260, 1330), (470, 1330)), ((260, 900), (470, 900)),
            ((470, 1400), (470, 1260)), ((470, 1400), (900, 1400)), ((470, 1260), (900, 1260)),
            ((470, 980), (470, 820)), ((470, 980), (900, 980)), ((470, 820), (600, 820)), ((600, 880), (600, 760)), ((600, 880), (900, 880)), ((600, 760), (900, 760))]
    for k, ((x0, y0), (x1, y1)) in enumerate(segs):
        q = np.clip(p * len(segs) - k, 0, 1)
        if q <= 0: continue
        ax.plot([x0, x0 + (x1 - x0) * q], [y0, y0 + (y1 - y0) * q], color=MUTED, lw=4, alpha=a, solid_capstyle="round", zorder=9)
    tips = [(900, 1400, AMB), (900, 1260, MUTED), (900, 980, AMB), (900, 880, MUTED), (900, 760, AMB)]
    for (x, y, col) in tips:
        if p > 0.95: ax.add_patch(Circle((x, y), 16, fc=to_rgba(col, a), zorder=10))
    h = ease(seg(lt, 1.8, 2.3))
    if h > 0:
        ax.add_patch(FancyBboxPatch((440, 1215), 520, 230, boxstyle="round,pad=0,rounding_size=30", fc=to_rgba(MI, 0.08 * a * h), ec=to_rgba(MI, a * h), lw=2.5, zorder=8))
        lbl(ax, 700, 1165, "linked cases", a * h, MIL, 24, ec=MI)
    g = ease(seg(lt, 3.6, 4.1))
    if g > 0:
        ax.plot([470, 470], [990, 1240], color=to_rgba(RO, a * g), lw=4, ls=(0, (4, 6)), zorder=9.5)
        tx(ax, 360, 1140, "?", 60, RO, a * g, z=10)
        lbl(ax, 700, 690, "a genetic gap: missed cases?", a * ease(seg(lt, 4.0, 4.5)), WHITE, 24, ec=RO)

def s13(ax, t, lt, a, v):
    shield(ax, 540, 1130, 1.3 * pop(lt, 0.1), a)
    person(ax, 540, 1110, 1.6 * pop(lt, 0.3), AMB, a, z=10, fill=0.3)
    for k, (s, st) in enumerate([("every child", 1.0), ("every time", 1.8)]):
        q = ease(seg(lt, st, st + 0.5))
        if q <= 0: continue
        x = 300 + k * 480
        lbl(ax, x, 820, s, a * q, WHITE, 28, ec=MI)

def V():
    sc = [(s0, 0, 0), (s1, 1, 1), (s2, 2, 2), (s3, 3, 3), (s4, 4, 4), (s5, 5, 5), (s6, 6, 6), (s7, 7, 7), (s8, 8, 9), (s10, 10, 10), (s11, 11, 11), (s12, 12, 12), (s13, 13, 13)]
    hd = [(0, 0, "VIRAL INFECTION", "Polio"), (1, 1, "HOW IT SPREADS", "Faecal-oral route"), (2, 2, "INSIDE THE BODY", "The gut first"),
          (3, 3, "THE DANGER", "Attacking nerves"), (4, 4, "HOW OFTEN", "1 in 200"), (5, 5, "WHO IS AT RISK", "Young children"),
          (6, 6, "TREATMENT", "No cure"), (7, 7, "PREVENTION", "Vaccines"), (8, 9, "CLOSE TO HOME", "The last two countries"),
          (10, 10, "BIOINFORMATICS", "Testing sewage"), (11, 11, "BIOINFORMATICS", "Reading the genome"), (12, 12, "BIOINFORMATICS", "A family tree"),
          (13, 13, "END POLIO", "Vaccinate every child")]
    return Video("v_polio", "DISEASE EXPLAINER", RO, sc, hd, gap=0.25, start=0.4, outro=2.6)

if __name__ == "__main__":
    V().main(sys.argv, seed=2)
