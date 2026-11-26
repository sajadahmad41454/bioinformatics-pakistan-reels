"""FUN / MEME Reel: drone flight over the 'power plant' in your cells -- rows of ATP synthase turbines
on the inner mitochondrial membrane (rotor spins with proton flow, ATP released from the F1 head).
Pseudo-3D renderer (same approach as meme_drone.py): ray-cast ground + depth-sorted sprites (numpy + PIL).
  python3 meme_atp.py test 1 5 9 14     -> PNG test frames
  python3 meme_atp.py render K N        -> part K of N (mp4, no audio)
  python3 meme_atp.py audio             -> music.wav
"""
import sys, os, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import soundfile as sf

W, H, FPS = 1080, 1920, 30
DUR = 16.0
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "meme_atp"
FB = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
FM = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
F = 980.0
CX, CY = W / 2, 1040
FOG = np.array([40, 18, 58], float)

def hexc(h): h = h.lstrip("#"); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float)
def ease(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
def seg(x, a, b): return float(np.clip((x - a) / (b - a), 0, 1))

# ---------------- camera ----------------
KEYS = [(0.0, (0, -2300, 1500), (0, -200, 0)),
        (4.5, (-650, -1500, 620), (-150, -420, 60)),
        (9.0, (250, -880, 260), (520, -330, 90)),
        (12.5, (600, -600, 230), (760, -180, 95)),
        (16.0, (760, -470, 250), (900, 60, 80))]
def crom(p0, p1, p2, p3, u):
    return 0.5 * (2 * p1 + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u ** 2 + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3)
def cam(t):
    ts = [k[0] for k in KEYS]; P = [np.array(k[1], float) for k in KEYS]; L = [np.array(k[2], float) for k in KEYS]
    i = max(0, min(len(ts) - 2, np.searchsorted(ts, t, side="right") - 1))
    u = ease((t - ts[i]) / (ts[i + 1] - ts[i])) * 0.5 + 0.5 * (t - ts[i]) / (ts[i + 1] - ts[i])
    g = lambda A, j: A[max(0, min(len(A) - 1, j))]
    pos = crom(g(P, i - 1), g(P, i), g(P, i + 1), g(P, i + 2), u)
    tgt = crom(g(L, i - 1), g(L, i), g(L, i + 1), g(L, i + 2), u)
    fw = tgt - pos; fw /= np.linalg.norm(fw)
    up = np.array([0, 0, 1.0]); rt = np.cross(fw, up); rt /= np.linalg.norm(rt)
    roll = 0.09 * np.sin(2 * np.pi * t / DUR * 1.3)
    cu = np.cross(rt, fw)
    rt, cu = rt * np.cos(roll) + cu * np.sin(roll), cu * np.cos(roll) - rt * np.sin(roll)
    return pos, fw, rt, cu

def proj(P, C):
    pos, fw, rt, cu = C
    d = np.asarray(P, float) - pos
    z = d @ fw; x = d @ rt; y = d @ cu
    return CX + F * x / np.maximum(z, 1e-3), CY - F * y / np.maximum(z, 1e-3), z

def fogk(z): return float(np.clip((z - 350) / 3000, 0, 0.88))

# ---------------- membrane (ray cast) ----------------
GW, GH = 270, 480
gy, gx = np.mgrid[0:GH, 0:GW].astype(float)
def ground(C):
    pos, fw, rt, cu = C
    sx = (gx + 0.5) * W / GW; sy = (gy + 0.5) * H / GH
    dx = (sx - CX) / F; dy = -(sy - CY) / F
    ray = fw[None, None, :] + dx[..., None] * rt + dy[..., None] * cu
    hit = ray[..., 2] < -1e-4
    tz = -pos[2] / np.where(hit, ray[..., 2], -1e-4)
    X = pos[0] + ray[..., 0] * tz; Y = pos[1] + ray[..., 1] * tz
    # lipid-head 'cobblestones' + soft undulation
    heads = (np.sin(X / 9.0) * np.sin(Y / 9.0 + 0.5 * np.sin(X / 31))) ** 2
    n = (np.sin(X / 53) * np.sin(Y / 47) + 0.6 * np.sin((X + Y) / 29)) / 1.6
    col = hexc("#C8552B") + n[..., None] * 20 + heads[..., None] * 34
    ridge = np.exp(-((((Y + 160) % 320) - 160) / 70) ** 2)[..., None]       # slightly brighter strips under the rows
    col = col + ridge * hexc("#3A1A0A") * 0.6
    dist = tz * np.linalg.norm(ray, axis=-1)
    # distant detail averages out
    col = np.where((dist > 2200)[..., None], hexc("#C8552B") + n[..., None] * 20 + 17, col)
    fk = np.clip((dist - 350) / 3000, 0, 0.88)[..., None]
    col = col * (1 - fk) + FOG * fk
    sky = hexc("#1A0B26") + (hexc("#3B1C4F") - hexc("#1A0B26")) * np.clip(1 - gy / GH * 2, 0, 1)[..., None]
    col = np.where(hit[..., None], col, sky)
    im = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8), "RGB").resize((W, H), Image.BICUBIC)
    return im.filter(ImageFilter.GaussianBlur(1.3)).convert("RGBA")

