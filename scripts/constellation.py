"""Loop-action bias, drawn as a constellation.

States are stars, transitions are hairlines, and the stall is the agent orbiting
a star without going anywhere. Pass one: outcome-only credit sweeps back from the
goal and lights the orbit as brightly as the real path. Pass two: branch-aware
credit scores each step as it happens (the paper's ALFWorld signals: arrive +0.5,
inventory change +1.0, repeated "Nothing happens." -1.0) and the orbit goes red.

usage: constellation.py OUT.webp [--preview SECONDS]
"""
import math
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter

OUT = sys.argv[1]
PREVIEW = float(sys.argv[sys.argv.index("--preview") + 1]) if "--preview" in sys.argv else None

W, H = 1280, 420
S = 2
FPS = 20
DUR = 16.0

BG = (6, 8, 12)
HAIR = (30, 36, 46)
TXT = (232, 235, 240)
MUTE = (128, 136, 148)
FAINT = (70, 77, 88)
GOLD = (236, 204, 140)
WARM = (255, 214, 170)
RED = (236, 92, 82)
WHITE = (255, 248, 240)

FD = "/System/Library/Fonts/"
F = lambda n, s, i=0: ImageFont.truetype(FD + n, int(s * S), index=i)
f_cap = F("HelveticaNeue.ttc", 19, 7)
f_lab = F("HelveticaNeue.ttc", 13, 7)
f_mono = F("Menlo.ttc", 12)
f_tiny = F("Menlo.ttc", 10)
f_val = F("Menlo.ttc", 12)

stars_xy = [(150, 250), (430, 205), (700, 258), (945, 212), (1150, 244)]
names = ["start", "countertop", "holding mug", "coffee machine", "done"]
ORBIT_R = 38


def seg(a, b, n=90):
    t = np.linspace(0, 1, n)[:, None]
    return np.array(a) * (1 - t) + np.array(b) * t


def orbit(n=140):
    c = np.array(stars_xy[1], float)
    th = np.linspace(0, 2 * math.pi, n)
    # leave the star, circle it, come back
    pts = np.stack([c[0] + ORBIT_R * np.sin(th), c[1] - ORBIT_R * (1 - np.cos(th))], 1)
    return pts


P = stars_xy
steps = [
    (seg(P[0], P[1]), "go to countertop 1", "You arrive at countertop 1.", 0.5, (285, 212)),
    (orbit(), "take mug 1 from countertop 1", "Nothing happens.", -1.0, (P[1][0] - ORBIT_R - 26, P[1][1] - ORBIT_R)),
    (orbit(), "examine countertop 1", "Nothing happens.", -1.0, (P[1][0] + ORBIT_R + 26, P[1][1] - ORBIT_R)),
    (seg(P[1], P[2]), "take mug 1 from countertop 1", "You pick up the mug 1.", 1.0, (565, 215)),
    (seg(P[2], P[3]), "go to coffeemachine 1", "You arrive at coffeemachine 1.", 0.5, (822, 218)),
    (seg(P[3], P[4]), "put mug 1 in/on coffeemachine 1", "You put the mug 1 in the coffeemachine 1.", 1.0, (1048, 212)),
]

# timeline
A_RUN, A_SEG = 0.9, 0.85
A_GOAL = A_RUN + 6 * A_SEG
A_SW0, A_SW1 = A_GOAL + 0.3, A_GOAL + 1.7
B_START = 8.7
B_RUN, B_SEG = 9.1, 0.65
B_GOAL = B_RUN + 6 * B_SEG
RESULT = B_GOAL + 0.4
FADE_OUT = 15.3

rng = np.random.default_rng(3)
bg_stars = [(rng.uniform(0, W), rng.uniform(0, H), rng.pareto(2.2) * 0.25 + 0.12, rng.integers(1, 4), rng.uniform(0, 6.3))
            for _ in range(260)]


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def at(path, u):
    u = min(max(u, 0.0), 1.0) * (len(path) - 1)
    i = int(u)
    j = min(i + 1, len(path) - 1)
    return path[i] * (1 - (u - i)) + path[j] * (u - i)


def mix(c, k):
    k = min(max(k, 0.0), 1.0)
    return tuple(int(BG[i] + (c[i] - BG[i]) * k) for i in range(3))


