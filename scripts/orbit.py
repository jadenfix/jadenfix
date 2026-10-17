"""Header banner: a test mass on a precessing Schwarzschild orbit.

Units G = c = M = 1. The orbit equation is u'' = 1/L^2 - u + 3u^2 with u = 1/r.
p is tuned so the periapsis advances exactly 90 degrees per radial period, so
the rosette closes after four orbits and the animation loops without a seam.
"""
import math
import random
import sys
from pathlib import Path

E_ECC = 0.6
TARGET = 2.5 * math.pi  # 2*pi + 90 degrees between periapses


def consts(p, e=E_ECC):
    L2 = p * p / (p - 3 - e * e)
    E2 = (p - 2 - 2 * e) * (p - 2 + 2 * e) / (p * (p - 3 - e * e))
    return L2, math.sqrt(E2)


def deriv(u, w, L2):
    return w, 1.0 / L2 - u + 3 * u * u


def radial_period_angle(p, h=1e-4):
    L2, _ = consts(p)
    u, w, phi, sign_changes, prev = (1 + E_ECC) / p, 0.0, 0.0, 0, 0
    while True:
        u, w = rk4(u, w, h, L2)
        phi += h
        s = 1 if w > 0 else -1
        if prev and s != prev:
            sign_changes += 1
            if sign_changes == 2:
                return phi
        prev = s


def rk4(u, w, h, L2):
    k1 = deriv(u, w, L2)
    k2 = deriv(u + h / 2 * k1[0], w + h / 2 * k1[1], L2)
    k3 = deriv(u + h / 2 * k2[0], w + h / 2 * k2[1], L2)
    k4 = deriv(u + h * k3[0], w + h * k3[1], L2)
    return (u + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]),
            w + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]))


lo, hi = 10.0, 20.0
for _ in range(40):
    mid = (lo + hi) / 2
    if radial_period_angle(mid, 1e-3) > TARGET:
        lo = mid  # too much precession -> move outward
    else:
        hi = mid
P = (lo + hi) / 2
L2, EN = consts(P)
L = math.sqrt(L2)
RP, RA = P / (1 + E_ECC), P / (1 - E_ECC)

# integrate one closed cycle (4 radial periods = 10*pi of phi), recording t
CYCLE = 4 * TARGET
h = 2e-4
u, w, phi, t = (1 + E_ECC) / P, 0.0, 0.0, 0.0
samples = [(0.0, 1 / u, 0.0)]
step_out = 0.04
next_out = step_out
while phi < CYCLE - 1e-9:
    hh = min(h, CYCLE - phi)
    r = 1 / u
    t += EN * r * r / (L * (1 - 2 / r)) * hh  # dt/dphi, first order is plenty at this step
    u, w = rk4(u, w, hh, L2)
    phi += hh
    if phi >= next_out - 1e-12 or phi >= CYCLE - 1e-9:
        samples.append((phi, 1 / u, t))
        next_out += step_out
T_CYCLE = t

# screen mapping
W, H = 1200, 420
CX, CY = 905, 210
SCALE = 178 / RA
ROT = math.radians(45)


def xy(phi, r):
    a = phi + ROT
    return CX + SCALE * r * math.cos(a), CY - SCALE * r * math.sin(a)


pts = [xy(ph, r) for ph, r, _ in samples]
times = [tt for _, _, tt in samples]
# two cycles back to back so the trail can reach behind the start of the loop
pts2 = pts + pts[1:]
times2 = times + [T_CYCLE + tt for tt in times[1:]]
arc = [0.0]
for a, b in zip(pts2, pts2[1:]):
    arc.append(arc[-1] + math.dist(a, b))
L1 = arc[len(pts) - 1]
TOTAL = arc[-1]
d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts2)


def arc_at(tq):
    lo_i, hi_i = 0, len(times2) - 1
    while hi_i - lo_i > 1:
        m = (lo_i + hi_i) // 2
        if times2[m] <= tq:
            lo_i = m
        else:
            hi_i = m
    f = (tq - times2[lo_i]) / (times2[hi_i] - times2[lo_i])
    return arc[lo_i] + f * (arc[hi_i] - arc[lo_i])


