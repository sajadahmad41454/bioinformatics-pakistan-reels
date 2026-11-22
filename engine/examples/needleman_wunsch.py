import sys as _s, os as _o; _s.path.insert(0, _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), ".."))
from eng import *
import eng

# ---------- own theme: deep indigo grid, mint / coral / amber accents ----------
eng.BG = "#0B0A1F"; eng.BGCMAP = LSC.from_list("g", [eng.BG, "#2A1F5C"]); eng.TEAL = "#A5B4FC"; eng.MUTED = "#AFA9D6"
BG = eng.BG; MUTED = eng.MUTED
MI = "#5EEAD4"; MIL = "#CCFBF1"; CO = "#FB7185"; COL = "#FFE4E6"; AM = "#FCD34D"; AML = "#FEF3C7"; LV = "#C4B5FD"
CARDC = "#16133A"; LN = "#3B3478"; TERM = "#100E2B"
NB = {"A": MI, "C": AM, "G": LV, "T": CO}

# toy example, computed and checked in code (match +1, mismatch -1, gap -1)
TOP = "GATC"; SIDE = "GCATG"
def nw(a, b, m=1, s=-1, d=-1):
    F = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1): F[i][0] = i * d
    for j in range(len(b) + 1): F[0][j] = j * d
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            F[i][j] = max(F[i-1][j-1] + (m if a[i-1] == b[j-1] else s), F[i-1][j] + d, F[i][j-1] + d)
    return F
F = nw(SIDE, TOP)
assert F == [[0, -1, -2, -3, -4], [-1, 1, 0, -1, -2], [-2, 0, 0, -1, 0], [-3, -1, 1, 0, -1], [-4, -2, 0, 2, 1], [-5, -3, -1, 1, 1]]
PATH = [(5, 4), (4, 3), (3, 2), (2, 1), (1, 1), (0, 0)]   # traceback (i = row in SIDE, j = col in TOP)
ALN_TOP = "G-ATC"; ALN_SIDE = "GCATG"
assert sum((1 if a == b else -1) if "-" not in (a, b) else -1 for a, b in zip(ALN_TOP, ALN_SIDE)) == F[5][4] == 1

CS = 105; GX = 170; GY = 1440      # grid: left x, top y; rows i=0..5, cols j=0..4
def cxy(i, j): return GX + j * CS + CS / 2, GY - i * CS - CS / 2
def fmt(v): return str(v).replace("-", "−")

def tile(ax, x, y, b, al, s=70, z=10):
    if al <= 0.01: return
    c = MUTED if b == "-" else NB[b]
    ax.add_patch(FancyBboxPatch((x - s / 2 + 3, y - s / 2 + 3), s - 6, s - 6, boxstyle="round,pad=0,rounding_size=12",
                                fc=to_rgba(c, 0.18 * al), ec=to_rgba(c, al), lw=2.5, zorder=z))
    tx(ax, x, y, "–" if b == "-" else b, s * 0.42, c, al, z=z + 1, fam=MONO)

def lbl(ax, x, y, s, al, col=WHITE, size=22, z=14, ec=LV, ha="center"):
    if al <= 0.01: return
    w = wpx(s, size) * 1.08 + 56
    xx_ = x if ha == "center" else x + w / 2
    pill(ax, xx_, y, w, size * 2.3, CARDC, al, ec=ec, lw=2, z=z)
    tx(ax, xx_, y, s, size, col, al, z=z + 1)

# ---------------- scenes ----------------
def s0(ax, t, lt, a, v):
    q1 = ease(seg(lt, 0.1, 0.6)); q2 = ease(seg(lt, 0.6, 1.1))
    for k, b in enumerate(SIDE): tile(ax, 540 - 2 * 92 + k * 92, 1300, b, a * q1, s=84)
    off = 60 * np.sin(lt * 1.6) * (1 - ease(seg(lt, 4.5, 5.5)))
    for k, b in enumerate(TOP): tile(ax, 540 - 1.5 * 92 + k * 92 + off, 1150, b, a * q2, s=84)
    qm = pop(lt, 1.6)
    if qm > 0: tx(ax, 540, 990, "?", 100 * qm, AM, a * (1 - ease(seg(lt, 5.0, 5.6))), z=12)
    c = ease(seg(lt, 5.6, 6.2))
    lbl(ax, 540, 960, "Needleman & Wunsch · J. Mol. Biol. · 1970", a * c, AML, 21, ec=AM)
    tx(ax, 540, 880, "dynamic programming", 24, MUTED, a * ease(seg(lt, 6.4, 6.9)), w="semibold")