# ---------------- sprites ----------------
def sphere(r, col, spec=0.5):
    s = int(2 * r + 4); y, x = np.mgrid[0:s, 0:s].astype(float)
    nx, ny = (x - s / 2) / r, (y - s / 2) / r; r2 = nx ** 2 + ny ** 2
    nz = np.sqrt(np.clip(1 - r2, 0, 1)); m = np.clip((1 - np.sqrt(r2)) * r, 0, 1)
    lx, ly, lz = -0.4, -0.55, 0.73
    dif = np.clip(nx * lx + ny * ly + nz * lz, 0, 1)
    rgb = col[None, None, :] / 255 * (0.3 + 0.85 * dif)[..., None]
    sp = np.clip((nx * lx + ny * ly + nz * (lz + 1)) / np.sqrt(lx * lx + ly * ly + (lz + 1) ** 2), 0, 1) ** 35 * spec
    rgb = rgb + sp[..., None]
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 1) * 255, m * 255]).astype(np.uint8), "RGBA")
BASE = {"alpha": sphere(64, hexc("#F0ABFC"), 0.6), "beta": sphere(64, hexc("#8B5CF6"), 0.6),
        "ring": sphere(48, hexc("#22D3EE"), 0.8), "gam": sphere(40, hexc("#F43F5E"), 0.9),
        "cap": sphere(48, hexc("#E9D5FF"), 0.5), "hp": sphere(32, hexc("#FF6B6B"), 0.9),
        "atp": sphere(40, hexc("#FDE047"), 1.0)}
_SC = {}
def spr(key, d, fk):
    d = int(max(3, min(1400, d))); fb = round(fk * 10) / 10
    k = (key, d, fb)
    if k not in _SC:
        if len(_SC) > 5000: _SC.clear()
        im = BASE[key].resize((d, d), Image.BILINEAR)
        if fb > 0:
            a = np.asarray(im).astype(float)
            a[..., :3] = a[..., :3] * (1 - fb) + FOG * fb
            im = Image.fromarray(a.astype(np.uint8), "RGBA")
        _SC[k] = im
    return _SC[k]
_GC = {}
def glow(d, col):
    s = int(max(4, min(900, d))); k = (s, col)
    if k not in _GC:
        if len(_GC) > 800: _GC.clear()
        y, x = np.mgrid[0:s, 0:s].astype(float); r = np.hypot(x - s / 2, y - s / 2) / (s / 2)
        a = np.clip(1 - r, 0, 1) ** 2.2
        c = hexc(col)
        _GC[k] = Image.fromarray(np.dstack([np.full((s, s), c[0]), np.full((s, s), c[1]), np.full((s, s), c[2]), a * 170]).astype(np.uint8), "RGBA")
    return _GC[k]

