import sys as _s, os as _o; _s.path.insert(0, _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), ".."))
from eng import *
import eng

# ---------- own theme: deep ocean/water blue, cyan accent, orange bacteria ----------
eng.BG = "#03141A"; eng.BGCMAP = LSC.from_list("g", [eng.BG, "#0B3A47"]); eng.TEAL = "#22D3EE"; eng.MUTED = "#A9C6CE"
BG = eng.BG; MUTED = eng.MUTED
CY = "#22D3EE"; CYL = "#A5F3FC"; OR = "#FB923C"; ORL = "#FED7AA"; CARDC = "#08242D"; LN = "#1A4A57"
AMB = "#FBBF24"; OKC = "#4ADE80"; RED = "#F87171"; VIOC = "#C4B5FD"

def lbl(ax, x, y, s, al, col=WHITE, size=24, z=14, ec=CY, w=None):
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

def bact(ax, x, y, L, ang, al, t=0, col=OR, z=12, flag=True):
    """rod-shaped Salmonella with wavy flagella"""
    al = min(al, 1)
    if al <= 0.01 or L <= 1: return
    c, s = np.cos(ang), np.sin(ang); dx, dy = c * L / 2, s * L / 2; lw = max(4, L * 0.36)
    if flag:
        for k in range(5):
            ox = (k - 2) / 2 * L * 0.4
            bx, by = x + c * ox, y + s * ox
            for sg in (1, -1):
                u = np.linspace(0, 1, 30); d = L * 0.55 * u
                wv = 0.09 * L * np.sin(u * 9 + t * 8 + k)
                px = bx + sg * (-s) * (L * 0.12 + d) + c * wv; py = by + sg * c * (L * 0.12 + d) + s * wv
                ax.plot(px, py, color=to_rgba(ORL, 0.55 * al), lw=1.3, zorder=z - 0.2)
    ax.plot([x - dx, x + dx], [y - dy, y + dy], color=to_rgba(col, 0.25 * al), lw=lw * 1.9, solid_capstyle="round", zorder=z)
    ax.plot([x - dx, x + dx], [y - dy, y + dy], color=to_rgba(col, al), lw=lw, solid_capstyle="round", zorder=z + 0.1)
    ax.plot([x - dx * 0.6, x + dx * 0.6], [y - dy * 0.6 + lw * 0.12, y + dy * 0.6 + lw * 0.12], color=to_rgba(ORL, 0.6 * al), lw=max(1, lw * 0.22), solid_capstyle="round", zorder=z + 0.2)

def person(ax, x, y, s, col, al, z=10, fill=0.35):
    al = min(al, 1)
    if al <= 0.01 or s <= 0.01: return
    ax.add_patch(Circle((x, y + 40 * s), 24 * s, fc=to_rgba(col, fill * al), ec=to_rgba(col, al), lw=3, zorder=z))
    ax.add_patch(FancyBboxPatch((x - 36 * s, y - 45 * s), 72 * s, 62 * s, boxstyle=f"round,pad=0,rounding_size={26*s}", fc=to_rgba(col, fill * al), ec=to_rgba(col, al), lw=3, zorder=z))

R0 = np.random.default_rng(11)
CL = [(R0.uniform(-260, 260), R0.uniform(-190, 190), R0.uniform(0, np.pi), R0.uniform(80, 120)) for _ in range(9)]

# ---------------- scenes ----------------
def s0(ax, t, lt, a, v):
    for k, (dx, dy, an, L) in enumerate(CL):
        q = pop(lt, 0.1 + k * 0.09)
        if q <= 0: continue
        bact(ax, 540 + dx + 8 * np.sin(t * 1.2 + k), 1110 + dy + 8 * np.cos(t + k), L * q, an + 0.2 * np.sin(t * 0.6 + k), a, t)
    lbl(ax, 540, 820, "Salmonella Typhi", a * ease(seg(lt, 1.4, 2.0)), ORL, 30, ec=OR)