DUR = 32  # seconds per closed cycle
K = 240
layers = [  # (name, trail length px, width, color, opacity)
    ("t1", 900, 1.2, "#ffb27a", 0.22),
    ("t2", 320, 1.6, "#ffc79e", 0.45),
    ("t3", 90, 2.2, "#ffe6d2", 0.85),
    ("hd", 0.01, 6, "#ffffff", 1.0),
]
css = []
strokes = []
for name, seg, sw, col, op in layers:
    frames = []
    for k in range(K + 1):
        tq = T_CYCLE + T_CYCLE * k / K
        frames.append(f"{100 * k / K:.3f}%{{stroke-dashoffset:{-(arc_at(tq) - seg):.1f}px}}")
    rest = -(arc_at(T_CYCLE * 1.18) - seg)  # resting pose if motion is off
    css.append(f"@keyframes {name}{{{''.join(frames)}}}")
    css.append(f".{name}{{stroke-dasharray:{seg}px {TOTAL * 2:.0f}px;stroke-dashoffset:{rest:.1f}px;"
               f"animation:{name} {DUR}s linear infinite}}")
    cap = "round"
    filt = ' filter="url(#glow)"' if name == "hd" else ""
    strokes.append(f'<path d="{d}" class="{name}" fill="none" stroke="{col}" stroke-opacity="{op}" '
                   f'stroke-width="{sw}" stroke-linecap="{cap}"{filt}/>')

rng = random.Random(11)
stars = []
for i in range(110):
    x, y = rng.uniform(8, W - 8), rng.uniform(8, H - 8)
    if math.dist((x, y), (CX, CY)) < 40:
        continue
    r = rng.choice([0.5, 0.6, 0.7, 0.8, 1.0, 1.2])
    o = rng.uniform(0.2, 0.75)
    cls = ' class="tw"' if i % 6 == 0 else ""
    sty = f' style="animation-delay:-{rng.uniform(0, 7):.1f}s"' if cls else ""
    stars.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#dfe6f0" opacity="{o:.2f}"{cls}{sty}/>')

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"
shadow = 3 * math.sqrt(3) * SCALE  # apparent shadow radius, 3*sqrt(3) M

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Jaden Fix. A test mass orbiting a Schwarzschild black hole.">
<defs>
  <radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0.45" stop-color="#ff9a5a" stop-opacity="0"/>
    <stop offset="0.52" stop-color="#ff9a5a" stop-opacity="0.55"/>
    <stop offset="0.62" stop-color="#e2621f" stop-opacity="0.18"/>
    <stop offset="1" stop-color="#e2621f" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="vignette" cx="0.75" cy="0.5" r="0.8">
    <stop offset="0" stop-color="#11151d"/><stop offset="1" stop-color="#07090d"/>
  </radialGradient>
  <filter id="glow" x="-200%" y="-200%" width="500%" height="500%">
    <feGaussianBlur stdDeviation="3.5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<style>
{chr(10).join(css)}
.tw{{animation:tw 5s ease-in-out infinite}}
@keyframes tw{{0%,100%{{opacity:.75}}50%{{opacity:.12}}}}
.disk{{transform-origin:{CX}px {CY}px;animation:spin 40s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<rect width="{W}" height="{H}" rx="14" fill="url(#vignette)"/>
<g>{"".join(stars)}</g>

<path d="{d}" fill="none" stroke="#c9d1d9" stroke-opacity="0.07" stroke-width="1"/>
<circle cx="{CX}" cy="{CY}" r="{shadow * 2.1:.1f}" fill="url(#halo)"/>
<g class="disk" fill="none" stroke="#ffb27a" stroke-linecap="round">
  <circle cx="{CX}" cy="{CY}" r="{shadow * 1.08:.1f}" stroke-width="1.2" stroke-opacity="0.55" stroke-dasharray="2 7 14 5 1 9"/>
  <circle cx="{CX}" cy="{CY}" r="{shadow * 1.22:.1f}" stroke-width="0.8" stroke-opacity="0.25" stroke-dasharray="20 9 3 12"/>
</g>
<circle cx="{CX}" cy="{CY}" r="{shadow:.1f}" fill="#000"/>
{chr(10).join(strokes)}

<text x="64" y="168" font-family="{SANS}" font-size="62" font-weight="650" letter-spacing="-1.5" fill="#f0f3f6">Jaden Fix</text>
<text x="66" y="212" font-family="{SANS}" font-size="19" fill="#aeb7c2">Software engineer, platform &amp; applied AI at AfterQuery.</text>
<text x="66" y="240" font-family="{SANS}" font-size="16" fill="#7d8792">Before that: agents at Scale AI, founding engineer at Roe (YC).</text>
<text x="66" y="368" font-family="{MONO}" font-size="11" fill="#5c6570">fig. 0  test mass around a Schwarzschild black hole, p = {P:.2f}M, e = {E_ECC}</text>
<text x="66" y="386" font-family="{MONO}" font-size="11" fill="#5c6570">periapsis advances 90° per orbit, RK4-integrated, animated in coordinate time</text>
</svg>
'''
out = Path(sys.argv[1])
(out / "orbit.svg").write_text(svg)
print(f"p={P:.4f} rp={RP:.2f} ra={RA:.2f} T_cycle={T_CYCLE:.0f}M len={TOTAL:.0f}px size={len(svg)//1024}KB")
