"""Fun / meme Reel: kinesin walking hand-over-hand along a microtubule, hauling a vesicle.
Pure numpy + PIL renderer (pseudo-3D shaded sprites). Usage:
  python3 meme_kinesin.py test 0.0 3.3      -> PNG test frames
  python3 meme_kinesin.py render K N         -> part K of N (mp4, no audio)
  python3 meme_kinesin.py audio              -> music.wav
"""
import sys, os, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import soundfile as sf

W, H, FPS = 1080, 1920, 30
STEP = 0.6                       # s per step (one beat at 100 bpm)
NSTEP = 24
DUR = STEP * NSTEP               # 14.4 s, loops seamlessly
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "meme_kinesin"
FB = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
FM = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"

# panel (the "video" inside the meme frame)
PX, PY, PW, PH = 0, 560, 1080, 1060
A = 44.0                          # tubulin monomer spacing (px); dimer = 2A = one 8 nm step
D = 2 * A
ANG = 22                          # microtubule tilt (deg)

def sphere(rx, ry, col, alpha=1.0, spec=0.55, rim=0.0, light=(-0.45, -0.6)):
    """shaded ellipsoid sprite (RGBA uint8)"""
    w, h = int(2 * rx + 4), int(2 * ry + 4)
    y, x = np.mgrid[0:h, 0:w].astype(float)
    nx = (x - w / 2) / rx; ny = (y - h / 2) / ry
    r2 = nx ** 2 + ny ** 2
    inside = np.clip((1 - np.sqrt(r2)) * min(rx, ry) * 1.2, 0, 1)
    nz = np.sqrt(np.clip(1 - r2, 0, 1))
    lx, ly = light; lz = np.sqrt(max(0, 1 - lx * lx - ly * ly))
    dif = np.clip(nx * lx + ny * ly + nz * lz, 0, 1)
    c = np.array(col, float) / 255
    shade = 0.28 + 0.85 * dif
    rgb = c[None, None, :] * shade[..., None]
    hx, hy, hz = lx, ly, lz + 1; n_ = np.sqrt(hx * hx + hy * hy + hz * hz)
    sp = np.clip((nx * hx + ny * hy + nz * hz) / n_, 0, 1) ** 40 * spec
    rgb = rgb + sp[..., None]
    if rim: rgb = rgb + (rim * (1 - nz) ** 3)[..., None] * np.array([0.6, 0.9, 1.0])
    a = inside * alpha
    if alpha < 1: a = inside * np.clip(alpha * (0.55 + 0.9 * (1 - nz) ** 2) + sp, 0, 1)
    out = np.dstack([np.clip(rgb, 0, 1) * 255, a * 255]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")

def hexc(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

# ---------- sprites ----------
TUB_A = hexc("#7C4DBA"); TUB_B = hexc("#4E3C9E")
BEAD = {}
def bead(kind, depth):
    k = (kind, round(depth, 1))
    if k not in BEAD:
        base = np.array(TUB_A if kind == 0 else TUB_B, float) * (0.45 + 0.55 * depth)
        BEAD[k] = sphere(25, 23, base.astype(int), spec=0.35 * depth)
    return BEAD[k]
HEAD = sphere(56, 40, hexc("#2BB39A"), spec=0.6)
HEAD2 = sphere(56, 40, hexc("#1F9C88"), spec=0.6)
VES = sphere(270, 270, hexc("#3B82F6"), alpha=0.82, spec=0.8, rim=0.9)

# ---------- background (blurred cytoplasm, depth of field) ----------
def make_bg():
    rng = np.random.default_rng(4)
    w, h = PW + 200, PH + 200
    y, x = np.mgrid[0:h, 0:w].astype(float)
    g = np.clip(1 - np.hypot(x - w * 0.55, y - h * 0.45) / (w * 0.9), 0, 1)
    c0 = np.array(hexc("#0E3B3A"), float); c1 = np.array(hexc("#3E8C7E"), float)
    img = Image.fromarray((c0 + (c1 - c0) * g[..., None] ** 1.3).astype(np.uint8), "RGB").convert("RGBA")
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for _ in range(26):   # far filaments
        x0, y0 = rng.uniform(-200, w), rng.uniform(-200, h); ang = rng.uniform(0, np.pi); L = rng.uniform(400, 1300)
        col = (150, 90, 200, int(rng.uniform(50, 120))) if rng.random() < 0.6 else (220, 160, 120, int(rng.uniform(40, 90)))
        d.line([x0, y0, x0 + L * np.cos(ang), y0 + L * np.sin(ang)], fill=col, width=int(rng.uniform(6, 16)))
    for _ in range(14):   # blobs
        cx, cy, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(30, 90)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 200, 190, int(rng.uniform(30, 70))))
    lay = lay.filter(ImageFilter.GaussianBlur(14))
    return Image.alpha_composite(img, lay)
