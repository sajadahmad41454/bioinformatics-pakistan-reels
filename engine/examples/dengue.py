import sys as _s, os as _o; _s.path.insert(0, _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), ".."))
from eng import *
import eng

# ---------- own theme: night indigo background, fuchsia accent, cyan water ----------
eng.BG = "#0A0820"; eng.BGCMAP = LSC.from_list("g", [eng.BG, "#2B1A5E"]); eng.TEAL = "#E879F9"; eng.MUTED = "#B8B0D8"
BG = eng.BG; MUTED = eng.MUTED
FU = "#E879F9"; FUL = "#F5D0FE"; CY = "#22D3EE"; CYL = "#A5F3FC"; CARDC = "#17123A"; LN = "#3B2F78"; OKC = "#4ADE80"; RED = "#F87171"; SUN = "#FBBF24"
SERO = [("DENV-1", "#38BDF8"), ("DENV-2", "#F472B6"), ("DENV-3", "#FBBF24"), ("DENV-4", "#4ADE80")]
BODY = "#2A2540"

def lbl(ax, x, y, s, al, col=WHITE, size=24, z=14, ec=FU, w=None):
    if al <= 0.01: return
    w = w or (wpx(s, size) * 1.08 + 64)
    pill(ax, x, y, w, size * 2.4, CARDC, al, ec=ec, lw=2, z=z)
    tx(ax, x, y, s, size, col, al, z=z + 1)

def cross(ax, x, y, s, al, z=15):
    for sg in (1, -1): ax.plot([x - s, x + s], [y - s * sg, y + s * sg], color=RED, lw=9, alpha=al, solid_capstyle="round", zorder=z)

def check(ax, x, y, s, al, col=OKC, z=15):
    ax.plot([x - s, x - 0.3 * s, x + s], [y, y - 0.7 * s, y + 0.8 * s], color=col, lw=9, alpha=al, solid_capstyle="round", zorder=z)

def virus(ax, x, y, r, al, col=FU, t=0, z=12):
    """flavivirus-like particle: smooth sphere with a tiled (icosahedral-ish) surface"""
    al = min(al, 1)
    if al <= 0.01 or r <= 1: return
    ax.add_patch(Circle((x, y), r * 1.35, fc=to_rgba(col, 0.10 * al), ec="none", zorder=z))
    ax.add_patch(Circle((x, y), r, fc=to_rgba(col, 0.30 * al), ec=to_rgba(col, al), lw=max(1.5, r / 12), zorder=z + 0.1))
    for k in range(6):
        a = k * np.pi / 3 + t * 0.3
        ax.add_patch(Circle((x + r * 0.58 * np.cos(a), y + r * 0.58 * np.sin(a)), r * 0.22, fc=to_rgba(col, 0.55 * al), ec=to_rgba(WHITE, 0.35 * al), lw=1, zorder=z + 0.2))
    ax.add_patch(Circle((x, y), r * 0.24, fc=to_rgba(col, 0.75 * al), ec=to_rgba(WHITE, 0.4 * al), lw=1, zorder=z + 0.2))

def banded(ax, P, al, lw, z, n=10):
    P = np.asarray(P, float)
    for k in range(len(P) - 1):
        a, b = P[k], P[k + 1]
        for j in range(n):
            u0, u1 = j / n, (j + 1) / n
            c = WHITE if j % 3 == 1 else "#4B4566"
            ax.plot([a[0] + (b[0] - a[0]) * u0, a[0] + (b[0] - a[0]) * u1], [a[1] + (b[1] - a[1]) * u0, a[1] + (b[1] - a[1]) * u1], color=c, lw=lw, alpha=al, zorder=z, solid_capstyle="butt")