def glass(ax, x, y, s, al, t, dirty=0, z=9):
    al = min(al, 1)
    if al <= 0.01: return
    ax.add_patch(Polygon([(x - 95 * s, y + 150 * s), (x + 95 * s, y + 150 * s), (x + 75 * s, y - 150 * s), (x - 75 * s, y - 150 * s)], closed=True, fc=to_rgba(WHITE, 0.06 * al), ec=to_rgba(CYL, al), lw=4, zorder=z))
    lv = y + 80 * s + 5 * np.sin(t * 2)
    wcol = mixc(CY, "#8C7B4A", dirty)
    ax.add_patch(Polygon([(x - 90 * s, lv), (x + 90 * s, lv), (x + 76 * s, y - 145 * s), (x - 76 * s, y - 145 * s)], closed=True, fc=to_rgba(wcol, 0.35 * al), ec="none", zorder=z - 0.1))

def plate(ax, x, y, s, al, z=9):
    al = min(al, 1)
    if al <= 0.01: return
    ax.add_patch(Ellipse((x, y - 40 * s), 300 * s, 80 * s, fc=to_rgba(WHITE, 0.12 * al), ec=to_rgba(CYL, al), lw=4, zorder=z))
    ax.add_patch(Wedge((x, y - 40 * s), 105 * s, 0, 180, fc=to_rgba(AMB, 0.55 * al), ec=to_rgba(AMB, al), lw=3, zorder=z + 0.1))

def s1(ax, t, lt, a, v):
    glass(ax, 300, 1120, 1.0, a * pop(lt, 0.1), t, dirty=ease(seg(lt, 1.0, 2.2)))
    plate(ax, 780, 1100, 1.0, a * pop(lt, 0.4))
    d = ease(seg(lt, 0.9, 2.6))
    for k in range(6):
        u = np.clip(d * 1.3 - k * 0.06, 0, 1)
        if u <= 0: continue
        tx_ = 300 if k < 3 else 780; ty = 1100 + (k % 3) * 45 - 20
        bact(ax, tx_ + (k % 3 - 1) * 55, 1450 - (1450 - ty) * u, 40, k, a, t, z=12, flag=False)
    lbl(ax, 300, 870, "water", a * ease(seg(lt, 1.6, 2.1)), WHITE, 26, ec=CY)
    lbl(ax, 780, 870, "food", a * ease(seg(lt, 1.9, 2.4)), WHITE, 26, ec=AMB)

def thermo(ax, x, y, al, lev, z=9):
    al = min(al, 1)
    if al <= 0.01: return
    ax.add_patch(FancyBboxPatch((x - 30, y - 150), 60, 330, boxstyle="round,pad=0,rounding_size=30", fc=to_rgba(WHITE, 0.08 * al), ec=to_rgba(CYL, al), lw=4, zorder=z))
    ax.add_patch(Circle((x, y - 170), 55, fc=to_rgba(RED, al), ec=to_rgba(CYL, al), lw=4, zorder=z + 0.1))
    ax.add_patch(Rectangle((x - 14, y - 160), 28, 40 + 270 * lev, fc=to_rgba(RED, al), zorder=z + 0.2))

def s2(ax, t, lt, a, v):
    thermo(ax, 250, 1150, a * pop(lt, 0.1), ease(seg(lt, 0.3, 1.6)))
    for k, (s, st) in enumerate([("prolonged fever", 0.6), ("headache", 1.6), ("weakness", 2.3), ("abdominal pain", 2.9)]):
        q = ease(seg(lt, st, st + 0.45))
        if q <= 0: continue
        yy_ = 1330 - k * 135; xo = (1 - q) * 60
        pill(ax, 690 + xo, yy_, 440, 90, CARDC, a * q, ec=OR, lw=2, z=10)
        tx(ax, 690 + xo, yy_, s, 27, WHITE, a * q, z=11)

