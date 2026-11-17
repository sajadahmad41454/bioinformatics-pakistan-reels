import sys as _s, os as _o; _s.path.insert(0, _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), ".."))
from eng import *
import eng

# ---------- own theme: deep indigo-blue background, blue-circle accent, amber glucose, mint insulin ----------
eng.BG = "#07081A"; eng.BGCMAP = LSC.from_list("g", [eng.BG, "#1E2370"]); eng.TEAL = "#60A5FA"; eng.MUTED = "#B4BCDD"
BG = eng.BG; MUTED = eng.MUTED
BL = "#60A5FA"; BLL = "#DBEAFE"; GL = "#FBBF24"; GLL = "#FDE68A"; MI = "#34D399"; MIL = "#D1FAE5"
CARDC = "#121531"; LN = "#2E3566"; RED = "#F87171"; OKC = "#4ADE80"; GR = "#6B7194"; PINK = "#F472B6"; VIOL = "#A78BFA"

def lbl(ax, x, y, s, al, col=WHITE, size=24, z=14, ec=BL, w=None):
    if al <= 0.01: return
    w = w or (wpx(s, size) * 1.08 + 64)
    pill(ax, x, y, w, size * 2.4, CARDC, al, ec=ec, lw=2, z=z)
    tx(ax, x, y, s, size, col, al, z=z + 1)

def cross(ax, x, y, s, al, z=15, col=RED):
    if al <= 0.01: return
    for sg in (1, -1): ax.plot([x - s, x + s], [y - s * sg, y + s * sg], color=col, lw=8, alpha=min(al, 1), solid_capstyle="round", zorder=z)

def check(ax, x, y, s, al, col=OKC, z=15):
    if al <= 0.01: return
    ax.plot([x - s, x - 0.3 * s, x + s], [y, y - 0.7 * s, y + 0.8 * s], color=col, lw=9, alpha=min(al, 1), solid_capstyle="round", zorder=z)

def glucose(ax, x, y, r, al, rot=0.0, z=12, col=GL):
    al = min(al, 1)
    if al <= 0.01 or r <= 1: return
    ang = rot + np.arange(6) * np.pi / 3
    P = np.stack([x + r * np.cos(ang), y + r * np.sin(ang)], 1)
    ax.add_patch(Polygon(P, closed=True, fc=to_rgba(col, 0.35 * al), ec=to_rgba(GLL if col == GL else col, al), lw=max(1.2, r * 0.12), zorder=z))
    ax.add_patch(Circle(P[0], r * 0.22, fc=to_rgba(GLL, al), zorder=z + 0.1))

def key(ax, x, y, s, al, rot=0.0, col=MI, z=13):
    """insulin drawn as a small key"""
    al = min(al, 1)
    if al <= 0.01 or s <= 0.01: return
    c, sn = np.cos(rot), np.sin(rot)
    R = lambda px, py: (x + px * c - py * sn, y + px * sn + py * c)
    ax.add_patch(Circle(R(-26 * s, 0), 16 * s, fc=to_rgba(col, 0.3 * al), ec=to_rgba(col, al), lw=max(1.5, 4 * s), zorder=z))
    p0, p1 = R(-10 * s, 0), R(34 * s, 0)
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=to_rgba(col, al), lw=max(1.5, 6 * s), solid_capstyle="round", zorder=z)
    for dx in (22, 32):
        a_, b_ = R(dx * s, 0), R(dx * s, -12 * s)
        ax.plot([a_[0], b_[0]], [a_[1], b_[1]], color=to_rgba(col, al), lw=max(1.5, 5 * s), solid_capstyle="round", zorder=z)

