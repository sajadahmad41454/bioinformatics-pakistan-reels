import numpy as np, matplotlib, sys, json, subprocess, textwrap, os
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as LSC, to_rgba, to_rgb
from matplotlib.collections import LineCollection
from matplotlib.patches import FancyBboxPatch, Circle, Wedge, Polygon, Ellipse, Rectangle
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
import soundfile as sf
import warnings; warnings.filterwarnings("ignore")
plt.rcParams["font.family"] = "Inter"

W, H, FPS = 1080, 1920, 30
BG = "#050E1E"; TEAL = "#2DD4BF"; SKY = "#38BDF8"; GREEN = "#22C55E"; WHITE = "#FFFFFF"; MUTED = "#94A8C4"
DIM = "#4F6585"; GOLD = "#FBBF24"; MAG = "#F43F5E"; ORANGE = "#FB923C"; VIO = "#A78BFA"; CARD = "#0C1D37"; LINE = "#1E3A5F"
BCOL = {"A": TEAL, "T": SKY, "G": GREEN, "C": GOLD}
MONO = "DejaVu Sans Mono"

def ease(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
def eout(x): x = np.clip(x, 0, 1); return 1 - (1 - x) ** 3
def seg(t, a, b): return float(np.clip((t - a) / (b - a), 0, 1))
def win(t, a, b, f=0.45): return ease(seg(t, a, a + f)) * (1 - ease(seg(t, b - f, b)))
def pop(t, a, d=0.4):
    x = seg(t, a, a + d)
    if x <= 0: return 0.0
    return 1 + 0.18 * np.sin(x * np.pi) if x < 1 else 1.0
def mixc(c1, c2, k):
    a, b = np.array(to_rgb(c1)), np.array(to_rgb(c2)); return tuple(a * (1 - k) + b * k)
def tx(ax, x, y, s, size, col, al, w="bold", ha="center", z=20, fam=None, va="center", rot=0):
    if al <= 0.01 or size <= 0.5: return
    kw = dict(color=col, fontsize=size, fontweight=w, ha=ha, va=va, alpha=float(min(al, 1)), zorder=z, rotation=rot)
    if fam: kw["family"] = fam
    ax.text(x, y, s, **kw)
def pill(ax, cx, cy, w, h, fc, al, ec="none", lw=0, z=15):
    if al <= 0.01 or w <= 1: return
    f_ = to_rgba(fc); f_ = (f_[0], f_[1], f_[2], f_[3] * min(al, 1))
    e_ = "none" if ec == "none" else to_rgba(ec, min(al, 1))
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={h/2}", fc=f_, ec=e_, lw=lw, zorder=z))
def card(ax, x, y, w, h, al, ec=None, z=8, r=24, fc=CARD, lw=1.5):
    if al <= 0.01: return
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec or LINE, lw=lw, alpha=min(al, 1), zorder=z))
def glowdot(ax, x, y, r, c, al, z=10):
    if al <= 0.01: return
    ax.add_patch(Circle((x, y), r * 2.2, fc=c, alpha=0.10 * al, ec="none", zorder=z))
    ax.add_patch(Circle((x, y), r * 1.5, fc=c, alpha=0.18 * al, ec="none", zorder=z))
    ax.add_patch(Circle((x, y), r, fc=c, alpha=min(al, 1), ec="none", zorder=z + 0.1))
def ring(ax, x, y, r, c, al, lw=3, z=10, ls="-"):
    if al <= 0.01: return
    ax.add_patch(Circle((x, y), r, fc="none", ec=c, lw=lw, alpha=min(al, 1), zorder=z, ls=ls))