BG = make_bg()

# ---------- microtubule strip (axis horizontal), periodic in D ----------
CW, CH = 2400, 1500               # axis-frame canvas
Y0 = 930                          # tube axis y in canvas
R = 72                            # tube radius
def make_strip():
    L = CW + 4 * D
    im = Image.new("RGBA", (int(L), CH), (0, 0, 0, 0))
    NP = 13
    items = []
    for p in range(NP):
        th = 2 * np.pi * p / NP
        depth = np.cos(th)
        if depth < -0.15: continue
        off = R * np.sin(th)
        shift = (3 * A / NP) * p        # 3-start helix
        n = 0
        x = -2 * A + shift
        while x < L + A:
            items.append((depth, x, Y0 + off, n % 2))
            x += A; n += 1
    items.sort(key=lambda z: z[0])
    for depth, x, y, kind in items:
        s = bead(kind, max(0.0, depth))
        im.alpha_composite(s, (int(x - s.width / 2), int(y - s.height / 2)))
    return im
STRIP = make_strip()

def ease(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)

def heads(t):
    """positions (axis-frame) of the two heads relative to camera; hand-over-hand"""
    k = int(t // STEP); ph = (t % STEP) / STEP
    cam = D * t / STEP                                   # centre of mass moves one dimer (8 nm) per step
    # head 0 lands on even dimers, head 1 on odd: rear head swings 2D forward each step
    pos = [0.0, 0.0]; lift = [0.0, 0.0]
    mover = k % 2
    for h in (0, 1):
        # last landing position of head h
        if h == mover:
            u = ease(seg(ph, 0.15, 0.85))
            pos[h] = k * D + 2 * D * u
            lift[h] = np.sin(np.pi * u) * 125
        else:
            pos[h] = (k + 1) * D
    return pos, lift, cam, ph

def seg(x, a, b): return float(np.clip((x - a) / (b - a), 0, 1))

def kin_layer(t):
    pos, lift, cam, ph = heads(t)
    cx0 = 1050                                           # camera-centre x in canvas
    im = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    # microtubule (scroll)
    off = (cam % (2 * D))
    im.alpha_composite(STRIP.crop((int(off + 2 * D), 0, int(off + 2 * D) + CW, CH)))
    d = ImageDraw.Draw(im)
    top = Y0 - R - 34
    hp = [(cx0 + pos[h] - cam, top - lift[h]) for h in (0, 1)]
    # junction (neck) above heads, stalk to vesicle
    jx = (hp[0][0] + hp[1][0]) / 2 - 10; jy = top - 190 - 10 * np.sin(2 * np.pi * t / STEP)
    for h in (0, 1):
        d.line([hp[h][0], hp[h][1] - 18, (hp[h][0] + jx) / 2, (hp[h][1] + jy) / 2 + 14, jx, jy], fill=(40, 170, 150, 255), width=16, joint="curve")
    # coiled-coil stalk (two twisted strands) up-back to vesicle
    vx = jx - 190 + 12 * np.sin(2 * np.pi * t / (2 * STEP)); vy = jy - 400 + 10 * np.sin(2 * np.pi * t / (4 * STEP))
    u = np.linspace(0, 1, 90)
    sx = jx + (vx + 90 - jx) * u + 18 * np.sin(u * np.pi) ; sy = jy + (vy + 215 - jy) * u
    for sgn, col in ((1, (60, 200, 180, 255)), (-1, (30, 140, 125, 255))):
        wob = sgn * 10 * np.sin(u * 40 - t * 6)
        d.line(list(zip(sx + wob, sy)), fill=col, width=12, joint="curve")
    # heads (back one first)
    order = sorted((0, 1), key=lambda h: -lift[h])
    for h in order:
        s = HEAD if h == 0 else HEAD2
        im.alpha_composite(s, (int(hp[h][0] - s.width / 2), int(hp[h][1] - s.height / 2)))
    im.alpha_composite(VES, (int(vx - VES.width / 2 + 90), int(vy - VES.height / 2)))
    return im, ph

def wrap_lines():
    return [[("When you feel like ", 0), ("giving up,", 1)],
            [("remember: a tiny ", 0), ("kinesin", 1), (" protein", 0)],
            [("is walking ", 0), ("nonstop", 1), (", 8 nm at a time,", 0)],
            [("to deliver cargo inside your cells.", 0)]]

FT = ImageFont.truetype(FB, 54); FS = ImageFont.truetype(FM, 30); FS2 = ImageFont.truetype(FM, 27)
WM = Image.open(os.path.join(HERE, "watermark.png")).convert("RGBA")
WM = WM.resize((int(WM.width * 88 / WM.height), 88))

def frame(f):
    t = (f / FPS) % DUR
    can, ph = kin_layer(t)
    rot = can.rotate(ANG, resample=Image.BICUBIC, center=(1050, 930))
    # camera bob
    bx = int(6 * np.sin(2 * np.pi * t / DUR * 2)); by = int(5 * np.cos(2 * np.pi * t / DUR * 3))
    crop = rot.crop((1050 - PW // 2 - 20 + bx, 930 - PH // 2 - 60 + by, 1050 + PW // 2 - 20 + bx, 930 + PH // 2 - 60 + by))
    bgx = int(100 + 40 * np.sin(2 * np.pi * t / DUR)); bgy = int(100 + 25 * np.cos(2 * np.pi * t / DUR))
    panel = BG.crop((bgx, bgy, bgx + PW, bgy + PH)).copy()
    panel.alpha_composite(crop)
    # vignette
    out = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    out.alpha_composite(panel, (PX, PY))
    d = ImageDraw.Draw(out)
    y = 250
    for ln in wrap_lines():
        tw = sum(d.textlength(s, font=FT) for s, _ in ln); x = (W - tw) / 2
        for s, hl in ln:
            d.text((x, y), s, font=FT, fill=(255, 212, 0) if hl else (255, 255, 255))
            x += d.textlength(s, font=FT)
        y += 70
    s1 = "real science: kinesin walks hand-over-hand,"
    s2 = "about 8 nm per step, one ATP per step"
    d.text(((W - d.textlength(s1, font=FS)) / 2, PY + PH + 34), s1, font=FS, fill=(170, 190, 200))
    d.text(((W - d.textlength(s2, font=FS)) / 2, PY + PH + 74), s2, font=FS, fill=(170, 190, 200))
    out.alpha_composite(WM, ((W - WM.width) // 2, PY + PH + 140))
    return np.asarray(out.convert("RGB"))

def audio():
    SR = 24000; n = int(DUR * SR); tt = np.arange(n) / SR
    note = lambda m: 440 * 2 ** ((m - 69) / 12)
    beat = STEP; bar = 4 * beat
    prog = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 65]]
    pad = np.zeros(n); keys = np.zeros(n); bass = np.zeros(n); drums = np.zeros(n); plink = np.zeros(n)
    rng = np.random.default_rng(1)
    for b in range(int(DUR / bar) + 1):
        c = prog[b % 4]; s0 = int(b * bar * SR); s1 = min(n, int((b + 1) * bar * SR))
        if s0 >= n: break
        sg = tt[s0:s1] - b * bar; env = np.minimum(1, sg / 0.3) * np.clip((bar - sg) / 0.4, 0, 1)
        for m in c:
            for det in (-0.12, 0.12): pad[s0:s1] += env * np.sin(2 * np.pi * note(m) * (1 + det / 100) * sg)
        for j, off in enumerate((0, 1.5, 2.5)):   # lo-fi bass
            st = s0 + int(off * beat * SR); e = min(n, st + int(0.9 * beat * SR)); q = np.arange(max(0, e - st)) / SR
            bass[st:e] += np.exp(-q * 3) * np.sin(2 * np.pi * note(c[0] - 24) * q)
        for j in range(4):
            st = s0 + int(j * beat * SR)
            if j in (0, 2):   # kick
                e = min(n, st + int(0.3 * SR)); q = np.arange(max(0, e - st)) / SR
                drums[st:e] += 1.2 * np.exp(-q * 14) * np.sin(2 * np.pi * (50 + 70 * np.exp(-q * 35)) * q)
            else:             # snare-ish
                e = min(n, st + int(0.18 * SR)); L = max(0, e - st)
                drums[st:e] += 0.45 * np.exp(-np.arange(L) / SR * 22) * np.convolve(rng.normal(0, 1, L), [1, -1], "same")
            for hh in (0, 0.5):  # hats
                st2 = st + int(hh * beat * SR); e2 = min(n, st2 + int(0.05 * SR)); L2 = max(0, e2 - st2)
                drums[st2:e2] += 0.12 * np.exp(-np.arange(L2) / SR * 80) * np.diff(rng.normal(0, 1, L2 + 1))
    for k in range(NSTEP):   # cute 'step' plink on each head landing (85% of the step)
        st = int((k * STEP + 0.85 * STEP) * SR) % n; e = min(n, st + int(0.35 * SR)); q = np.arange(e - st) / SR
        m = [76, 79, 81, 84][k % 4]
        plink[st:e] += np.exp(-q * 12) * (np.sin(2 * np.pi * note(m) * q) + 0.3 * np.sin(4 * np.pi * note(m) * q))
    pad = np.convolve(pad, np.ones(40) / 40, "same")
    nm = lambda x: x / (np.abs(x).max() + 1e-9)
    mix = 0.30 * nm(pad) + 0.42 * nm(bass) + 0.42 * nm(drums) + 0.30 * nm(plink)
    # vinyl crackle
    mix += 0.015 * (rng.random(n) < 0.0008) * rng.normal(0, 4, n)
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