def cellshape(ax, x, y, r, al, col=BL, z=8, name=None, lock=True, open_=0.0):
    al = min(al, 1)
    if al <= 0.01 or r <= 1: return
    ax.add_patch(Circle((x, y), r, fc=to_rgba(col, 0.12 * al), ec=to_rgba(col, al), lw=4, zorder=z))
    ax.add_patch(Circle((x + r * 0.15, y - r * 0.1), r * 0.28, fc=to_rgba(col, 0.25 * al), ec=to_rgba(col, 0.7 * al), lw=2, zorder=z + 0.1))
    if lock:
        lx, ly = x - r, y
        ax.add_patch(FancyBboxPatch((lx - 22, ly - 22), 44, 44, boxstyle="round,pad=0,rounding_size=8", fc=to_rgba(MI if open_ > 0.5 else GR, al), ec=to_rgba(WHITE, 0.7 * al), lw=2, zorder=z + 0.3))
        ax.add_patch(Circle((lx, ly + 2), 6, fc=to_rgba(BG, al), zorder=z + 0.4))
    if name: tx(ax, x, y - r - 40, name, 24, col, al, w="semibold", z=z + 1)

def person(ax, x, y, s, col, al, z=10, fill=0.35):
    al = min(al, 1)
    if al <= 0.01 or s <= 0.01: return
    ax.add_patch(Circle((x, y + 40 * s), 24 * s, fc=to_rgba(col, fill * al), ec=to_rgba(col, al), lw=3, zorder=z))
    ax.add_patch(FancyBboxPatch((x - 36 * s, y - 45 * s), 72 * s, 62 * s, boxstyle=f"round,pad=0,rounding_size={26*s}", fc=to_rgba(col, fill * al), ec=to_rgba(col, al), lw=3, zorder=z))

def vessel(ax, y, al, h=150, z=7, fill=0.0):
    al = min(al, 1)
    if al <= 0.01: return
    ax.add_patch(FancyBboxPatch((40, y - h / 2), 1000, h, boxstyle=f"round,pad=0,rounding_size={h/2}", fc=to_rgba("#7F1D1D", (0.30 + 0.25 * fill) * al), ec=to_rgba(RED, 0.8 * al), lw=3, zorder=z))

R0 = np.random.default_rng(11)
GP = [(R0.uniform(-330, 330), R0.uniform(-260, 260), R0.uniform(18, 34), R0.uniform(0, 6)) for _ in range(18)]

# ---------------- scenes ----------------
def s0(ax, t, lt, a, v):
    q = pop(lt, 0.1, 0.6)
    ring(ax, 540, 1210, 190 * q, BL, a, lw=30, z=9)
    ring(ax, 540, 1210, 235 * q, BL, a * 0.15, lw=10, z=8)
    for k, (dx, dy, r, ph) in enumerate(GP):
        qq = pop(lt, 0.5 + k * 0.06)
        if qq <= 0: continue
        th = ph + 0.25 * t
        xx_ = 540 + 0.85 * (dx * np.cos(0.15 * t) - dy * np.sin(0.15 * t)); yy_ = 1210 + 0.8 * dx * np.sin(0.15 * t) + dy * np.cos(0.15 * t)
        glucose(ax, xx_, yy_, r * qq * 0.9, a * 0.85, rot=th, z=10)
    lbl(ax, 540, 840, "glucose = sugar for energy", a * ease(seg(lt, 1.4, 1.9)) * (1 - ease(seg(lt, 4.0, 4.4))), GLL, 26, ec=GL)
    # 95% of people with diabetes
    q2 = ease(seg(lt, 4.3, 4.8))
    if q2 > 0:
        card(ax, 120, 760, 840, 150, a * q2, ec=BL, fc=CARDC, z=12, lw=2.5)
        n = int(100 * ease(seg(lt, 4.5, 6.2)))
        for k in range(n):
            r_, c_ = divmod(k, 50)
            ax.add_patch(Circle((168 + c_ * 15.0, 860 - r_ * 22), 5.5, fc=to_rgba(BL if k < 96 else GR, a * q2), zorder=13))
        tx(ax, 540, 790, "95%+ of people with diabetes have type 2", 22, BLL, a * ease(seg(lt, 5.4, 5.9)), w="semibold", z=13)