def arrow(ax, x0, y0, x1, y1, c, al, lw=3, z=12):
    if al <= 0.01: return
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=c, lw=lw, alpha=min(al, 1), mutation_scale=22), zorder=z)
def molecule(ax, cx, cy, s, col, al, rot=0, z=14):
    if al <= 0.01: return
    hexa = [(cx + s * np.cos(rot + k * np.pi / 3), cy + s * np.sin(rot + k * np.pi / 3)) for k in range(6)]
    ax.add_patch(Polygon(hexa, closed=True, fc=to_rgba(col, 0.15 * al), ec=col, lw=2.5, alpha=al, zorder=z))
    p = hexa[0]; q = (p[0] + s * 1.1 * np.cos(rot), p[1] + s * 1.1 * np.sin(rot))
    ax.plot([p[0], q[0]], [p[1], q[1]], color=col, lw=2.5, alpha=al, zorder=z)
    ax.add_patch(Circle(q, s * 0.28, fc=col, alpha=al, zorder=z))
    p2 = hexa[3]; q2 = (p2[0] + s * 0.9 * np.cos(rot + np.pi + 0.5), p2[1] + s * 0.9 * np.sin(rot + np.pi + 0.5))
    ax.plot([p2[0], q2[0]], [p2[1], q2[1]], color=col, lw=2.5, alpha=al, zorder=z)
    ax.add_patch(Circle(q2, s * 0.22, fc=WHITE, alpha=al * 0.9, zorder=z))
def helix(ax, t, cy, x0, x1, R, al, turns=2.4, lw=7, rungs=24, split=0, c1=SKY, c2=GREEN, z=4):
    if al <= 0.01: return
    xs = np.linspace(x0, x1, 360); th = (xs - x0) / (x1 - x0) * 2 * np.pi * turns + t * 2.0
    for sgn, col, dz in ((1, c1, 1), (-1, c2, -1)):
        y = cy + sgn * (R * np.cos(th) + split); zz = dz * np.sin(th)
        pts = np.stack([xs, y], 1); segs = np.stack([pts[:-1], pts[1:]], 1)
        ax.add_collection(LineCollection(segs, colors=[to_rgba(col, (0.5 + 0.5 * v) * al) for v in zz[:-1]], linewidths=lw + 3 * zz[:-1], capstyle="round", zorder=z))
        ax.add_collection(LineCollection(segs, colors=[to_rgba(col, 0.07 * al)] * len(segs), linewidths=lw * 3.5, zorder=z - 1))
    for k, x in enumerate(np.linspace(x0 + 12, x1 - 12, rungs)):
        th_ = (x - x0) / (x1 - x0) * 2 * np.pi * turns + t * 2.0
        ax.plot([x, x], [cy + R * np.cos(th_) + split, cy - R * np.cos(th_) - split], color="ATGC"[k % 4] and BCOL["ATGC"[k % 4]], lw=4, alpha=0.4 * al * (1 - min(1, split / 40)), zorder=z - 0.5)

_FP = FontProperties(family="Inter", weight="semibold"); _WC = {}
def wpx(w, size):
    k = (w, size)
    if k not in _WC: _WC[k] = TextPath((0, 0), w, size=size, prop=_FP).get_extents().width * 100 / 72
    return _WC[k]

yy, xx = np.mgrid[0:H:8, 0:W:8]
BGCMAP = LSC.from_list("g", [BG, "#11305C"])
_r = np.random.default_rng(2)
PP = _r.uniform([0, 0], [W, H], (70, 2)); PV = _r.normal(0, 1, (70, 2)) * [5, 9]; PS = _r.uniform(3, 22, 70)

