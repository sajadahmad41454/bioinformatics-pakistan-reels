"""FUN / MEME Reel: drone flight over a cell's microtubule 'highways' (kinesin outbound, dynein inbound).
Pseudo-3D renderer: ray-cast ground texture + depth-sorted sprites/tubes (numpy + PIL).
  python3 meme_drone.py test 1 5 9 14     -> PNG test frames
  python3 meme_drone.py render K N        -> part K of N (mp4, no audio)
  python3 meme_drone.py audio             -> music.wav
"""
import sys, os, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import soundfile as sf

W, H, FPS = 1080, 1920, 30
DUR = 16.0
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "meme_drone"
FB = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
FM = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
F = 980.0                    # focal length (px)
CX, CY = W / 2, 1040         # principal point
FOG = np.array([18, 62, 70], float)
CELL_R = 1000.0
NUC = np.array([0.0, 0.0, 70.0]); NUC_R = 280.0
MTOC = np.array([380.0, 30.0, 30.0])

def hexc(h): h = h.lstrip("#"); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float)
def ease(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
def seg(x, a, b): return float(np.clip((x - a) / (b - a), 0, 1))

# ---------------- camera path (Catmull-Rom through keyframes) ----------------
KEYS = [(0.0, (0, -260, 2700), (0, 0, 0)),
        (4.5, (-350, -1550, 1250), (60, 0, 0)),
        (9.0, (1150, -820, 420), (420, 20, 60)),
        (12.5, (1020, -300, 290), (380, 40, 60)),
        (16.0, (860, 240, 300), (240, 40, 70))]
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
    roll = 0.10 * np.sin(2 * np.pi * t / DUR * 1.3)        # gentle drone bank
    cu = np.cross(rt, fw)
    rt, cu = rt * np.cos(roll) + cu * np.sin(roll), cu * np.cos(roll) - rt * np.sin(roll)
    return pos, fw, rt, cu

def proj(P, C):
    pos, fw, rt, cu = C
    d = np.asarray(P, float) - pos
    z = d @ fw; x = d @ rt; y = d @ cu
    return CX + F * x / np.maximum(z, 1e-3), CY - F * y / np.maximum(z, 1e-3), z

def fogk(z): return float(np.clip((z - 400) / 3600, 0, 0.85))

# ---------------- ground texture (ray cast at low res) ----------------
GW, GH = 270, 480
gy, gx = np.mgrid[0:GH, 0:GW].astype(float)
def ground(C):
    pos, fw, rt, cu = C
    sx = (gx + 0.5) * W / GW; sy = (gy + 0.5) * H / GH
    dx = (sx - CX) / F; dy = -(sy - CY) / F
    ray = fw[None, None, :] + dx[..., None] * rt + dy[..., None] * cu
    tz = -pos[2] / np.where(ray[..., 2] < -1e-4, ray[..., 2], -1e-4)
    hit = ray[..., 2] < -1e-4
    X = pos[0] + ray[..., 0] * tz; Y = pos[1] + ray[..., 1] * tz
    r = np.hypot(X, Y)
    n = (np.sin(X / 37) * np.sin(Y / 41) + 0.6 * np.sin((X + Y) / 23) + 0.5 * np.sin((X - 2 * Y) / 61)) / 2.1
    cyt = hexc("#2F8C80") + n[..., None] * 18
    inner = hexc("#3A9A8A")
    col = cyt + (inner - cyt) * np.clip(1 - r / 900, 0, 1)[..., None] * 0.6
    memb = np.exp(-((r - CELL_R) / 26) ** 2)[..., None]
    col = col * (1 - memb) + hexc("#9AE6D8") * memb
    outside = (r > CELL_R + 20)[..., None]
    col = np.where(outside, hexc("#0D2A33") + n[..., None] * 8, col)
    dist = tz * np.linalg.norm(ray, axis=-1)
    fk = np.clip((dist - 400) / 3600, 0, 0.85)[..., None]
    col = col * (1 - fk) + FOG * fk
    sky = hexc("#0B2229") + (hexc("#1B4F57") - hexc("#0B2229")) * np.clip(1 - gy / GH * 2, 0, 1)[..., None]
    col = np.where(hit[..., None], col, sky)
    im = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8), "RGB").resize((W, H), Image.BICUBIC)
    return im.filter(ImageFilter.GaussianBlur(1.2)).convert("RGBA")

