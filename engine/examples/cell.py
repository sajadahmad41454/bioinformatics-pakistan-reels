import sys as _s; _s.path.append("/home/claude/ten")
from eng import *
from vids import draw_cell, monitor
RED = "#EF4444"; CRIM = "#B91C1C"; ICE = "#BAE6FD"; NAVY = "#0B2447"; BLUE = "#3B82F6"
rng = np.random.default_rng(7)

# ---------- tissue ----------
_TC = []
for j in range(-9, 10):
    for i in range(-8, 9):
        x = i * 96 + (48 if j % 2 else 0); y = j * 84
        _TC.append((x + rng.normal(0, 6), y + rng.normal(0, 6), rng.uniform(0.9, 1.1), rng.uniform(0, 6.28)))
_TC = np.array(_TC)
_EX = rng.normal(0, 1, (90, 2)); _EXS = rng.uniform(0.8, 1.35, 90); _EXR = rng.uniform(0, 1, 90)

def tissue(ax, t, cx, cy, zoom, al, R=470, focus=0.0, tumor=0.0, z=5):
    """cells in world coords; tumor in 0..1 grows a cluster at the origin"""
    rad_t = 40 + 230 * tumor
    for (x, y, s, ph) in _TC:
        X = cx + x * zoom; Y = cy + y * zoom
        d = np.hypot(X - cx, Y - cy) / R
        if d > 1.05: continue
        fa = al * np.clip(1 - d ** 4, 0, 1)
        if fa < 0.02: continue
        wob = 1 + 0.03 * np.sin(t * 1.3 + ph)
        r0 = np.hypot(x, y)
        ab = tumor > 0 and r0 < rad_t
        if ab:
            k = np.clip((rad_t - r0) / 60, 0, 1)
            col = mixc(SKY, RED, k); nuc = mixc("#1E3A8A", "#7F1D1D", k); sc = s * (1 + 0.25 * k * np.sin(ph * 3) ** 2)
            ang = np.degrees(ph) * k
        else:
            col = SKY; nuc = "#1E3A8A"; sc = s; ang = 0
        w = 88 * zoom * sc * wob; h = 76 * zoom * sc / wob
        ax.add_patch(Ellipse((X, Y), w, h, angle=ang, fc=to_rgba(col, 0.13 * fa), ec=to_rgba(col, 0.75 * fa), lw=max(1, 2.2 * zoom), zorder=z))
        nr = (0.34 if not ab else 0.44) * 76 * zoom * sc
        ax.add_patch(Circle((X + 4 * zoom, Y + 3 * zoom), nr / 2 * 1.3, fc=to_rgba(nuc, 0.25 * fa), ec="none", zorder=z + 0.05))
        ax.add_patch(Circle((X + 4 * zoom, Y + 3 * zoom), nr / 2, fc=to_rgba(mixc(nuc, WHITE, 0.25), 0.9 * fa), ec=to_rgba(ICE if not ab else RED, 0.6 * fa), lw=1, zorder=z + 0.1))
    # extra piled abnormal cells
    m = int(90 * np.clip((tumor - 0.25) / 0.75, 0, 1))
    for k in range(m):
        rr = rad_t * 0.75 * np.sqrt(_EXR[k]); a = np.arctan2(_EX[k, 1], _EX[k, 0])
        X = cx + rr * np.cos(a) * zoom + 3 * np.sin(t * 3 + k); Y = cy + rr * np.sin(a) * zoom
        s = 30 * _EXS[k] * zoom
        ax.add_patch(Ellipse((X, Y), s * 2.1, s * 1.7, angle=k * 37, fc=to_rgba(RED, 0.35 * al), ec=to_rgba("#FCA5A5", 0.8 * al), lw=1.4, zorder=z + 0.3))
        ax.add_patch(Circle((X, Y), s * 0.45, fc=to_rgba("#7F1D1D", 0.95 * al), zorder=z + 0.4))
    if focus > 0:
        ring(ax, cx, cy, 70 * zoom + 8 * np.sin(t * 3), ICE, al * focus, lw=3, z=z + 1)
        ring(ax, cx, cy, 70 * zoom + 22, ICE, al * focus * 0.3, lw=10, z=z + 1)