def mosquito(ax, x, y, s, al, t=0, z=10, flap=True):
    """side-view Aedes-style mosquito facing left: dark body with white bands and banded legs"""
    al = min(al, 1)
    if al <= 0.01: return
    T = lambda px, py: (x + px * s, y + py * s)
    # wings (flapping)
    fl = 0.5 + 0.5 * np.sin(t * 40) if flap else 0.6
    for k, ang in enumerate((25 + 30 * fl, 10 + 20 * fl)):
        ax.add_patch(Ellipse(T(40, 40), 230 * s, 52 * s, angle=ang, fc=to_rgba(CYL, (0.14 if k else 0.20) * al), ec=to_rgba(CYL, 0.5 * al), lw=1.5, zorder=z + (0.5 if k else -0.5)))
    # legs (three pairs)
    for k, (bx, kx, ky, fx, fy) in enumerate([(-20, -90, -60, -150, -170), (10, 20, -80, 0, -190), (40, 140, -50, 230, -160)]):
        banded(ax, [T(bx, -10), T(kx, ky), T(fx, fy)], al, max(1.5, 4 * s), z - 0.3)
    # abdomen with white bands
    ax.add_patch(Ellipse(T(150, -5), 200 * s, 52 * s, angle=-12, fc=to_rgba(BODY, al), ec=to_rgba(MUTED, 0.8 * al), lw=2, zorder=z))
    for k in range(5):
        cx_, cy_ = T(85 + k * 32, 9 - k * 6.8)
        ax.add_patch(Ellipse((cx_, cy_), 9 * s, 44 * s, angle=-12, fc=to_rgba(WHITE, 0.85 * al), ec="none", zorder=z + 0.1))
    # thorax with lyre marking
    ax.add_patch(Ellipse(T(10, 5), 100 * s, 78 * s, fc=to_rgba(BODY, al), ec=to_rgba(MUTED, 0.8 * al), lw=2, zorder=z + 0.2))
    ax.plot(*zip(T(-5, 30), T(-12, 5), T(-2, -18)), color=WHITE, lw=max(1, 3 * s), alpha=al, zorder=z + 0.3)
    ax.plot(*zip(T(22, 30), T(28, 5), T(18, -18)), color=WHITE, lw=max(1, 3 * s), alpha=al, zorder=z + 0.3)
    # head, eye, proboscis, antennae
    ax.add_patch(Circle(T(-55, 0), 26 * s, fc=to_rgba(BODY, al), ec=to_rgba(MUTED, 0.8 * al), lw=2, zorder=z + 0.2))
    ax.add_patch(Circle(T(-60, 6), 13 * s, fc=to_rgba("#6D28D9", al), zorder=z + 0.3))
    ax.plot(*zip(T(-78, -6), T(-185, -60)), color=MUTED, lw=max(1, 4 * s), alpha=al, zorder=z + 0.1, solid_capstyle="round")
    for d in (1, -1):
        ax.plot(*zip(T(-70, 14), T(-125, 30 + 20 * d)), color=MUTED, lw=max(1, 2 * s), alpha=al * 0.8, zorder=z + 0.1)

def person(ax, x, y, s, col, al, z=10):
    al = min(al, 1)
    if al <= 0.01: return
    ax.add_patch(Circle((x, y + 40 * s), 24 * s, fc=to_rgba(col, 0.35 * al), ec=col, lw=3, alpha=al, zorder=z))
    ax.add_patch(FancyBboxPatch((x - 36 * s, y - 45 * s), 72 * s, 62 * s, boxstyle=f"round,pad=0,rounding_size={26*s}", fc=to_rgba(col, 0.35 * al), ec=col, lw=3, alpha=al, zorder=z))

def thermo(ax, x, y, s, al, lev, z=10):
    al = min(al, 1)
    if al <= 0.01: return
    ax.add_patch(FancyBboxPatch((x - 22 * s, y - 60 * s), 44 * s, 220 * s, boxstyle=f"round,pad=0,rounding_size={22*s}", fc=to_rgba(WHITE, 0.08 * al), ec=to_rgba(WHITE, 0.85 * al), lw=3, zorder=z))
    ax.add_patch(Circle((x, y - 80 * s), 40 * s, fc=to_rgba(RED, al), ec=to_rgba(WHITE, 0.85 * al), lw=3, zorder=z + 0.1))
    hh = 200 * s * lev
    if hh > 2: ax.add_patch(Rectangle((x - 11 * s, y - 70 * s), 22 * s, hh, fc=to_rgba(RED, al), zorder=z + 0.2))