def s1(ax, t, lt, a, v):
    rows, cols = 4, 9
    for k in range(rows * cols):
        r_, c_ = divmod(k, cols)
        q = pop(lt, 0.1 + k * 0.03)
        person(ax, 160 + c_ * 95, 1380 - r_ * 120, 0.7 * q, BL, a, fill=0.3)
    n = 34 * ease(seg(lt, 0.4, 2.4))
    tx(ax, 540, 900, f"{int(n)} million+", 72, WHITE, a * ease(seg(lt, 0.4, 0.8)), z=12)
    tx(ax, 540, 810, "adults with diabetes in Pakistan (2024)", 24, BLL, a * ease(seg(lt, 1.6, 2.1)), w="semibold")
    tx(ax, 540, 755, "IDF Diabetes Atlas estimate", 19, MUTED, a * ease(seg(lt, 2.2, 2.7)), w="normal")

def pancreas(ax, x, y, s, al, z=9, col=PINK):
    al = min(al, 1)
    if al <= 0.01 or s <= 0.01: return
    u = np.linspace(0, 1, 60)
    xs = x - 170 * s + 340 * s * u; ys = y + 35 * s * np.sin(u * np.pi * 1.2) - 25 * s * u
    w_ = (60 - 32 * u) * s
    top = np.stack([xs, ys + w_ / 2], 1); bot = np.stack([xs, ys - w_ / 2], 1)[::-1]
    ax.add_patch(Polygon(np.vstack([top, bot]), closed=True, fc=to_rgba(col, 0.3 * al), ec=to_rgba(col, al), lw=3, zorder=z))

def s2(ax, t, lt, a, v):
    # plate
    q = pop(lt, 0.0)
    if q > 0:
        ax.add_patch(Ellipse((240, 1330), 260 * q, 90 * q, fc=to_rgba(WHITE, 0.1 * a), ec=to_rgba(MUTED, a), lw=3, zorder=9))
        ax.add_patch(Ellipse((240, 1345), 150 * q, 50 * q, fc=to_rgba(GL, 0.4 * a), ec="none", zorder=9.1))
    vq = ease(seg(lt, 0.3, 0.8))
    vessel(ax, 1100, a * vq)
    tx(ax, 900, 1210, "blood", 20, RED, a * vq, w="semibold")
    for k in range(9):
        u = ease(seg(lt, 0.6 + k * 0.12, 1.6 + k * 0.12))
        if u <= 0: continue
        sx, sy = 240 + 30 * np.sin(k), 1320
        tx_, ty_ = 120 + k * 100 + 20 * np.sin(t + k), 1100 + 30 * np.sin(k * 1.7 + t)
        glucose(ax, sx + (tx_ - sx) * u, sy + (ty_ - sy) * u, 22, a, rot=t + k, z=12)
    lbl(ax, 650, 1330, "glucose enters the blood", a * ease(seg(lt, 0.9, 1.4)), GLL, 22, ec=GL)
    pq = pop(lt, 2.0)
    pancreas(ax, 540, 850, 1.2 * pq, a)
    tx(ax, 540, 760, "pancreas", 22, PINK, a * ease(seg(lt, 2.2, 2.6)), w="semibold")
    for k in range(6):
        u = ease(seg(lt, 2.6 + k * 0.15, 3.6 + k * 0.15))
        if u <= 0: continue
        x0, y0 = 450 + k * 35, 880
        x1, y1 = 200 + k * 140, 1070 + 20 * np.sin(k)
        key(ax, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, 0.75, a, rot=0.4 * np.sin(t + k), z=13)
    lbl(ax, 790, 950, "insulin", a * ease(seg(lt, 2.8, 3.2)), MIL, 22, ec=MI)