# ---------- scenes ----------
def s0(ax, t, lt, a, v):
    z = 0.85 + 1.6 * ease(seg(lt, 2.0, 7.0))
    tissue(ax, t, 540, 1110, z, a, R=400, focus=ease(seg(lt, 3.0, 4.0)))
    n = int(3e13 * eout(seg(lt, 0.2, 3.0)))
    tx(ax, 540, 760, f"{n:,}+", 40, WHITE, a * (1 - ease(seg(lt, 4.5, 5.2))), fam=MONO)
    tx(ax, 540, 712, "cells in one human body", 20, MUTED, a * (1 - ease(seg(lt, 4.5, 5.2))), w="normal")

def s1(ax, t, lt, a, v):
    draw_cell(ax, 540, 1070, 220, t, a, tint=SKY)
    labs = ["growth", "division", "repair", "survival"]
    for k in range(4):
        ang = np.pi / 4 + k * np.pi / 2 + 0.1 * t
        x, y = 540 + 300 * np.cos(ang), 1070 + 300 * np.sin(ang)
        fail = ease(seg(lt, 1.0 + k * 0.35, 1.3 + k * 0.35))
        flick = 1 if fail >= 1 else (0.4 + 0.6 * (np.sin(t * 40 + k) > 0)) if fail > 0 else 1
        c = mixc(GREEN, RED, fail)
        ax.plot([540 + 230 * np.cos(ang), x - 40 * np.cos(ang)], [1070 + 230 * np.sin(ang), y - 40 * np.sin(ang)], color=c, lw=2, alpha=a * 0.6, ls="--", zorder=9)
        ax.add_patch(Circle((x, y), 38, fc=to_rgba(c, 0.18 * a), ec=to_rgba(c, a * flick), lw=3, zorder=10))
        ax.add_patch(Circle((x, y), 12, fc=to_rgba(c, a * flick), zorder=10.1))
        tx(ax, x, y - 62, labs[k], 18, c, a, w="semibold")

def gauge(ax, cx, cy, r, val, label, al, t):
    al = min(al, 1)
    th = np.linspace(np.pi, 0, 60)
    for i in range(59):
        f = i / 59; c = GREEN if 0.3 < f < 0.7 else (GOLD if 0.18 < f < 0.82 else RED)
        ax.plot(cx + r * np.cos(th[i:i + 2]), cy + r * np.sin(th[i:i + 2]), color=c, lw=14, alpha=al * 0.8, solid_capstyle="butt", zorder=8)
    an = np.pi * (1 - val)
    ax.plot([cx, cx + r * 0.85 * np.cos(an)], [cy, cy + r * 0.85 * np.sin(an)], color=WHITE, lw=5, alpha=al, zorder=9, solid_capstyle="round")
    ax.add_patch(Circle((cx, cy), 14, fc=WHITE, alpha=al, zorder=9.1))
    tx(ax, cx, cy - 55, label, 22, WHITE, al)

def s2(ax, t, lt, a, v):
    labs = ["GROWTH", "DIVISION", "SURVIVAL"]
    for k in range(3):
        bad = ease(seg(lt, 3.0 + k * 0.7, 4.2 + k * 0.7))
        val = 0.5 + 0.03 * np.sin(t * 2 + k) + bad * (0.42 + 0.03 * np.sin(t * 9 + k))
        if k == 2: val = 0.5 + 0.03 * np.sin(t * 2) + bad * (0.42 + 0.03 * np.sin(t * 9))
        cx = 540; cy = 1330 - k * 240
        gauge(ax, cx, cy, 150, val, labs[k], a * pop(lt, 0.2 + k * 0.4), t)
    tx(ax, 860, 1200, "balanced", 18, GREEN, a * (1 - ease(seg(lt, 3.0, 3.5))), w="semibold")
    tx(ax, 860, 1200, "disrupted", 18, RED, a * ease(seg(lt, 3.4, 4.0)), w="semibold")