# ---------------- scenes ----------------
def s0(ax, t, lt, a, v):
    q = pop(lt, 0.1)
    mosquito(ax, 560 + 12 * np.sin(t * 1.3), 1120 + 18 * np.sin(t * 2.1), 1.9 * q, a * min(1, q * 2), t)
    for k in range(5):
        p = ease(seg(lt, 1.2 + k * 0.25, 1.8 + k * 0.25))
        an = k * 1.26 + t * 0.4
        virus(ax, 540 + 400 * np.cos(an), 1100 + 300 * np.sin(an), 30 * p, a * p, t=t)
    tx(ax, 540, 690, "dengue virus  ·  carried by mosquitoes", 24, MUTED, a * ease(seg(lt, 2.6, 3.2)), w="semibold")

def s1(ax, t, lt, a, v):
    q = pop(lt, 0.1)
    mosquito(ax, 600, 1220, 1.5 * q, a * min(1, q * 2), t)
    # skin at bottom-left
    p = ease(seg(lt, 0.8, 1.4))
    if p > 0:
        ax.add_patch(FancyBboxPatch((60, 860), 520, 120, boxstyle="round,pad=0,rounding_size=40", fc=to_rgba("#C08457", 0.55 * a * p), ec=to_rgba("#E9B98A", a * p), lw=3, zorder=8))
        tx(ax, 320, 920, "skin", 22, WHITE, a * p, w="semibold", z=9)
    d = ease(seg(lt, 1.6, 3.0))
    for k in range(3):
        u = (d + k * 0.18) % 1 if d >= 1 else max(0, d - k * 0.15)
        if u <= 0: continue
        x0, y0 = 600 - 185 * 1.5, 1220 - 60 * 1.5
        virus(ax, x0 + (300 - x0) * u, y0 + (950 - y0) * u, 16, a * min(1, u * 4) * (1 - 0.6 * (u > 0.98)), t=t, z=13)
    lbl(ax, 760, 1450, "Aedes aegypti (female)", a * ease(seg(lt, 2.4, 3.0)), FUL, 24)

def s2(ax, t, lt, a, v):
    q = pop(lt, 0.1)
    if q > 0:
        r = 70 * q
        ax.add_patch(Circle((540, 1340), r, fc=to_rgba(SUN, 0.9 * a), zorder=10))
        for k in range(12):
            an = k * np.pi / 6 + t * 0.3
            ax.plot([540 + r * 1.3 * np.cos(an), 540 + r * 1.7 * np.cos(an)], [1340 + r * 1.3 * np.sin(an), 1340 + r * 1.7 * np.sin(an)], color=SUN, lw=6, alpha=a, solid_capstyle="round", zorder=10)
        tx(ax, 540, 1180, "daytime biters", 30, SUN, a * ease(seg(lt, 0.5, 1.0)), z=11)
    for k, (x, lab, st) in enumerate([(300, "indoors", 1.4), (780, "outdoors", 2.1)]):
        p = ease(seg(lt, st, st + 0.5))
        if p <= 0: continue
        card(ax, x - 200, 760, 400, 340, a * p, ec=LN, fc=CARDC, z=8)
        if k == 0:  # house
            ax.add_patch(Polygon([(x - 110, 930), (x, 1030), (x + 110, 930)], closed=True, fc="none", ec=to_rgba(WHITE, a * p), lw=4, zorder=9))
            ax.add_patch(Rectangle((x - 85, 830), 170, 100, fc="none", ec=to_rgba(WHITE, a * p), lw=4, zorder=9))
            ax.add_patch(Rectangle((x - 22, 830), 44, 60, fc=to_rgba(WHITE, 0.3 * a * p), ec="none", zorder=9))
        else:       # tree
            ax.add_patch(Rectangle((x - 12, 830), 24, 80, fc=to_rgba("#A16207", a * p), zorder=9))
            ax.add_patch(Circle((x, 960), 75, fc=to_rgba(OKC, 0.45 * a * p), ec=to_rgba(OKC, a * p), lw=3, zorder=9))
        mosquito(ax, x + 70 + 15 * np.sin(t * 2 + k), 990 + 10 * np.cos(t * 3 + k), 0.38, a * p, t, z=11)
        tx(ax, x, 795, lab, 24, WHITE, a * p, w="semibold", z=11)