# ---------------- sprites ----------------
def sphere(r, col, spec=0.5, alpha=1.0):
    s = int(2 * r + 4); y, x = np.mgrid[0:s, 0:s].astype(float)
    nx, ny = (x - s / 2) / r, (y - s / 2) / r; r2 = nx ** 2 + ny ** 2
    nz = np.sqrt(np.clip(1 - r2, 0, 1)); m = np.clip((1 - np.sqrt(r2)) * r, 0, 1)
    lx, ly, lz = -0.4, -0.55, 0.73
    dif = np.clip(nx * lx + ny * ly + nz * lz, 0, 1)
    rgb = col[None, None, :] / 255 * (0.3 + 0.85 * dif)[..., None]
    sp = np.clip((nx * lx + ny * ly + nz * (lz + 1)) / np.sqrt(lx * lx + ly * ly + (lz + 1) ** 2), 0, 1) ** 35 * spec
    rgb = rgb + sp[..., None]
    a = m * alpha
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 1) * 255, a * 255]).astype(np.uint8), "RGBA")
BASE = {"nuc": sphere(128, hexc("#6D5BD0"), 0.5), "kin": sphere(64, hexc("#FBBF24"), 0.8), "dyn": sphere(64, hexc("#22D3EE"), 0.8),
        "mito": sphere(64, hexc("#F97352"), 0.5), "rib": sphere(32, hexc("#C4B5FD"), 0.2), "mtoc": sphere(64, hexc("#FFF3B0"), 0.9)}
_SC = {}
def spr(key, d, fk):
    d = int(max(3, min(1400, d))); fb = round(fk * 10) / 10
    k = (key, d, fb)
    if k not in _SC:
        if len(_SC) > 4000: _SC.clear()
        im = BASE[key].resize((d, d), Image.BILINEAR)
        if fb > 0:
            a = np.asarray(im).astype(float)
            a[..., :3] = a[..., :3] * (1 - fb) + FOG * fb
            im = Image.fromarray(a.astype(np.uint8), "RGBA")
        _SC[k] = im
    return _SC[k]
GLOW = None
def glow(d):
    s = int(d); y, x = np.mgrid[0:s, 0:s].astype(float); r = np.hypot(x - s / 2, y - s / 2) / (s / 2)
    a = np.clip(1 - r, 0, 1) ** 2
    return Image.fromarray(np.dstack([np.full((s, s), 255), np.full((s, s), 240), np.full((s, s), 170), a * 200]).astype(np.uint8), "RGBA")

# ---------------- world ----------------
rng = np.random.default_rng(12)
def mt_path(phi):
    """microtubule from MTOC to cell edge, bent around the nucleus"""
    end = np.array([CELL_R * 0.96 * np.cos(phi), CELL_R * 0.96 * np.sin(phi), 18.0])
    u = np.linspace(0, 1, 40)[:, None]
    P = MTOC * (1 - u) + end * u
    P[:, 2] = 18 + 14 * (1 - u[:, 0]) ** 3
    for _ in range(3):
        r = np.hypot(P[:, 0], P[:, 1]); push = np.clip(NUC_R + 70 - r, 0, None)
        P[:, 0] += P[:, 0] / np.maximum(r, 1) * push; P[:, 1] += P[:, 1] / np.maximum(r, 1) * push
    wig = np.sin(u[:, 0] * np.pi * 2 + phi * 3) * 25
    nrm = np.array([-np.sin(phi), np.cos(phi), 0])
    P += wig[:, None] * nrm * np.sin(u[:, 0] * np.pi)[:, None]
    return P