SEQ = "ATGGGTGGCGTA"
def pathway(ax, t, lt, a, on, y=880):
    # membrane left, 3 proteins, nucleus right
    xs = np.linspace(170, 1000, 6)
    ax.plot([120, 120], [y - 150, y + 150], color=SKY, lw=8, alpha=a, zorder=8)
    ax.add_patch(Rectangle((120, y - 150), 18, 300, fc=to_rgba(SKY, 0.15 * a), zorder=7))
    tx(ax, 120, y + 180, "membrane", 16, MUTED, a, w="normal")
    nodes = [(250, y), (430, y + 50), (610, y - 40), (790, y + 20)]
    ax.add_patch(Circle((940, y), 85, fc=to_rgba(VIO, 0.18 * a), ec=VIO, lw=3, alpha=a, zorder=8))
    tx(ax, 940, y - 120, "nucleus", 16, MUTED, a, w="normal")
    pts = [(130, y)] + nodes + [(870, y)]
    for i in range(len(pts) - 1):
        ax.plot([pts[i][0], pts[i + 1][0]], [pts[i][1], pts[i + 1][1]], color=LINE, lw=3, alpha=a, zorder=8)
    for i, (x, yy) in enumerate(nodes):
        hot = on > 0 and i == 1
        c = mixc(GOLD, RED, on) if hot else GOLD
        ax.add_patch(Ellipse((x, yy), 70, 52, fc=to_rgba(c, 0.25 * a), ec=c, lw=3, alpha=a, zorder=9))
    rate = 0.35 + 1.6 * on; npul = 1 + int(4 * on)
    for p in range(npul):
        ph = (t * rate + p / npul) % 1
        L = len(pts) - 1; s = ph * L; i = min(int(s), L - 1); f = s - i
        x = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f; yy = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f
        glowdot(ax, x, yy, 9, mixc(GOLD, RED, on), a, z=10)
    if on > 0:
        g = 0.5 + 0.5 * np.sin(t * 6)
        ax.add_patch(Circle((940, y), 85 + 10 * g, fc="none", ec=RED, lw=3, alpha=a * on * 0.6, zorder=9))

def s3(ax, t, lt, a, v):
    helix(ax, t, 1370, 110, 970, 60, a, turns=2.0, lw=5, c1=SKY, c2=BLUE)
    mut = ease(seg(lt, 1.0, 1.6))
    x0 = 540 - len(SEQ) * 72 / 2 + 36
    for k, b in enumerate(SEQ):
        x = x0 + k * 72; y = 1210
        isM = k == 5
        ch = ("A" if mut > 0.5 else b) if isM else b
        c = mixc(BCOL[b], RED, mut) if isM else BCOL[b]
        sc = pop(lt, 1.0) if isM and mut > 0 else 1
        card(ax, x - 30 * sc, y - 34 * sc, 60 * sc, 68 * sc, a, ec=c, lw=2.5 if isM else 1.2, z=9, r=10, fc=to_rgba(c, 0.15) if isM else CARD)
        tx(ax, x, y, ch, 30 * sc, c, a, fam=MONO, z=10)
    tx(ax, 540, 1125, "one possible change: a single-letter mutation", 18, RED, a * mut, w="semibold")
    pathway(ax, t, lt, a, ease(seg(lt, 2.0, 3.0)), y=850)
    tx(ax, 430, 960, "growth gene", 17, GOLD, a * ease(seg(lt, 1.8, 2.4)), w="semibold")
    tx(ax, 540, 680, "signal stuck ON", 24, RED, a * ease(seg(lt, 2.6, 3.2)))