def container(ax, x, y, w, h, al, kind, t, z=9):
    al = min(al, 1)
    if al <= 0.01: return
    if kind == "tyre":
        ax.add_patch(Ellipse((x, y), w, h, fc=to_rgba("#27272A", al), ec=to_rgba("#71717A", al), lw=4, zorder=z))
        ax.add_patch(Ellipse((x, y + 4), w * 0.55, h * 0.45, fc=to_rgba(CY, 0.55 * al), ec=to_rgba(CYL, al), lw=2, zorder=z + 0.1))
        return
    if kind == "bucket":
        P = [(x - w / 2, y + h / 2), (x + w / 2, y + h / 2), (x + w * 0.38, y - h / 2), (x - w * 0.38, y - h / 2)]
    else:  # pot
        P = [(x - w * 0.42, y + h / 2), (x + w * 0.42, y + h / 2), (x + w * 0.5, y + h * 0.1), (x + w * 0.3, y - h / 2), (x - w * 0.3, y - h / 2), (x - w * 0.5, y + h * 0.1)]
    ax.add_patch(Polygon(P, closed=True, fc=to_rgba("#475569" if kind == "bucket" else "#B45309", 0.8 * al), ec=to_rgba(WHITE, 0.7 * al), lw=3, zorder=z))
    ax.add_patch(Ellipse((x, y + h / 2), w * (1 if kind == "bucket" else 0.84), 34, fc=to_rgba(CY, 0.65 * al), ec=to_rgba(CYL, al), lw=2, zorder=z + 0.1))

def s3(ax, t, lt, a, v):
    items = [(230, "bucket", 0.1), (540, "tyre", 0.5), (850, "pot", 0.9)]
    for k, (x, kind, st) in enumerate(items):
        q = pop(lt, st)
        if q <= 0: continue
        container(ax, x, 1050, 220 * q, (200 if kind != "tyre" else 170) * q, a, kind, t)
        # ripples + eggs at surface
        ty_ = 1050 + (100 if kind != "tyre" else 4) * q
        for m in range(3):
            ph = (t * 0.6 + m / 3) % 1
            ax.add_patch(Ellipse((x, ty_), 40 + 120 * ph, 8 + 18 * ph, fc="none", ec=to_rgba(CYL, a * (1 - ph) * 0.7), lw=2, zorder=10))
        for m in range(5):
            ax.add_patch(Ellipse((x - 40 + m * 20, ty_ + 2), 10, 5, fc=to_rgba("#18181B", a), ec=to_rgba(WHITE, 0.5 * a), lw=1, zorder=10.5))
    lbl(ax, 540, 1330, "eggs laid in stagnant water", a * ease(seg(lt, 1.5, 2.1)), CYL, 26, ec=CY)

def s4(ax, t, lt, a, v):
    for k in range(7):
        q = pop(lt, 0.1 + k * 0.1)
        if q <= 0: continue
        person(ax, 150 + k * 130, 1100 + 8 * np.sin(t * 2 + k), 1.15 * q, OKC, a)
    lbl(ax, 540, 880, "most infections: mild or no symptoms", a * ease(seg(lt, 0.9, 1.5)), WHITE, 26, ec=OKC)

def s5(ax, t, lt, a, v):
    x0, x1, y = 120, 960, 1340
    p = ease(seg(lt, 0.1, 1.4))
    ax.plot([x0, x0 + (x1 - x0) * p], [y, y], color=MUTED, lw=4, alpha=a, zorder=9, solid_capstyle="round")
    for d in range(0, 11):
        xx_ = x0 + (x1 - x0) * d / 10
        if (xx_ - x0) / (x1 - x0) > p: break
        ax.plot([xx_, xx_], [y - 12, y + 12], color=MUTED, lw=2, alpha=a, zorder=9)
        if d in (0, 4, 7, 10): tx(ax, xx_, y - 40, f"day {d}", 18, MUTED, a, w="normal")
    b = ease(seg(lt, 1.2, 1.8))
    if b > 0:
        xa, xb = x0 + (x1 - x0) * 0.4, x0 + (x1 - x0) * 0.7
        ax.add_patch(FancyBboxPatch((xa, y - 18), (xb - xa) * b, 36, boxstyle="round,pad=0,rounding_size=18", fc=to_rgba(FU, 0.8 * a), ec="none", zorder=10))
        tx(ax, (xa + xb) / 2, y + 50, "symptoms usually start", 20, FUL, a * b, w="semibold")
        tx(ax, x0, y + 50, "bite", 20, WHITE, a * b, w="semibold")
    thermo(ax, 190, 1000, 1.0, a * pop(lt, 2.0), 0.85 * ease(seg(lt, 2.2, 3.5)) + 0.1)
    for k, (s, st) in enumerate([("sudden high fever", 2.6), ("headache", 4.0), ("muscle & joint pain", 4.9)]):
        q = ease(seg(lt, st, st + 0.5))
        if q <= 0: continue
        yy_ = 1110 - k * 110; xo = (1 - q) * 60
        pill(ax, 610 + xo, yy_, 560, 84, CARDC, a * q, ec=FU, lw=2, z=10)
        tx(ax, 610 + xo, yy_, s, 28, WHITE, a * q, z=11)