def s3(ax, t, lt, a, v):
    p = ease(seg(lt, 0.2, 2.0))
    card(ax, 140, 900, 800, 480, a, ec=LN, fc=CARDC, z=8)
    tx(ax, 540, 1230, f"~{max(1, round(9 * p))} million", 76, ORL, a, z=10)
    tx(ax, 540, 1120, "people get sick every year", 28, WHITE, a * ease(seg(lt, 1.0, 1.5)), w="semibold", z=10)
    tx(ax, 540, 1050, "estimate, WHO (2019)", 21, MUTED, a * ease(seg(lt, 1.5, 2.0)), w="normal", z=10)
    for k in range(9):
        person(ax, 220 + k * 80, 970, 0.75 * pop(lt, 0.5 + k * 0.1), OR, a, z=10, fill=0.4)

def s4(ax, t, lt, a, v):
    q = pop(lt, 0.1)
    person(ax, 300, 1120, 2.6 * q, OKC, a, z=9, fill=0.18)
    for k in range(3):
        bact(ax, 285 + k * 18, 1060 + 30 * np.sin(t + k), 30, 0.5 + k, a * 0.8 * ease(seg(lt, 0.8, 1.3)), t, z=11, flag=False)
    tx(ax, 300, 900, "recovered", 24, OKC, a * ease(seg(lt, 0.4, 0.9)), w="semibold")
    d = ease(seg(lt, 1.6, 3.0))
    arrow(ax, 440, 1130, 440 + 220 * d, 1130, OR, a * min(1, d * 3), lw=4)
    for k in range(3):
        person(ax, 740 + (k - 1) * 110, 1100, 1.2 * pop(lt, 2.4 + k * 0.15), OR, a, fill=0.35)
    lbl(ax, 540, 800, "can still carry the bacteria", a * ease(seg(lt, 2.2, 2.8)), WHITE, 26, ec=OR)

def s5(ax, t, lt, a, v):
    q = pop(lt, 0.1)
    if q > 0:
        ax.add_patch(FancyBboxPatch((270, 960), 90 * q, 330 * q, boxstyle="round,pad=0,rounding_size=40", fc=to_rgba(WHITE, 0.10 * a), ec=to_rgba(CYL, a), lw=4, zorder=9))
        ax.add_patch(FancyBboxPatch((275, 965), 80 * q, 200 * q, boxstyle="round,pad=0,rounding_size=36", fc=to_rgba("#DC2626", 0.85 * a), ec="none", zorder=9.1))
        ax.add_patch(Rectangle((262, 1270), 106 * q, 46 * q, fc=to_rgba(VIOC, a), zorder=9.2))
    d = pop(lt, 0.9)
    if d > 0:
        ax.add_patch(Circle((720, 1120), 190 * d, fc=to_rgba("#7F1D1D", 0.45 * a), ec=to_rgba(CYL, a), lw=4, zorder=9))
        rng = np.random.default_rng(5)
        for k in range(12):
            g = ease(seg(lt, 1.4 + k * 0.08, 1.9 + k * 0.08))
            r_, th = rng.uniform(20, 150), rng.uniform(0, 6.28)
            ax.add_patch(Circle((720 + r_ * np.cos(th), 1120 + r_ * np.sin(th)), 15 * g + 0.1, fc=to_rgba(ORL, 0.9 * a * g), zorder=9.5))
    arrow(ax, 380, 1120, 510, 1120, CY, a * ease(seg(lt, 0.8, 1.2)), lw=4)
    lbl(ax, 540, 830, "bacteria grown from a blood sample", a * ease(seg(lt, 2.4, 3.0)), WHITE, 24, ec=CY)

