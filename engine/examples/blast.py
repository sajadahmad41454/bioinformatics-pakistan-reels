import sys as _s, os as _o; _s.path.insert(0, _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), ".."))
from eng import *
import eng
from vids import browser, icon

# ---------- own theme: terminal green on near-black, amber + cyan accents ----------
eng.BG = "#030C07"; eng.BGCMAP = LSC.from_list("g", [eng.BG, "#0E3A22"]); eng.TEAL = "#4ADE80"; eng.MUTED = "#A7C4B0"
BG = eng.BG; MUTED = eng.MUTED
GR = "#4ADE80"; GRL = "#BBF7D0"; AM = "#FBBF24"; AML = "#FDE68A"; CY = "#22D3EE"; CYL = "#CFFAFE"; PK = "#F472B6"
CARDC = "#0A1A11"; LN = "#1F4A31"; GREY = "#5B7565"; TERM = "#02070A"
NB = {"A": "#4ADE80", "C": "#FBBF24", "G": "#22D3EE", "T": "#F472B6"}

# real toy data (computed with BLAST+ 2.12.0 in this run)
QUERY = "TTGGAATGCTGTGACATTATTACGACGCGAACCCCTCGTAACGCAGTGTCCCGGACAGCTGAAATTGGGCGCCCGGGCCCATATTTCCGACAACCATAAA"
ROW = ["myseq", "geneB", "97.000", "100", "3", "0", "1", "100", "101", "200", "9.33e-47", "169"]
COLS = ["qseqid", "sseqid", "pident", "length", "mismatch", "gapopen", "qstart", "qend", "sstart", "send", "evalue", "bitscore"]

def lbl(ax, x, y, s, al, col=WHITE, size=24, z=14, ec=GR):
    if al <= 0.01: return
    w = wpx(s, size) * 1.08 + 64
    pill(ax, x, y, w, size * 2.4, CARDC, al, ec=ec, lw=2, z=z)
    tx(ax, x, y, s, size, col, al, z=z + 1)

def bases(ax, x, y, seq, al, bw=40, z=10, hl=None, txt=True):
    for i, b in enumerate(seq):
        c = NB[b]; on = 1.0 if (hl is None or hl[0] <= i < hl[1]) else 0.25
        ax.add_patch(FancyBboxPatch((x + i * bw + 2, y - bw / 2 + 2), bw - 4, bw - 4, boxstyle="round,pad=0,rounding_size=6",
                                    fc=to_rgba(c, 0.22 * al * on), ec=to_rgba(c, al * on), lw=2, zorder=z))
        if txt: tx(ax, x + i * bw + bw / 2, y, b, bw * 0.45, c, al * on, z=z + 1, fam=MONO)

def dbstack(ax, x, y, s, al, col=CY, z=9):
    for k in range(4):
        yy_ = y - k * 50 * s
        ax.add_patch(Rectangle((x - 110 * s, yy_ - 50 * s), 220 * s, 50 * s, fc=to_rgba(col, 0.12 * al), ec="none", zorder=z + k * 0.01))
        ax.add_patch(Ellipse((x, yy_), 220 * s, 60 * s, fc=to_rgba(CARDC, al), ec=to_rgba(col, al), lw=3, zorder=z + 0.02 + k * 0.01))
    ax.add_patch(Ellipse((x, y - 200 * s), 220 * s, 60 * s, fc="none", ec=to_rgba(col, al), lw=3, zorder=z))
    ax.plot([x - 110 * s, x - 110 * s], [y, y - 200 * s], color=to_rgba(col, al), lw=3, zorder=z)
    ax.plot([x + 110 * s, x + 110 * s], [y, y - 200 * s], color=to_rgba(col, al), lw=3, zorder=z)

def term(ax, x, y, w, h, al, title="bash", z=8):
    if al <= 0.01: return
    card(ax, x, y, w, h, al, ec=GR, z=z, r=18, fc=TERM, lw=2.5)
    ax.add_patch(FancyBboxPatch((x, y + h - 56), w, 56, boxstyle="round,pad=0,rounding_size=18", fc=to_rgba("#0D2418", al), ec="none", zorder=z + 0.1))
    for j, c in enumerate(["#F87171", AM, GR]): ax.add_patch(Circle((x + 34 + j * 28, y + h - 28), 9, fc=to_rgba(c, al), zorder=z + 0.2))
    tx(ax, x + w / 2, y + h - 28, title, 17, MUTED, al, w="normal", z=z + 0.3, fam=MONO)