def s6(ax, t, lt, a, v):
    for k, (name, col) in enumerate(SERO):
        q = pop(lt, 0.1 + k * 0.35)
        if q <= 0: continue
        x = 180 + k * 240; y = 1110 + 14 * np.sin(t * 1.5 + k)
        virus(ax, x, y, 78 * q, a, col=col, t=t)
        tx(ax, x, 930, name, 26, col, a, z=13)
    tx(ax, 540, 800, "4 serotypes", 34, WHITE, a * ease(seg(lt, 1.8, 2.4)))

def shield(ax, x, y, s, col, al, z=9):
    if al <= 0.01: return
    P = [(x, y + 110 * s), (x + 90 * s, y + 75 * s), (x + 80 * s, y - 40 * s), (x, y - 115 * s), (x - 80 * s, y - 40 * s), (x - 90 * s, y + 75 * s)]
    ax.add_patch(Polygon(P, closed=True, fc=to_rgba(col, 0.18 * al), ec=to_rgba(col, al), lw=4, zorder=z))

def s7(ax, t, lt, a, v):
    sh = ease(seg(lt, 0.5, 1.2))
    for k, (name, col) in enumerate(SERO):
        x = 180 + k * 240; y = 1110
        virus(ax, x, y, 60, a, col=col, t=t)
        tx(ax, x, 920, name, 22, col, a, z=13)
        if k == 1:
            shield(ax, x, y + 5, 1.2, OKC, a * sh, z=14)
            check(ax, x, 830, 26, a * ease(seg(lt, 1.2, 1.6)))
        else:
            c = ease(seg(lt, 2.4 + 0.25 * k, 2.8 + 0.25 * k))
            cross(ax, x, 830, 22, a * c)
    tx(ax, 540, 1320, "had DENV-2 → protected against DENV-2 only", 24, MUTED, a * ease(seg(lt, 1.4, 2.0)), w="semibold")

def s8(ax, t, lt, a, v):
    person(ax, 540, 1060, 2.2 * pop(lt, 0.1), FUL, a)
    for k, (name, col, st) in enumerate([("1st: DENV-2", SERO[1][1], 0.3), ("2nd: DENV-3", SERO[2][1], 1.2)]):
        q = ease(seg(lt, st, st + 0.5))
        if q <= 0: continue
        x = 220 if k == 0 else 860
        virus(ax, x, 1180, 48 * q, a, col=col, t=t)
        tx(ax, x, 1070, name, 22, col, a * q, z=13)
    w = ease(seg(lt, 2.3, 2.9))
    if w > 0:
        P = [(540, 905 + 70), (540 - 70, 905 - 50), (540 + 70, 905 - 50)]
        pill(ax, 540, 850, 820, 100, "#3A0F1E", a * w, ec=RED, lw=3, z=12)
        tx(ax, 540, 850, "greater risk of severe dengue", 32, RED, a * w, z=13)