def s1(ax, t, lt, a, v):
    q = ease(seg(lt, 0.1, 0.7)); u = ease(seg(lt, 0.8, 2.2))
    x0, x1 = 140, 940
    for k, (y, c, n) in enumerate([(1280, LV, "sequence 1"), (1120, MI, "sequence 2")]):
        ax.add_patch(FancyBboxPatch((x0, y - 28), (x1 - x0), 56, boxstyle="round,pad=0,rounding_size=28", fc=to_rgba(c, 0.25 * a * q), ec=to_rgba(c, a * q), lw=3, zorder=9))
        tx(ax, x0 + 30, y + 60, n, 21, c, a * q, w="semibold", ha="left")
    for xx_ in np.linspace(x0 + 20, x1 - 20, 16):
        ax.plot([xx_, xx_], [1252, 1148], color=to_rgba(WHITE, 0.35 * a * u), lw=2, zorder=8)
    for xx_ in (x0, x1):
        ax.plot([xx_, xx_], [1340, 1060], color=to_rgba(AM, a * u), lw=3, ls=(0, (6, 5)), zorder=10)
    lbl(ax, 540, 960, "end to end = global", a * ease(seg(lt, 2.0, 2.5)), AML, 26, ec=AM)

def s2(ax, t, lt, a, v):
    rows = [("match", "+1", MI, "G", "G", 0.3), ("mismatch", "−1", CO, "G", "C", 1.6), ("gap", "−1", AM, "A", "-", 3.4)]
    for k, (name, sc, c, b1, b2, t0) in enumerate(rows):
        q = ease(seg(lt, t0, t0 + 0.45)); y = 1330 - k * 200
        if q <= 0.01: continue
        card(ax, 110, y - 80, 860, 160, a * q, ec=c, fc=CARDC, z=8, lw=2.5)
        tile(ax, 200, y + 32, b1, a * q, s=62); tile(ax, 200, y - 34, b2, a * q, s=62)
        tx(ax, 290, y, name, 38, WHITE, a * q, ha="left", z=11)
        tx(ax, 900, y, sc, 64, c, a * q, ha="right", z=11, fam=MONO)

