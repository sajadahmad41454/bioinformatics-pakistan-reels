import sys as _s, os as _o; _s.path.insert(0, _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), ".."))
from eng import *
import eng

# ---------- own theme: warm charcoal, coral-orange + sky + lime accents ("genome ruler") ----------
eng.BG = "#140B06"; eng.BGCMAP = LSC.from_list("g", [eng.BG, "#3D2010"]); eng.TEAL = "#FDBA74"; eng.MUTED = "#C9B3A3"
BG = eng.BG; MUTED = eng.MUTED
OR = "#FB923C"; ORL = "#FED7AA"; SK = "#7DD3FC"; SKL = "#E0F2FE"; LI = "#BEF264"; LIL = "#ECFCCB"; RO = "#FB7185"
CARDC = "#22140C"; LN = "#4A2E1C"; TERM = "#0C0604"

# ---- real toy data (bwa mem + samtools 1.19.2, computed in this run) ----
UNSORTED = [("read1", 730), ("read2", 165), ("read3", 705), ("read4", 878), ("read5", 867), ("read6", 845), ("read7", 201),
            ("read8", 850), ("read9", 89), ("read10", 630), ("read11", 415), ("read12", 188), ("read13", 805), ("read14", 636),
            ("read15", 485), ("read16", 228), ("read17", 636), ("read18", 656)]
REGION = [("read2", 165), ("read12", 188), ("read7", 201), ("read16", 228)]
FIRST = ["read9", "0", "chr1", "89", "60", "100M"]
NAMES = ["QNAME", "FLAG", "RNAME", "POS", "MAPQ", "CIGAR", "RNEXT", "PNEXT", "TLEN", "SEQ", "QUAL"]
DESC = ["read name", "flag", "reference", "position", "mapping quality", "CIGAR"]

def lbl(ax, x, y, s, al, col=WHITE, size=24, z=14, ec=OR):
    if al <= 0.01: return
    w = wpx(s, size) * 1.08 + 64
    pill(ax, x, y, w, size * 2.4, CARDC, al, ec=ec, lw=2, z=z)
    tx(ax, x, y, s, size, col, al, z=z + 1)

def term(ax, x, y, w, h, al, title="bash", z=8):
    if al <= 0.01: return
    card(ax, x, y, w, h, al, ec=OR, z=z, r=18, fc=TERM, lw=2.5)
    ax.add_patch(FancyBboxPatch((x, y + h - 56), w, 56, boxstyle="round,pad=0,rounding_size=18", fc=to_rgba("#2A170C", al), ec="none", zorder=z + 0.1))
    for j, c in enumerate(["#F87171", "#FBBF24", LI]): ax.add_patch(Circle((x + 34 + j * 28, y + h - 28), 9, fc=to_rgba(c, al), zorder=z + 0.2))
    tx(ax, x + w / 2, y + h - 28, title, 17, MUTED, al, w="normal", z=z + 0.3, fam=MONO)

def typed(ax, x, y, lines, prog, al, size=24, col=ORL, z=12, lh=48):
    n = 0
    for i, ln in enumerate(lines):
        k = int(np.clip(prog - n, 0, len(ln))); n += len(ln)
        if k <= 0: break
        tx(ax, x, y - i * lh, ln[:k], size, col, al, w="normal", ha="left", z=z, fam=MONO)

def fileicon(ax, x, y, s, al, name, col, z=9, body=None):
    if al <= 0.01: return
    w, h = 150 * s, 190 * s
    P = [(x - w, y - h), (x + w, y - h), (x + w, y + h - 50 * s), (x + w - 50 * s, y + h), (x - w, y + h)]
    ax.add_patch(Polygon(P, closed=True, fc=to_rgba(CARDC, al), ec=to_rgba(col, al), lw=3, zorder=z))
    ax.add_patch(Polygon([(x + w - 50 * s, y + h), (x + w - 50 * s, y + h - 50 * s), (x + w, y + h - 50 * s)], closed=True, fc=to_rgba(col, 0.4 * al), ec=to_rgba(col, al), lw=2, zorder=z + 0.1))
    tx(ax, x, y + 20 * s, name, 34 * s, col, al, z=z + 1)
    if body:
        for k in range(4):
            ax.plot([x - w + 30 * s, x + w - 30 * s - (k % 2) * 60 * s], [y - 50 * s - k * 30 * s] * 2, color=to_rgba(col, 0.45 * al), lw=4 * s, zorder=z + 1, solid_capstyle="round")

