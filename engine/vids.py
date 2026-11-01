from eng import *
R = np.random.default_rng(7)

# ======================= shared drawings =======================
def draw_cell(ax, cx, cy, Rr, t, al, z=6, tint=TEAL):
    th = np.linspace(0, 2 * np.pi, 200)
    r = Rr * (1 + 0.03 * np.sin(5 * th + t * 1.5) + 0.02 * np.sin(9 * th - t))
    P = np.c_[cx + r * np.cos(th), cy + r * np.sin(th)]
    ax.add_patch(Polygon(P, closed=True, fc=to_rgba(tint, 0.10 * al), ec=to_rgba(tint, 0.9 * al), lw=4, zorder=z))
    ax.add_patch(Polygon(P * 1, closed=True, fc="none", ec=to_rgba(tint, 0.15 * al), lw=18, zorder=z - 0.1))
    ax.add_patch(Circle((cx - Rr * 0.12, cy + Rr * 0.05), Rr * 0.32, fc=to_rgba(VIO, 0.35 * al), ec=to_rgba(VIO, al), lw=3, zorder=z + 0.1))
    ax.add_patch(Circle((cx - Rr * 0.05, cy + Rr * 0.12), Rr * 0.08, fc=to_rgba(VIO, 0.8 * al), ec="none", zorder=z + 0.2))
    for k in range(5):
        a = k * 1.25 + 0.4 + 0.1 * np.sin(t + k); d = Rr * 0.62
        ax.add_patch(Ellipse((cx + d * np.cos(a), cy + d * np.sin(a)), Rr * 0.22, Rr * 0.1, angle=np.degrees(a) + 90, fc=to_rgba(ORANGE, 0.5 * al), ec=to_rgba(ORANGE, al), lw=2, zorder=z + 0.1))
    for k in range(14):
        a = k * 0.45 + t * 0.2; d = Rr * (0.4 + 0.45 * ((k * 37) % 10) / 10)
        ax.add_patch(Circle((cx + d * np.cos(a), cy + d * np.sin(a)), 5, fc=to_rgba(SKY, 0.6 * al), zorder=z + 0.1))

def monitor(ax, x, y, w, h, al, z=8, title=None):
    card(ax, x, y, w, h, al, ec=SKY, z=z, r=18, fc="#0A1830", lw=2.5)
    ax.add_patch(Rectangle((x + w / 2 - 50, y - 50), 100, 50, fc=LINE, alpha=al, zorder=z))
    ax.add_patch(FancyBboxPatch((x + w / 2 - 130, y - 64), 260, 16, boxstyle="round,pad=0,rounding_size=8", fc=LINE, alpha=al, zorder=z))
    if title: tx(ax, x + w / 2, y + h - 30, title, 16, MUTED, al, w="normal", z=z + 1, fam=MONO)

def browser(ax, x, y, w, h, al, url, z=8):
    card(ax, x, y, w, h, al, ec=LINE, z=z, r=20, fc="#0A1830", lw=2)
    for j, c in enumerate([MAG, GOLD, GREEN]): ax.add_patch(Circle((x + 32 + j * 28, y + h - 32), 9, fc=c, alpha=al, zorder=z + 1))
    pill(ax, x + w / 2 + 40, y + h - 32, w - 260, 40, "#13294A", al, z=z + 1)
    tx(ax, x + 170, y + h - 32, url, 17, MUTED, al, w="normal", ha="left", z=z + 2, fam=MONO)

def flask(ax, cx, cy, s, al, t, col=GREEN, z=10):
    F = [(-22, 70), (22, 70), (22, 25), (70, -55), (-70, -55), (-22, 25)]
    ax.add_patch(Polygon([(cx + x * s, cy + y * s) for x, y in F], closed=True, fc=to_rgba(col, 0.25 * al), ec=col, lw=3, alpha=al, zorder=z))
    for k in range(4):
        bt = (t * 0.8 + k * 0.25) % 1
        ax.add_patch(Circle((cx + (-25 + k * 16) * s, cy + (-40 + bt * 90) * s), 5 * s, fc=col, alpha=al * (1 - bt), zorder=z + 1))

def icon(ax, kind, cx, cy, s, col, al, t=0, z=12):
    if al <= 0.01: return
    if kind == "search":
        ring(ax, cx - 6 * s, cy + 6 * s, 16 * s, col, al, lw=4, z=z); ax.plot([cx + 6 * s, cx + 20 * s], [cy - 6 * s, cy - 20 * s], color=col, lw=5, alpha=al, zorder=z, solid_capstyle="round")
    elif kind == "book":
        ax.add_patch(Rectangle((cx - 22 * s, cy - 18 * s), 20 * s, 36 * s, fc="none", ec=col, lw=3, alpha=al, zorder=z)); ax.add_patch(Rectangle((cx + 2 * s, cy - 18 * s), 20 * s, 36 * s, fc="none", ec=col, lw=3, alpha=al, zorder=z))
    elif kind == "cube":
        P = np.array([[0, 20], [18, 10], [18, -12], [0, -22], [-18, -12], [-18, 10]]) * s + [cx, cy]
        ax.add_patch(Polygon(P, closed=True, fc=to_rgba(col, 0.2 * al), ec=col, lw=3, alpha=al, zorder=z)); ax.plot([cx - 18 * s, cx, cx + 18 * s], [cy + 10 * s, cy, cy + 10 * s], color=col, lw=2.5, alpha=al, zorder=z); ax.plot([cx, cx], [cy, cy - 22 * s], color=col, lw=2.5, alpha=al, zorder=z)
    elif kind == "fold":
        xs = np.linspace(-22, 22, 80); ax.plot(cx + xs * s, cy + 10 * s * np.sin(xs / 4) + xs * 0.3 * s, color=col, lw=4, alpha=al, zorder=z)
        ax.plot(cx + xs * s * 0.7, cy - 14 * s + 6 * s * np.cos(xs / 3), color=col, lw=4, alpha=al * 0.7, zorder=z)
    elif kind == "net":
        pts = np.array([[0, 0], [-20, 14], [20, 16], [-16, -18], [18, -16]]) * s + [cx, cy]
        for p in pts[1:]: ax.plot([pts[0, 0], p[0]], [pts[0, 1], p[1]], color=col, lw=2.5, alpha=al, zorder=z)
        for p in pts: ax.add_patch(Circle(p, 6 * s, fc=col, alpha=al, zorder=z + 0.1))
    elif kind == "flow":
        for k in range(3): pill(ax, cx - 20 * s + k * 20 * s, cy + 16 * s - k * 16 * s, 26 * s, 14 * s, col, al, z=z)
    elif kind == "dna":
        xs = np.linspace(-24, 24, 60); ax.plot(cx + xs * s, cy + 12 * s * np.sin(xs / 6), color=col, lw=3, alpha=al, zorder=z); ax.plot(cx + xs * s, cy - 12 * s * np.sin(xs / 6), color=WHITE, lw=3, alpha=al * 0.7, zorder=z)
    elif kind == "chart":
        for k, h in enumerate([14, 26, 20, 36]): ax.add_patch(Rectangle((cx - 24 * s + k * 13 * s, cy - 18 * s), 9 * s, h * s, fc=col, alpha=al, zorder=z))
    elif kind == "brain":
        net = np.array([[-18, 12], [-18, -12], [0, 18], [0, 0], [0, -18], [18, 8], [18, -8]]) * s + [cx, cy]
        for a in range(2):
            for b in range(2, 5): ax.plot(*zip(net[a], net[b]), color=col, lw=1.5, alpha=al * 0.7, zorder=z)
        for a in range(2, 5):
            for b in range(5, 7): ax.plot(*zip(net[a], net[b]), color=col, lw=1.5, alpha=al * 0.7, zorder=z)
        for p in net: ax.add_patch(Circle(p, 5 * s, fc=col, alpha=al, zorder=z + .1))
    elif kind == "hospital":
        ax.add_patch(Rectangle((cx - 8 * s, cy - 22 * s), 16 * s, 44 * s, fc=col, alpha=al, zorder=z)); ax.add_patch(Rectangle((cx - 22 * s, cy - 8 * s), 44 * s, 16 * s, fc=col, alpha=al, zorder=z))
    elif kind == "pipe":
        ax.plot([cx - 24 * s, cx + 24 * s], [cy, cy], color=col, lw=5, alpha=al, zorder=z)
        for k in range(3): ax.add_patch(Circle((cx - 24 * s + k * 24 * s, cy), 8 * s, fc=BG, ec=col, lw=3, alpha=al, zorder=z + .1))
    elif kind == "linux":
        card(ax, cx - 26 * s, cy - 20 * s, 52 * s, 40 * s, al, ec=col, z=z, r=6); tx(ax, cx - 14 * s, cy, ">_", 16 * s, col, al, z=z + 1, fam=MONO, ha="left")
    elif kind == "code":
        tx(ax, cx, cy, "{ }", 26 * s, col, al, z=z, fam=MONO)
    elif kind == "db":
        for k in range(3): ax.add_patch(Ellipse((cx, cy + 16 * s - k * 16 * s), 44 * s, 14 * s, fc=to_rgba(col, 0.2 * al), ec=col, lw=2.5, alpha=al, zorder=z + k * 0.01))
    elif kind == "git":
        pts = [(cx - 14 * s, cy - 18 * s), (cx - 14 * s, cy + 18 * s), (cx + 14 * s, cy + 2 * s)]
        ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], color=col, lw=3, alpha=al, zorder=z); ax.plot([pts[0][0], pts[2][0]], [pts[0][1] + 10 * s, pts[2][1]], color=col, lw=3, alpha=al, zorder=z)
        for p in pts: ax.add_patch(Circle(p, 6 * s, fc=BG, ec=col, lw=3, alpha=al, zorder=z + .1))