def s4(ax, t, lt, a, v):
    cx, cy, R = 540, 1100, 230
    ph = [("G1", 0.0, 0.4, SKY), ("S", 0.4, 0.7, TEAL), ("G2", 0.7, 0.88, VIO), ("M", 0.88, 1.0, GOLD)]
    for n, f0, f1, c in ph:
        ax.add_patch(Wedge((cx, cy), R, 90 - 360 * f1, 90 - 360 * f0, width=46, fc=to_rgba(c, 0.55 * a), ec=BG, lw=3, zorder=8))
        m = (f0 + f1) / 2; an = np.radians(90 - 360 * m)
        tx(ax, cx + (R + 45) * np.cos(an), cy + (R + 45) * np.sin(an), n, 22, c, a)
    broken = ease(seg(lt, 2.2, 2.8))
    gan = np.radians(90 - 360 * 0.4)
    gc = mixc(GREEN, RED, broken)
    gx0, gy0 = cx + (R - 70) * np.cos(gan), cy + (R - 70) * np.sin(gan)
    gx1, gy1 = cx + (R + 25) * np.cos(gan), cy + (R + 25) * np.sin(gan)
    if broken < 1:
        ax.plot([gx0, gx1], [gy0, gy1], color=gc, lw=10, alpha=a, zorder=11, solid_capstyle="round")
    else:
        mx, my = (gx0 + gx1) / 2, (gy0 + gy1) / 2
        ax.plot([gx0, mx - 12], [gy0, my - 8], color=RED, lw=10, alpha=a, zorder=11, solid_capstyle="round")
        ax.plot([mx + 12, gx1], [my + 10, gy1], color=RED, lw=10, alpha=a, zorder=11, solid_capstyle="round")
    tx(ax, gx1 + 70, gy1 - 10, "checkpoint", 18, gc, a, w="semibold")
    # traveller
    if lt < 2.4:
        f = min(0.385, (lt * 0.3) % 1)
    else:
        f = ((lt - 2.4) * 0.65) % 1
    an = np.radians(90 - 360 * f)
    glowdot(ax, cx + (R - 23) * np.cos(an), cy + (R - 23) * np.sin(an), 13, WHITE, a, z=12)
    tx(ax, cx, cy + 20, "cell", 22, MUTED, a, w="normal"); tx(ax, cx, cy - 15, "cycle", 22, MUTED, a, w="normal")
    for k, (nm, ex) in enumerate([("Tumor suppressors", "e.g. TP53"), ("DNA repair genes", "e.g. BRCA1")]):
        q = pop(lt, 0.4 + k * 0.5); x = 300 + k * 480; y = 720
        if q <= 0: continue
        c = mixc(GREEN, RED, broken)
        card(ax, x - 210, y - 55, 420, 110, a, ec=c, lw=2.5, z=9, r=20)
        tx(ax, x, y + 16, nm, 22, WHITE, a, z=10); tx(ax, x, y - 22, ex, 17, c, a, w="normal", z=10, fam=MONO)

def s5(ax, t, lt, a, v):
    g = ease(seg(lt, 0.6, 6.2))
    tissue(ax, t, 540, 1080, 1.0, a, R=400, tumor=g)
    yrs = eout(seg(lt, 0.6, 6.2))
    ax.plot([200, 880], [640, 640], color=LINE, lw=6, alpha=a, zorder=8, solid_capstyle="round")
    ax.plot([200, 200 + 680 * yrs], [640, 640], color=RED, lw=6, alpha=a, zorder=9, solid_capstyle="round")
    tx(ax, 200, 680, "time", 17, MUTED, a, w="normal", ha="left"); tx(ax, 880, 680, "often years", 17, MUTED, a, w="normal", ha="right")
    q = ease(seg(lt, 4.0, 4.6))
    tx(ax, 840, 1420, "healthy tissue", 18, SKY, a * q, w="semibold"); tx(ax, 240, 1420, "abnormal cluster", 18, RED, a * q, w="semibold")

