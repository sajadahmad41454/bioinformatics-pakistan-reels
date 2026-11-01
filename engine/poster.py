"""Instagram poster (1080x1350, 4:5) for scholarship and science-news posts.

Usage from Python:
    from poster import poster
    poster(out="posters/x.png", kind="SCHOLARSHIP", title="Gates Cambridge\nScholarship 2027",
           subtitle="Fully funded Master's & PhD at the University of Cambridge, UK",
           bullets=["Full tuition fees", "..."], key_label="DEADLINE", key_value="8 Dec 2026 / 6 Jan 2027",
           key_note="depends on course", footer="Official link in caption")
Every fact on a poster must come from an official source checked the same day.
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
from matplotlib.colors import LinearSegmentedColormap as LSC, to_rgba
plt.rcParams["font.family"] = "Inter"

W, H = 1080, 1350
BG = "#050E1E"; WHITE = "#FFFFFF"; MUTED = "#94A8C4"; CARD = "#0C1D37"; LINE = "#1E3A5F"; TEAL = "#2DD4BF"
THEMES = {"SCHOLARSHIP": ("#FBBF24", "🎓"), "SCIENCE NEWS": ("#2DD4BF", "🔬"), "OPPORTUNITY": ("#A78BFA", "✦")}

def _t(ax, x, y, s, size, col, w="bold", ha="center", va="center", al=1, z=5, fam=None, ls=1.15):
    kw = dict(color=col, fontsize=size, fontweight=w, ha=ha, va=va, alpha=al, zorder=z, linespacing=ls)
    if fam: kw["family"] = fam
    ax.text(x, y, s, **kw)

def poster(out, kind, title, subtitle, bullets, key_label, key_value, key_note="", footer="Official link in caption", source=""):
    acc = THEMES.get(kind, THEMES["OPPORTUNITY"])[0]
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100); ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    yy, xx = np.mgrid[0:H:6, 0:W:6]
    g = np.clip(1 - np.hypot(xx - 820, yy - 1150) / 1100, 0, 1) ** 2
    ax.imshow(g, extent=[0, W, 0, H], origin="lower", cmap=LSC.from_list("g", [BG, "#13325F"]), aspect="auto", zorder=0)
    r = np.random.default_rng(len(title))
    P = r.uniform([0, 0], [W, H], (60, 2)); ax.scatter(P[:, 0], P[:, 1], s=r.uniform(3, 18, 60), c=acc, alpha=0.12, lw=0, zorder=1)
    # header
    tw = len(kind) * 15 + 70
    ax.add_patch(FancyBboxPatch((70, 1235), tw, 56, boxstyle="round,pad=0,rounding_size=28", fc=acc, ec="none", zorder=3))
    _t(ax, 70 + tw / 2, 1263, kind, 20, BG)
    _t(ax, 1010, 1263, "Bioinformatics for Pakistan", 19, MUTED, w="semibold", ha="right")
    # title
    nl = title.count("\n") + 1
    _t(ax, 70, 1150, title, 58 if nl <= 2 else 50, WHITE, ha="left", va="top", ls=1.08)
    ty = 1150 - nl * (90 if nl <= 2 else 78) - 28
    ax.plot([70, 190], [ty, ty], color=acc, lw=6, solid_capstyle="round", zorder=3)
    import textwrap
    sub = textwrap.fill(subtitle, 52)
    _t(ax, 70, ty - 30, sub, 25, MUTED, w="normal", ha="left", va="top", ls=1.3)
    sy = ty - 34 - (sub.count("\n") + 1) * 47 - 40
    # bullets card
    n = len(bullets); ch = 70 + n * 62
    ax.add_patch(FancyBboxPatch((70, sy - ch), 940, ch, boxstyle="round,pad=0,rounding_size=26", fc=to_rgba(CARD, 0.92), ec=LINE, lw=2, zorder=3))
    for k, b in enumerate(bullets):
        y = sy - 55 - k * 62
        ax.add_patch(Circle((112, y), 9, fc=acc, zorder=4))
        _t(ax, 140, y, b, 25, WHITE, w="semibold", ha="left")
    # key fact (deadline / date)
    ky = sy - ch - 40
    ax.add_patch(FancyBboxPatch((70, ky - 150), 940, 150, boxstyle="round,pad=0,rounding_size=26", fc=to_rgba(acc, 0.14), ec=acc, lw=3, zorder=3))
    _t(ax, 110, ky - 45, key_label, 19, acc, ha="left")
    _t(ax, 110, ky - 98, key_value, 36, WHITE, ha="left")
    if key_note: _t(ax, 970, ky - 98, key_note, 19, MUTED, w="normal", ha="right")
    # footer
    _t(ax, 540, 120, footer, 24, acc, w="semibold")
    _t(ax, 540, 75, "@bioinformatics_pakistan", 20, MUTED, w="semibold")
    if source: _t(ax, 540, 40, source, 14, "#5E7391", w="normal")
    fig.savefig(out, dpi=100, facecolor=BG); plt.close(fig)