def drip(ax, x, y, s, al, t, z=10):
    al = min(al, 1)
    if al <= 0.01: return
    ax.add_patch(FancyBboxPatch((x - 60 * s, y), 120 * s, 170 * s, boxstyle=f"round,pad=0,rounding_size={30*s}", fc=to_rgba(CY, 0.18 * al), ec=to_rgba(CYL, al), lw=3, zorder=z))
    ax.add_patch(FancyBboxPatch((x - 50 * s, y + 10 * s), 100 * s, 100 * s, boxstyle=f"round,pad=0,rounding_size={24*s}", fc=to_rgba(CY, 0.5 * al), ec="none", zorder=z + 0.1))
    ax.plot([x, x], [y, y - 80 * s], color=CYL, lw=3, alpha=al, zorder=z)
    ax.plot([x, x + 40 * s, x + 90 * s], [y - 80 * s, y - 160 * s, y - 180 * s], color=CYL, lw=3, alpha=al, zorder=z)
    ph = (t * 1.2) % 1
    ax.add_patch(Circle((x, y - 10 * s - 60 * s * ph), 7 * s, fc=to_rgba(CYL, al * (1 - ph)), zorder=z + 0.2))

def s9(ax, t, lt, a, v):
    q = pop(lt, 0.1)
    if q > 0:
        card(ax, 90, 1050, 420, 330, a, ec=LN, fc=CARDC, z=8)
        pill(ax, 300, 1250, 200 * q, 76 * q, "#DDD6FE", a, z=9)
        ax.plot([300, 300], [1250 - 38 * q, 1250 + 38 * q], color=BG, lw=3, alpha=a, zorder=9.5)
        cross(ax, 300, 1250, 70 * ease(seg(lt, 0.6, 1.0)) + 1, a * ease(seg(lt, 0.6, 1.0)), z=10)
        tx(ax, 300, 1080, "no specific antiviral", 23, WHITE, a, w="semibold", z=10)
    p = ease(seg(lt, 1.6, 2.2))
    if p > 0:
        card(ax, 570, 1050, 420, 330, a * p, ec=CY, fc=CARDC, z=8, lw=2.5)
        drip(ax, 780, 1215, 0.75, a * p, t)
        tx(ax, 780, 1080, "supportive care", 23, CYL, a * p, w="semibold", z=10)
    tx(ax, 540, 880, "treatment is guided by doctors", 24, MUTED, a * ease(seg(lt, 2.6, 3.2)), w="semibold")

def tube(ax, x, y, s, al, col, z=9):
    al = min(al, 1)
    if al <= 0.01: return
    ax.add_patch(FancyBboxPatch((x - 30 * s, y - 120 * s), 60 * s, 240 * s, boxstyle=f"round,pad=0,rounding_size={30*s}", fc=to_rgba(WHITE, 0.06 * al), ec=to_rgba(WHITE, 0.8 * al), lw=3, zorder=z))
    ax.add_patch(FancyBboxPatch((x - 22 * s, y - 112 * s), 44 * s, 120 * s, boxstyle=f"round,pad=0,rounding_size={20*s}", fc=to_rgba("#DC2626", 0.85 * al), ec="none", zorder=z + 0.1))
    ax.add_patch(Rectangle((x - 36 * s, y + 120 * s), 72 * s, 26 * s, fc=to_rgba(col, al), zorder=z + 0.2))

def s10(ax, t, lt, a, v):
    for k, (x, title, sub, col, st) in enumerate([(290, "NS1 antigen", "viral protein", FU, 0.1), (790, "RT-PCR", "viral RNA", CY, 1.8)]):
        q = ease(seg(lt, st, st + 0.6))
        if q <= 0: continue
        card(ax, x - 220, 800, 440, 600, a * q, ec=col, z=8, fc=CARDC, lw=2.5)
        tube(ax, x, 1150, 0.9, a * q, col)
        tx(ax, x, 950, title, 30, WHITE, a * q, z=10)
        tx(ax, x, 880, "detects " + sub, 22, col, a * q, z=10, w="semibold")