TYPES = ["Breast", "Lung", "Colorectal", "Leukemia", "Brain", "Skin"]
def s6(ax, t, lt, a, v):
    for k, nm in enumerate(TYPES):
        q = pop(lt, 0.3 + k * 0.25)
        if q <= 0: continue
        x = 300 + (k % 2) * 480; y = 1340 - (k // 2) * 220
        card(ax, x - 215, y - 85, 430, 170, a, ec=LINE, lw=2, z=8)
        tx(ax, x, y + 45, nm, 26, WHITE, a, z=9)
        r_ = np.random.default_rng(k + 11)
        pos = r_.uniform(0, 1, 7); cols = r_.choice([RED, GOLD, VIO, TEAL], 7)
        ax.plot([x - 175, x + 175], [y - 25, y - 25], color=LINE, lw=10, alpha=a, zorder=9, solid_capstyle="round")
        for p, c in zip(pos, cols):
            ax.plot([x - 175 + 350 * p] * 2, [y - 45, y - 5], color=c, lw=5, alpha=a * ease(seg(lt, 1.2 + k * 0.2, 1.6 + k * 0.2)), zorder=10)
    tx(ax, 540, 690, "different genes, different behavior", 22, GOLD, a * ease(seg(lt, 2.8, 3.4)), w="semibold")

def s7(ax, t, lt, a, v):
    monitor(ax, 120, 760, 840, 640, a, title="tumor_vs_normal.fastq")
    r_ = np.random.default_rng(3)
    rows = 14; off = int(max(0, lt) * 6)
    for i in range(rows):
        rr = np.random.default_rng(i + off)
        s = "".join(rr.choice(list("ACGT"), 30))
        y = 1310 - i * 36
        for j, ch in enumerate(s):
            c = RED if rr.uniform() < 0.02 else BCOL[ch]
            tx(ax, 175 + j * 24.5, y, ch, 17, c, a * (0.35 + 0.65 * (i == rows - 1 or True)) * (0.5 + 0.5 * (i > 2)), fam=MONO, w="normal", z=10)
    p = seg(lt, 0.3, 2.6)
    pill(ax, 540, 690, 520, 44, LINE, a, z=9); pill(ax, 280 + 260 * p, 690, 520 * p, 44, TEAL, a, z=10)
    tx(ax, 540, 690, f"analyzing {int(p*100)}%", 18, BG if p > 0.5 else WHITE, a, z=11, fam=MONO)

_VX = np.r_[rng.normal(0, 0.9, 260), rng.normal(3.2, 0.7, 22), rng.normal(-3.0, 0.7, 18)]
_VY = np.r_[np.abs(rng.normal(0, 1.4, 260)), rng.uniform(3, 8, 22), rng.uniform(3, 7.5, 18)]
def s8(ax, t, lt, a, v):
    x0, y0, w, h = 170, 760, 760, 620
    ax.plot([x0, x0 + w], [y0, y0], color=MUTED, lw=2, alpha=a, zorder=8); ax.plot([x0 + w / 2, x0 + w / 2], [y0, y0 + h], color=LINE, lw=2, alpha=a, zorder=8, ls="--")
    ax.plot([x0, x0], [y0, y0 + h], color=MUTED, lw=2, alpha=a, zorder=8)
    tx(ax, x0 + w / 2, y0 - 35, "change in expression (tumor vs healthy)", 17, MUTED, a, w="normal")
    tx(ax, x0 - 30, y0 + h / 2, "significance", 17, MUTED, a, w="normal", rot=90)
    n = int(len(_VX) * eout(seg(lt, 0.2, 2.5))); col = ease(seg(lt, 3.0, 4.0))
    X = x0 + w / 2 + _VX[:n] * 95; Y = y0 + 10 + _VY[:n] * 75
    C = []
    for vx, vy in zip(_VX[:n], _VY[:n]):
        base = np.array(to_rgb(DIM))
        tgt = np.array(to_rgb(RED if vx > 1.8 and vy > 2.5 else (SKY if vx < -1.8 and vy > 2.5 else DIM)))
        C.append(tuple(base * (1 - col) + tgt * col) + (a * 0.9,))
    if n: ax.scatter(X, Y, s=60, c=C, linewidths=0, zorder=9)
    tx(ax, x0 + w - 110, y0 + h - 20, "higher in tumor", 18, RED, a * col, w="semibold")
    tx(ax, x0 + 110, y0 + h - 20, "lower in tumor", 18, SKY, a * col, w="semibold")
    q = ease(seg(lt, 6.5, 7.2))
    if q > 0:
        for k, (nm, xx, yy) in enumerate([("gene A", 3.6, 7.2), ("gene B", -3.3, 6.6)]):
            px, py = x0 + w / 2 + xx * 95, y0 + 10 + yy * 75
            ring(ax, px, py, 22 + 4 * np.sin(t * 4), GOLD, a * q, lw=3, z=11)

_NN = rng.uniform([170, 760], [910, 1400], (22, 2))
_NE = [(i, j) for i in range(22) for j in range(i + 1, 22) if np.hypot(*(_NN[i] - _NN[j])) < 230]
def s9(ax, t, lt, a, v):
    hubs = [4, 13]
    deg = np.zeros(22)
    for i, j in _NE: deg[i] += 1; deg[j] += 1
    o = list(np.argsort(-deg)); h0 = o[0]
    h1 = next(k for k in o[1:] if np.hypot(*(_NN[k] - _NN[h0])) > 380)
    hubs = [h0, h1]
    g = ease(seg(lt, 0.0, 1.0)); hq = ease(seg(lt, 1.6, 2.4))
    for i, j in _NE:
        hot = (i in hubs or j in hubs)
        c = mixc(LINE, GOLD, hq * 0.7) if hot else LINE
        ax.plot([_NN[i, 0], _NN[j, 0]], [_NN[i, 1], _NN[j, 1]], color=c, lw=2.5 if hot else 1.8, alpha=a * g, zorder=8)
    for k, (x, y) in enumerate(_NN):
        ih = k in hubs
        r = 16 + 2 * deg[k] * (1 + 0.4 * hq * ih)
        c = mixc(SKY, GOLD, hq) if ih else SKY
        glowdot(ax, x, y, r * 0.6, c, a * g, z=9)
    for n_, h in enumerate(hubs):
        q = pop(lt, 2.6 + n_ * 0.6)
        if q <= 0: continue
        x, y = _NN[h]; lab = ["potential biomarker", "potential target"][n_]
        yy = y + 75 if n_ == 0 else y - 75
        pill(ax, x, yy, 300 * q, 52 * q, (0.03, 0.07, 0.14, 0.92), a, ec=GOLD, lw=2, z=12)
        tx(ax, x, yy, lab, 19 * q, GOLD, a, z=13)

def s10(ax, t, lt, a, v):
    draw_cell(ax, 540, 1170, 170 * (1 + 0.04 * np.sin(t * 1.5)), t, a, tint=SKY)
    q = ease(seg(lt, 1.2, 2.2))
    tx(ax, 540, 880, "Understanding cancer", 44, WHITE, a * q)
    tx(ax, 540, 815, "starts with understanding", 44, WHITE, a * q)
    tx(ax, 540, 745, "cells.", 56, RED, a * ease(seg(lt, 1.8, 2.6)))

class CV(Video):
    def audio(self, seed=0):
        SR = self.SR; n = int(self.END * SR); tt = np.arange(n) / SR; voice = np.zeros(n)
        for i, s in enumerate(self.T):
            a_, _ = sf.read(f"{self.name}/l{i}.wav"); a_ = a_ if a_.ndim == 1 else a_.mean(1); k = int(s * SR); voice[k:k + len(a_)] += a_[:n - k]
        voice = voice / np.abs(voice).max() * 0.9
        note = lambda m: 440 * 2 ** ((m - 69) / 12)
        TH = self.T[7] - 0.6                       # hopeful turn at bioinformatics
        dark = [[45, 52, 57, 60], [41, 48, 53, 57], [43, 50, 55, 58], [40, 47, 52, 56]]   # Am F Gm E
        hope = [[48, 55, 60, 64], [43, 50, 55, 59], [45, 52, 57, 60], [41, 48, 53, 57]]   # C G Am F
        bar = 4.0; pad = np.zeros(n); arp = np.zeros(n); bass = np.zeros(n); hb = np.zeros(n)
        for b in range(int(self.END / bar) + 1):
            s0 = int(b * bar * SR)
            if s0 >= n: break
            h = b * bar >= TH; c = (hope if h else dark)[b % 4]
            s1 = min(n, int((b + 1) * bar * SR) + int(0.6 * SR)); sg = tt[s0:s1] - b * bar
            env = np.minimum(1, sg / 1.2) * np.clip((bar + 0.6 - sg) / 1.2, 0, 1)
            for m in c:
                for det in (-0.12, 0.12): pad[s0:s1] += env * np.sin(2 * np.pi * note(m) * (1 + det / 100) * sg)
            bass[s0:s1] += env * np.sin(2 * np.pi * note(c[0] - 12) * sg)
            if h:
                for j in range(16):
                    m = c[[0, 1, 2, 3, 2, 1, 3, 2][j % 8]] + 12; st = s0 + int(j * 0.25 * SR)
                    if st >= n: break
                    e = min(n, st + int(0.9 * SR)); q = np.arange(e - st) / SR
                    arp[st:e] += np.exp(-q * 5) * np.sin(2 * np.pi * note(m) * q) * (0.6 if j % 4 == 0 else 0.35)
        # restrained heartbeat before the turn
        bt = 0.6
        while bt < TH:
            for off, amp in ((0, 1.0), (0.24, 0.6)):
                st = int((bt + off) * SR); e = min(n, st + int(0.3 * SR)); q = np.arange(e - st) / SR
                hb[st:e] += amp * np.exp(-q * 14) * np.sin(2 * np.pi * (48 + 30 * np.exp(-q * 25)) * q)
            bt += 1.15
        # low subtle pulses (suspense) every 2 s before the turn
        pul = np.zeros(n)
        for st_ in np.arange(1.0, TH, 2.0):
            st = int(st_ * SR); e = min(n, st + int(1.6 * SR)); q = np.arange(e - st) / SR
            pul[st:e] += np.sin(np.pi * q / 1.6) ** 2 * np.sin(2 * np.pi * 110 * q) * np.sin(2 * np.pi * 0.7 * q)
        pad = np.convolve(pad, np.ones(60) / 60, "same")
        music = pad / np.abs(pad).max() * 0.45 + bass / np.abs(bass).max() * 0.35 + hb / np.abs(hb).max() * 0.55 + pul / np.abs(pul).max() * 0.12
        music += arp / max(1e-9, np.abs(arp).max()) * 0.30
        rng_ = np.random.default_rng(seed)
        for (fn, i0, i1) in self.scenes[1:]:
            st = int(max(0, self.T[i0] - 0.75) * SR); L = int(0.7 * SR)
            if st + L >= n: continue
            nz = np.convolve(rng_.normal(0, 1, L), np.ones(20) / 20, "same"); music[st:st + L] += nz * np.sin(np.linspace(0, np.pi, L)) ** 2 * 1.4
        env = np.convolve(np.abs(voice), np.ones(int(0.3 * SR)) / int(0.3 * SR), "same")
        duck = 1 - 0.55 * np.clip(env / 0.05, 0, 1)
        fade = np.minimum(1, tt / 1.5) * np.minimum(1, (self.END - tt) / 2.0)
        lift = 1 + 0.35 * np.clip((tt - TH) / 3, 0, 1)
        music *= 0.21 * duck * fade * lift
        mix = voice + music; mix /= max(1, np.abs(mix).max() / 0.95)
        sf.write(f"{self.name}/mix.wav", np.stack([mix, mix], 1), SR)

def V():
    return CV("v_cell", "CANCER BIOLOGY", RED,
              [(s0, 0, 0), (s1, 1, 1), (s2, 2, 2), (s3, 3, 3), (s4, 4, 4), (s5, 5, 5), (s6, 6, 6), (s7, 7, 7), (s8, 8, 9), (s9, 10, 11), (s10, 12, 12)],
              [(0, 0, "INSIDE YOU", "Trillions of cells"), (1, 1, "THE QUESTION", "What if the\ncontrols fail?"), (2, 2, "THREE CONTROLS", "Growth in balance"),
               (3, 3, "THE ACCELERATOR", "Growth genes"), (4, 4, "THE BRAKES", "Checkpoints & repair"), (5, 5, "OVER TIME", "A tumor can form"),
               (6, 6, "NOT ONE DISEASE", "Many cancers"), (7, 7, "ENTER", "Bioinformatics"), (8, 9, "TUMOR vs HEALTHY", "Reading the data"),
               (10, 11, "THE GOAL", "Biomarkers & targets"), (12, 12, "THE FIRST STEP", "Back to the cell")], gap=0.45, start=0.4, outro=2.8)

if __name__ == "__main__":
    V().main(sys.argv, seed=2)