# genome ruler: positions 1..1000 mapped to x 90..990
RX0, RX1 = 90, 990
def gx(p): return RX0 + (RX1 - RX0) * (p - 1) / 1000
def ruler(ax, y, al, z=9, ticks=(1, 200, 400, 600, 800, 1000)):
    if al <= 0.01: return
    ax.add_patch(FancyBboxPatch((RX0, y - 9), RX1 - RX0, 18, boxstyle="round,pad=0,rounding_size=9", fc=to_rgba(SK, 0.25 * al), ec=to_rgba(SK, al), lw=2, zorder=z))
    for p in ticks:
        ax.plot([gx(p)] * 2, [y - 22, y - 12], color=to_rgba(MUTED, al), lw=2, zorder=z)
        tx(ax, gx(p), y - 44, str(p), 17, MUTED, al, w="normal", z=z, fam=MONO)
    tx(ax, RX1, y + 36, "chr1 (1,000 bp)", 19, SK, al, w="semibold", ha="right", z=z)

def readbar(ax, pos, y, al, col=OR, h=20, z=10, name=None):
    if al <= 0.01: return
    ax.add_patch(FancyBboxPatch((gx(pos), y - h / 2), gx(pos + 99) - gx(pos), h, boxstyle="round,pad=0,rounding_size=6",
                                fc=to_rgba(col, 0.55 * al), ec=to_rgba(col, al), lw=1.5, zorder=z))
    if name: tx(ax, gx(pos) - 10, y, name, 15, col, al, w="semibold", ha="right", z=z, fam=MONO)

# ---------------- scenes ----------------
def s0(ax, t, lt, a, v):
    f = pop(lt, 0.1)
    fileicon(ax, 540, 1170, 1.15 * min(f, 1.1), a, "aln.sam", OR, body=True)
    qm = pop(lt, 1.6)
    if qm > 0: tx(ax, 790, 1360, "?", 120 * qm, SK, a, z=12)
    tx(ax, 540, 860, "from your aligner (e.g. BWA)", 22, MUTED, a * ease(seg(lt, 0.8, 1.3)), w="semibold")
    b = pop(lt, 3.2)
    if b > 0: lbl(ax, 540, 760, "SAMtools", a, ORL, 34 * b, ec=OR)

def s1(ax, t, lt, a, v):
    for k, (nm, c) in enumerate([("SAM", OR), ("BAM", SK), ("CRAM", LI)]):
        q = pop(lt, 0.9 + 0.6 * k)
        if q <= 0: continue
        x = 220 + k * 320
        card(ax, x - 130, 1020, 260, 300, a, ec=c, fc=CARDC, z=9, lw=3)
        tx(ax, x, 1190, nm, 52 * min(q, 1.1), c, a, z=10)
    tx(ax, 540, 880, "a set of utilities for alignment files", 24, WHITE, a * ease(seg(lt, 2.8, 3.3)), w="semibold")