def typed(ax, x, y, lines, prog, al, size=24, col=GRL, z=12, lh=50):
    """type lines char by char; prog = number of chars shown"""
    n = 0
    for i, ln in enumerate(lines):
        k = int(np.clip(prog - n, 0, len(ln))); n += len(ln)
        if k <= 0: break
        s = ln[:k]
        if i == 0 or ln.startswith("$"):
            tx(ax, x, y - i * lh, s, size, col, al, w="normal", ha="left", z=z, fam=MONO)
        else:
            tx(ax, x, y - i * lh, s, size, col, al, w="normal", ha="left", z=z, fam=MONO)

# ---------------- scenes ----------------
def s0(ax, t, lt, a, v):
    seq = QUERY[:18]
    q = ease(seg(lt, 0.0, 0.6))
    bases(ax, 540 - 18 * 25, 1330, seq, a * q, bw=50)
    tx(ax, 540, 1230, "your sequence", 24, MUTED, a * q, w="semibold")
    qm = pop(lt, 0.8)
    if qm > 0: tx(ax, 540, 1110, "?", 110 * qm, AM, a, z=12)
    d = pop(lt, 2.0)
    dbstack(ax, 540, 960, 0.9 * d, a)
    tx(ax, 540, 720, "sequence database", 24, CY, a * ease(seg(lt, 2.3, 2.8)), w="semibold")
    # search pulses
    for k in range(3):
        u = (lt * 0.7 + k / 3) % 1
        ring(ax, 540, 880, 40 + 160 * u, GR, a * ease(seg(lt, 3.0, 3.5)) * (1 - u) * 0.8, lw=3, z=8)

DBSEQ = QUERY[30:34] + "GATCCA" + QUERY[2:14] + "ACGTTA"
def s1(ax, t, lt, a, v):
    bw = 34
    x0 = 540 - len(DBSEQ) * bw / 2
    q = ease(seg(lt, 0.0, 0.5))
    tx(ax, 540, 935, "database sequence", 20, CY, a * q, w="semibold")
    # query window of 12 bases slides then locks onto the match at index 10
    qs = QUERY[2:14]; target = 10
    u = ease(seg(lt, 0.6, 3.2)); pos = 0 + (target - 0) * u
    xq = x0 + pos * bw
    lock = ease(seg(lt, 3.2, 3.7))
    bases(ax, x0, 1000, DBSEQ, a * q, bw=bw, hl=(target, target + 12) if lock > 0.5 else None)
    bases(ax, xq, 1180, qs, a * q, bw=bw)
    tx(ax, xq, 1250, "query", 20, GR, a * q, w="semibold", ha="left")
    if lock > 0:
        for i in range(12):
            ax.plot([xq + i * bw + bw / 2] * 2, [1158, 1022], color=to_rgba(GR, 0.7 * a * lock), lw=2.5, zorder=9)
        ax.add_patch(FancyBboxPatch((x0 + target * bw - 8, 970), 12 * bw + 16, 240, boxstyle="round,pad=0,rounding_size=14", fc="none", ec=to_rgba(AM, a * lock), lw=3, zorder=11))
    lbl(ax, 540, 800, "local similarity", a * ease(seg(lt, 3.8, 4.3)), AML, 26, ec=AM)