class Video:
    def __init__(self, name, tag, tagcol, scenes, heads, gap=0.45, start=0.7, outro=2.8):
        """scenes: list of (func, i0, i1); heads: list of (i0, i1, small, big)"""
        J = json.load(open("tts.json"))[name]
        self.name, self.tag, self.tagcol = name, tag, tagcol
        self.D, self.L, self.SR = J["durs"], J["lines"], J["sr"]
        self.T = []; t = start
        for d in self.D: self.T.append(t); t += d + gap
        self.END = self.T[-1] + self.D[-1] + outro
        self.N = int(self.END * FPS); self.scenes = scenes; self.heads = heads

    def tw(self, i0, i1):
        a = self.T[i0] - 0.35
        b = (self.T[i1 + 1] - 0.1) if i1 + 1 < len(self.T) else self.END - 1.2
        return a, b

    def frame(self, f):
        t = f / FPS
        fig = plt.figure(figsize=(W / 100, H / 100), dpi=100); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
        fig.patch.set_facecolor(BG)
        gx = 540 + 180 * np.sin(t * 0.25); gy = 1100 + 160 * np.cos(t * 0.2)
        ax.imshow(np.clip(1 - np.hypot(xx - gx, yy - gy) / 1000, 0, 1) ** 2, extent=[0, W, 0, H], origin="lower", cmap=BGCMAP, aspect="auto", zorder=-5)
        p = (PP + PV * t) % [W, H]
        ax.scatter(p[:, 0], p[:, 1], s=PS, c=TEAL, alpha=0.16, linewidths=0, zorder=-3)
        for (fn, i0, i1) in self.scenes:
            a, b = self.tw(i0, i1)
            al = win(t, a, b, 0.45)
            if al > 0: fn(ax, t, t - self.T[i0], al, self)
        for (i0, i1, s1, s2) in self.heads:
            a, b = self.tw(i0, i1); al = win(t, a, b, 0.45)
            if al > 0:
                dy = (1 - eout(seg(t, a, a + 0.6))) * 30
                tx(ax, W / 2, 1650 - dy, s1, 24, GOLD, al)
                big = s2.split("\n")
                for k, s in enumerate(big): tx(ax, W / 2, 1580 - dy - k * 72, s, 50, WHITE, al)
        # top bar
        tw_ = len(self.tag) * 14 + 60
        pill(ax, 60 + tw_ / 2, 1820, tw_, 56, self.tagcol, 0.95, z=30)
        tx(ax, 60 + tw_ / 2, 1820, self.tag, 18, BG, 1, z=31)
        tx(ax, 1020, 1820, "Bioinformatics for Pakistan", 17, MUTED, 0.9, w="semibold", ha="right", z=31)
        # subtitles
        for i, (a_, d) in enumerate(zip(self.T, self.D)):
            al = win(t, a_ - 0.15, a_ + d + 0.3, 0.25)
            if al <= 0: continue
            prog = seg(t, a_, a_ + d) * len(self.L[i])
            lines = textwrap.wrap(self.L[i], 34); acc = 0
            for li, ln in enumerate(lines):
                y = 520 + ((len(lines) - 1) / 2 - li) * 54
                ws = ln.split(); sz = 31; sp = sz * 100 / 72 * 0.30
                tot = sum(wpx(w, sz) for w in ws) + sp * (len(ws) - 1); x = W / 2 - tot / 2
                for w in ws:
                    done = acc + len(w) <= prog + 2
                    tx(ax, x, y, w, sz, WHITE if done else "#5E7391", al, w="semibold", ha="left", z=50)
                    x += wpx(w, sz) + sp; acc += len(w) + 1
        # outro
        o = ease(seg(t, self.END - 2.3, self.END - 1.7))
        if o > 0:
            ax.add_patch(Rectangle((0, 0), W, H, fc=BG, alpha=0.88 * o, zorder=70))
            helix(ax, t, 1150, 300, 780, 55, o, turns=1.6, lw=8, rungs=14, z=71)
            tx(ax, W / 2, 980, "BIOINFORMATICS", 62, WHITE, o, z=72)
            tx(ax, W / 2, 900, "FOR PAKISTAN", 62, TEAL, o, z=72)
            b = pop(t, self.END - 1.5)
            if b > 0:
                pill(ax, W / 2, 740, 520 * b, 92 * b, GOLD, o, z=72)
                tx(ax, W / 2, 740, "Follow for more", 30 * b, BG, o, z=73)
            tx(ax, W / 2, 620, "Save  ·  Share  ·  Join our LinkedIn group", 22, MUTED, o * ease(seg(t, self.END - 1.2, self.END - 0.8)), w="normal", z=72)
        ax.add_patch(Rectangle((0, 0), W * t / self.END, 8, fc=self.tagcol, alpha=0.9, zorder=80))
        fig.canvas.draw(); buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy(); plt.close(fig); return buf

    def audio(self, seed=0):
        SR = self.SR; n = int(self.END * SR); tt = np.arange(n) / SR; voice = np.zeros(n)
        for i, s in enumerate(self.T):
            a, _ = sf.read(f"{self.name}/l{i}.wav"); a = a if a.ndim == 1 else a.mean(1); k = int(s * SR); voice[k:k + len(a)] += a[:n - k]
        voice = voice / np.abs(voice).max() * 0.9
        note = lambda m: 440 * 2 ** ((m - 69) / 12)
        progs = [[[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]], [[50, 57, 62, 65], [46, 53, 58, 62], [41, 48, 53, 57], [48, 55, 60, 64]],
                 [[52, 59, 64, 67], [48, 55, 60, 64], [43, 50, 55, 59], [50, 57, 62, 66]]]
        ch = progs[seed % 3]; bar = 4.0; pad = np.zeros(n); arp = np.zeros(n); bass = np.zeros(n)
        for b in range(int(self.END / bar) + 1):
            c = ch[b % 4]; s0 = int(b * bar * SR); s1 = min(n, int((b + 1) * bar * SR) + int(0.6 * SR))
            if s0 >= n: break
            sg = tt[s0:s1] - b * bar; env = np.minimum(1, sg / 0.9) * np.clip((bar + 0.6 - sg) / 1.2, 0, 1)
            for m in c:
                for det in (-0.1, 0.1): pad[s0:s1] += env * np.sin(2 * np.pi * note(m) * (1 + det / 100) * sg)
            bass[s0:s1] += env * np.sin(2 * np.pi * note(c[0] - 12) * sg)
            for j in range(16):
                m = c[[0, 1, 2, len(c) - 1, 2, 1, 0, 1][j % 8]] + 12; st = s0 + int(j * 0.25 * SR)
                if st >= n: break
                e = min(n, st + int(0.8 * SR)); q = np.arange(e - st) / SR
                arp[st:e] += np.exp(-q * 5.5) * np.sin(2 * np.pi * note(m) * q) * (0.6 if j % 4 == 0 else 0.33)
            if b % 1 == 0:   # soft kick pulse
                for j in range(4):
                    st = s0 + int(j * 1.0 * SR); e = min(n, st + int(0.25 * SR)); q = np.arange(max(0, e - st)) / SR
                    bass[st:e] += 1.4 * np.exp(-q * 18) * np.sin(2 * np.pi * (55 + 60 * np.exp(-q * 30)) * q)
        pad = np.convolve(pad, np.ones(60) / 60, "same")
        music = pad / np.abs(pad).max() * 0.42 + arp / np.abs(arp).max() * 0.32 + bass / np.abs(bass).max() * 0.4
        rng = np.random.default_rng(seed)
        for (fn, i0, i1) in self.scenes[1:]:
            st = int(max(0, self.T[i0] - 0.75) * SR); L = int(0.7 * SR)
            if st + L >= n: continue
            nz = np.convolve(rng.normal(0, 1, L), np.ones(20) / 20, "same"); music[st:st + L] += nz * np.sin(np.linspace(0, np.pi, L)) ** 2 * 1.8
        env = np.convolve(np.abs(voice), np.ones(int(0.3 * SR)) / int(0.3 * SR), "same")
        duck = 1 - 0.6 * np.clip(env / 0.05, 0, 1)
        fade = np.minimum(1, tt / 1.5) * np.minimum(1, (self.END - tt) / 2.0)
        music *= 0.21 * duck * fade
        mix = voice + music; mix /= max(1, np.abs(mix).max() / 0.95)
        sf.write(f"{self.name}/mix.wav", np.stack([mix, mix], 1), SR)

    def main(self, argv, seed=0):
        if argv[1] == "test":
            import matplotlib.image as mpimg
            ts = [float(x) for x in argv[2:]] or [self.T[i] + self.D[i] * 0.7 for i in range(len(self.T))] + [self.END - 0.5]
            for s in ts: mpimg.imsave(f"{self.name}/t_{s:05.1f}.png", self.frame(int(s * FPS)))
        elif argv[1] == "render":
            k, nparts = int(argv[2]), int(argv[3]); q = (self.N + nparts - 1) // nparts; a, b = k * q, min(self.N, (k + 1) * q)
            out = f"{self.name}/part{k}.mp4"
            p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                  "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "veryfast", out], stdin=subprocess.PIPE)
            for f in range(a, b): p.stdin.write(self.frame(f).tobytes())
            p.stdin.close(); p.wait(); print("done", out, flush=True)
        elif argv[1] == "audio":
            self.audio(seed)
        elif argv[1] == "info":
            print(self.name, self.N, round(self.END, 1))