def sam_line(ax, t, lt, a, v):
    d = v.T[3] - v.T[2]
    # line 2: 11 required columns
    q = ease(seg(lt, 0.3, 0.8))
    card(ax, 50, 1360, 980, 76, a * q, ec=OR, fc=TERM, z=8, lw=2)
    tx(ax, 540, 1398, "read9  0  chr1  89  60  100M  *  0  0  CGCCTT…  IIIIII…", 19, ORL, a * q, w="normal", z=9, fam=MONO)
    tx(ax, 540, 1470, "one alignment = one line (tab-separated)", 20, MUTED, a * q, w="semibold")
    for k, nm in enumerate(NAMES):
        r_, c_ = divmod(k, 4)
        x = 60 + c_ * 245; y = 1230 - r_ * 92
        qk = ease(seg(lt, 1.2 + 0.18 * k, 1.5 + 0.18 * k))
        hl = lt > d and k < 6
        al = a * qk * (1.0 if (lt <= d or k < 6) else 0.3)
        card(ax, x, y - 34, 225, 68, al, ec=OR if hl else LN, fc=CARDC, z=9, lw=2.5 if hl else 1.5)
        tx(ax, x + 112, y, nm, 22, ORL if hl else WHITE, al, z=10, fam=MONO)
    tx(ax, 540, 900, "11 required columns", 30, SK, a * ease(seg(lt, 3.4, 3.9)) * (1 - ease(seg(lt, d - 0.2, d + 0.2))))
    # line 3: meaning of the first six
    if lt > d:
        for k, (val, ds) in enumerate(zip(FIRST, DESC)):
            qk = ease(seg(lt, d + 0.2 + 0.35 * k, d + 0.6 + 0.35 * k))
            x = 70 + (k % 3) * 320; y = 900 - (k // 3) * 110
            tx(ax, x, y + 18, val, 26, LIL, a * qk, ha="left", z=10, fam=MONO)
            tx(ax, x, y - 22, ds, 19, MUTED, a * qk, w="semibold", ha="left", z=10)

def s4(ax, t, lt, a, v):
    q = ease(seg(lt, 0.2, 0.7))
    tx(ax, 90, 1340, "aln.sam", 28, OR, a * q, ha="left", fam=MONO)
    tx(ax, 990, 1340, "5,337 bytes", 26, WHITE, a * q, ha="right", fam=MONO)
    ax.add_patch(FancyBboxPatch((90, 1250), 900 * q, 50, boxstyle="round,pad=0,rounding_size=12", fc=to_rgba(OR, 0.6 * a), ec=to_rgba(OR, a), lw=2, zorder=9))
    u = ease(seg(lt, 2.6, 4.0))
    q2 = ease(seg(lt, 2.4, 2.8))
    tx(ax, 90, 1130, "aln.sorted.bam", 28, SK, a * q2, ha="left", fam=MONO)
    tx(ax, 990, 1130, "957 bytes", 26, WHITE, a * ease(seg(lt, 3.8, 4.2)), ha="right", fam=MONO)
    wv = 900 * (1 - u) + 900 * 957 / 5337 * u
    if q2 > 0:
        ax.add_patch(FancyBboxPatch((90, 1040), wv, 50, boxstyle="round,pad=0,rounding_size=12", fc=to_rgba(SK, 0.6 * a * q2), ec=to_rgba(SK, a * q2), lw=2, zorder=9))
    lbl(ax, 540, 880, "same data, compressed (BGZF)", a * ease(seg(lt, 4.4, 4.9)), SKL, 24, ec=SK)

def s5(ax, t, lt, a, v):
    term(ax, 50, 1220, 980, 230, a, "step 1")
    typed(ax, 90, 1310, ["$ samtools sort -o aln.sorted.bam aln.sam"], 44 * seg(lt, 0.2, 1.8), a, size=23)
    ruler(ax, 700, a * ease(seg(lt, 0.3, 0.8)))
    u = ease(seg(lt, 2.2, 3.6))
    order = sorted(range(len(UNSORTED)), key=lambda k: UNSORTED[k][1])
    rank = {k: r for r, k in enumerate(order)}
    for k, (nm, p) in enumerate(UNSORTED):
        y0 = 1135 - k * 21; y1 = 1135 - rank[k] * 21
        readbar(ax, p, y0 + (y1 - y0) * u, a * ease(seg(lt, 0.4 + 0.04 * k, 0.7 + 0.04 * k)), col=OR if u < 1 else LI, h=17)
    tx(ax, 540, 1180, "by leftmost position", 22, LI, a * ease(seg(lt, 3.6, 4.0)), w="semibold")

def s6(ax, t, lt, a, v):
    term(ax, 50, 1220, 980, 230, a, "step 2")
    typed(ax, 90, 1310, ["$ samtools index aln.sorted.bam"], 32 * seg(lt, 0.2, 1.6), a, size=25)
    q = pop(lt, 2.0)
    if q > 0:
        fileicon(ax, 330, 1010, 0.6 * min(q, 1.1), a, "BAM", SK)
        arrow(ax, 450, 1010, 610, 1010, MUTED, a * ease(seg(lt, 2.3, 2.7)), lw=3)
    q2 = pop(lt, 2.7)
    if q2 > 0: fileicon(ax, 750, 1010, 0.6 * min(q2, 1.1), a, ".bai", LI)
    tx(ax, 540, 830, "aln.sorted.bam.bai", 26, LIL, a * ease(seg(lt, 3.0, 3.4)), fam=MONO)
    lbl(ax, 540, 740, "fast random access", a * ease(seg(lt, 4.2, 4.7)), ORL, 24)

FS = ["$ samtools flagstat aln.sorted.bam", "20 + 0 in total (QC-passed reads", "    + QC-failed reads)", "20 + 0 primary",
      "0 + 0 secondary", "...", "18 + 0 mapped (90.00% : N/A)", "..."]
def s7(ax, t, lt, a, v):
    i = 7 + sum(t >= v.T[k] - 0.2 for k in (8, 9))
    term(ax, 50, 840, 980, 610, a, "step 3")
    for k, ln in enumerate(FS):
        q = ease(seg(lt, 0.2 + (0 if k == 0 else 1.6 + 0.12 * k), 0.6 + (0 if k == 0 else 1.6 + 0.12 * k)))
        hl = (i == 8 and k in (1, 6)) or (i == 9 and k in (1, 2))
        col = (ORL if k == 0 else (LIL if hl else MUTED))
        tx(ax, 90, 1350 - k * 58, ln, 23 if k else 24, col, a * q * (1 if (i == 7 or hl or k == 0) else 0.45), w="bold" if hl else "normal", ha="left", z=10, fam=MONO)
    if i == 8:
        q = ease(seg(t, v.T[8] + 0.3, v.T[8] + 0.8))
        cx, cy, R = 540, 730, 0
        x0 = 140; wbar = 800
        for j in range(20):
            col = LI if j < 18 else RO
            ax.add_patch(FancyBboxPatch((x0 + j * 40, 700), 32, 60, boxstyle="round,pad=0,rounding_size=6", fc=to_rgba(col, 0.6 * a * q), ec=to_rgba(col, a * q), lw=1.5, zorder=10))
        tx(ax, 540, 650, "18 mapped  ·  2 unmapped", 22, WHITE, a * q, w="semibold")
    if i == 9:
        q = ease(seg(t, v.T[9] + 0.3, v.T[9] + 0.8))
        lbl(ax, 300, 720, "#PASS = 20", a * q, LIL, 24, ec=LI)
        lbl(ax, 780, 720, "#FAIL = 0", a * ease(seg(t, v.T[9] + 1.2, v.T[9] + 1.7)), "#FECDD3", 24, ec=RO)

def s10(ax, t, lt, a, v):
    d = v.T[11] - v.T[10]
    term(ax, 50, 1180, 980, 290, a, "step 4")
    typed(ax, 90, 1370, ["$ samtools view aln.sorted.bam \\", "    chr1:200-300 | cut -f1-6"], 62 * seg(lt, 0.2, 2.4), a, size=23)
    if lt > d - 0.2:
        q = ease(seg(lt, d - 0.2, d + 0.2))
        ax.add_patch(Rectangle((60, 1185), 960, 230, fc=to_rgba(TERM, a * q), zorder=12.5))
        typed(ax, 90, 1370, ["$ samtools view -c aln.sorted.bam \\", "    chr1:200-300"], 60 * seg(lt, d + 0.1, d + 1.8), a, size=23, z=13)
        if lt > d + 2.0: tx(ax, 90, 1250, "4", 30, LIL, a * ease(seg(lt, d + 2.0, d + 2.3)), ha="left", z=13, fam=MONO)
    ruler(ax, 700, a * ease(seg(lt, 0.4, 0.9)))
    w = ease(seg(lt, 2.5, 3.0))
    if w > 0:
        ax.add_patch(Rectangle((gx(200), 690), gx(300) - gx(200), 420, fc=to_rgba(LI, 0.12 * a * w), ec=to_rgba(LI, a * w), lw=2, ls=(0, (6, 4)), zorder=8))
        tx(ax, (gx(200) + gx(300)) / 2, 1130, "200–300", 19, LI, a * w, w="semibold", fam=MONO)
    for k, (nm, p) in enumerate(REGION):
        q = ease(seg(lt, 3.1 + 0.3 * k, 3.5 + 0.3 * k))
        readbar(ax, p, 1050 - k * 70, a * q, col=OR, h=30)
        tx(ax, gx(p + 99) + 14, 1050 - k * 70, f"{nm}  POS {p}", 18, ORL, a * q, w="semibold", ha="left", z=10, fam=MONO)

def s12(ax, t, lt, a, v):
    steps = [("sort", OR), ("index", SK), ("flagstat", LI), ("view", RO)]
    for k, (s, c) in enumerate(steps):
        q = pop(lt, 0.2 + 0.55 * k)
        if q <= 0: continue
        y = 1360 - k * 150
        pill(ax, 540, y, 560 * min(q, 1.05), 96, CARDC, a, ec=c, lw=3, z=10)
        tx(ax, 540, y, "samtools " + s, 32 * min(q, 1.05), c, a, z=11, fam=MONO)
        if k < 3: arrow(ax, 540, y - 52, 540, y - 96, MUTED, a * ease(seg(lt, 0.5 + 0.55 * k, 0.8 + 0.55 * k)), lw=3)

def V():
    sc = [(s0, 0, 0), (s1, 1, 1), (sam_line, 2, 3), (s4, 4, 4), (s5, 5, 5), (s6, 6, 6), (s7, 7, 9), (s10, 10, 11), (s12, 12, 12)]
    hd = [(0, 0, "TOOL / PIPELINE", "SAMtools"), (1, 1, "WHAT IT IS", "One toolkit, three formats"), (2, 3, "THE FORMAT", "Inside a SAM file"),
          (4, 4, "SAM vs BAM", "Same data, smaller"), (5, 5, "STEP 1", "Sort"), (6, 6, "STEP 2", "Index"),
          (7, 9, "STEP 3", "Check with flagstat"), (10, 11, "STEP 4", "View a region"), (12, 12, "THE ROUTINE", "Four commands")]
    return Video("v_sam", "TOOL / PIPELINE", OR, sc, hd, gap=0.2, start=0.4, outro=2.6)

if __name__ == "__main__":
    V().main(sys.argv, seed=1)