def s6(ax, t, lt, a, v):
    card(ax, 140, 900, 800, 480, a, ec=LN, fc=CARDC, z=8)
    tx(ax, 540, 1290, "2016", 70, ORL, a * ease(seg(lt, 0.2, 0.7)), z=10)
    px, py = 540, 1130
    p = pop(lt, 0.8)
    if p > 0:
        for m in range(3):
            ph = (t * 0.7 + m / 3) % 1
            ax.add_patch(Circle((px, py), 20 + 60 * ph, fc="none", ec=to_rgba(OR, a * (1 - ph)), lw=3, zorder=9))
        ax.add_patch(Circle((px, py), 18 * p, fc=to_rgba(OR, a), ec=to_rgba(WHITE, a), lw=2, zorder=9.5))
    tx(ax, 540, 1010, "Sindh, Pakistan", 32, WHITE, a * ease(seg(lt, 1.2, 1.7)), z=10)
    lbl(ax, 540, 800, "XDR = extensively drug-resistant", a * ease(seg(lt, 3.0, 3.6)), WHITE, 25, ec=RED)

def capsule(ax, x, y, s, al, col=AMB, z=10):
    al = min(al, 1)
    if al <= 0.01: return
    ax.add_patch(FancyBboxPatch((x - 60 * s, y - 24 * s), 60 * s, 48 * s, boxstyle=f"round,pad=0,rounding_size={24*s}", fc=to_rgba(col, al), ec="none", zorder=z))
    ax.add_patch(FancyBboxPatch((x, y - 24 * s), 60 * s, 48 * s, boxstyle=f"round,pad=0,rounding_size={24*s}", fc=to_rgba(WHITE, al), ec="none", zorder=z))

def s7(ax, t, lt, a, v):
    names = ["chloramphenicol", "ampicillin", "co-trimoxazole", "fluoroquinolones", "3rd-gen cephalosporins"]
    cols = [AMB, CY, VIOC, OKC, OR]
    for k, n in enumerate(names):
        q = ease(seg(lt, 0.1 + k * 0.25, 0.5 + k * 0.25))
        if q <= 0: continue
        y = 1400 - k * 118
        card(ax, 120, y - 50, 840, 100, a * q, ec=LN, fc=CARDC, z=8)
        capsule(ax, 220, y, 0.9, a * q, col=cols[k])
        tx(ax, 310, y, n, 27, WHITE, a * q, ha="left", z=10)
        cross(ax, 890, y, 22, a * ease(seg(lt, 1.6 + k * 0.3, 1.9 + k * 0.3)))
    tx(ax, 540, 810, "ceftriaxone is a 3rd-gen cephalosporin", 22, MUTED, a * ease(seg(lt, 3.2, 3.7)), w="semibold")

SEQ = "ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACC"
SCOL = {"A": "#22D3EE", "T": "#FB923C", "G": "#4ADE80", "C": "#FBBF24"}
def s8(ax, t, lt, a, v):
    bact(ax, 540, 1360, 140 * pop(lt, 0.1), 0.15, a, t)
    arrow(ax, 540, 1280, 540, 1210, CY, a * ease(seg(lt, 0.6, 1.0)), lw=4)
    card(ax, 60, 1020, 960, 170, a * ease(seg(lt, 0.6, 1.0)), ec=LN, z=8, fc=CARDC)
    sh = int(lt * 7)
    for j in range(26):
        b = SEQ[(j + sh) % len(SEQ)]
        tx(ax, 110 + j * 33.5, 1105, b, 24, SCOL[b], a * ease(seg(lt, 0.8 + j * 0.02, 1.2 + j * 0.02)), fam=MONO, z=10)
    for k in range(5):
        q = ease(seg(lt, 1.8 + k * 0.2, 2.2 + k * 0.2))
        x0 = 120 + (k * 157) % 600
        ax.add_patch(Rectangle((x0 + (1 - q) * 80, 920 - k * 22), 260, 12, fc=to_rgba([CY, OR, OKC, AMB, VIOC][k], 0.85 * a * q), zorder=9))
    lbl(ax, 540, 790, "whole-genome sequencing", a * ease(seg(lt, 2.4, 3.0)), WHITE, 26, ec=CY)