PHIS = np.linspace(0, 2 * np.pi, 24, endpoint=False) + 0.07
MTS = [mt_path(p) for p in PHIS]
def along(P, u):
    L = np.cumsum(np.r_[0, np.linalg.norm(np.diff(P, axis=0), axis=1)]); s = u * L[-1]
    i = min(len(P) - 2, np.searchsorted(L, s) - 1); i = max(0, i); w = (s - L[i]) / max(1e-6, L[i + 1] - L[i])
    return P[i] * (1 - w) + P[i + 1] * w
CARGO = []
for m in range(len(MTS)):
    for j in range(3):
        kind = "kin" if (m + j) % 2 == 0 else "dyn"
        CARGO.append((m, kind, rng.uniform(0, 1), rng.uniform(0.05, 0.085), rng.uniform(16, 24)))
MITO = []
for _ in range(16):
    r = rng.uniform(420, 900); a = rng.uniform(0, 2 * np.pi); ang = rng.uniform(0, np.pi)
    c = np.array([r * np.cos(a), r * np.sin(a), 22]); dv = np.array([np.cos(ang), np.sin(ang), 0])
    MITO.append([c + dv * k for k in np.linspace(-55, 55, 6)])
RIB = np.c_[rng.uniform(-1, 1, (700, 2)) * CELL_R, np.full(700, 8.0)]
RIB = RIB[(np.hypot(RIB[:, 0], RIB[:, 1]) < CELL_R - 30) & (np.hypot(RIB[:, 0], RIB[:, 1]) > NUC_R + 20)]
ER = []
for k in range(7):
    a0 = rng.uniform(0, 2 * np.pi); a = a0 + np.linspace(0, 1.3, 30); rr = NUC_R + 60 + 30 * k * 0.6 + 22 * np.sin(a * 7 + k)
    ER.append(np.c_[rr * np.cos(a), rr * np.sin(a), np.full(30, 10.0)])
GOLGI = []
for k in range(5):
    a = np.linspace(-0.55, 0.55, 20) + 0.15; rr = 120 + k * 22
    GOLGI.append(np.c_[MTOC[0] + 40 + rr * np.cos(a) - 120, MTOC[1] + 140 + rr * np.sin(a) - 0, np.full(20, 14.0)])

def poly_items(P, C, width, col, items, alpha=255, step=1):
    x, y, z = proj(P, C)
    for i in range(0, len(P) - 1, step):
        j = min(len(P) - 1, i + step)
        if z[i] < 30 or z[j] < 30: continue
        zz = (z[i] + z[j]) / 2
        items.append((zz, "line", (x[i], y[i], x[j], y[j]), max(1, F * width / zz), col, alpha))

LABELS = [  # (t0, t1, world point, text, colour)
    (1.6, 4.8, np.array([0, -CELL_R, 40.0]), "Cell membrane · city limits", "#9AE6D8"),
    (2.4, 6.0, NUC + [0, 0, NUC_R * 0.6], "Nucleus · HQ (DNA inside)", "#C4B5FD"),
    (6.2, 10.0, MTOC + [0, 0, 30], "MTOC · central bus terminal", "#FFF3B0"),
    (8.8, 11.6, None, "Kinesin lane · outbound to the edge", "#FBBF24"),
    (11.5, 15.0, None, "Dynein lane · inbound to the centre", "#22D3EE"),
]

FT = ImageFont.truetype(FB, 58); FS = ImageFont.truetype(FM, 29); FL = ImageFont.truetype(FB, 30); FH = ImageFont.truetype(MONO, 26)
WM = Image.open(os.path.join(HERE, "watermark.png")).convert("RGBA"); WM = WM.resize((int(WM.width * 80 / WM.height), 80))