# ---------------- world: dimer rows of ATP synthase ----------------
rng = np.random.default_rng(7)
TURB = []   # (x, y, phase, speed)
for ry in np.arange(-2080, 1300, 320):
    for rx in np.arange(-1700, 1800, 210):
        for side in (-1, 1):
            x = rx + rng.uniform(-14, 14); y = ry + side * 42 + rng.uniform(-6, 6)
            TURB.append((x, y, rng.uniform(0, 2 * np.pi), rng.uniform(0.9, 1.15) * (2 * np.pi * 1.4)))
TURB = np.array(TURB)
NR = 10        # c-subunits drawn in the ring (illustrative only; the number varies between species)
HEAD_Z = 98

def atp_pos(tb, t, j):
    """ATP released from the head: rises and drifts, period 1.6 s, 2 per turbine"""
    x, y, ph, w = tb
    u = ((t + ph * 0.25 + j * 0.8) / 1.6) % 1
    a = ph + j * 2.1
    P = np.array([x + np.cos(a) * (30 + 120 * u), y + np.sin(a) * (30 + 120 * u), HEAD_Z + 20 + 210 * u])
    return P, u
def hp_pos(tb, t, j):
    """proton leaving the rotor on the F1 side of the membrane, period 1.2 s, 3 per turbine"""
    x, y, ph, w = tb
    u = ((t + ph * 0.3 + j * 0.4) / 1.2) % 1
    a = ph * 2 + j * 2.09 + u * 1.2
    P = np.array([x + np.cos(a) * (34 + 70 * u), y + np.sin(a) * (34 + 70 * u), 8 + 36 * u])
    return P, u

def turbine_items(tb, t, C, items):
    x, y, ph, w = tb
    hx, hy, hz = proj([x, y, HEAD_Z], C)
    if hz < 40 or hz > 3600: return
    if not (-400 < hx < W + 400 and -400 < hy < H + 400): return
    big = F * 60 / hz
    if big < 7:
        items.append((hz, "spr", "beta", hx, hy, big)); return
    ang = ph + w * t
    # c-ring (rotor) in the membrane
    for k in range(NR):
        a = ang + 2 * np.pi * k / NR
        P = [x + 26 * np.cos(a), y + 26 * np.sin(a), 6]
        sx, sy, sz = proj(P, C)
        if sz > 30: items.append((sz, "spr", "ring", sx, sy, F * 18 / sz))
    # central stalk + off-centre marker (rotates with the ring)
    sx0, sy0, sz0 = proj([x, y, 10], C); sx1, sy1, sz1 = proj([x, y, HEAD_Z - 10], C)
    if sz0 > 30 and sz1 > 30:
        items.append(((sz0 + sz1) / 2 + 2, "line", (sx0, sy0, sx1, sy1), max(1, F * 11 / ((sz0 + sz1) / 2)), (236, 236, 245), 240))
    for zz in (34, 58):
        P = [x + 9 * np.cos(ang + 0.6), y + 9 * np.sin(ang + 0.6), zz]
        sx, sy, sz = proj(P, C)
        if sz > 30: items.append((sz, "spr", "gam", sx, sy, F * 14 / sz))
    # peripheral stalk (stator)
    a0 = ph * 0.7
    p0 = proj([x + 44 * np.cos(a0), y + 44 * np.sin(a0), 6], C); p1 = proj([x + 44 * np.cos(a0), y + 44 * np.sin(a0), HEAD_Z], C)
    p2 = proj([x + 18 * np.cos(a0), y + 18 * np.sin(a0), HEAD_Z + 28], C)
    if min(p0[2], p1[2], p2[2]) > 30:
        zz = (p0[2] + p1[2]) / 2
        items.append((zz, "line", (p0[0], p0[1], p1[0], p1[1]), max(1, F * 6 / zz), (180, 160, 200), 230))
        items.append((zz, "line", (p1[0], p1[1], p2[0], p2[1]), max(1, F * 6 / zz), (180, 160, 200), 230))
    # F1 head: 3 alpha + 3 beta, alternating, fixed (stator)
    for k in range(6):
        a = ph + np.pi * k / 3
        P = [x + 24 * np.cos(a), y + 24 * np.sin(a), HEAD_Z + (6 if k % 2 else 0)]
        sx, sy, sz = proj(P, C)
        if sz > 30: items.append((sz, "spr", "alpha" if k % 2 == 0 else "beta", sx, sy, F * 44 / sz))
    sx, sy, sz = proj([x, y, HEAD_Z + 26], C)
    if sz > 30: items.append((sz, "spr", "cap", sx, sy, F * 24 / sz))
    if hz < 1900:
        for j in range(3):
            P, u = hp_pos(tb, t, j); sx, sy, sz = proj(P, C)
            if sz > 220:
                r = 9 * np.sin(np.pi * u) ** 0.5
                items.append((sz, "glowspr", "hp", sx, sy, F * 2 * r / sz, "#FF5A5A"))
        for j in range(2):
            P, u = atp_pos(tb, t, j); sx, sy, sz = proj(P, C)
            if sz > 300:
                r = 13 * np.sin(np.pi * u) ** 0.4
                items.append((sz, "glowspr", "atp", sx, sy, F * 2 * r / sz, "#FFE66D"))