def s3(ax, t, lt, a, v):
    op = ease(seg(lt, 1.4, 1.8))
    cellshape(ax, 680, 1100, 230, a * pop(lt, 0.0), BL, name=None, open_=op)
    tx(ax, 680, 820, "cell", 24, BL, a, w="semibold")
    u = ease(seg(lt, 0.3, 1.4))
    key(ax, 150 + (430 - 150) * u, 1100, 1.4, a, rot=0, z=14)
    for k in range(6):
        g = ease(seg(lt, 1.8 + k * 0.15, 2.8 + k * 0.15))
        sx, sy = 130 + (k % 3) * 70, 1300 - (k // 3) * 80 - 60 * (k % 2)
        ex, ey = 640 + 90 * np.cos(k * 1.1), 1110 + 90 * np.sin(k * 1.1)
        glucose(ax, sx + (ex - sx) * g, sy + (ey - sy) * g, 22, a, rot=t + k, z=12)
    lbl(ax, 540, 1430, "the key opens the door", a * ease(seg(lt, 1.6, 2.1)), MIL, 23, ec=MI)

def s4(ax, t, lt, a, v):
    names = [("muscle", PINK), ("fat", GL), ("liver", VIOL)]
    for k, (n, col) in enumerate(names):
        x = 210 + k * 330; y = 1150
        cellshape(ax, x, y, 110, a * pop(lt, 0.1 + 0.2 * k), col, name=n)
        b = seg(lt, 1.0 + 0.3 * k, 2.0 + 0.3 * k)
        if b > 0:
            kx = x - 110 - 120 + 100 * np.sin(np.pi * b) * (1 if b < 0.5 else 1)
            key(ax, x - 230 + 110 * np.sin(np.pi * min(b, 1)), y + 150, 0.8, a, rot=-0.6, z=14)
            cross(ax, x - 110, y + 70, 18, a * ease(seg(lt, 1.6 + 0.3 * k, 2.0 + 0.3 * k)), z=16)
        for j in range(3):
            glucose(ax, x - 60 + j * 60, 1350 + 12 * np.sin(t * 2 + j + k), 16, a * ease(seg(lt, 2.0, 2.5)), rot=t + j, z=11)
    lbl(ax, 540, 840, "insulin resistance", a * ease(seg(lt, 2.4, 2.9)), WHITE, 30, ec=RED)

def s5(ax, t, lt, a, v):
    pancreas(ax, 300, 1300, 1.0 * pop(lt, 0.0), a)
    tx(ax, 300, 1210, "pancreas", 20, PINK, a, w="semibold")
    for k in range(2):
        u = (lt * 0.4 + k * 0.5) % 1
        key(ax, 400 + 300 * u, 1320 - 40 * u, 0.7, a * (1 - u) * ease(seg(lt, 0.3, 0.6)), z=13)
    lbl(ax, 720, 1400, "too little insulin", a * ease(seg(lt, 0.6, 1.1)), MIL, 22, ec=MI)
    fill = ease(seg(lt, 1.0, 3.6))
    vessel(ax, 1000, a, h=170, fill=fill)
    n = int(4 + 26 * fill)
    for k in range(n):
        x = 90 + (k * 97 + 15 * np.sin(t + k)) % 900
        y = 1000 + 55 * np.sin(k * 2.3 + t * 0.8)
        glucose(ax, x, y, 18, a, rot=t + k, z=12)
    # level meter
    card(ax, 400, 740, 280, 140, a, ec=LN, fc=CARDC, z=10)
    ax.add_patch(Rectangle((430, 770), 220 * fill, 26, fc=to_rgba(mixc(GL, RED, fill), a), zorder=11))
    ax.add_patch(Rectangle((430, 770), 220, 26, fc="none", ec=to_rgba(MUTED, a), lw=2, zorder=11.1))
    tx(ax, 540, 840, "blood sugar", 20, MUTED, a, w="semibold", z=11)

def icon_scale(ax, x, y, al, col):
    ax.add_patch(FancyBboxPatch((x - 60, y - 45), 120, 90, boxstyle="round,pad=0,rounding_size=18", fc=to_rgba(col, 0.2 * al), ec=to_rgba(col, al), lw=3, zorder=11))
    ax.add_patch(Wedge((x, y + 10), 30, 20, 160, width=8, fc=to_rgba(col, al), zorder=11.1))
    ax.plot([x, x + 18], [y + 10, y + 28], color=to_rgba(WHITE, al), lw=3, zorder=11.2)

def icon_shoe(ax, x, y, al, col, t):
    ax.add_patch(Circle((x, y), 50, fc="none", ec=to_rgba(col, al), lw=4, zorder=11))
    ax.plot([x, x], [y, y + 34], color=to_rgba(col, al), lw=4, solid_capstyle="round", zorder=11.1)
    ax.plot([x, x + 24], [y, y - 10], color=to_rgba(col, al), lw=4, solid_capstyle="round", zorder=11.1)

def icon_dna(ax, x, y, al, t):
    th = np.linspace(0, 2 * np.pi * 1.2, 80)
    ys_ = y - 55 + 110 * th / th.max()
    ax.plot(x + 26 * np.sin(th + t), ys_, color=to_rgba(BL, al), lw=4, zorder=11)
    ax.plot(x - 26 * np.sin(th + t), ys_, color=to_rgba(MI, al), lw=4, zorder=11)

def s6(ax, t, lt, a, v):
    items = [("extra weight", GL), ("too little exercise", PINK), ("genetics", BL)]
    for k, (n, col) in enumerate(items):
        q = ease(seg(lt, 0.2 + 0.9 * k, 0.7 + 0.9 * k))
        if q <= 0: continue
        y = 1360 - k * 200; xo = (1 - q) * 60
        card(ax, 120 + xo, y - 80, 840, 160, a * q, ec=col, fc=CARDC, z=9, lw=2.5)
        al = a * q
        if k == 0: icon_scale(ax, 230 + xo, y, al, col)
        elif k == 1: icon_shoe(ax, 230 + xo, y, al, col, t)
        else: icon_dna(ax, 230 + xo, y, al, t)
        tx(ax, 340 + xo, y, n, 34, WHITE, al, ha="left", z=12)
    tx(ax, 540, 760, "all raise the risk", 26, MUTED, a * ease(seg(lt, 3.0, 3.5)), w="semibold")

def drop(ax, x, y, s, al, col=BL, z=11):
    th = np.linspace(0, 2 * np.pi, 60)
    pts = [(x, y + 60 * s)] + [(x + 34 * s * np.cos(u), y + 34 * s * np.sin(u)) for u in np.linspace(np.pi * 0.1 + np.pi, np.pi * 1.9 + np.pi, 40)]
    pts = [(x, y + 62 * s)] + [(x + 36 * s * np.cos(u), y - 4 * s + 36 * s * np.sin(u)) for u in np.linspace(np.pi * 0.85, np.pi * 2.15, 40)][::-1]
    ax.add_patch(Polygon(pts, closed=True, fc=to_rgba(col, 0.35 * al), ec=to_rgba(col, al), lw=3, zorder=z))

def s7(ax, t, lt, a, v):
    items = ["thirst", "frequent urination", "blurred vision", "tiredness"]
    for k, n in enumerate(items):
        q = ease(seg(lt, 0.2 + 0.7 * k, 0.6 + 0.7 * k))
        if q <= 0: continue
        r_, c_ = divmod(k, 2)
        x = 300 + c_ * 480; y = 1270 - r_ * 330
        card(ax, x - 215, y - 140, 430, 280, a * q, ec=LN, fc=CARDC, z=9, lw=2)
        al = a * q; cy = y + 40
        if k == 0: drop(ax, x, cy, 1.0, al)
        elif k == 1:
            for j in range(3):
                ring(ax, x, cy, 18 + j * 18, BL, al * (1 - ((t * 0.8 + j / 3) % 1)), lw=3, z=11)
        elif k == 2:
            ax.add_patch(Ellipse((x, cy), 130, 64, fc=to_rgba(WHITE, 0.08 * al), ec=to_rgba(BLL, al), lw=3, zorder=11))
            for j in range(3): ax.add_patch(Circle((x + 4 * j - 4, cy), 22, fc=to_rgba(BL, 0.25 * al), ec="none", zorder=11.1))
        else:
            ax.add_patch(FancyBboxPatch((x - 55, cy - 26), 110, 52, boxstyle="round,pad=0,rounding_size=8", fc="none", ec=to_rgba(BLL, al), lw=3, zorder=11))
            ax.add_patch(Rectangle((x + 55, cy - 10), 10, 20, fc=to_rgba(BLL, al), zorder=11))
            ax.add_patch(Rectangle((x - 48, cy - 19), 22, 38, fc=to_rgba(RED, al), zorder=11.1))
        tx(ax, x, y - 85, n, 24, WHITE, al, w="semibold", z=12)

def s8(ax, t, lt, a, v):
    person(ax, 540, 1220, 2.2 * pop(lt, 0.0), OKC, a, fill=0.25)
    yrs = ease(seg(lt, 0.4, 2.2))
    ax.plot([150, 150 + 780 * yrs], [930, 930], color=to_rgba(MUTED, a), lw=4, zorder=9)
    for k in range(5):
        if yrs * 5 >= k + 0.5:
            ax.add_patch(Circle((228 + k * 156, 930), 12, fc=to_rgba(BL, a), zorder=10))
            tx(ax, 228 + k * 156, 880, f"year {k+1}", 18, MUTED, a, w="normal")
    lbl(ax, 540, 780, "no symptoms", a * ease(seg(lt, 1.0, 1.5)), WHITE, 26, ec=BL)

def heart(ax, x, y, s, al, col=RED, z=11):
    u = np.linspace(0, 2 * np.pi, 80)
    hx = 16 * np.sin(u) ** 3; hy = 13 * np.cos(u) - 5 * np.cos(2 * u) - 2 * np.cos(3 * u) - np.cos(4 * u)
    ax.add_patch(Polygon(np.stack([x + hx * s, y + hy * s], 1), closed=True, fc=to_rgba(col, 0.3 * al), ec=to_rgba(col, al), lw=3, zorder=z))

def s9(ax, t, lt, a, v):
    items = ["heart", "eyes", "kidneys", "nerves"]
    cx, cy = 540, 1100
    glucose(ax, cx, cy, 60 * pop(lt, 0.0), a, rot=t * 0.4, z=12)
    for k, n in enumerate(items):
        q = ease(seg(lt, 0.8 + 0.6 * k, 1.3 + 0.6 * k))
        if q <= 0: continue
        ang = np.pi * (0.75 - 0.5 * k)
        x = cx + 300 * np.cos(np.pi / 4 + k * np.pi / 2); y = cy + 250 * np.sin(np.pi / 4 + k * np.pi / 2)
        x, y = [(300, 1330), (780, 1330), (780, 870), (300, 870)][k]
        ax.plot([cx, cx + (x - cx) * q], [cy, cy + (y - cy) * q], color=to_rgba(RED, 0.6 * a), lw=6, zorder=9)
        ax.add_patch(Circle((x, y), 95, fc=to_rgba(CARDC, a * q), ec=to_rgba(RED, a * q), lw=3, zorder=10))
        al = a * q
        if k == 0: heart(ax, x, y + 6, 3.2, al)
        elif k == 1:
            ax.add_patch(Ellipse((x, y + 10), 110, 56, fc=to_rgba(WHITE, 0.1 * al), ec=to_rgba(WHITE, al), lw=3, zorder=11))
            ax.add_patch(Circle((x, y + 10), 20, fc=to_rgba(BL, al), zorder=11.1))
        elif k == 2:
            for sx in (-24, 24):
                ax.add_patch(Ellipse((x + sx, y + 10), 38, 66, fc=to_rgba(PINK, 0.35 * al), ec=to_rgba(PINK, al), lw=3, zorder=11))
        else:
            ax.add_patch(Circle((x - 30, y + 10), 13, fc=to_rgba(GL, al), zorder=11))
            ax.plot([x - 30, x + 40], [y + 10, y + 10], color=to_rgba(GL, al), lw=4, zorder=11)
            for j in range(3): ax.plot([x - 30, x - 55 + j * 25], [y + 10, y + 40], color=to_rgba(GL, al), lw=3, zorder=11)
        tx(ax, x, y - 140, n, 24, WHITE, al, w="semibold")

def s10(ax, t, lt, a, v):
    q = pop(lt, 0.0)
    if q > 0:
        ax.add_patch(FancyBboxPatch((370, 830), 340 * q, 520 * q, boxstyle="round,pad=0,rounding_size=50", fc=to_rgba(CARDC, a), ec=to_rgba(BL, a), lw=4, zorder=9))
        ax.add_patch(FancyBboxPatch((410, 1120), 260 * q, 170 * q, boxstyle="round,pad=0,rounding_size=20", fc=to_rgba("#0B1E3A", a), ec=to_rgba(BLL, 0.6 * a), lw=2, zorder=10))
        ax.add_patch(Rectangle((520, 800), 40, 40, fc=to_rgba(MUTED, a), zorder=9))
    s = ease(seg(lt, 0.6, 1.4))
    drop(ax, 540, 760 - 0 * s, 0.9, a * s, col=RED)
    sc = ease(seg(lt, 1.2, 2.2))
    if sc > 0:
        ax.add_patch(Rectangle((440, 1190), 200 * sc, 30, fc=to_rgba(BL, a), zorder=11))
        tx(ax, 540, 1250, "glucose", 22, BLL, a, w="semibold", z=11)
    check(ax, 540, 990, 50, a * ease(seg(lt, 2.0, 2.4)), col=OKC)

CH = 22
def s11(ax, t, lt, a, v):
    rng = np.random.default_rng(5)
    card(ax, 60, 760, 960, 620, a, ec=LN, fc=CARDC, z=8)
    p = ease(seg(lt, 0.2, 2.6))
    xs_ = np.linspace(110, 980, 600)
    base = rng.exponential(1.0, 600) * 55
    peaks = [40, 95, 150, 190, 240, 300, 330, 380, 430, 470, 520, 570]
    for pk in peaks:
        base += 380 * rng.uniform(0.55, 1.0) * np.exp(-((np.arange(600) - pk) / 2.2) ** 2)
    n = int(600 * p)
    cols = [BL if (i * CH // 600) % 2 == 0 else VIOL for i in range(600)]
    ax.scatter(xs_[:n], 800 + np.minimum(base[:n], 520), s=14, c=cols[:n], alpha=a, linewidths=0, zorder=9)
    sl = ease(seg(lt, 2.4, 2.9))
    if sl > 0:
        ax.plot([100, 100 + 890 * sl], [1060, 1060], color=to_rgba(RED, a), lw=2.5, ls=(0, (6, 6)), zorder=10)
    for k, pk in enumerate(peaks):
        h = ease(seg(lt, 3.0 + k * 0.08, 3.4 + k * 0.08))
        if h > 0 and base[pk] > 260:
            ring(ax, xs_[pk], 800 + min(base[pk], 520), 20, GL, a * h, lw=3, z=11)
    tx(ax, 540, 1460, f"{2.5 * ease(seg(lt, 0.2, 1.6)):.1f} million people", 34, WHITE, a * ease(seg(lt, 0.2, 0.6)))
    lbl(ax, 540, 690, "611 genome regions linked", a * ease(seg(lt, 3.6, 4.1)), GLL, 26, ec=GL)

CL = [BL, GL, MI, PINK, VIOL, "#F97316", "#22D3EE", "#E5E7EB"]
CC = [(260, 1340), (540, 1380), (820, 1340), (220, 1100), (860, 1100), (300, 870), (540, 960), (780, 870)]
R1 = np.random.default_rng(9)
PTS = [(R1.integers(0, 8), R1.uniform(120, 960), R1.uniform(780, 1440), R1.normal(0, 38), R1.normal(0, 38)) for _ in range(160)]
def s12(ax, t, lt, a, v):
    g = ease(seg(lt, 0.3, 2.0))
    for (c, x0, y0, dx, dy) in PTS:
        cx, cy = CC[c]
        x = x0 + (cx + dx - x0) * g; y = y0 + (cy + dy - y0) * g
        col = mixc(GR, CL[c], g)
        ax.add_patch(Circle((x, y), 9, fc=to_rgba(col, a), zorder=10))
    for k, (cx, cy) in enumerate(CC):
        q = ease(seg(lt, 2.0 + 0.1 * k, 2.4 + 0.1 * k))
        ring(ax, cx, cy, 95, CL[k], a * q * 0.8, lw=2.5, z=9)
    lbl(ax, 540, 690, "8 clusters · different pathways", a * ease(seg(lt, 2.4, 2.9)), WHITE, 25, ec=BL)

def s13(ax, t, lt, a, v):
    items = [("healthy diet", GL), ("active 150 min / week", MI), ("no smoking", RED)]
    for k, (n, col) in enumerate(items):
        q = ease(seg(lt, 0.1 + 0.9 * k, 0.6 + 0.9 * k))
        if q <= 0: continue
        y = 1360 - k * 200; xo = (1 - q) * 60; al = a * q
        card(ax, 120 + xo, y - 80, 840, 160, al, ec=col, fc=CARDC, z=9, lw=2.5)
        ix = 230 + xo
        if k == 0:
            ax.add_patch(Circle((ix, y), 48, fc=to_rgba(WHITE, 0.08 * al), ec=to_rgba(MUTED, al), lw=3, zorder=11))
            ax.add_patch(Wedge((ix, y), 34, 90, 210, fc=to_rgba(OKC, al), zorder=11.1))
            ax.add_patch(Wedge((ix, y), 34, 210, 330, fc=to_rgba(GL, al), zorder=11.1))
            ax.add_patch(Wedge((ix, y), 34, 330, 450, fc=to_rgba(PINK, al), zorder=11.1))
        elif k == 1:
            ring(ax, ix, y, 46, GR, al, lw=6, z=11)
            fr = ease(seg(lt, 1.2, 2.4))
            if fr > 0: ax.add_patch(Wedge((ix, y), 49, 90 - 360 * fr, 90, width=8, fc=to_rgba(MI, al), zorder=11.1))
        else:
            ax.add_patch(Rectangle((ix - 50, y - 10), 80, 20, fc=to_rgba(WHITE, al), zorder=11))
            ax.add_patch(Rectangle((ix + 30, y - 10), 20, 20, fc=to_rgba("#F97316", al), zorder=11))
            cross(ax, ix, y, 38, al, z=12)
        check(ax, 900 + xo, y, 22, al * ease(seg(lt, 0.5 + 0.9 * k, 0.9 + 0.9 * k)), col=OKC)
        tx(ax, 340 + xo, y, n, 32, WHITE, al, ha="left", z=12)

def V():
    sc = [(s0, 0, 0), (s1, 1, 1), (s2, 2, 2), (s3, 3, 3), (s4, 4, 4), (s5, 5, 5), (s6, 6, 6), (s7, 7, 7), (s8, 8, 8),
          (s9, 9, 9), (s10, 10, 10), (s11, 11, 11), (s12, 12, 12), (s13, 13, 13)]
    hd = [(0, 0, "METABOLIC DISEASE", "Type 2 diabetes"), (1, 1, "CLOSE TO HOME", "Pakistan"), (2, 2, "AFTER A MEAL", "Glucose and insulin"),
          (3, 3, "HOW INSULIN WORKS", "A key for cells"), (4, 4, "WHAT GOES WRONG", "Insulin resistance"), (5, 5, "WHAT GOES WRONG", "Not enough insulin"),
          (6, 6, "RISK FACTORS", "Weight, activity, genes"), (7, 7, "WARNING SIGNS", "Know the signs"), (8, 8, "THE CATCH", "Often silent"),
          (9, 9, "COMPLICATIONS", "Damage over time"), (10, 10, "DIAGNOSIS", "A simple blood test"), (11, 11, "BIOINFORMATICS", "Scanning the genome"),
          (12, 12, "BIOINFORMATICS", "Eight clusters"), (13, 13, "LOWER YOUR RISK", "Small daily steps")]
    return Video("v_diab", "DISEASE EXPLAINER", BL, sc, hd, gap=0.25, start=0.4, outro=2.6)

if __name__ == "__main__":
    V().main(sys.argv, seed=1)