def nearest_cargo(t, C, kind):
    best = None
    for (m, k, u0, v, r) in CARGO:
        if k != kind: continue
        u = (u0 + (v if k == "kin" else -v) * t) % 1
        P = along(MTS[m], u) + [0, 0, 26]
        x, y, z = proj(P, C)
        if not (420 < z < 1300) or not (220 < x < 860 and 820 < y < 1460): continue
        if best is None or abs(z - 700) < abs(best[2] - 700): best = (x, y, z)
    return best

def frame(f):
    t = f / FPS
    C = cam(t)
    im = ground(C)
    items = []
    for P in ER: poly_items(P, C, 14, (120, 230, 170), items, alpha=150, step=2)
    for P in GOLGI: poly_items(P, C, 12, (244, 114, 182), items, alpha=220, step=2)
    for P in MTS: poly_items(P, C, 11, (167, 105, 255), items, alpha=235, step=1)
    x, y, z = proj(RIB, C)
    for i in np.nonzero(z > 60)[0]: items.append((z[i], "spr", "rib", x[i], y[i], F * 7 / z[i]))
    for chain in MITO:
        for P in chain:
            x, y, z = proj(P, C)
            if z > 140: items.append((z, "spr", "mito", x, y, F * 2 * 24 / z))
    for (m, kind, u0, v, r) in CARGO:
        u = (u0 + (v if kind == "kin" else -v) * t) % 1
        P = along(MTS[m], u) + [0, 0, r + 6]
        x, y, z = proj(P, C)
        if z > 140:
            items.append((z, "spr", kind, x, y, F * 2 * r / z))
            # little motor 'legs' to the track
            items.append((z + 1, "line", (x, y + F * r / z * 0.6, x, y + F * (r + 8) / z), max(1, F * 4 / z), (230, 230, 230), 200))
    x, y, z = proj(NUC, C)
    if z > 60: items.append((z, "spr", "nuc", x, y, F * 2 * NUC_R / z))
    x, y, z = proj(MTOC, C)
    if z > 40: items.append((z - 1, "glow", None, x, y, F * 2 * 70 / z)); items.append((z, "spr", "mtoc", x, y, F * 2 * 20 / z))
    items.sort(key=lambda it: -it[0])
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for it in items:
        z = it[0]; fk = fogk(z)
        if it[1] == "line":
            (x0, y0, x1, y1), w, col, al = it[2], it[3], it[4], it[5]
            if max(x0, x1) < -200 or min(x0, x1) > W + 200 or max(y0, y1) < -200 or min(y0, y1) > H + 200: continue
            c = tuple(int(v) for v in (np.array(col) * (1 - fk) + FOG * fk)) + (al,)
            d.line([x0, y0, x1, y1], fill=c, width=int(min(w, 120)))
            if w > 4: d.ellipse([x1 - w / 2, y1 - w / 2, x1 + w / 2, y1 + w / 2], fill=c)
        elif it[1] == "spr":
            _, _, key, x, y, dd = it
            if dd < 2 or x + dd < 0 or x - dd > W or y + dd < 0 or y - dd > H: continue
            s = spr(key, dd, fk); lay.alpha_composite(s, (int(x - s.width / 2), int(y - s.height / 2))) if -s.width < x < W + s.width else None
        elif it[1] == "glow":
            _, _, _, x, y, dd = it
            if 4 < dd < 1600:
                g = glow(dd * (1 + 0.08 * np.sin(t * 6))); lay.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
    im.alpha_composite(lay)
    # depth-of-field-ish vignette
    im = Image.alpha_composite(im, VIG)
    d = ImageDraw.Draw(im)
    # map pins
    for (t0, t1, P, txt, col) in LABELS:
        a = ease(seg(t, t0, t0 + 0.35)) * (1 - ease(seg(t, t1 - 0.35, t1)))
        if a <= 0.01: continue
        if P is None:
            nc = nearest_cargo(t, C, "kin" if "Kinesin" in txt else "dyn")
            if nc is None: continue
            x, y, z = nc
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
    bx = np.clip(x - bw / 2, 30, W - 30 - bw); by = y - 150
    d.line([x, y - 10, x, by + bh], fill=c + (230,), width=4)
    d.ellipse([x - 11, y - 11, x + 11, y + 11], fill=c + (255,), outline=(255, 255, 255, 255), width=3)
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=32, fill=(8, 24, 28, 225), outline=c + (255,), width=3)
    d.text((bx + 28, by + 15), txt, font=FL, fill=(255, 255, 255, 255))
    if a < 1:
        arr = np.asarray(lay).copy(); arr[..., 3] = (arr[..., 3] * a).astype(np.uint8); lay = Image.fromarray(arr)
    im.alpha_composite(lay)