def progcard(ax, y, al, name, a_lbl, b_lbl, ca, cb, mid=None):
    if al <= 0.01: return
    card(ax, 90, y - 95, 900, 190, al, ec=ca, fc=CARDC, z=9, lw=2.5)
    tx(ax, 140, y + 45, name, 40, WHITE, al, ha="left", z=11, fam=MONO)
    pill(ax, 230, y - 35, 180, 54, ca, al * 0.9, z=11); tx(ax, 230, y - 35, a_lbl, 22, BG, al, z=12)
    if mid:
        arrow(ax, 330, y - 35, 430, y - 35, MUTED, al, lw=3); pill(ax, 540, y - 35, 200, 54, CARDC, al, ec=AM, lw=2, z=11); tx(ax, 540, y - 35, mid, 20, AML, al, z=12)
        arrow(ax, 650, y - 35, 730, y - 35, MUTED, al, lw=3)
    else:
        arrow(ax, 330, y - 35, 720, y - 35, MUTED, al, lw=3); tx(ax, 525, y - 5, "vs", 18, MUTED, al, w="normal")
    pill(ax, 840, y - 35, 200, 54, cb, al * 0.9, z=11); tx(ax, 840, y - 35, b_lbl, 22, BG, al, z=12)

def s2(ax, t, lt, a, v):
    d3 = v.T[3] - v.T[2]
    progcard(ax, 1330, a * ease(seg(lt, 0.2, 0.7)), "blastn", "DNA", "DNA", GR, GR)
    progcard(ax, 1090, a * ease(seg(lt, 2.4, 2.9)), "blastp", "protein", "protein", PK, PK)
    progcard(ax, 850, a * ease(seg(lt, d3 + 0.1, d3 + 0.6)), "blastx", "DNA", "protein", GR, PK, mid="translate")

def fileicon(ax, x, y, al, name, col, lines):
    if al <= 0.01: return
    P = [(x - 190, y - 230), (x + 190, y - 230), (x + 190, y + 170), (x + 130, y + 230), (x - 190, y + 230)]
    ax.add_patch(Polygon(P, closed=True, fc=to_rgba(CARDC, al), ec=to_rgba(col, al), lw=3, zorder=9))
    ax.add_patch(Polygon([(x + 130, y + 230), (x + 130, y + 170), (x + 190, y + 170)], closed=True, fc=to_rgba(col, 0.4 * al), ec=to_rgba(col, al), lw=2, zorder=9.1))
    for i, ln in enumerate(lines):
        tx(ax, x - 160, y + 150 - i * 40, ln, 19, AML if ln.startswith(">") else GRL, al, w="normal", ha="left", z=10, fam=MONO)
    tx(ax, x, y - 280, name, 26, col, al, z=10, fam=MONO)

def s4(ax, t, lt, a, v):
    fq = pop(lt, 0.2)
    fileicon(ax, 290, 1120, a * min(fq, 1), "query.fasta", GR, [">myseq", QUERY[:20], QUERY[20:40], QUERY[40:60], QUERY[60:80], QUERY[80:100]])
    d = pop(lt, 2.2)
    dbstack(ax, 800, 1260, 0.95 * d, a)
    tx(ax, 800, 840, "database", 26, CY, a * ease(seg(lt, 2.4, 2.8)), z=10, fam=MONO)
    tx(ax, 540, 1120, "+", 60, MUTED, a * ease(seg(lt, 1.8, 2.2)))

def s5(ax, t, lt, a, v):
    term(ax, 50, 820, 980, 600, a, "build the database")
    cmd = ["$ makeblastdb -in genes.fasta \\", "    -dbtype nucl -out mydb"]
    prog = 60 * seg(lt, 0.3, 2.6)
    typed(ax, 90, 1290, cmd, prog, a, size=27)
    o = ease(seg(lt, 2.8, 3.2))
    tx(ax, 90, 1150, "Adding sequences from FASTA;", 22, MUTED, a * o, w="normal", ha="left", z=12, fam=MONO)
    tx(ax, 90, 1108, "added 3 sequences", 22, MUTED, a * o, w="normal", ha="left", z=12, fam=MONO)
    h = ease(seg(lt, 3.6, 4.1))
    if h > 0:
        lbl(ax, 300, 960, "-dbtype nucl = DNA", a * h, AML, 22, ec=AM)
        lbl(ax, 770, 960, "-dbtype prot = protein", a * ease(seg(lt, 4.1, 4.6)), PK, 22, ec=PK)