def grid(ax, t, lt, a, v):
    T = v.T
    def at(i): return t - T[i]
    q = ease(seg(at(3), 0.0, 0.6))
    # labels
    for j, b in enumerate(TOP): tile(ax, cxy(0, j + 1)[0], GY + 52, b, a * ease(seg(at(3), 0.3 + 0.12 * j, 0.7 + 0.12 * j)), s=70)
    for i, b in enumerate(SIDE): tile(ax, GX - 52, cxy(i + 1, 0)[1], b, a * ease(seg(at(3), 1.6 + 0.12 * i, 2.0 + 0.12 * i)), s=70)
    tx(ax, cxy(0, 0)[0], GY + 52, "–", 26, MUTED, a * q, fam=MONO); tx(ax, GX - 52, cxy(0, 0)[1], "–", 26, MUTED, a * q, fam=MONO)
    # cells
    onpath = set(PATH[:max(0, int(np.ceil(6 * seg(at(10), 0.4, 3.2))))]) if t >= T[10] else set()
    fill_order = [(i, j) for i in range(1, 6) for j in range(1, 5) if (i, j) != (1, 1)]
    fp = seg(t, T[8] + 0.1, T[9] + 0.4) * len(fill_order)
    for i in range(6):
        for j in range(5):
            x, y = GX + j * CS, GY - (i + 1) * CS
            hl = (i, j) in onpath
            fc = to_rgba(CO, 0.28 * a) if hl else to_rgba(CARDC, 0.9 * a * q)
            ax.add_patch(Rectangle((x + 3, y + 3), CS - 6, CS - 6, fc=fc, ec=to_rgba(LN if not hl else CO, a * q), lw=2, zorder=8))
            # value visibility
            if i == 0 or j == 0:
                k = i + j; al = ease(seg(at(4), 1.2 + 0.28 * k, 1.5 + 0.28 * k))
            elif (i, j) == (1, 1):
                al = ease(seg(at(7), 3.8, 4.3))
            else:
                al = ease(np.clip(fp - fill_order.index((i, j)), 0, 1))
            if al > 0.01:
                col = WHITE
                if (i, j) == (5, 4) and t >= T[9]: col = AM
                tx(ax, x + CS / 2, y + CS / 2, fmt(F[i][j]), 34, col, a * al, z=10, fam=MONO)
    # focus on cell (1,1) during lines 5-7
    foc = win(t, T[5] - 0.1, T[8] + 0.2, 0.3)
    if foc > 0:
        x, y = cxy(1, 1)
        ax.add_patch(Rectangle((x - CS / 2 + 2, y - CS / 2 + 2), CS - 4, CS - 4, fc="none", ec=to_rgba(AM, a * foc), lw=4, zorder=11))
        sh = ease(seg(at(5), 0.3, 1.0))
        cols = {"d": MI, "u": AM, "l": AM}
        if t >= T[6]:
            emph = {"d": ease(seg(at(6), 0.0, 0.4)), "u": ease(seg(at(6), 2.2, 2.6)), "l": ease(seg(at(6), 2.2, 2.6))}
        else: emph = {"d": 0, "u": 0, "l": 0}
        for key, (x0, y0) in {"d": cxy(0, 0), "u": cxy(1 - 1, 1), "l": cxy(1, 0)}.items():
            c = cols[key] if emph[key] > 0.5 else WHITE
            arrow(ax, x0 + (x - x0) * 0.36, y0 + (y - y0) * 0.36, x0 + (x - x0) * 0.86, y0 + (y - y0) * 0.86, c, a * foc * sh, lw=4, z=12)
    # traceback arrows along path
    if t >= T[10]:
        pr = seg(at(10), 0.4, 3.2) * 5
        for k in range(5):
            u = np.clip(pr - k, 0, 1)
            if u <= 0: break
            (i0, j0), (i1, j1) = PATH[k], PATH[k + 1]
            xa, ya = cxy(i0, j0); xb, yb = cxy(i1, j1)
            diag = (i0 - i1 == 1 and j0 - j1 == 1)
            c = CO
            if t >= T[11]: c = MI if diag else AM
            ax.plot([xa, xa + (xb - xa) * u], [ya, ya + (yb - ya) * u], color=to_rgba(c, 0.5 * a), lw=7, solid_capstyle="round", zorder=9)
            ring(ax, xa, ya, 34, c, a, lw=3, z=9.5)
        if pr >= 5: ring(ax, *cxy(0, 0), 34, CO if t < T[11] else MI, a, lw=3, z=9.5)
    # ---- right panel ----
    PX = 735; PW = 290
    def panel(al, h=420, top=1440, ec=LN):
        card(ax, PX, top - h, PW, h, al, ec=ec, fc=TERM, z=8, lw=2)
    p4 = win(t, T[4] + 0.2, T[5] - 0.1, 0.3)
    if p4 > 0:
        panel(a * p4, 200)
        tx(ax, PX + PW / 2, 1385, "each gap step", 21, MUTED, a * p4, w="semibold")
        tx(ax, PX + PW / 2, 1310, "−1", 56, AM, a * p4, fam=MONO)
    p56 = win(t, T[5] + 0.1, T[7] - 0.1, 0.3)
    if p56 > 0:
        panel(a * p56, 470)
        items = [("diagonal", "match / mismatch", MI, 0.0), ("from above", "gap", AM, 2.2), ("from left", "gap", AM, 2.2)]
        for k, (n, s, c, t0) in enumerate(items):
            e = ease(seg(at(6), t0, t0 + 0.4)) if t >= T[6] else 0
            y = 1370 - k * 140
            tx(ax, PX + 30, y, n, 26, WHITE, a * p56, ha="left", z=10)
            tx(ax, PX + 30, y - 46, s, 22, c, a * p56 * e, w="semibold", ha="left", z=10)
    p7 = win(t, T[7] - 0.05, T[8] + 0.1, 0.3)
    if p7 > 0:
        panel(a * p7, 470, ec=AM)
        tx(ax, PX + PW / 2, 1395, "G vs G = match", 22, MIL, a * p7, w="semibold")
        rows = [("diag", "0 + 1 = 1", MI, 0.6), ("up", "−1 − 1 = −2", MUTED, 1.6), ("left", "−1 − 1 = −2", MUTED, 1.6)]
        for k, (n, s, c, t0) in enumerate(rows):
            e = ease(seg(at(7), t0, t0 + 0.4)); y = 1320 - k * 92
            tx(ax, PX + 24, y + 18, n, 18, MUTED, a * p7 * e, w="semibold", ha="left", z=10)
            tx(ax, PX + 24, y - 20, s, 24, c, a * p7 * e, ha="left", z=10, fam=MONO)
        e = ease(seg(at(7), 3.2, 3.6))
        tx(ax, PX + PW / 2, 1060, "max = 1", 34, AM, a * p7 * e, z=10, fam=MONO)
    p8 = win(t, T[8] + 0.05, T[10] - 0.1, 0.3)
    if p8 > 0:
        panel(a * p8, 300, ec=AM if t >= T[9] else LN)
        tx(ax, PX + PW / 2, 1385, "row by row", 22, MUTED, a * p8, w="semibold")
        e = ease(seg(at(9), 0.3, 0.8)) if t >= T[9] else 0
        tx(ax, PX + PW / 2, 1300, "best score", 22, WHITE, a * p8 * e, w="semibold")
        tx(ax, PX + PW / 2, 1220, "1", 64, AM, a * p8 * e, fam=MONO)
    p10 = win(t, T[10] + 0.05, T[12] - 0.1, 0.3)
    if p10 > 0:
        panel(a * p10, 420)
        tx(ax, PX + PW / 2, 1395, "trace back", 24, CO, a * p10)
        e = ease(seg(at(11), 0.0, 0.4)) if t >= T[11] else 0
        e2 = ease(seg(at(11), 2.2, 2.6)) if t >= T[11] else 0
        tx(ax, PX + 26, 1300, "diagonal", 24, MI, a * p10 * e, ha="left", z=10)
        tx(ax, PX + 26, 1255, "pair 2 letters", 21, WHITE, a * p10 * e, w="semibold", ha="left", z=10)
        tx(ax, PX + 26, 1165, "vertical", 24, AM, a * p10 * e2, ha="left", z=10)
        tx(ax, PX + 26, 1120, "gap in top seq", 21, WHITE, a * p10 * e2, w="semibold", ha="left", z=10)