LABELS = [(1.3, 4.6, np.array([-260.0, -900.0, 0.0]), "Inner membrane · the power grid", "#FDBA74", None),
          (5.0, 8.6, None, "ATP synthase · the turbine", "#F0ABFC", "head"),
          (8.8, 12.1, None, "Protons (H+) · spin the rotor", "#67E8F9", "ring"),
          (12.2, 15.4, None, "ATP · the energy currency", "#FDE047", "atp")]

FT = ImageFont.truetype(FB, 58); FS = ImageFont.truetype(FM, 29); FL = ImageFont.truetype(FB, 30); FH = ImageFont.truetype(MONO, 26)
WM = Image.open(os.path.join(HERE, "watermark.png")).convert("RGBA"); WM = WM.resize((int(WM.width * 80 / WM.height), 80))

def anchor(tb, what):
    x, y = tb[0], tb[1]
    if what == "head": return [x, y, HEAD_Z + 30]
    if what == "ring": return [x + 26, y, 6]
    return [x, y, HEAD_Z + 95]             # just above the head, where ATP is released

_PIN = {}
def nearest(t, C, what, tm):
    """choose the turbine nearest the screen centre at the label's start time t0 (deterministic,
    so parallel render parts agree), then follow that turbine"""
    if what not in _PIN:
        C0 = cam(tm); best = None
        for i, tb in enumerate(TURB):
            sx, sy, sz = proj(anchor(tb, what), C0)
            if not (260 < sz < 1300) or not (240 < sx < 840 and 820 < sy < 1350): continue
            sc = abs(sx - CX) + abs(sy - 1150) * 0.7
            if best is None or sc < best[0]: best = (sc, i)
        _PIN[what] = None if best is None else best[1]
    i = _PIN[what]
    if i is None: return None
    return proj(anchor(TURB[i], what), C)

def frame(f):
    t = f / FPS
    C = cam(t)
    im = ground(C)
    items = []
    for tb in TURB: turbine_items(tb, t, C, items)
    items.sort(key=lambda it: -it[0])
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for it in items:
        z = it[0]; fk = fogk(z)
        if it[1] == "line":
            (x0, y0, x1, y1), w, col, al = it[2], it[3], it[4], it[5]
            if max(x0, x1) < -200 or min(x0, x1) > W + 200 or max(y0, y1) < -200 or min(y0, y1) > H + 200: continue
            c = tuple(int(v) for v in (np.array(col) * (1 - fk) + FOG * fk)) + (al,)
            d.line([x0, y0, x1, y1], fill=c, width=int(min(w, 140)))
            if w > 4:
                d.ellipse([x1 - w / 2, y1 - w / 2, x1 + w / 2, y1 + w / 2], fill=c)
                d.ellipse([x0 - w / 2, y0 - w / 2, x0 + w / 2, y0 + w / 2], fill=c)
        else:
            key, x, y, dd = it[2], it[3], it[4], it[5]
            if dd < 2 or x + dd < 0 or x - dd > W or y + dd < 0 or y - dd > H: continue
            if it[1] == "glowspr":
                g = glow(dd * 3.2, it[6]); lay.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
            s = spr(key, dd, fk); lay.alpha_composite(s, (int(x - s.width / 2), int(y - s.height / 2)))
    im.alpha_composite(lay)
    im = Image.alpha_composite(im, VIG)
    for (t0, t1, P, txt, col, what) in LABELS:
        a = ease(seg(t, t0, t0 + 0.35)) * (1 - ease(seg(t, t1 - 0.35, t1)))
        if a <= 0.01: continue
        if P is None:
            nc = nearest(t, C, what, (t0 + t1) / 2)
            if nc is None: continue
            x, y, z = nc
            a *= seg(y, 640, 760) * (1 - seg(y, 1380, 1480)) * seg(x, 60, 140) * (1 - seg(x, 940, 1020))
            if a <= 0.01: continue
        else:
            x, y, z = proj(P, C)
            if z < 50: continue
        pin(im, x, y, txt, col, a)
    hud(im, t)
    meme(im, t)
    return np.asarray(im.convert("RGB"))