def cardrow(ax, x, y, w, h, al, num, title, sub, col, kind, t, hl=0, url=None):
    card(ax, x, y, w, h, al, ec=mixc(LINE, col, 0.4 + 0.6 * hl), lw=1.5 + 2 * hl, z=8)
    ax.add_patch(Circle((x + 70, y + h / 2), 44, fc=to_rgba(col, 0.15 * al), ec=to_rgba(col, al), lw=2, zorder=9))
    icon(ax, kind, x + 70, y + h / 2, 1.0, col, al, t)
    if num: tx(ax, x + w - 30, y + h - 30, num, 18, col, al * 0.8, ha="right", z=10)
    tx(ax, x + 135, y + h / 2 + (22 if sub else 0) + (10 if url else 0), title, 28, WHITE, al, ha="left", z=10)
    if sub: tx(ax, x + 135, y + h / 2 - 18 + (10 if url else 0), sub, 18, MUTED, al, w="normal", ha="left", z=10)
    if url: tx(ax, x + 135, y + h / 2 - 50, url, 15, col, al, w="normal", ha="left", z=10, fam=MONO)

# ======================= V01 virtual cell =======================
def v1_s0(ax, t, lt, a, v):
    for k in range(4):
        ph = (lt * 0.6 + k / 4) % 1
        ring(ax, 540, 1120, 80 + ph * 330, MAG, a * (1 - ph) * 0.8, lw=3)
    glowdot(ax, 540, 1120, 40, MAG, a)
    tx(ax, 540, 1120, "LIVE", 24, WHITE, a, z=12)
    card(ax, 340, 760, 400, 90, a * ease(seg(lt, 0.4, 0.9)), ec=GOLD)
    tx(ax, 540, 805, "7 OCTOBER 2026", 28, GOLD, a * ease(seg(lt, 0.4, 0.9)), z=10)
def v1_s1(ax, t, lt, a, v):
    g = eout(seg(lt, 0.3, 3.5))
    tx(ax, 540, 1190, f"${1.8*g:.1f}B", 150, GOLD, a)
    tx(ax, 540, 1060, "committed to AI models of living cells", 24, MUTED, a, w="normal")
    for k in range(9):
        h = (80 + k * 28) * eout(seg(lt, 0.3 + k * 0.12, 1.3 + k * 0.12))
        ax.add_patch(FancyBboxPatch((180 + k * 82, 760), 56, h + 0.1, boxstyle="round,pad=0,rounding_size=8", fc=mixc(TEAL, GOLD, k / 8), alpha=a * 0.85, ec="none", zorder=8))
def v1_s2(ax, t, lt, a, v):
    names = ["Biohub", "US Dept. of Energy", "NIH", "Google DeepMind", "Isomorphic Labs", "Meta"]
    cx, cy = 540, 1120
    glowdot(ax, cx, cy, 70, TEAL, a, z=9); tx(ax, cx, cy + 12, "Virtual", 20, BG, a, z=12); tx(ax, cx, cy - 16, "Biology", 20, BG, a, z=12)
    for k, n in enumerate(names):
        ang = np.pi / 2 + k * 2 * np.pi / 6; x, y = cx + 340 * np.cos(ang), cy + 300 * np.sin(ang)
        p = pop(lt, 0.3 + k * 0.45)
        if p <= 0: continue
        ax.plot([cx, x], [cy, y], color=TEAL, lw=2, alpha=0.4 * a, zorder=7)
        pill(ax, x, y, (len(n) * 15 + 50) * p, 64 * p, CARD, a, ec=[TEAL, SKY, GREEN, GOLD, VIO, ORANGE][k], lw=2.5, z=10)
        tx(ax, x, y, n, 21 * p, WHITE, a, z=11)
        ph = (t * 0.7 + k / 6) % 1
        glowdot(ax, x + (cx - x) * ph, y + (cy - y) * ph, 6, GOLD, a * 0.8, z=8)
def v1_s3(ax, t, lt, a, v):
    draw_cell(ax, 560, 1130, 230, t, a)
    tx(ax, 560, 860, "virtual cell model", 20, MUTED, a, w="normal")
    i1 = ease(seg(lt, 0.8, 1.6)); i2 = ease(seg(lt, 1.6, 2.4))
    molecule(ax, 140, 1280, 34, GOLD, a * i1, rot=t)
    tx(ax, 140, 1200, "drug", 20, GOLD, a * i1)
    arrow(ax, 200, 1260, 330 + 0 * i1, 1200, GOLD, a * i1)
    helix(ax, t, 990, 90, 200, 16, a * i2, turns=1.2, lw=3, rungs=6)
    tx(ax, 145, 930, "gene edit", 20, SKY, a * i2)
    arrow(ax, 210, 1000, 330, 1060, SKY, a * i2)
    o = seg(lt, 2.6, 3.6)
    if o > 0:
        tx(ax, 920, 1340, "predicted", 18, MUTED, a * ease(o), w="normal")
        for k, (lab, v_, c) in enumerate([("growth", 0.3, SKY), ("stress", 0.8, MAG), ("repair", 0.6, GREEN)]):
            y = 1270 - k * 70; ww = 150 * v_ * eout(o)
            tx(ax, 830, y, lab, 17, WHITE, a * ease(o), ha="right", w="normal")
            ax.add_patch(FancyBboxPatch((845, y - 12), ww + 0.1, 24, boxstyle="round,pad=0,rounding_size=12", fc=c, alpha=a, zorder=10))