def s6(ax, t, lt, a, v):
    term(ax, 50, 820, 980, 600, a, "run the search")
    cmd = ["$ blastn -query query.fasta \\", "    -db mydb -out results.tsv \\", "    -outfmt 6 -evalue 1e-5"]
    prog = 90 * seg(lt, 0.3, 4.0)
    typed(ax, 90, 1290, cmd, prog, a, size=27)
    tags = [("query", 1290 - 0 * 50, GR, 0.6), ("database", 1240, CY, 1.5), ("output file", 1240, AM, 2.4), ("table", 1190, PK, 3.6)]
    yb = 1000
    for k, (s, _, c, t0) in enumerate(tags):
        q = ease(seg(lt, t0, t0 + 0.4))
        lbl(ax, 160 + k * 245, yb - (k % 2) * 80, s, a * q, c, 21, ec=c)
    tx(ax, 540, 880, "-evalue 1e-5: keep hits with E below 0.00001", 20, MUTED, a * ease(seg(lt, 4.4, 4.9)), w="normal", z=12)

def evscale(ax, al, mark):
    """log10 E-value axis from 1e-50 to 10"""
    if al <= 0.01: return
    x0, x1, y = 120, 960, 700
    f = lambda e: x0 + (x1 - x0) * (np.log10(e) + 50) / 51
    ax.plot([x0, x1], [y, y], color=to_rgba(MUTED, al), lw=3, zorder=10)
    for e, s in [(1e-50, "1e-50"), (1e-25, "1e-25"), (1e-5, "1e-5"), (10, "10")]:
        ax.plot([f(e)] * 2, [y - 12, y + 12], color=to_rgba(MUTED, al), lw=3, zorder=10)
        tx(ax, f(e), y - 45, s, 18, MUTED, al, w="normal", z=10, fam=MONO)
    tx(ax, x0, y + 72, "more significant", 18, GR, al, w="semibold", ha="left", z=10)
    tx(ax, x1, y + 72, "chance", 18, "#F87171", al, w="semibold", ha="right", z=10)
    if mark > 0:
        xm = f(9.33e-47)
        ax.add_patch(Polygon([(xm, y + 16), (xm - 14, y + 40), (xm + 14, y + 40)], closed=True, fc=to_rgba(AM, al * mark), zorder=11))
        glowdot(ax, xm, y, 10, AM, al * mark, z=11)