def s12(ax, t, lt, a, v):
    q = ease(seg(lt, 0.0, 0.5)); S = 110; x0 = 540 - 2 * S
    tx(ax, 120, 1330, "top", 20, MUTED, a * q, w="semibold", ha="left"); tx(ax, 120, 1200, "side", 20, MUTED, a * q, w="semibold", ha="left")
    for k, (b1, b2) in enumerate(zip(ALN_TOP, ALN_SIDE)):
        e = ease(seg(lt, 0.2 + 0.15 * k, 0.6 + 0.15 * k)); x = x0 + k * S + 50
        tile(ax, x, 1330, b1, a * e, s=96); tile(ax, x, 1200, b2, a * e, s=96)
        sc = (1 if b1 == b2 else -1) if "-" not in (b1, b2) else -1
        c = MI if sc > 0 else (AM if "-" in (b1, b2) else CO)
        e2 = ease(seg(lt, 1.2 + 0.25 * k, 1.6 + 0.25 * k))
        pill(ax, x, 1060, 90, 56, c, a * e2 * 0.95, z=11); tx(ax, x, 1060, ("+1" if sc > 0 else "−1"), 24, BG, a * e2, z=12, fam=MONO)
    e3 = ease(seg(lt, 2.8, 3.3))
    lbl(ax, 540, 920, "3 matches · 1 mismatch · 1 gap", a * e3, WHITE, 24, ec=LV)
    tx(ax, 540, 820, "score = 1", 40, AM, a * ease(seg(lt, 3.4, 3.8)), fam=MONO)

def s13(ax, t, lt, a, v):
    q = ease(seg(lt, 0.0, 0.5))
    u = ease(seg(lt, 0.3, 3.0)); m = int(4 + 8 * u); n = int(3 + 6 * u)
    s = 520 / max(m, n * 1.0 + 3)
    xa = 540 - n * s / 2; ya = 1420
    for i in range(m):
        for j in range(n):
            ax.add_patch(Rectangle((xa + j * s + 2, ya - (i + 1) * s + 2), s - 4, s - 4, fc=to_rgba(LV, 0.35 * a * q), ec=to_rgba(LV, 0.8 * a * q), lw=1.5, zorder=9))
    tx(ax, 540, ya + 40, f"n = {n}", 24, MI, a * q, fam=MONO)
    tx(ax, xa - 30, ya - m * s / 2, f"m = {m}", 24, CO, a * q, fam=MONO, ha="right")
    lbl(ax, 540, 760, "time & memory grow with m × n", a * ease(seg(lt, 2.4, 2.9)), AML, 26, ec=AM)

def V():
    sc = [(s0, 0, 0), (s1, 1, 1), (s2, 2, 2), (grid, 3, 11), (s12, 12, 12), (s13, 13, 13)]
    hd = [(0, 0, "ALGORITHM", "Needleman–Wunsch"), (1, 1, "THE GOAL", "Global alignment"), (2, 2, "THE RULES", "Scoring"),
          (3, 4, "STEP 1", "Build the grid"), (5, 7, "STEP 2", "Best of three moves"), (8, 9, "STEP 3", "Fill & read the score"),
          (10, 11, "STEP 4", "Trace back"), (12, 12, "RESULT", "The alignment"), (13, 13, "COST", "Time & memory")]
    return Video("v_nw", "ALGORITHM", MI, sc, hd, gap=0.25, start=0.4, outro=2.6)

if __name__ == "__main__":
    V().main(sys.argv, seed=1)