def s9(ax, t, lt, a, v):
    # simple tree: root -> branches; H58 clade highlighted
    p = ease(seg(lt, 0.1, 1.4))
    segs = [((150, 1120), (300, 1120)), ((300, 1340), (300, 900)), ((300, 1340), (520, 1340)), ((300, 900), (520, 900)),
            ((520, 1400), (520, 1280)), ((520, 1400), (900, 1400)), ((520, 1280), (900, 1280)),
            ((520, 980), (520, 820)), ((520, 980), (900, 980)), ((520, 820), (660, 820)), ((660, 900), (660, 760)), ((660, 900), (900, 900)), ((660, 760), (900, 760))]
    for k, ((x0, y0), (x1, y1)) in enumerate(segs):
        q = np.clip(p * len(segs) - k, 0, 1)
        if q <= 0: continue
        hl = k >= 7 and lt > 1.8
        ax.plot([x0, x0 + (x1 - x0) * q], [y0, y0 + (y1 - y0) * q], color=OR if hl else CYL, lw=6 if hl else 4, alpha=a, solid_capstyle="round", zorder=9)
    for (x, y) in [(900, 1400), (900, 1280), (900, 980), (900, 900), (900, 760)]:
        if p > 0.95: ax.add_patch(Circle((x, y), 14, fc=to_rgba(CYL, a), zorder=10))
    h = ease(seg(lt, 1.8, 2.4))
    if h > 0:
        ax.add_patch(FancyBboxPatch((480, 720), 520, 300, boxstyle="round,pad=0,rounding_size=30", fc=to_rgba(OR, 0.10 * a * h), ec=to_rgba(OR, a * h), lw=2.5, ls="--", zorder=8))
        m2 = ease(seg(lt, 3.0, 3.5))
        lbl(ax, 740, 1080, "H58 lineage", a * h * (1 - m2), ORL, 26, ec=OR)
        lbl(ax, 740, 1080, "H58: already multidrug-resistant", a * h * m2, WHITE, 24, ec=AMB)

def s10(ax, t, lt, a, v):
    cx, cy = 400, 1130
    q = pop(lt, 0.1)
    if q > 0:
        ax.add_patch(FancyBboxPatch((cx - 260 * q, cy - 140 * q), 520 * q, 280 * q, boxstyle=f"round,pad=0,rounding_size={130*q}", fc=to_rgba(OR, 0.15 * a), ec=to_rgba(OR, a), lw=5, zorder=8))
        ax.add_patch(Ellipse((cx - 30, cy), 300 * q, 160 * q, fc="none", ec=to_rgba(ORL, 0.8 * a), lw=3, zorder=8.5))
        tx(ax, cx - 30, cy, "chromosome", 20, ORL, a, w="semibold", z=9)
    m = ease(seg(lt, 0.8, 2.4))
    px = 860 - (860 - (cx + 170)) * m; py = cy + 260 * (1 - m)
    ring(ax, px, py, 50, CY, a * pop(lt, 0.6), lw=6, z=10)
    tx(ax, px, py + 85, "plasmid", 22, CYL, a * pop(lt, 0.6) * (1 - ease(seg(lt, 2.2, 2.6))), w="semibold")
    for k, (g, st) in enumerate([("blaCTX-M-15", 2.6), ("qnrS", 3.1)]):
        lbl(ax, 540 + (k * 2 - 1) * 210, 860, g, a * ease(seg(lt, st, st + 0.5)), CYL, 24, ec=CY)
    mx = ease(seg(lt, 3.8, 4.4))
    if mx > 0:
        lbl(ax, 300, 1410, "MDR", a * mx, WHITE, 26, ec=AMB)
        arrow(ax, 390, 1410, 650, 1410, WHITE, a * mx, lw=4)
        lbl(ax, 740, 1410, "XDR", a * mx, WHITE, 26, ec=RED)