def pin(im, x, y, txt, col, a):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    c = tuple(int(v) for v in hexc(col))
    tw = d.textlength(txt, font=FL); bw, bh = tw + 56, 64
    bx = np.clip(x - bw / 2, 30, W - 30 - bw); by = y - 160
    d.line([x, y - 10, x, by + bh], fill=c + (230,), width=4)
    d.ellipse([x - 11, y - 11, x + 11, y + 11], fill=c + (255,), outline=(255, 255, 255, 255), width=3)
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=32, fill=(22, 10, 30, 225), outline=c + (255,), width=3)
    d.text((bx + 28, by + 15), txt, font=FL, fill=(255, 255, 255, 255))
    if a < 1:
        arr = np.asarray(lay).copy(); arr[..., 3] = (arr[..., 3] * a).astype(np.uint8); lay = Image.fromarray(arr)
    im.alpha_composite(lay)

def make_vig():
    y, x = np.mgrid[0:H, 0:W].astype(float)
    r = np.hypot((x - W / 2) / W, (y - H / 2) / H)
    a = np.clip((r - 0.35) / 0.4, 0, 1) ** 1.5 * 170
    top = np.clip(1 - y / 720, 0, 1) ** 1.4 * 238
    bot = np.clip((y - 1530) / 170, 0, 1) ** 1.2 * 240
    al = np.clip(np.maximum(np.maximum(a, top), bot), 0, 255)
    return Image.fromarray(np.dstack([np.zeros((H, W, 3)), al]).astype(np.uint8), "RGBA")
VIG = make_vig()

def hud(im, t):
    d = ImageDraw.Draw(im)
    c = (255, 255, 255, 220); L = 70; m = 60; y0, y1 = 520, 1560
    for (x, y, sx, sy) in [(m, y0, 1, 1), (W - m, y0, -1, 1), (m, y1, 1, -1), (W - m, y1, -1, -1)]:
        d.line([x, y, x + sx * L, y], fill=c, width=5); d.line([x, y, x, y + sy * L], fill=c, width=5)
    cx, cy = W / 2, 1040
    d.line([cx - 34, cy, cx - 12, cy], fill=c, width=3); d.line([cx + 12, cy, cx + 34, cy], fill=c, width=3)
    d.line([cx, cy - 34, cx, cy - 12], fill=c, width=3); d.line([cx, cy + 12, cx, cy + 34], fill=c, width=3)
    if int(t * 2) % 2 == 0: d.ellipse([m + 6, y0 + 22, m + 30, y0 + 46], fill=(239, 68, 68, 255))
    d.text((m + 42, y0 + 18), "REC", font=FH, fill=c)
    d.text((W - m - 250, y0 + 18), "MITO-CAM 4K", font=FH, fill=c)
    ss = int(t); ff = int((t - ss) * FPS)
    d.text((m + 6, y1 - 50), f"00:00:{ss:02d}:{ff:02d}", font=FH, fill=c)
    # battery icon that charges up through the clip
    bx = W - m - 110; d.rectangle([bx, y1 - 46, bx + 90, y1 - 20], outline=c, width=3); d.rectangle([bx + 92, y1 - 39, bx + 98, y1 - 27], fill=c)
    lvl = 0.25 + 0.75 * ease(seg(t, 0.5, 14.5))
    d.rectangle([bx + 6, y1 - 40, bx + 6 + int(78 * lvl), y1 - 26], fill=(250, 204, 21, 235))