def make_vig():
    y, x = np.mgrid[0:H, 0:W].astype(float)
    r = np.hypot((x - W / 2) / W, (y - H / 2) / H)
    a = np.clip((r - 0.35) / 0.4, 0, 1) ** 1.5 * 170
    top = np.clip(1 - y / 720, 0, 1) ** 1.4 * 235          # dark band behind the meme text
    bot = np.clip((y - 1530) / 170, 0, 1) ** 1.2 * 238
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
    d.text((W - m - 250, y0 + 18), "CELL-CAM 4K", font=FH, fill=c)
    ss = int(t); ff = int((t - ss) * FPS)
    d.text((m + 6, y1 - 50), f"00:00:{ss:02d}:{ff:02d}", font=FH, fill=c)
    bx = W - m - 110; d.rectangle([bx, y1 - 46, bx + 90, y1 - 20], outline=c, width=3); d.rectangle([bx + 92, y1 - 39, bx + 98, y1 - 27], fill=c)
    d.rectangle([bx + 6, y1 - 40, bx + 6 + 66, y1 - 26], fill=(74, 222, 128, 230))

def meme(im, t):
    d = ImageDraw.Draw(im)
    if t < 8.6:
        a = ease(seg(t, 0.2, 0.6)) * (1 - ease(seg(t, 8.2, 8.6)))
        L = [[("Drone footage of the ", 0)], [("traffic", 1), (" inside your cells", 0)]]
    else:
        a = ease(seg(t, 8.6, 9.0))
        L = [[("Two-way lanes. Zero honking.", 0)], [("Karachi traffic", 1), (" could never.", 0)]]
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
    ss = ["real science: kinesins carry cargo toward microtubule",
          "plus ends (the cell edge); dynein carries it toward",
          "minus ends (the cell centre)"]
    for k, s in enumerate(ss):
        d.text(((W - d.textlength(s, font=FS)) / 2, 1618 + k * 38), s, font=FS, fill=(205, 225, 230, 235))
    im.alpha_composite(WM, ((W - WM.width) // 2, 1748))

def audio():
    SR = 24000; n = int(DUR * SR); tt = np.arange(n) / SR; rng = np.random.default_rng(3)
    note = lambda m: 440 * 2 ** ((m - 69) / 12)
    bpm = 112; beat = 60 / bpm; bar = 4 * beat
    prog = [[50, 57, 62, 65], [46, 53, 58, 62], [43, 50, 55, 58], [45, 52, 57, 61]]
    pad = np.zeros(n); bass = np.zeros(n); dr = np.zeros(n); arp = np.zeros(n)
    for b in range(int(DUR / bar) + 1):
        c = prog[b % 4]; s0 = int(b * bar * SR); s1 = min(n, int((b + 1) * bar * SR))
        if s0 >= n: break
        sg = tt[s0:s1] - b * bar; env = np.minimum(1, sg / 0.4) * np.clip((bar - sg) / 0.4, 0, 1)
        for m in c:
            for det in (-0.15, 0.15): pad[s0:s1] += env * np.sign(np.sin(2 * np.pi * note(m) * (1 + det / 100) * sg)) * 0.3 + env * np.sin(2 * np.pi * note(m) * sg)
        for j in range(8):
            st = s0 + int(j * beat / 2 * SR); e = min(n, st + int(0.22 * SR)); q = np.arange(max(0, e - st)) / SR
            bass[st:e] += np.exp(-q * 9) * np.sin(2 * np.pi * note(c[0] - 12) * q)
            m = c[[0, 2, 1, 3, 2, 1, 3, 2][j]] + 12
            arp[st:e] += np.exp(-q * 14) * np.sin(2 * np.pi * note(m) * q)
        for j in range(4):
            st = s0 + int(j * beat * SR)
            if b >= 1 or j >= 2:
                e = min(n, st + int(0.3 * SR)); q = np.arange(max(0, e - st)) / SR
                dr[st:e] += 1.3 * np.exp(-q * 13) * np.sin(2 * np.pi * (48 + 80 * np.exp(-q * 35)) * q)
            if j % 2 == 1 and b >= 1 and st < n - 10:
                e = min(n, st + int(0.16 * SR)); L = max(0, e - st)
                dr[st:e] += 0.5 * np.exp(-np.arange(L) / SR * 24) * np.convolve(rng.normal(0, 1, L), [1, -1], "same")
            for h in (0, 0.5):
                st2 = st + int(h * beat * SR); e2 = min(n, st2 + int(0.04 * SR)); L2 = max(0, e2 - st2)
                if L2 == 0: continue
                dr[st2:e2] += 0.14 * np.diff(rng.normal(0, 1, L2 + 1)) * np.exp(-np.arange(L2) / SR * 90)
    # drone propeller hum + whooshes on camera moves
    hum = (np.sin(2 * np.pi * 118 * tt) + 0.5 * np.sin(2 * np.pi * 236 * tt + np.sin(2 * np.pi * 9 * tt))) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.3 * tt))
    wh = np.zeros(n)
    for c0 in (4.2, 8.6, 12.2):
        st = int((c0 - 0.6) * SR); L = int(1.2 * SR); e = min(n, st + L)
        nz = np.convolve(rng.normal(0, 1, L), np.ones(30) / 30, "same")[: e - st]
        wh[st:e] += nz * np.sin(np.linspace(0, np.pi, L))[: e - st] ** 2
    # a tiny cartoon 'beep beep' right before the punchline (horn-like, but polite)
    bp = np.zeros(n)
    for c0 in (8.15, 8.38):
        st = int(c0 * SR); e = min(n, st + int(0.14 * SR)); q = np.arange(e - st) / SR
        bp[st:e] += np.sign(np.sin(2 * np.pi * 620 * q)) * np.minimum(1, (0.14 - q) / 0.03) * 0.5
    nm = lambda x: x / (np.abs(x).max() + 1e-9)
    intro = np.clip(tt / 0.8, 0, 1); outro = np.clip((DUR - tt) / 1.2, 0, 1)
    mix = (0.22 * nm(pad) + 0.38 * nm(bass) + 0.45 * nm(dr) + 0.18 * nm(arp)) * np.clip(tt / 1.8, 0.35, 1)
    mix += 0.10 * nm(hum) + 0.35 * nm(wh) + 0.22 * nm(bp)
    mix *= intro * outro
    mix = mix / np.abs(mix).max() * 0.9
    sf.write(f"{OUT}/music.wav", np.stack([mix, mix], 1), SR)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    N = int(round(DUR * FPS))
    if sys.argv[1] == "test":
        for s in sys.argv[2:]:
            Image.fromarray(frame(int(float(s) * FPS))).save(f"{OUT}/t_{float(s):05.2f}.png")
    elif sys.argv[1] == "render":
        k, np_ = int(sys.argv[2]), int(sys.argv[3]); q = (N + np_ - 1) // np_; a, b = k * q, min(N, (k + 1) * q)
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "veryfast", f"{OUT}/part{k}.mp4"], stdin=subprocess.PIPE)
        for f in range(a, b): p.stdin.write(frame(f).tobytes())
        p.stdin.close(); p.wait(); print("done", k, flush=True)
    elif sys.argv[1] == "audio":
        audio()