def results(ax, t, lt, a, v):
    T0 = v.T[7]
    i = max(k for k in range(7, 12) if t >= v.T[k] - 0.3) if t >= v.T[7] - 0.3 else 7
    HL = {7: set(range(12)), 8: {2, 3, 4, 5}, 9: {6, 7, 8, 9}, 10: {10}, 11: {10}}[i]
    card(ax, 50, 1390, 980, 80, a, ec=GR, fc=TERM, z=8, lw=2)
    tx(ax, 70, 1492, "$ cat results.tsv", 18, MUTED, a, w="normal", ha="left", z=9, fam=MONO)
    tx(ax, 540, 1430, "  ".join(ROW), 17, GRL, a * ease(seg(lt, 0.2, 0.6)), w="normal", z=9, fam=MONO)
    for k, (c, val) in enumerate(zip(COLS, ROW)):
        col_, r_ = divmod(k, 6)
        x = 70 + col_ * 480; y = 1320 - r_ * 72
        q = ease(seg(lt, 0.5 + 0.08 * k, 0.9 + 0.08 * k))
        on = k in HL
        al = a * q * (1.0 if on else 0.35)
        card(ax, x, y - 30, 460, 60, al, ec=AM if (on and i > 7) else LN, fc=CARDC, z=9, lw=2.5 if (on and i > 7) else 1.5)
        tx(ax, x + 20, y, c, 21, MUTED, al, w="normal", ha="left", z=10, fam=MONO)
        tx(ax, x + 440, y, val, 23, AML if (on and i > 7) else WHITE, al, ha="right", z=10, fam=MONO)
    # lower panel per line
    if i == 8:
        q = ease(seg(t, v.T[8] + 0.3, v.T[8] + 0.8))
        tx(ax, 540, 820, "97 identical / 100 aligned bases", 26, WHITE, a * q, z=10)
        tx(ax, 540, 760, "3 mismatches  ·  0 gap openings", 24, MUTED, a * q, w="semibold", z=10)
    if i == 9:
        q = ease(seg(t, v.T[9] + 0.2, v.T[9] + 0.8))
        # geneB bar 300 bp, query maps 101-200
        x0, x1 = 120, 960; sc = (x1 - x0) / 300
        ax.add_patch(Rectangle((x0, 690), x1 - x0, 30, fc=to_rgba(CY, 0.3 * a * q), ec=to_rgba(CY, a * q), lw=2, zorder=10))
        tx(ax, x0, 660, "geneB (300 bp)", 18, CY, a * q, w="semibold", ha="left")
        u = ease(seg(t, v.T[9] + 0.8, v.T[9] + 2.0))
        xa = x0 + 100 * sc; xb = x0 + 200 * sc
        ax.add_patch(Rectangle((xa, 790), (xb - xa), 30, fc=to_rgba(GR, 0.35 * a * q), ec=to_rgba(GR, a * q), lw=2, zorder=10))
        tx(ax, (xa + xb) / 2, 850, "query 1–100", 18, GR, a * q, w="semibold")
        if u > 0:
            for xx_ in (xa, xb): ax.plot([xx_, xx_], [790, 720], color=to_rgba(AM, a * u), lw=2.5, ls=(0, (5, 4)), zorder=10)
            tx(ax, xa, 660, "101", 18, AML, a * u, w="semibold"); tx(ax, xb, 660, "200", 18, AML, a * u, w="semibold")
    if i in (10, 11):
        q = ease(seg(t, v.T[10] + 0.3, v.T[10] + 0.8))
        evscale(ax, a * q, ease(seg(t, v.T[11] + 0.3, v.T[11] + 0.8)))
        tx(ax, 540, 840, "expected chance hits", 24, WHITE, a * q * (1 - ease(seg(t, v.T[11], v.T[11] + 0.4))), w="semibold")
        tx(ax, 540, 840, r"9.33e-47  $\approx$  $10^{-46}$", 32, AML, a * ease(seg(t, v.T[11] + 0.2, v.T[11] + 0.6)), z=11)

def s12(ax, t, lt, a, v):
    q = ease(seg(lt, 0.0, 0.5))
    browser(ax, 70, 760, 940, 680, a * q, "blast.ncbi.nlm.nih.gov")
    tx(ax, 110, 1310, "Enter query sequence", 22, WHITE, a * q, ha="left", z=10)
    card(ax, 110, 1000, 860, 270, a * q, ec=LN, fc="#061810", z=9, r=12)
    n = int(60 * seg(lt, 0.6, 3.0))
    s = QUERY[:n]
    for k in range(0, 60, 30):
        tx(ax, 135, 1220 - k // 30 * 45, s[k:k + 30], 22, GRL, a * q, w="normal", ha="left", z=10, fam=MONO)
    b = pop(lt, 3.2)
    if b > 0:
        pill(ax, 540, 880, 220 * b, 76 * b, "#2563EB", a, z=10)
        tx(ax, 540, 880, "BLAST", 28 * b, WHITE, a, z=11)

def V():
    sc = [(s0, 0, 0), (s1, 1, 1), (s2, 2, 3), (s4, 4, 4), (s5, 5, 5), (s6, 6, 6), (results, 7, 11), (s12, 12, 12)]
    hd = [(0, 0, "TOOL / PIPELINE", "BLAST"), (1, 1, "THE IDEA", "Find local matches"), (2, 3, "STEP 1", "Pick a program"),
          (4, 4, "STEP 2", "Two inputs"), (5, 5, "STEP 3", "Build a database"), (6, 6, "STEP 4", "Run the search"),
          (7, 7, "STEP 5", "Read the table"), (8, 8, "READING THE ROW", "Identity"), (9, 9, "READING THE ROW", "Where it aligns"),
          (10, 11, "READING THE ROW", "The E-value"), (12, 12, "NO INSTALL?", "BLAST on the web")]
    return Video("v_blast", "TOOL / PIPELINE", GR, sc, hd, gap=0.25, start=0.4, outro=2.6)

if __name__ == "__main__":
    V().main(sys.argv, seed=2)