def meme(im, t):
    d = ImageDraw.Draw(im)
    if t < 8.6:
        a = ease(seg(t, 0.2, 0.6)) * (1 - ease(seg(t, 8.2, 8.6)))
        L = [[("Drone footage of the", 0)], [("power plant", 1), (" in your cells", 0)]]
    else:
        a = ease(seg(t, 8.6, 9.0))
        L = [[("Runs on proton power.", 0)], [("Zero ", 0), ("load-shedding", 1), (".", 0)]]
    if a > 0.01:
        y = 250
        for ln in L:
            tw = sum(d.textlength(s, font=FT) for s, _ in ln); x = (W - tw) / 2
            for s, hl in ln:
                col = (255, 212, 0) if hl else (255, 255, 255)
                d.text((x + 3, y + 4), s, font=FT, fill=(0, 0, 0, int(160 * a)))
                d.text((x, y), s, font=FT, fill=col + (int(255 * a),))
                x += d.textlength(s, font=FT)
            y += 78
    ss = ["real science: protons flowing through ATP synthase",
          "spin its rotor, and the rotation drives ATP synthesis",
          "(Boyer & Walker, Nobel Prize in Chemistry 1997)"]
    for k, s in enumerate(ss):
        d.text(((W - d.textlength(s, font=FS)) / 2, 1618 + k * 38), s, font=FS, fill=(230, 215, 235, 235))
    im.alpha_composite(WM, ((W - WM.width) // 2, 1748))

def audio():
    SR = 24000; n = int(DUR * SR); tt = np.arange(n) / SR; rng = np.random.default_rng(5)
    note = lambda m: 440 * 2 ** ((m - 69) / 12)
    bpm = 104; beat = 60 / bpm; bar = 4 * beat
    prog = [[48, 55, 60, 64], [45, 52, 57, 60], [41, 48, 53, 57], [43, 50, 55, 59]]
    pad = np.zeros(n); bass = np.zeros(n); dr = np.zeros(n); arp = np.zeros(n)
    for b in range(int(DUR / bar) + 1):
        c = prog[b % 4]; s0 = int(b * bar * SR); s1 = min(n, int((b + 1) * bar * SR))
        if s0 >= n: break
        sg = tt[s0:s1] - b * bar; env = np.minimum(1, sg / 0.5) * np.clip((bar - sg) / 0.5, 0, 1)
        for m in c:
            for det in (-0.12, 0.12): pad[s0:s1] += env * np.sin(2 * np.pi * note(m) * (1 + det / 100) * sg) + 0.25 * env * np.sin(2 * np.pi * 2 * note(m) * sg)
        for j in range(8):
            st = s0 + int(j * beat / 2 * SR); e = min(n, st + int(0.24 * SR)); q = np.arange(max(0, e - st)) / SR
            if j % 2 == 0: bass[st:e] += np.exp(-q * 8) * np.sin(2 * np.pi * note(c[0] - 12) * q)
            m = c[[0, 1, 2, 3, 2, 1, 2, 3][j]] + 12
            arp[st:e] += np.exp(-q * 12) * np.sin(2 * np.pi * note(m) * q) * (0.6 + 0.4 * np.sin(2 * np.pi * 3 * q))
        for j in range(4):
            st = s0 + int(j * beat * SR)
            if j in (0, 2) and (b >= 1 or j == 2):
                e = min(n, st + int(0.3 * SR)); q = np.arange(max(0, e - st)) / SR
                dr[st:e] += 1.3 * np.exp(-q * 12) * np.sin(2 * np.pi * (46 + 70 * np.exp(-q * 30)) * q)
            if j % 2 == 1 and b >= 1 and st < n - 10:
                e = min(n, st + int(0.18 * SR)); L = max(0, e - st)
                dr[st:e] += 0.5 * np.exp(-np.arange(L) / SR * 20) * np.convolve(rng.normal(0, 1, L), [1, -1], "same")
            for h in (0, 0.5):
                st2 = st + int(h * beat * SR); e2 = min(n, st2 + int(0.035 * SR)); L2 = max(0, e2 - st2)
                if L2 == 0: continue
                dr[st2:e2] += 0.12 * np.diff(rng.normal(0, 1, L2 + 1)) * np.exp(-np.arange(L2) / SR * 90)
    # turbine whirr (rotor) + drone hum + whooshes on camera moves
    hum = np.sin(2 * np.pi * 96 * tt) + 0.4 * np.sin(2 * np.pi * 192 * tt + np.sin(2 * np.pi * 8.4 * tt))
    whirr = np.sin(2 * np.pi * 8.4 * tt) ** 8 * np.convolve(rng.normal(0, 1, n), np.ones(12) / 12, "same")
    wh = np.zeros(n)
    for c0 in (4.3, 8.6, 12.3):
        st = int((c0 - 0.6) * SR); L = int(1.2 * SR); e = min(n, st + L)
        nz = np.convolve(rng.normal(0, 1, L), np.ones(30) / 30, "same")[: e - st]
        wh[st:e] += nz * np.sin(np.linspace(0, np.pi, L))[: e - st] ** 2
    # 'power-up' rising zap right before the punchline
    zp = np.zeros(n); st = int(7.9 * SR); L = int(0.65 * SR); q = np.arange(L) / SR
    fr = 300 + 900 * (q / q[-1]) ** 2; ph_ = 2 * np.pi * np.cumsum(fr) / SR
    zp[st:st + L] += np.sign(np.sin(ph_)) * 0.5 * np.minimum(1, q / 0.05) * np.clip((0.65 - q) / 0.08, 0, 1)
    # little 'pop' each time the labels appear
    pp = np.zeros(n)
    for c0 in (1.3, 5.0, 8.8, 12.2):
        st = int(c0 * SR); L = int(0.09 * SR); q = np.arange(L) / SR
        pp[st:st + L] += np.sin(2 * np.pi * (900 - 4000 * q) * q) * np.exp(-q * 40)
    nm = lambda x: x / (np.abs(x).max() + 1e-9)
    intro = np.clip(tt / 0.8, 0, 1); outro = np.clip((DUR - tt) / 1.2, 0, 1)
    mix = (0.20 * nm(pad) + 0.36 * nm(bass) + 0.45 * nm(dr) + 0.20 * nm(arp)) * np.clip(tt / 1.8, 0.35, 1)
    mix += 0.08 * nm(hum) + 0.07 * nm(whirr) + 0.33 * nm(wh) + 0.20 * nm(zp) + 0.22 * nm(pp)
    mix *= intro * outro
    mix = mix / np.abs(mix).max() * 0.9
    sf.write(f"{OUT}/music.wav", np.stack([mix, mix], 1), SR)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    N = int(round(DUR * FPS))
    if sys.argv[1] == "test":
        for s in sys.argv[2:]:
            Image.fromarray(frame(int(float(s) * FPS))).save(f"{OUT}/t_{float(s):05.2f}.png")
    elif sys.argv[1] == "sheet":           # contact sheet every 0.5 s at 1/5 scale
        ts = np.arange(0, DUR, 0.5); th = []
        for s in ts: th.append(Image.fromarray(frame(int(s * FPS))).resize((216, 384)))
        cols = 8; rows = (len(th) + cols - 1) // cols
        sh = Image.new("RGB", (216 * cols, 384 * rows))
        for i, im in enumerate(th): sh.paste(im, ((i % cols) * 216, (i // cols) * 384))
        sh.save(f"{OUT}/sheet.png")
    elif sys.argv[1] == "render":
        k, np_ = int(sys.argv[2]), int(sys.argv[3]); q = (N + np_ - 1) // np_; a, b = k * q, min(N, (k + 1) * q)
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "veryfast", f"{OUT}/part{k}.mp4"], stdin=subprocess.PIPE)
        for f in range(a, b): p.stdin.write(frame(f).tobytes())
        p.stdin.close(); p.wait(); print("done", k, flush=True)
    elif sys.argv[1] == "audio":
        audio()