SEQ = "AGTTGTTAGTCTACGTGGACCGACAAAGACAGATTCTTTGAGGGAGCTAAGCTCAACGTAGTTCTAACAGTTT"
SCOL = {"A": "#E879F9", "T": "#22D3EE", "G": "#4ADE80", "C": "#FBBF24"}
def s11(ax, t, lt, a, v):
    card(ax, 60, 1250, 960, 150, a, ec=LN, z=8, fc=CARDC)
    sh = int(t * 6)
    for j in range(26):
        b = SEQ[(j + sh) % len(SEQ)]
        tx(ax, 110 + j * 33.5, 1325, b, 22, SCOL[b], a, fam=MONO, z=10)
    tx(ax, 540, 1222, "sequencing the viral genome", 18, MUTED, a, w="normal")
    p = ease(seg(lt, 1.2, 3.0))
    if p > 0:
        rx, ry = 540, 1170
        ax.plot([rx, rx], [ry, ry - 50 * p], color=MUTED, lw=3, alpha=a, zorder=9)
        xs = [180 + k * 240 for k in range(4)]
        ax.plot([rx - (rx - xs[0]) * p, rx + (xs[-1] - rx) * p], [ry - 50] * 2, color=MUTED, lw=3, alpha=a, zorder=9)
        for k, (name, col) in enumerate(SERO):
            q = pop(lt, 2.4 + k * 0.2)
            if q <= 0: continue
            ax.plot([xs[k], xs[k]], [ry - 50, 1030], color=col, lw=3, alpha=a, zorder=9)
            pill(ax, xs[k], 990, 190 * q, 70 * q, col, a, z=10)
            tx(ax, xs[k], 990, name, 22 * q, BG, a, z=11)
    lbl(ax, 540, 840, "identify serotypes · track outbreaks", a * ease(seg(lt, 4.4, 5.0)), WHITE, 25)

def s12(ax, t, lt, a, v):
    acts = [("empty stagnant water", CY, 0.1), ("use repellent", FU, 1.3), ("cover up by day", SUN, 2.3)]
    for k, (s, col, st) in enumerate(acts):
        q = ease(seg(lt, st, st + 0.5))
        if q <= 0: continue
        y = 1340 - k * 200; xo = (1 - q) * 80
        card(ax, 110 + xo, y - 80, 860, 160, a * q, ec=col, fc=CARDC, z=8, lw=2.5)
        ax.add_patch(Circle((210 + xo, y), 50, fc=to_rgba(col, 0.25 * a * q), ec=to_rgba(col, a * q), lw=3, zorder=9))
        check(ax, 210 + xo, y + 4, 24, a * q, col=col, z=10)
        tx(ax, 300 + xo, y, s, 32, WHITE, a * q, ha="left", z=10)

def s13(ax, t, lt, a, v):
    thermo(ax, 330, 1130, 1.2, a * pop(lt, 0.1), 0.9)
    p = ease(seg(lt, 0.6, 1.2))
    if p > 0:
        card(ax, 470, 1000, 500, 300, a * p, ec=FU, fc=CARDC, z=8, lw=2.5)
        # simple stethoscope-like medical cross
        ax.add_patch(Rectangle((720 - 22, 1170 - 70), 44, 140, fc=to_rgba(FU, a * p), zorder=9))
        ax.add_patch(Rectangle((720 - 70, 1170 - 22), 140, 44, fc=to_rgba(FU, a * p), zorder=9))
        tx(ax, 720, 1045, "see a doctor early", 28, WHITE, a * p, z=10)

def V():
    return Video("v_dengue", "DISEASE EXPLAINER", FU,
                 [(s0, 0, 0), (s1, 1, 1), (s2, 2, 2), (s3, 3, 3), (s4, 4, 4), (s5, 5, 5), (s6, 6, 6), (s7, 7, 7), (s8, 8, 8),
                  (s9, 9, 9), (s10, 10, 10), (s11, 11, 11), (s12, 12, 12), (s13, 13, 13)],
                 [(0, 0, "MOSQUITO-BORNE", "Dengue"), (1, 1, "THE CARRIER", "Aedes mosquito"), (2, 2, "WHEN IT BITES", "During the day"),
                  (3, 3, "WHERE IT BREEDS", "Stagnant water"), (4, 4, "AFTER INFECTION", "Often silent"), (5, 5, "SYMPTOMS", "4–7 days later"),
                  (6, 6, "THE VIRUS", "Four types"), (7, 7, "IMMUNITY", "Type-specific"), (8, 8, "WHY IT MATTERS", "Second infections"),
                  (9, 9, "TREATMENT", "Supportive care"), (10, 10, "DIAGNOSIS", "Lab tests"), (11, 11, "BIOINFORMATICS", "Reading the genome"),
                  (12, 12, "PROTECT YOURSELF", "Prevention"), (13, 13, "DON'T WAIT", "Get checked")],
                 gap=0.3, start=0.4, outro=2.6)

if __name__ == "__main__":
    V().main(sys.argv, seed=1)