def tracked(d, xy, txt, fnt, fill, track):
    x, y = xy
    for ch in txt:
        d.text((x, y), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + track * S


def frame(t):
    base = Image.new("RGB", (W * S, H * S), BG)
    glow = Image.new("RGB", (W * S, H * S), (0, 0, 0))
    db, dg = ImageDraw.Draw(base), ImageDraw.Draw(glow)
    sc = lambda pts: [(float(x) * S, float(y) * S) for x, y in pts]
    master = ease(t / 0.8) * (1 - ease((t - FADE_OUT) / 0.7))

    # sky: faint stars with a slow, loop-safe shimmer
    for x, y, m, cyc, ph in bg_stars:
        k = m * (0.75 + 0.25 * math.sin(2 * math.pi * cyc * t / DUR + ph))
        r = 0.9 * S
        db.ellipse([x * S - r, y * S - r, x * S + r, y * S + r], fill=mix((200, 210, 230), k))

    pass_b = t >= B_START
    run0, sl = (B_RUN, B_SEG) if pass_b else (A_RUN, A_SEG)
    kk = (t - run0) / sl
    cur = math.floor(kk) if kk >= 0 else -1
    frac = kk - cur if 0 <= cur < 6 else 0.0
    done = kk >= 6

    lit = [None] * 6
    if not pass_b and t >= A_SW0:
        w = ease((t - A_SW0) / (A_SW1 - A_SW0))
        for i in range(6):
            r_ = ease(w * 6 - (5 - i))
            if r_ > 0:
                lit[i] = (GOLD, r_, "+1")
    if pass_b:
        for i in range(6):
            if cur > i or done or (cur == i and frac > 0.6):
                v = steps[i][3]
                lit[i] = (WARM if v > 0 else RED, ease((kk - i - 0.6) / 0.3), f"{v:+.1f}".replace("+1.0", "+1").replace("-1.0", "-1"))
    hk = master * (1 - ease((t - B_START + 0.5) / 0.5)) if not pass_b else master * ease((t - B_START) / 0.6)

    # hairlines
    for i, (path, *_r) in enumerate(steps):
        if i == 2:
            continue
        db.line(sc(path), fill=mix(HAIR, master), width=S)
    for i, (path, *_r) in enumerate(steps):
        if lit[i] is None:
            continue
        col, s, _ = lit[i]
        s *= master * (1 - ease((t - B_START + 0.5) / 0.5)) if not pass_b else master
        db.line(sc(path), fill=mix(col, 0.9 * s), width=int(1.5 * S))
        dg.line(sc(path), fill=mix(col, 0.55 * s), width=4 * S)

    # credit drifting back along the lines in pass one
    if not pass_b and A_SW0 <= t <= B_START - 0.5:
        for i, (path, *_r) in enumerate(steps):
            if lit[i] is None:
                continue
            for p in range(3):
                u = 1 - ((t * 0.55 + p / 3 + i * 0.17) % 1.0)
                x, y = at(path, u)
                r = 1.6 * S
                dg.ellipse([x * S - r, y * S - r, x * S + r, y * S + r], fill=mix(GOLD, lit[i][1] * master * (1 - ease((t - B_START + 0.5) / 0.5))))

    # value labels
    for i in range(6):
        if lit[i] is None:
            continue
        col, s, lab = lit[i]
        s *= hk
        x, y = steps[i][4]
        db.text((x * S, y * S), lab, font=f_val, fill=mix(col, s), anchor="mm")

    # stars
    visited = [0, 1 if cur >= 0 and frac > 0.97 or cur >= 1 else 0, 1 if cur >= 4 else 0, 1 if cur >= 5 else 0, 1 if done else 0]
    visited[0] = 1 if cur >= 0 else 0
    for j, ((x, y), nm) in enumerate(zip(stars_xy, names)):
        v = visited[j] if (0 <= cur or done) else 0
        core = 0.55 + 0.45 * v
        r = (2.4 + 0.8 * v) * S
        db.ellipse([x * S - r, y * S - r, x * S + r, y * S + r], fill=mix(WHITE, core * master))
        rg = (7 + 5 * v) * S
        dg.ellipse([x * S - rg, y * S - rg, x * S + rg, y * S + rg], fill=mix((200, 215, 255), (0.25 + 0.35 * v) * master))
        db.text((x * S, (y + 22) * S), nm, font=f_lab, fill=mix(MUTE if not v else TXT, master * (0.8 + 0.2 * v)), anchor="ma")

    # goal pulse
    g0 = B_GOAL if pass_b else A_GOAL
    if g0 <= t <= g0 + 1.2:
        q = (t - g0) / 1.2
        x, y = P[4]
        r = (6 + 44 * ease(q)) * S
        dg.ellipse([x * S - r, y * S - r, x * S + r, y * S + r], outline=mix(WARM if pass_b else GOLD, (1 - q) * 0.8 * master), width=S)

    # agent
    if 0 <= cur < 6:
        path = steps[cur][0]
        u = frac if cur in (1, 2) else ease(frac)
        tail = [at(path, max(0.0, u - d)) for d in np.linspace(0, 0.22, 16)]
        for j in range(len(tail) - 1):
            a = 1 - j / len(tail)
            dg.line(sc([tail[j], tail[j + 1]]), fill=mix(WHITE, 0.7 * a * master), width=int(2.5 * S))
        x, y = tail[0]
        r = 3.2 * S
        db.ellipse([x * S - r, y * S - r, x * S + r, y * S + r], fill=mix(WHITE, master))
        rg = 12 * S
        dg.ellipse([x * S - rg, y * S - rg, x * S + rg, y * S + rg], fill=mix(WHITE, 0.55 * master))

    # caption
    tracked(db, (60 * S, 46 * S), "FIG. 1  ·  LOOP-ACTION BIAS", f_tiny, mix(FAINT, master), 2.4)
    cap = ("Outcome-only: a winning episode gives every step +1." if not pass_b
           else "Branch-aware: each step is scored by what it changed.")
    db.text((60 * S, 66 * S), cap, font=f_cap, fill=mix(TXT, hk))
    if not pass_b and t > A_SW1 + 0.2:
        db.text((60 * S, 96 * S), "The orbit that went nowhere earns as much as the path that won.", font=f_lab,
                fill=mix(GOLD, ease((t - A_SW1 - 0.2) / 0.5) * hk))

    # action log, bottom left
    ly = 360
    if 0 <= cur < 6:
        _, act, obs, _v, _p = steps[cur]
        n = int(len(act) * min(1, frac / 0.4))
        db.text((60 * S, ly * S), "> " + act[:n], font=f_mono, fill=mix(MUTE, master))
        if frac > 0.45:
            ox = 60 * S + db.textlength("> " + act + "   ", font=f_mono)
            db.text((ox, ly * S), obs, font=f_mono, fill=mix(RED if obs.startswith("Nothing") else FAINT, ease((frac - 0.45) / 0.15) * master))
    if pass_b and t >= RESULT:
        k = ease((t - RESULT) / 0.6) * master
        x = 60 * S
        for txt, col in (("SUCCESS AFTER TRAINING      ", FAINT), ("OUTCOME-ONLY ", MUTE), ("0.24", RED), ("      UNTRAINED ", MUTE),
                         ("0.79", TXT), ("      BRANCH-AWARE ", MUTE), ("1.00", WARM)):
            db.text((x, ly * S), txt, font=f_mono, fill=mix(col, k))
            x += db.textlength(txt, font=f_mono)

    b = np.asarray(base.resize((W, H), Image.LANCZOS), np.float32) / 255
    g = np.asarray(glow.resize((W, H), Image.LANCZOS), np.float32) / 255
    bloom = gaussian_filter(g, (2, 2, 0)) * 0.8 + gaussian_filter(g, (8, 8, 0)) * 0.6 + gaussian_filter(g, (22, 22, 0)) * 0.3
    out = 1 - (1 - b) * (1 - np.clip(bloom, 0, 1))
    return Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8))


if __name__ == "__main__":
    if PREVIEW is not None:
        frame(PREVIEW).save(OUT)
        sys.exit()
    import multiprocessing as mp
    n = int(DUR * FPS)
    with mp.get_context("fork").Pool(8) as pool:
        frames = pool.map(frame, [i / FPS for i in range(n)])
    frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=int(1000 / FPS), loop=0, quality=80, method=6)
    print("done", n, "frames")