def syringe(ax, x, y, s, al, z=9):
    al = min(al, 1)
    if al <= 0.01: return
    ax.add_patch(FancyBboxPatch((x - 160 * s, y - 40 * s), 280 * s, 80 * s, boxstyle=f"round,pad=0,rounding_size={14*s}", fc=to_rgba(WHITE, 0.12 * al), ec=to_rgba(CYL, al), lw=4, zorder=z))
    ax.add_patch(Rectangle((x - 150 * s, y - 30 * s), 170 * s, 60 * s, fc=to_rgba(CY, 0.55 * al), zorder=z + 0.1))
    ax.plot([x + 120 * s, x + 230 * s], [y, y], color=to_rgba(CYL, al), lw=4, zorder=z)
    ax.plot([x - 160 * s, x - 230 * s], [y, y], color=to_rgba(CYL, al), lw=8, zorder=z)
    ax.plot([x - 230 * s, x - 230 * s], [y - 45 * s, y + 45 * s], color=to_rgba(CYL, al), lw=8, zorder=z)

def s11(ax, t, lt, a, v):
    syringe(ax, 540, 1330, 1.1, a * pop(lt, 0.1))
    card(ax, 140, 860, 800, 330, a * ease(seg(lt, 0.6, 1.1)), ec=CY, fc=CARDC, z=8, lw=2.5)
    tx(ax, 540, 1120, "2019  ·  Pakistan", 34, ORL, a * ease(seg(lt, 0.6, 1.1)), z=10)
    tx(ax, 540, 1040, "first country to add the", 26, WHITE, a * ease(seg(lt, 1.6, 2.1)), w="semibold", z=10)
    tx(ax, 540, 990, "typhoid conjugate vaccine", 26, WHITE, a * ease(seg(lt, 1.6, 2.1)), w="semibold", z=10)
    tx(ax, 540, 925, "to routine immunisation", 26, CYL, a * ease(seg(lt, 2.6, 3.1)), w="semibold", z=10)

def s12(ax, t, lt, a, v):
    acts = [("safe water", CY, 0.1), ("good hygiene", OKC, 1.0), ("vaccination", OR, 1.9)]
    for k, (s, col, st) in enumerate(acts):
        q = ease(seg(lt, st, st + 0.5))
        if q <= 0: continue
        y = 1340 - k * 200; xo = (1 - q) * 80
        card(ax, 110 + xo, y - 80, 860, 160, a * q, ec=col, fc=CARDC, z=8, lw=2.5)
        ax.add_patch(Circle((210 + xo, y), 50, fc=to_rgba(col, 0.25 * a * q), ec=to_rgba(col, a * q), lw=3, zorder=9))
        check(ax, 210 + xo, y + 4, 24, a * q, col=col, z=10)
        tx(ax, 300 + xo, y, s, 32, WHITE, a * q, ha="left", z=10)

def V():
    sc = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12]
    hd = [("BACTERIAL INFECTION", "Typhoid fever"), ("HOW IT SPREADS", "Food and water"), ("SYMPTOMS", "What it feels like"),
          ("HOW COMMON", "Millions every year"), ("CARRIERS", "Recovered, still carrying"), ("DIAGNOSIS", "A blood test"),
          ("CLOSE TO HOME", "XDR typhoid"), ("A GROWING PROBLEM", "Five antibiotic classes"), ("BIOINFORMATICS", "Reading the genome"),
          ("BIOINFORMATICS", "A family tree"), ("BIOINFORMATICS", "One plasmid, one step"), ("PREVENTION", "A world first"), ("STAY SAFE", "Prevent typhoid")]
    return Video("v_typhoid", "DISEASE EXPLAINER", OR,
                 [(f, i, i) for i, f in enumerate(sc)], [(i, i, a, b) for i, (a, b) in enumerate(hd)],
                 gap=0.28, start=0.4, outro=2.6)

if __name__ == "__main__":
    V().main(sys.argv, seed=1)