def v1_s4(ax, t, lt, a, v):
    monitor(ax, 120, 1000, 520, 400, a, title="in silico experiments")
    for k in range(24):
        x = 175 + (k % 6) * 80; y = 1310 - (k // 6) * 75
        on = (k * 7) % 24 < 24 * seg(lt, 0.3, 2.3)
        good = k in (3, 14, 20) and lt > 2.6
        ax.add_patch(Circle((x, y), 22, fc=to_rgba(GREEN if good else (SKY if on else LINE), a * (1 if good else 0.6)), ec="none", zorder=10))
    f = ease(seg(lt, 2.8, 3.6))
    arrow(ax, 670, 1200, 800, 1200, GREEN, a * f, lw=4)
    flask(ax, 900, 1190, 1.3, a * f, t)
    tx(ax, 900, 1030, "only the best", 20, GREEN, a * f)
    tx(ax, 900, 995, "go to the lab", 20, GREEN, a * f)
def v1_s5(ax, t, lt, a, v):
    for k in range(3):
        ax.add_patch(Ellipse((540, 900 + k * 70), 420, 110, fc=to_rgba(TEAL, 0.15 * a), ec=to_rgba(TEAL, a), lw=3, zorder=8 + k * 0.01))
    tx(ax, 540, 1040, "OPEN  ·  AI-READY", 26, TEAL, a, z=12)
    for k in range(18):
        ph = (t * 0.5 + k / 18) % 1; x = 160 + (k * 97) % 760
        y = 1500 - ph * 420
        al_ = a * np.clip(1 - abs(ph - 0.5) * 2, 0, 1) * 1.4
        icon(ax, "cube", x, y, 0.8, [SKY, GOLD, GREEN, VIO][k % 4], min(al_, a), z=9)

# ======================= V02 Evo 2 =======================
SEQ = "ATGCGTACCGATTGCAAGTCCGATAGCTTAGGCATCGATCGGATCCATGGCATTACG"
def v2_s0(ax, t, lt, a, v):
    card(ax, 400, 1060, 280, 200, a, ec=TEAL, r=40)
    tx(ax, 540, 1160, "AI", 80, TEAL, a, z=12)
    for k in range(2):
        y = [1400, 900][k]; off = (t * 120 * (1 if k == 0 else -1)) % 50
        for j in range(26):
            x = -40 + j * 46 + off * (1 if k == 0 else -1); ch = SEQ[(j + k * 7) % len(SEQ)]
            d = abs(x - 540) / 540
            tx(ax, x, y, ch, 34, BCOL[ch], a * (1 - 0.6 * d), fam=MONO, z=10)
    ax.plot([540, 540], [1260, 1370], color=TEAL, lw=2, ls=(0, (4, 4)), alpha=a, zorder=9)
    ax.plot([540, 540], [930, 1060], color=TEAL, lw=2, ls=(0, (4, 4)), alpha=a, zorder=9)
    tx(ax, 760, 1340, "read", 20, MUTED, a, w="normal"); tx(ax, 760, 970, "write", 20, MUTED, a, w="normal")
def v2_s1(ax, t, lt, a, v):
    p = eout(seg(lt, 0.2, 0.9)); y0 = 760 + (1 - p) * 80
    card(ax, 150, y0, 780, 640, a * p, ec=WHITE, r=10, fc="#F8FAFC", lw=0)
    ax.add_patch(Rectangle((150, y0 + 540), 780, 100, fc="#B91C1C", alpha=a * p, zorder=9))
    tx(ax, 540, y0 + 590, "nature", 54, WHITE, a * p, z=10, w="bold")
    tx(ax, 540, y0 + 470, "Genome modeling and design", 30, "#0F172A", a * p, z=10)
    tx(ax, 540, y0 + 425, "across all domains of life", 30, "#0F172A", a * p, z=10)
    tx(ax, 540, y0 + 380, "with Evo 2", 30, "#0F172A", a * p, z=10)
    for k in range(5): ax.add_patch(Rectangle((210, y0 + 290 - k * 34), 660 - (k == 4) * 260, 12, fc="#CBD5E1", alpha=a * p, zorder=10))
    pill(ax, 540, y0 + 70, 420, 60, "#0F172A", a * ease(seg(lt, 1.0, 1.5)), z=11)
    tx(ax, 540, y0 + 70, "Arc Institute · March 2026", 20, WHITE, a * ease(seg(lt, 1.0, 1.5)), z=12)
def v2_s2(ax, t, lt, a, v):
    g = eout(seg(lt, 0.2, 2.6))
    tx(ax, 540, 1360, f"{9.3*g:.1f} trillion", 90, TEAL, a)
    tx(ax, 540, 1270, "DNA letters learned", 24, MUTED, a, w="normal")
    n = int(180 * eout(seg(lt, 1.2, 3.4)))
    for k in range(n):
        ang = k * 2.39996; r = 14 * np.sqrt(k)
        x = 540 + r * np.cos(ang); y = 960 + r * np.sin(ang) * 0.9
        ax.add_patch(Circle((x, y), 6, fc=[TEAL, SKY, GREEN, GOLD, VIO][k % 5], alpha=a * 0.85, zorder=8))
    tx(ax, 540, 760, "100,000+ species · bacteria · archaea · plants · animals", 19, WHITE, a * ease(seg(lt, 1.5, 2.2)), w="semibold")
def v2_s3(ax, t, lt, a, v):
    s = "GATTACAGGCTAGCAT"; mpos = 8
    for j, ch in enumerate(s):
        x = 160 + j * 48; mut = j == mpos and lt > 0.8
        c = MAG if mut else BCOL[ch]
        tx(ax, x, 1380, "T" if mut else ch, 36, c, a, fam=MONO)
    if lt > 0.8: ring(ax, 160 + mpos * 48, 1380, 32, MAG, a, lw=3)
    tx(ax, 540, 1300, "BRCA1 variant", 20, MUTED, a, w="normal")
    g = eout(seg(lt, 1.2, 3.2))
    ax.add_patch(Wedge((540, 1000), 210, 90 - 360 * 0.9 * g, 90, width=30, fc=TEAL, alpha=a, zorder=9))
    ring(ax, 540, 1000, 195, LINE, a, lw=30, z=8)
    tx(ax, 540, 1020, f">{int(90*g)}%", 76, WHITE, a)
    tx(ax, 540, 950, "accuracy", 22, TEAL, a)
    for k, (lab, c) in enumerate([("benign", GREEN), ("pathogenic", MAG)]):
        p = pop(lt, 2.0 + k * 0.3)
        pill(ax, 330 + k * 420, 750, 220 * p, 56 * p, to_rgba(c, 0.2), a, ec=c, lw=2, z=10)
        tx(ax, 330 + k * 420, 750, lab, 20 * p, c, a, z=11)
def v2_s4(ax, t, lt, a, v):
    g = eout(seg(lt, 0.2, 3.0)); cx, cy, r = 540, 1080, 280
    th = np.linspace(np.pi / 2, np.pi / 2 - 2 * np.pi * g, 300)
    ax.plot(cx + r * np.cos(th), cy + r * np.sin(th), color=LINE, lw=26, alpha=a, zorder=7, solid_capstyle="round")
    cols = [TEAL, GOLD, SKY, MAG, GREEN, VIO, ORANGE]
    for k in range(14):
        s0 = k / 14; s1 = s0 + 0.05
        if s0 > g: break
        th2 = np.linspace(np.pi / 2 - 2 * np.pi * s0, np.pi / 2 - 2 * np.pi * min(s1, g), 30)
        ax.plot(cx + r * np.cos(th2), cy + r * np.sin(th2), color=cols[k % 7], lw=26, alpha=a, zorder=8)
    tx(ax, cx, cy + 30, "AI-designed", 30, WHITE, a); tx(ax, cx, cy - 20, "genome", 30, TEAL, a)
    tx(ax, cx, 740, "bacteriophage-scale genomes, designed in silico", 19, MUTED, a * ease(seg(lt, 1.0, 1.6)), w="normal")
def v2_s5(ax, t, lt, a, v):
    items = [("Model weights", TEAL), ("Code", GOLD), ("Training data", SKY)]
    for k, (n, c) in enumerate(items):
        p = pop(lt, 0.3 + k * 0.5); y = 1320 - k * 200
        if p <= 0: continue
        card(ax, 180, y - 75, 720, 150, a, ec=c, z=8)
        x0 = 280; u = ease(seg(lt, 0.7 + k * 0.5, 1.1 + k * 0.5))
        ax.add_patch(Rectangle((x0 - 30, y - 40), 60, 50, fc=c, alpha=a, zorder=10))
        th = np.linspace(0, np.pi, 30); ax.plot(x0 + 20 * np.cos(th) + 18 * u, y + 10 + 28 * np.sin(th) + 12 * u, color=c, lw=6, alpha=a, zorder=10)
        tx(ax, 360, y, n, 34, WHITE, a, ha="left", z=10)
        tx(ax, 860, y, "FREE", 22, c, a, ha="right", z=10)

# ======================= V03 CRISPR =======================
DNA_T = "TACGGATCCTAGCATGGCTTACGATCGATTGCCAGTAGGCATCG"
CR_Y = 1060; CR_X0 = 40; CR_DX = 23.5; TG0, TG1 = 18, 38   # target bases
def crispr_scene(ax, t, lt, a, v):
    T_ = v.T; tt = t
    cut = ease(seg(tt, T_[3] + 0.6, T_[3] + 1.4))
    rep = ease(seg(tt, T_[4] + 0.8, T_[4] + 2.2))
    gap = 70 * cut * (1 - rep)
    draw = eout(seg(tt, T_[0] - 0.2, T_[0] + 1.8))
    for j, ch in enumerate(DNA_T):
        x = CR_X0 + j * CR_DX
        if x > CR_X0 + 1040 * draw: break
        shift = -gap / 2 if j < (TG0 + TG1) // 2 else gap / 2
        x += shift
        inT = TG0 <= j < TG1; ed = inT and rep > 0 and j in (29, 30)
        hl = ease(seg(tt, T_[2] + 2.0, T_[2] + 2.6)) if inT else 0
        c1 = MAG if ed else BCOL[ch]; c2 = BCOL["ATGC"["TACG".index(ch)]]
        ax.plot([x, x], [CR_Y + 10, CR_Y + 55], color=c1, lw=6, alpha=a, zorder=6)
        ax.plot([x, x], [CR_Y - 10, CR_Y - 55], color=c2, lw=6, alpha=a * 0.8, zorder=6)
        if hl > 0: ax.add_patch(Rectangle((x - 11, CR_Y - 70), 22, 140, fc=GOLD, alpha=0.12 * a * hl, zorder=5))
    for side in (-1, 1):
        for yb in (CR_Y + 58, CR_Y - 58):
            xs = np.array([CR_X0, CR_X0 + 1040 * draw])
            if gap > 1:
                mid = CR_X0 + ((TG0 + TG1) // 2) * CR_DX - CR_DX / 2
                xl = [CR_X0 - gap / 2, mid - gap / 2] if side < 0 else [mid + gap / 2, CR_X0 + 1040 * draw + gap / 2]
            else:
                if side > 0: continue
                xl = xs
            ax.plot(xl, [yb, yb], color=SKY if yb > CR_Y else GREEN, lw=7, alpha=a, zorder=7, solid_capstyle="round")
    if cut > 0 and rep < 0.5:
        mid = CR_X0 + ((TG0 + TG1) // 2) * CR_DX - CR_DX / 2
        for k in range(8):
            an = k * np.pi / 4 + t; r = 30 + 40 * cut
            ax.plot([mid + 20 * np.cos(an), mid + r * np.cos(an)], [CR_Y + 20 * np.sin(an), CR_Y + r * np.sin(an)], color=GOLD, lw=3, alpha=a * (1 - cut * 0.6), zorder=12)
        tx(ax, mid, CR_Y - 150, "double-strand break", 22, GOLD, a * cut)
    # guide RNA
    gA = ease(seg(tt, T_[1] + 0.3, T_[1] + 1.0))
    move = eout(seg(tt, T_[2] + 0.2, T_[2] + 2.2))
    tgtx = CR_X0 + TG0 * CR_DX; startx = 60
    gx = startx + (tgtx - startx) * move
    gy = CR_Y + 300 - 150 * ease(seg(tt, T_[2] + 2.0, T_[2] + 2.6))
    away = ease(seg(tt, T_[4] + 0.3, T_[4] + 1.0)); a = a * (1 - away) if False else a
    gfade = 1 - away
    if gA > 0:
        cas = ease(seg(tt, T_[2], T_[2] + 0.5))
        if cas > 0:
            ax.add_patch(FancyBboxPatch((gx - 40, gy - 70), (TG1 - TG0) * CR_DX + 80, 170, boxstyle="round,pad=0,rounding_size=70", fc=to_rgba(VIO, 0.35 * a * cas * gfade), ec=to_rgba(VIO, a * cas * gfade), lw=3, zorder=9))
            tx(ax, gx + (TG1 - TG0) * CR_DX / 2, gy + 70, "Cas9", 26, WHITE, a * cas * gfade, z=11)
        for j in range(TG1 - TG0):
            ch = "AUGC"["TACG".index(DNA_T[TG0 + j])] if False else "UACG"["ATGC".index(DNA_T[TG0 + j])]
            tx(ax, gx + j * CR_DX, gy, ch, 22, GOLD, a * gA * gfade, fam=MONO, z=12)
        ax.plot([gx - 8, gx + (TG1 - TG0) * CR_DX], [gy - 22, gy - 22], color=GOLD, lw=4, alpha=a * gA * gfade, zorder=12)
        if lt < 0 or tt < T_[2]:
            tx(ax, gx + 120, gy + 60, "guide RNA (20 letters)", 20, GOLD, a * gA * (1 - ease(seg(tt, T_[2], T_[2] + 0.4))), ha="left")
    if rep > 0:
        for k, (lab, c) in enumerate([("gene switched OFF", MAG), ("gene corrected", GREEN)]):
            p = pop(tt, T_[4] + 2.2 + k * 0.4)
            pill(ax, 300 + k * 480, 780, 380 * p, 64 * p, to_rgba(c, 0.18), a, ec=c, lw=2, z=12)
            tx(ax, 300 + k * 480, 780, lab, 22 * p, c, a, z=13)
def v3_s5(ax, t, lt, a, v):
    card(ax, 90, 740, 900, 680, a, ec=SKY)
    tx(ax, 140, 1370, "guide design", 20, MUTED, a, ha="left", w="normal", fam=MONO)
    tx(ax, 650, 1370, "on-target", 17, TEAL, a, w="normal"); tx(ax, 850, 1370, "off-target", 17, MAG, a, w="normal")
    rows = [("GGCATGGCTTACGATCGATT", .92, .05), ("CTAGCATGGCTTACGATCGA", .81, .22), ("ATCCTAGCATGGCTTACGAT", .74, .41), ("GATTGCCAGTAGGCATCGTA", .55, .63), ("TACGGATCCTAGCATGGCTT", .42, .80)]
    for k, (s, on, off) in enumerate(rows):
        p = pop(lt, 0.3 + k * 0.3); y = 1280 - k * 105
        if p <= 0: continue
        best = k == 0 and lt > 2.4
        if best: card(ax, 110, y - 42, 860, 84, a * ease(seg(lt, 2.4, 2.8)), ec=GOLD, z=8.5, r=14, fc="#13294A")
        tx(ax, 140, y, s, 19, WHITE, a, ha="left", fam=MONO, z=10)
        g = eout(seg(lt, 0.5 + k * 0.3, 1.5 + k * 0.3))
        for x0, val, c in ((580, on, TEAL), (780, off, MAG)):
            ax.add_patch(FancyBboxPatch((x0, y - 10), 140, 20, boxstyle="round,pad=0,rounding_size=10", fc=LINE, alpha=a, zorder=9))
            ax.add_patch(FancyBboxPatch((x0, y - 10), 140 * val * g + 0.1, 20, boxstyle="round,pad=0,rounding_size=10", fc=c, alpha=a, zorder=9.5))
    b = pop(lt, 2.6)
    pill(ax, 540, 690, 330 * b, 60 * b, GOLD, a, z=12); tx(ax, 540, 690, "BEST GUIDE", 22 * b, BG, a, z=13)

# ======================= V04 NGS =======================
FRAGS = [(R.uniform(0, 1), R.integers(5, 11)) for _ in range(14)]
def v4_s0(ax, t, lt, a, v):
    helix(ax, t, 1120, 80, 1000, 120, a, turns=3)
    n = int(3e9 * eout(seg(lt, 0.3, 3.0)))
    tx(ax, 540, 850, f"{n:,}", 64, WHITE, a, fam=MONO)
    tx(ax, 540, 780, "letters in one human genome", 22, MUTED, a, w="normal")
def v4_s1(ax, t, lt, a, v):
    sp = eout(seg(lt, 0.6, 2.2))
    for k in range(14):
        L = 120 + (k * 53) % 90; x0 = 60 + (k % 4) * 245; y0 = 1380 - (k // 4) * 150
        bx = 60 + k * 68; by = 1150
        x = bx * (1 - sp) + x0 * sp; y = by * (1 - sp) + y0 * sp; w = 68 * (1 - sp) + L * sp
        for j in range(int(w // 14)):
            ch = "ATGC"[(k * 3 + j) % 4]
            ax.add_patch(Rectangle((x + j * 14, y - 18), 12, 36, fc=BCOL[ch], alpha=a * 0.9, zorder=8))
    if sp > 0.95: tx(ax, 540, 760, "millions of short fragments", 24, MUTED, a, w="normal")
def v4_s2(ax, t, lt, a, v):
    card(ax, 90, 720, 900, 520, a, ec=SKY, z=6)
    tx(ax, 540, 1200, "flow cell", 18, MUTED, a, w="normal", z=8)
    for k in range(5):
        L = 160; x = 180 + k * 150 * 0 + (k % 5) * 0; y = 1450 - k * 0
    drop = eout(seg(lt, 0.8, 2.2))
    for k in range(5):
        x = 150 + k * 170; y = 1440 - drop * 420 - (k % 2) * 20
        ax.add_patch(Rectangle((x, y - 12), 110, 24, fc=TEAL, alpha=a * (1 - ease(seg(lt, 2.2, 2.6))), zorder=9))
        ax.add_patch(Rectangle((x - 18, y - 12), 18, 24, fc=GOLD, alpha=a * ease(seg(lt, 0.2, 0.7)) * (1 - ease(seg(lt, 2.2, 2.6))), zorder=9))
        ax.add_patch(Rectangle((x + 110, y - 12), 18, 24, fc=MAG, alpha=a * ease(seg(lt, 0.2, 0.7)) * (1 - ease(seg(lt, 2.2, 2.6))), zorder=9))
    if lt < 1.0: tx(ax, 540, 1500, "+ adapters", 22, GOLD, a * ease(seg(lt, 0.2, 0.7)))
    g = eout(seg(lt, 2.2, 4.2))
    for k in range(40):
        x = 150 + (k % 8) * 110; y = 790 + (k // 8) * 85
        r = 8 + 26 * g * (0.6 + 0.4 * ((k * 13) % 7) / 7)
        ax.add_patch(Circle((x, y), r, fc=to_rgba(TEAL, 0.35 * a), ec=to_rgba(TEAL, a), lw=1.5, zorder=8))
        if g > 0.3:
            for q in range(6):
                an = q + k; ax.add_patch(Circle((x + r * 0.5 * np.cos(an), y + r * 0.5 * np.sin(an)), 3, fc=WHITE, alpha=a * 0.6, zorder=8.5))
def v4_s3(ax, t, lt, a, v):
    card(ax, 90, 840, 900, 560, a, ec=SKY, z=6)
    cyc = int(lt / 0.55); ph = (lt % 0.55) / 0.55
    flash = np.exp(-ph * 4)
    for k in range(48):
        x = 150 + (k % 8) * 110; y = 900 + (k // 8) * 85
        ch = "ACGT"[(k * 7 + cyc * 3 + (k // 5)) % 4]
        glowdot(ax, x, y, 22, BCOL[ch], a * (0.35 + 0.65 * flash), z=8)
    tx(ax, 540, 1450, f"CYCLE {cyc+1}", 30, GOLD, a, fam=MONO)
    read = "".join("ACGT"[(0 * 7 + c * 3) % 4] for c in range(cyc + 1))[-18:]
    tx(ax, 540, 770, "read: " + read, 26, WHITE, a, fam=MONO)
def v4_s4(ax, t, lt, a, v):
    card(ax, 90, 720, 900, 720, a, ec=GREEN, z=6)
    tx(ax, 130, 1400, "sample_R1.fastq", 18, MUTED, a, ha="left", w="normal", fam=MONO, z=8)
    off = (lt * 60) % 120
    for r in range(12):
        y = 1340 - r * 52 + off
        if y > 1370 or y < 740: continue
        kind = r % 4; rid = (r // 4) + int(lt * 0.5) + 1
        s = [f"@read_{rid:06d}", "".join("ACGT"[(rid * 5 + j * 3 + j // 4) % 4] for j in range(30)), "+", "".join("IIIHHGGFFI"[(rid + j) % 10] for j in range(30))][kind]
        c = [GOLD, WHITE, MUTED, GREEN][kind]
        tx(ax, 130, y, s, 22, c, a, ha="left", fam=MONO, z=8)
    n = int(48_000_000 * eout(seg(lt, 0.3, 3.0)))
    pill(ax, 540, 650, 520, 64, GREEN, a, z=10); tx(ax, 540, 650, f"{n:,} reads", 26, BG, a, z=11, fam=MONO)
def v4_s5(ax, t, lt, a, v):
    ref = "ATGGCTAGCATCGATTACGGATCCATGCA"; x0 = 90; dx = 31; mpos = 15
    tx(ax, 540, 820, "reference genome", 18, MUTED, a, w="normal")
    for j, ch in enumerate(ref): tx(ax, x0 + j * dx, 870, ch, 24, WHITE, a, fam=MONO)
    reads = [(0, 10), (4, 12), (9, 11), (12, 10), (2, 9), (14, 12), (17, 11), (7, 10), (19, 10), (11, 9), (15, 13), (5, 8)]
    for k, (s, L) in enumerate(reads):
        f = eout(seg(lt, 0.2 + k * 0.18, 0.9 + k * 0.18))
        if f <= 0: continue
        y = 940 + (k % 8) * 62 + (1 - f) * 500
        ax.add_patch(FancyBboxPatch((x0 + s * dx - 12, y - 18), L * dx, 36, boxstyle="round,pad=0,rounding_size=10", fc=to_rgba(SKY, 0.25 * a * f), ec=to_rgba(SKY, a * f), lw=1.5, zorder=8))
        if s <= mpos < s + L:
            tx(ax, x0 + mpos * dx, y, "T", 22, MAG, a * f, fam=MONO, z=9)
    v_ = ease(seg(lt, 2.8, 3.4))
    if v_ > 0:
        ax.add_patch(Rectangle((x0 + mpos * dx - 16, 840), 32, 640, fc=MAG, alpha=0.15 * a * v_, zorder=7))
        pill(ax, x0 + mpos * dx, 1440, 320, 60, MAG, a * v_, z=12); tx(ax, x0 + mpos * dx, 1440, "variant found: G > T", 21, WHITE, a * v_, z=13)

# ======================= V05 free tools =======================
TOOLS = [("BLAST", "identify any sequence", "blast.ncbi.nlm.nih.gov", TEAL, "search"), ("UniProt", "protein encyclopedia", "uniprot.org", SKY, "book"),
         ("PDB", "solved 3D structures", "rcsb.org", GOLD, "cube"), ("AlphaFold DB", "200M+ predicted structures", "alphafold.ebi.ac.uk", VIO, "fold"),
         ("STRING", "protein interactions", "string-db.org", GREEN, "net"), ("Galaxy", "analysis without code", "usegalaxy.org", ORANGE, "flow")]
def v5_s0(ax, t, lt, a, v):
    P = [(400, 1450), (680, 1450), (680, 800), (540, 900), (400, 800)]
    ax.add_patch(Polygon(P, closed=True, fc=to_rgba(GOLD, 0.15 * a), ec=GOLD, lw=5, alpha=a, zorder=8))
    tx(ax, 540, 1240, "6", 170, BG, a, z=10); tx(ax, 540, 1080, "FREE", 44, BG, a, z=10); tx(ax, 540, 1025, "TOOLS", 44, BG, a, z=10)
def v5_grid(ax, t, lt, a, v):
    for k, (n, s, u, c, kd) in enumerate(TOOLS):
        p = pop(t, v.T[1 + k] - 0.1)
        if p <= 0: continue
        y = 1420 - k * 135
        cur = 1 if (v.T[1 + k] - 0.2 <= t < (v.T[2 + k] - 0.2)) else 0
        cardrow(ax, 70, y - 55, 940, 112, a, f"0{k+1}", n, None, c, kd, t, hl=cur, url=None)
        tx(ax, 440, y + 15, s, 19, MUTED, a, w="normal", ha="left", z=10)
        tx(ax, 440, y - 18, u, 17, c, a, w="normal", ha="left", z=10, fam=MONO)
    if t > v.T[7] - 0.2:
        b = pop(t, v.T[7])
        pill(ax, 540, 600 + 60, 380 * b, 70 * b, GOLD, a, z=14); tx(ax, 540, 660, "100% FREE", 28 * b, BG, a, z=15)

# ======================= V06 Galaxy =======================
NODES = [("Upload", "FASTQ files", SKY), ("FastQC", "quality check", TEAL), ("Trim", "remove bad reads", GOLD), ("HISAT2", "align to genome", VIO), ("featureCounts", "count per gene", GREEN), ("DESeq2", "find DEGs", MAG)]
def v6_s01(ax, t, lt, a, v):
    browser(ax, 70, 760, 940, 700, a, "usegalaxy.org")
    card(ax, 90, 780, 260, 590, a, z=9, r=12, fc="#0E2342"); tx(ax, 220, 1340, "TOOLS", 16, MUTED, a, z=10)
    n = int(9 * eout(seg(t, v.T[1], v.T[1] + 2.5)) * 3) + 6
    for k in range(min(n, 14)):
        pill(ax, 220, 1290 - k * 36, 200 - (k * 37) % 60, 20, ["#1E3A5F", "#23476F"][k % 2], a, z=10)
    card(ax, 370, 780, 400, 590, a, z=9, r=12, fc="#0E2342")
    tx(ax, 570, 1100, "Galaxy", 56, GOLD, a, z=10); tx(ax, 570, 1040, "free · web-based · no code", 18, MUTED, a, w="normal", z=10)
    card(ax, 790, 780, 200, 590, a, z=9, r=12, fc="#0E2342"); tx(ax, 890, 1340, "HISTORY", 16, MUTED, a, z=10)
    if t > v.T[1]:
        c = int(3000 * eout(seg(t, v.T[1] + 0.3, v.T[1] + 2.5)))
        pill(ax, 540, 690, 460, 66, TEAL, a * ease(seg(t, v.T[1] + 0.3, v.T[1] + 0.8)), z=12)
        tx(ax, 540, 690, f"{c:,}+ tools", 28, BG, a * ease(seg(t, v.T[1] + 0.3, v.T[1] + 0.8)), z=13, fam=MONO)
def v6_flow(ax, t, lt, a, v):
    starts = [v.T[2], v.T[2] + 1.6, v.T[3], v.T[3] + 1.9, v.T[4], v.T[4] + 2.6]
    pos = [(270, 1420), (810, 1420), (270, 1150), (810, 1150), (270, 880), (810, 880)]
    for k in range(5):
        if t < starts[k + 1]: break
        (x0, y0), (x1, y1) = pos[k], pos[k + 1]
        g = eout(seg(t, starts[k + 1] - 0.3, starts[k + 1] + 0.2))
        if k % 2 == 0: ax.plot([x0 + 190, x0 + 190 + (x1 - 190 - x0 - 190) * g], [y0, y1], color=TEAL, lw=4, alpha=a, zorder=7)
        else:
            xs = np.linspace(x0, x1, 50); ys = y0 + (y1 - y0) * (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, 50)))
            n = max(2, int(50 * g)); ax.plot(xs[:n], ys[:n] - 0, color=TEAL, lw=4, alpha=a * 0.6, zorder=7, ls=(0, (6, 6)))
    for k, (n, s, c) in enumerate(NODES):
        p = pop(t, starts[k])
        if p <= 0: continue
        x, y = pos[k]; done = t > (starts[k + 1] if k < 5 else v.T[5])
        card(ax, x - 190 * p, y - 75 * p, 380 * p, 150 * p, a, ec=c, lw=2 + 2 * (not done), z=8)
        ax.add_patch(Rectangle((x - 190 * p, y + 45 * p), 380 * p, 30 * p, fc=to_rgba(c, 0.3 * a), zorder=8.5))
        tx(ax, x - 170, y + 60, f"STEP {k+1}", 14 * p, c, a, ha="left", z=9)
        tx(ax, x, y + 5, n, 30 * p, WHITE, a, z=9)
        tx(ax, x, y - 38, s, 17 * p, MUTED, a, w="normal", z=9)
        if done: glowdot(ax, x + 160, y + 60, 9, GREEN, a, z=10)
    # mini outputs
    k_out = [(v.T[2] + 2.0, "qc"), (v.T[3] + 2.4, "aln"), (v.T[4] + 3.2, "vol")]
    for k, (ts, kind) in enumerate(k_out):
        al = a * ease(seg(t, ts, ts + 0.4)) * (1 - ease(seg(t, ts + 2.2, ts + 2.6)) if k < 2 else 1)
        if al <= 0.01: continue
        card(ax, 340, 640, 400, 160, al, ec=GOLD, z=12)
        if kind == "qc":
            for j in range(16): ax.add_patch(Rectangle((370 + j * 22, 660), 16, 100 - j * 3 - (j > 12) * 30, fc=GREEN if j < 13 else ORANGE, alpha=al, zorder=13))
        if kind == "aln":
            for j in range(5): pill(ax, 470 + (j * 47) % 140, 670 + j * 22, 160, 14, SKY, al, z=13)
            ax.plot([370, 710], [655, 655], color=WHITE, lw=3, alpha=al, zorder=13)
        if kind == "vol":
            for j in range(60):
                x_ = R.normal(0, 1) if False else np.sin(j * 1.7) * 1.6; y_ = abs(x_) * (0.5 + (j * 7 % 10) / 10)
                c_ = MAG if (x_ > 1 and y_ > 1) else SKY if (x_ < -1 and y_ > 1) else DIM
                ax.add_patch(Circle((540 + x_ * 90, 660 + y_ * 50), 5, fc=c_, alpha=al, zorder=13))
def v6_s5(ax, t, lt, a, v):
    card(ax, 240, 770, 600, 710, a, ec=TEAL)
    tx(ax, 540, 1430, "HISTORY", 20, MUTED, a)
    for k, (n, s, c) in enumerate(NODES):
        p = pop(lt, 0.2 + k * 0.2); y = 1350 - k * 100
        if p <= 0: continue
        pill(ax, 540, y, 520 * p, 76 * p, "#13294A", a, ec=c, lw=2, z=10)
        tx(ax, 320, y, f"{k+1}: {n}", 22 * p, WHITE, a, ha="left", z=11)
        glowdot(ax, 760, y, 10, GREEN, a * p, z=11)
    for k, lab in enumerate(["reproducible", "shareable"]):
        p = pop(lt, 1.8 + k * 0.3)
        pill(ax, 360 + k * 360, 712, 300 * p, 60 * p, GOLD if k == 0 else TEAL, a, z=12); tx(ax, 360 + k * 360, 712, lab, 22 * p, BG, a, z=13)

# ======================= V07 scholarships =======================
SCH = [("Commonwealth Scholarship", "UK", "Master's & PhD · via HEC", "20 OCT 2026", 6, MAG),
       ("Knowledge Corridor PhD", "USA", "HEC · QS top-100 US admits", "30 OCT 2026", 16, GOLD),
       ("OIST PhD Program", "JAPAN", "Fully funded · tuition waiver", "15 NOV 2026", 32, TEAL),
       ("Gates Cambridge", "UK", "PhD & postgrad · fully funded", "8 DEC / 6 JAN", 55, SKY)]
def v7_s0(ax, t, lt, a, v):
    for k in range(4):
        p = pop(lt, 0.2 + k * 0.35); x = 200 + k * 230; y = 1120 + (k % 2) * 40
        if p <= 0: continue
        n, c_, l, d, dl, col = SCH[k]
        card(ax, x - 95 * p, y - 120 * p, 190 * p, 240 * p, a, ec=col, lw=3, z=8)
        ax.add_patch(Rectangle((x - 95 * p, y + 70 * p), 190 * p, 50 * p, fc=col, alpha=a, zorder=8.5))
        tx(ax, x, y + 95 * p, c_, 18 * p, BG, a, z=9)
        tx(ax, x, y, d.split()[0] if "/" not in d else "8", 70 * p, WHITE, a, z=9)
        tx(ax, x, y - 70 * p, d.split()[1] if "/" not in d else "DEC", 22 * p, col, a, z=9)
    pill(ax, 540, 820, 420, 70, GOLD, a * ease(seg(lt, 1.6, 2.0)), z=10); tx(ax, 540, 820, "FULLY FUNDED", 28, BG, a * ease(seg(lt, 1.6, 2.0)), z=11)
def sch_card(k):
    def f(ax, t, lt, a, v):
        n, c_, l, d, dl, col = SCH[k]
        p = eout(seg(lt, 0.0, 0.5)); y0 = 900 + (1 - p) * 60
        card(ax, 90, y0, 900, 560, a * p, ec=col, lw=3, z=8)
        pill(ax, 220, y0 + 480, 200, 56, col, a * p, z=9); tx(ax, 220, y0 + 480, c_, 22, BG, a * p, z=10)
        tx(ax, 150, y0 + 380, n, 40, WHITE, a * p, ha="left", z=10)
        tx(ax, 150, y0 + 320, l, 22, MUTED, a * p, ha="left", w="normal", z=10)
        tx(ax, 150, y0 + 210, "DEADLINE", 18, col, a * p, ha="left", z=10)
        tx(ax, 150, y0 + 150, d, 44, WHITE, a * p, ha="left", z=10, fam=MONO)
        g = eout(seg(lt, 0.4, 1.8)); cx, cy = 820, y0 + 170
        ring(ax, cx, cy, 95, LINE, a * p, lw=16, z=9)
        ax.add_patch(Wedge((cx, cy), 103, 90 - 360 * min(1, dl / 60) * g, 90, width=16, fc=col, alpha=a * p, zorder=9.5))
        tx(ax, cx, cy + 14, f"{int(dl*g)}", 52, WHITE, a * p, z=10); tx(ax, cx, cy - 36, "days left", 16, MUTED, a * p, w="normal", z=10)
        # timeline
        ax.plot([120, 960], [760, 760], color=LINE, lw=6, alpha=a, zorder=7)
        for j in range(4):
            x = 120 + 840 * SCH[j][4] / 60; on = j <= k
            ax.add_patch(Circle((x, 760), 14, fc=SCH[j][5] if on else LINE, ec=BG, lw=3, alpha=a, zorder=8))
        ax.add_patch(Circle((120, 760), 10, fc=WHITE, alpha=a, zorder=8)); tx(ax, 120, 715, "today", 15, WHITE, a, w="normal")
    return f
def v7_s5(ax, t, lt, a, v):
    for k, (n, c_, l, d, dl, col) in enumerate(SCH):
        p = pop(lt, 0.1 + k * 0.25); y = 1380 - k * 160
        if p <= 0: continue
        card(ax, 90, y - 65, 900, 130, a, ec=col, lw=2, z=8)
        tx(ax, 130, y + 18, n, 28, WHITE, a, ha="left", z=10); tx(ax, 130, y - 25, c_, 18, col, a, ha="left", z=10)
        tx(ax, 950, y, d, 24, col, a, ha="right", z=10, fam=MONO)
    pill(ax, 540, 690, 460, 70, GOLD, a * ease(seg(lt, 1.4, 1.8)), z=10); tx(ax, 540, 690, "Links in the caption", 26, BG, a * ease(seg(lt, 1.4, 1.8)), z=11)

# ======================= V08 careers =======================
ROLES = [("Bioinformatics Scientist", ["Python / R", "NGS", "statistics"], TEAL, "dna"), ("Computational Biologist", ["modeling", "math", "ML"], SKY, "chart"),
         ("Clinical Bioinformatician", ["variant analysis", "genetics", "pipelines"], MAG, "hospital"), ("ML Scientist, Drug Discovery", ["deep learning", "chemistry", "PyTorch"], GOLD, "brain"),
         ("Bio Data Engineer", ["cloud", "Nextflow", "databases"], GREEN, "pipe")]
def v8_tree(ax, t, lt, a, v):
    cx, cy = 540, 1180
    glowdot(ax, cx, cy, 70, TEAL, a, z=9); tx(ax, cx, cy, "YOU", 26, BG, a, z=12)
    for k, (n, sk, c, kd) in enumerate(ROLES):
        ang = np.pi / 2 + (k - 2) * 0.62 + np.pi * 0
        ang = np.radians([150, 115, 90, 65, 30][k]); x, y = cx + 380 * np.cos(ang), cy + 300 * np.sin(ang) * 0.9 - 0
        g = eout(seg(lt, 0.3 + k * 0.25, 0.9 + k * 0.25))
        ax.plot([cx, cx + (x - cx) * g], [cy, cy + (y - cy) * g], color=c, lw=3, alpha=a * 0.7, zorder=8)
        if g > 0.9:
            cur = (v.T[1 + k] - 0.2 <= t < v.T[2 + k] - 0.2)
            ax.add_patch(Circle((x, y), 48 + 10 * cur, fc=to_rgba(c, 0.2 * a), ec=c, lw=2 + 2 * cur, alpha=a, zorder=9))
            icon(ax, kd, x, y, 0.9, c, a, t, z=10)
def v8_role(ax, t, lt, a, v):
    k = min(4, max(0, int(np.searchsorted(v.T, t + 0.2) - 2)))
    n, sk, c, kd = ROLES[k]
    lt2 = t - v.T[1 + k]
    p = eout(seg(lt2, -0.2, 0.3))
    card(ax, 90, 700, 900, 300, a * p, ec=c, lw=3, z=8)
    tx(ax, 130, 940, f"PATH {k+1} / 5", 18, c, a * p, ha="left", z=10)
    tx(ax, 130, 880, n, 38, WHITE, a * p, ha="left", z=10)
    x = 130
    for j, s in enumerate(sk):
        w = len(s) * 13 + 50; q = pop(lt2, 0.4 + j * 0.25)
        pill(ax, x + w / 2, 770, w * q, 52 * q, to_rgba(c, 0.18), a, ec=c, lw=1.5, z=10); tx(ax, x + w / 2, 770, s, 19 * q, c, a, z=11); x += w + 20
def v8_jobs(ax, t, lt, a, v):
    pill(ax, 540, 1350, 860, 100, "#13294A", a, ec=SKY, lw=2, z=8)
    icon(ax, "search", 160, 1350, 1.0, SKY, a, z=10)
    s = "bioinformatics jobs"; n = int(len(s) * seg(lt, 0.2, 1.4))
    tx(ax, 220, 1350, s[:n] + ("|" if (t * 2) % 1 < 0.5 else ""), 30, WHITE, a, ha="left", z=10, fam=MONO)
    boards = [("LinkedIn Jobs", SKY), ("Nature Careers", GREEN), ("EMBL Jobs", TEAL), ("EURAXESS", GOLD), ("CompBioJobs", VIO)]
    for k, (b, c) in enumerate(boards):
        p = pop(lt, 1.0 + k * 0.4); y = 1180 - k * 105
        if p <= 0: continue
        card(ax, 200, y - 42, 680, 84, a, ec=c, lw=2, z=8, r=42)
        glowdot(ax, 250, y, 10, c, a, z=10); tx(ax, 290, y, b, 28 * p, WHITE, a, ha="left", z=10)

# ======================= V09 roadmap =======================
STEPS = [("Biology basics", "DNA · genes · proteins", TEAL, "dna"), ("Linux & command line", "bash · files · servers", SKY, "linux"),
         ("Python / R + statistics", "code · data · tests", GOLD, "code"), ("Real public data", "NCBI · TCGA · GEO", VIO, "db"),
         ("One core pipeline", "RNA-seq or variant calling", GREEN, "pipe"), ("Projects on GitHub", "build · share · get hired", MAG, "git")]
def road_xy(s):
    y = 700 + s * 740; x = 540 + 230 * np.sin(s * np.pi * 2.5)
    return x, y
def v9_road(ax, t, lt, a, v):
    d = eout(seg(lt, 0.0, 2.5)); s = np.linspace(0, d, 300)
    x, y = road_xy(s)
    ax.plot(x, y, color=LINE, lw=46, alpha=a, zorder=5, solid_capstyle="round")
    ax.plot(x, y, color=MUTED, lw=3, ls=(0, (12, 12)), alpha=a * 0.6, zorder=5.5)
    cur = 0
    for k, (n, sub, c, kd) in enumerate(STEPS):
        sk = k / 5; px, py = road_xy(sk)
        if sk > d: break
        reached = t >= v.T[1 + k] - 0.2
        if reached: cur = k
        ax.add_patch(Circle((px, py), 40, fc=c if reached else BG, ec=c, lw=4, alpha=a, zorder=8))
        tx(ax, px, py, str(k + 1), 26, BG if reached else c, a, z=9)
        if reached:
            q = eout(seg(t, v.T[1 + k] - 0.2, v.T[1 + k] + 0.3)); side = -1 if px > 540 else 1
            cx_ = px + side * 300 * 1
            cx_ = np.clip(cx_, 250, 830)
            card(ax, cx_ - 210, py - 55, 420, 110, a * q, ec=c, lw=2, z=9)
            tx(ax, cx_ - 185, py + 18, n, 23, WHITE, a * q, ha="left", z=10); tx(ax, cx_ - 185, py - 20, sub, 17, MUTED, a * q, ha="left", w="normal", z=10)
    if t >= v.T[1] - 0.2:
        k = cur; t0 = v.T[1 + k] - 0.2; prev = (k - 1) / 5 if k > 0 else 0
        s_ = prev + (k / 5 - prev) * eout(seg(t, t0, t0 + 0.6))
        px, py = road_xy(s_); glowdot(ax, px + 0, py + 0, 14, WHITE, a, z=12)

# ======================= V10 genome cost =======================
def v10_s0(ax, t, lt, a, v):
    for k in range(13):
        p = pop(lt, 0.2 + k * 0.12); x = 180 + (k % 7) * 120; y = 1380 - (k // 7) * 150
        if p <= 0: continue
        card(ax, x - 48 * p, y - 55 * p, 96 * p, 110 * p, a, ec=SKY, z=8, r=10)
        ax.add_patch(Rectangle((x - 48 * p, y + 30 * p), 96 * p, 25 * p, fc=SKY, alpha=a, zorder=8.5))
        tx(ax, x, y - 10, str(1990 + k), 18 * p, WHITE, a, z=9)
    g = eout(seg(lt, 1.0, 3.5))
    tx(ax, 540, 920, f"${2.7*g:.1f} billion", 90, GOLD, a)
    tx(ax, 540, 810, "Human Genome Project · 1990–2003", 22, MUTED, a, w="normal")
def v10_chart(ax, t, lt, a, v):
    x0, x1, y0, y1 = 170, 960, 780, 1460
    yr = lambda y: x0 + (y - 2003) / (2022 - 2003) * (x1 - x0)
    lg = lambda c: y0 + (np.log10(c) - 2) / (9 - 2) * (y1 - y0)
    ax.plot([x0, x0], [y0, y1], color=DIM, lw=2, alpha=a, zorder=6); ax.plot([x0, x1], [y0, y0], color=DIM, lw=2, alpha=a, zorder=6)
    for c, lab in ((1e9, "$1B"), (1e7, "$10M"), (1e5, "$100K"), (1e3, "$1K"), (1e2, "$100")):
        tx(ax, x0 - 15, lg(c), lab, 17, MUTED, a, ha="right", w="normal"); ax.plot([x0, x1], [lg(c)] * 2, color=LINE, lw=1, alpha=a, zorder=5)
    for y_ in (2003, 2010, 2015, 2022): tx(ax, yr(y_), y0 - 35, str(y_), 17, MUTED, a, w="normal")
    pts = [(2003, 5e8), (2015, 1500), (2022, 150)]
    g = eout(seg(lt, 0.3, 3.0))
    xs = np.linspace(2003, 2003 + 19 * g, 100)
    ys = np.interp(xs, [p[0] for p in pts], np.log10([p[1] for p in pts]))
    ax.plot([yr(x) for x in xs], [lg(10 ** y) for y in ys], color=TEAL, lw=6, alpha=a, zorder=8)
    for (yy_, cc), lab in zip(pts, ["~$500M+", "< $1,500", "$100–200*"]):
        if yy_ <= 2003 + 19 * g + 0.01:
            glowdot(ax, yr(yy_), lg(cc), 10, TEAL, a, z=9); tx(ax, yr(yy_) + (0 if yy_ < 2020 else -10), lg(cc) + 45, lab, 20, WHITE, a, ha="center" if yy_ < 2020 else "right")
    m = ease(seg(t, v.T[2] + 0.2, v.T[2] + 1.6))
    if m > 0:
        xs2 = np.linspace(2003, 2003 + 19 * m, 50)
        ax.plot([yr(x) for x in xs2], [lg(5e8 / 2 ** ((x - 2003) / 2)) for x in xs2], color=GOLD, lw=4, ls=(0, (8, 6)), alpha=a, zorder=7)
        tx(ax, yr(2016), lg(5e8 / 2 ** 6.5) + 50, "Moore's law pace", 20, GOLD, a * m)
    tx(ax, 960, 720, "*advertised sequencing cost", 15, MUTED, a * g, ha="right", w="normal")
def v10_data(ax, t, lt, a, v):
    g = eout(seg(lt, 0.3, 3.5))
    for k in range(int(20 * g)):
        x = 230 + (k % 5) * 155; y = 800 + (k // 5) * 125
        card(ax, x - 60, y - 45, 120, 90, a, ec=SKY, z=8, r=12); ax.add_patch(Circle((x + 35, y - 25), 6, fc=GREEN, alpha=a, zorder=9))
        for j in range(3): ax.add_patch(Rectangle((x - 45, y + 20 - j * 18), 60, 8, fc=LINE, alpha=a, zorder=9))
    tx(ax, 540, 1400, f"~{int(100*g)} GB", 100, SKY, a, fam=MONO)
    tx(ax, 540, 1310, "raw data from one genome", 22, MUTED, a, w="normal")
def v10_end(ax, t, lt, a, v):
    helix(ax, t, 1300, 120, 960, 80, a, turns=2.5)
    for k in range(int(30 * eout(seg(lt, 0.4, 3.0)))):
        x = 180 + (k % 10) * 80; y = 880 + (k // 10) * 110
        ax.add_patch(Circle((x, y + 22), 14, fc=[TEAL, GOLD, SKY][k % 3], alpha=a, zorder=8))
        ax.add_patch(FancyBboxPatch((x - 22, y - 30), 44, 36, boxstyle="round,pad=0,rounding_size=16", fc=[TEAL, GOLD, SKY][k % 3], alpha=a, zorder=8))
    tx(ax, 540, 760, "the world needs more bioinformaticians", 24, WHITE, a * ease(seg(lt, 2.0, 2.6)))

# ======================= registry =======================
def V(name):
    if name == "v01_virtual_cell":
        return Video(name, "BREAKING NEWS", MAG, [(v1_s0, 0, 0), (v1_s1, 1, 1), (v1_s2, 2, 2), (v1_s3, 3, 3), (v1_s4, 4, 4), (v1_s5, 5, 5)],
                     [(0, 1, "BREAKING NEWS", "$1.8 billion to build\nAI models of cells"), (2, 2, "WHO'S INVOLVED", "A global alliance"), (3, 3, "THE GOAL", "A virtual cell"), (4, 4, "WHY IT MATTERS", "Test on a computer first"), (5, 5, "THE ENGINE", "Open biological data")]), 0
    if name == "v02_evo2":
        return Video(name, "RECENT RESEARCH", TEAL, [(v2_s0, 0, 0), (v2_s1, 1, 1), (v2_s2, 2, 2), (v2_s3, 3, 3), (v2_s4, 4, 4), (v2_s5, 5, 5)],
                     [(0, 0, "RECENT RESEARCH", "An AI that speaks DNA"), (1, 1, "PUBLISHED IN NATURE", "Meet Evo 2"), (2, 2, "TRAINED ON", "The tree of life"), (3, 3, "SKILL #1", "Spotting harmful mutations"), (4, 4, "SKILL #2", "Designing genomes"), (5, 5, "THE BEST PART", "Fully open source")]), 1
    if name == "v03_crispr":
        return Video(name, "EXPLAINER", SKY, [(crispr_scene, 0, 4), (v3_s5, 5, 5)],
                     [(0, 0, "EXPLAINER", "How CRISPR works"), (1, 1, "STEP 1", "Design a guide RNA"), (2, 2, "STEP 2", "Find the target"), (3, 3, "STEP 3", "Cut the DNA"), (4, 4, "STEP 4", "Repair = edit"), (5, 5, "WHERE WE COME IN", "Smart guide design")]), 2
    if name == "v04_ngs":
        return Video(name, "EXPLAINER", SKY, [(v4_s0, 0, 0), (v4_s1, 1, 1), (v4_s2, 2, 2), (v4_s3, 3, 3), (v4_s4, 4, 4), (v4_s5, 5, 5)],
                     [(0, 0, "EXPLAINER", "How DNA sequencing works"), (1, 1, "STEP 1", "Fragment the DNA"), (2, 2, "STEP 2", "Build clusters"), (3, 3, "STEP 3", "Read by color"), (4, 4, "STEP 4", "Millions of reads"), (5, 5, "STEP 5", "Align & find variants")]), 0
    if name == "v05_free_tools":
        return Video(name, "FREE TOOLS", GREEN, [(v5_s0, 0, 0), (v5_grid, 1, 7)], [(0, 7, "FREE TOOLS", "6 tools to bookmark")]), 1
    if name == "v06_galaxy":
        return Video(name, "FREE TOOL", ORANGE, [(v6_s01, 0, 1), (v6_flow, 2, 4), (v6_s5, 5, 5)],
                     [(0, 1, "FREE TOOL", "Galaxy: analysis\nwithout code"), (2, 4, "RNA-SEQ IN 6 STEPS", "Point, click, analyze"), (5, 5, "THE BONUS", "Reproducible science")]), 2
    if name == "v07_scholarships":
        return Video(name, "SCHOLARSHIPS", GOLD, [(v7_s0, 0, 0)] + [(sch_card(k), 1 + k, 1 + k) for k in range(4)] + [(v7_s5, 5, 5)],
                     [(0, 0, "SCHOLARSHIPS", "4 fully funded deadlines"), (1, 1, "UNITED KINGDOM", "Commonwealth"), (2, 2, "USA · VIA HEC", "Knowledge Corridor"), (3, 3, "JAPAN", "OIST PhD"), (4, 4, "UNITED KINGDOM", "Gates Cambridge"), (5, 5, "DON'T WAIT", "Start applying today")]), 0
    if name == "v08_careers":
        return Video(name, "CAREERS", VIO, [(v8_tree, 0, 5), (v8_role, 1, 5), (v8_jobs, 6, 6)],
                     [(0, 5, "CAREERS", "5 paths in bioinformatics"), (6, 6, "JOB HUNTING", "Where to find openings")]), 1
    if name == "v09_roadmap":
        return Video(name, "ROADMAP", TEAL, [(v9_road, 0, 6)], [(0, 6, "BEGINNER ROADMAP", "Start in 6 steps")]), 2
    if name == "v10_genome_cost":
        return Video(name, "DID YOU KNOW?", GOLD, [(v10_s0, 0, 0), (v10_chart, 1, 2), (v10_data, 3, 3), (v10_end, 4, 4)],
                     [(0, 0, "DID YOU KNOW?", "The $2.7 billion genome"), (1, 2, "THE PRICE CRASH", "From billions to ~$200"), (3, 3, "THE NEW PROBLEM", "A flood of data"), (4, 4, "THE SOLUTION", "Bioinformatics")]), 0

if __name__ == "__main__":
    v, seed = V(sys.argv[1]); v.main(sys.argv[1:], seed)
