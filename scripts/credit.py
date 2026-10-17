"""Loop-action bias, animated: one ALFWorld-style episode scored two ways.

Branch-aware values are the paper's auto-extracted ALFWorld signals:
"You arrive at" +0.5, inventory change +1.0, repeated "Nothing happens." -1.0.
"""
import sys
from pathlib import Path

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"

steps = [
    ("go to countertop 1", "You arrive at countertop 1. On it, you see a mug 1.", 0.5, ""),
    ("take mug 1 from countertop 1", "Nothing happens.", -1.0, "failed"),
    ("examine countertop 1", "Nothing happens.", -1.0, "stall"),
    ("take mug 1 from countertop 1", "You pick up the mug 1 from the countertop 1.", 1.0, ""),
    ("go to coffeemachine 1", "You arrive at coffeemachine 1.", 0.5, ""),
    ("put mug 1 in/on coffeemachine 1", "You put the mug 1 in/on the coffeemachine 1.", 1.0, "success"),
]

W, H = 1000, 452
DUR = 16.0
ROW0, ROWH = 112, 46
LOG_X = 28
COL_O, COL_B = 640, 880  # axis centers for the two score columns
UNIT = 58  # px per 1.0 of credit

ORANGE, RED, GREY = "#ff9a5a", "#f0605a", "#8b949e"


def pct(sec):
    return f"{100 * sec / DUR:.2f}%"


css, body = [], []
STEP_T = 1.55
T0 = 0.6


def appear(cls, start, kind="fade"):
    """Keyframes that hide an element until `start`, keep it until the loop fades."""
    a, b = pct(start), pct(start + 0.35)
    end, gone = pct(DUR - 0.9), pct(DUR - 0.3)
    if kind == "fade":
        hidden, shown = "opacity:0", "opacity:1"
    else:  # grow from the axis
        hidden, shown = "transform:scaleX(0)", "transform:scaleX(1)"
    css.append(f"@keyframes {cls}{{0%,{a}{{{hidden}}}{b},{end}{{{shown}}}{gone},100%{{{hidden}}}}}")
    css.append(f".{cls}{{animation:{cls} {DUR}s cubic-bezier(.2,.7,.2,1) infinite}}")


body.append(f'<text x="{LOG_X}" y="44" font-family="{SANS}" font-size="17" font-weight="600" fill="#e6edf3">Loop-action bias</text>')
body.append(f'<text x="{LOG_X}" y="68" font-family="{SANS}" font-size="13" fill="{GREY}">The episode succeeds, so outcome-only scoring gives every step the same credit. Including the one that did nothing.</text>')
body.append(f'<text x="{COL_O}" y="{ROW0 - 22}" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{GREY}">OUTCOME-ONLY</text>')
body.append(f'<text x="{COL_B}" y="{ROW0 - 22}" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{ORANGE}">BRANCH-AWARE</text>')
top, bot = ROW0 - 10, ROW0 + ROWH * len(steps) - 8
for cx in (COL_O, COL_B):
    body.append(f'<line x1="{cx}" y1="{top}" x2="{cx}" y2="{bot}" stroke="#30363d"/>')

for i, (act, obs, sig, tag) in enumerate(steps):
    y = ROW0 + ROWH * i
    t = T0 + STEP_T * i
    stall = tag in ("failed", "stall")
    # highlight band behind stall rows, appears with the branch-aware verdict
    if stall:
        appear(f"hl{i}", t + 0.9)
        body.append(f'<rect class="hl{i}" x="14" y="{y - 14}" width="{W - 28}" height="{ROWH - 4}" rx="6" fill="{RED}" fill-opacity="0.07"/>')
    appear(f"a{i}", t)
    body.append(f'<g class="a{i}"><text x="{LOG_X}" y="{y + 2}" font-family="{MONO}" font-size="13.5" fill="#e6edf3"><tspan fill="{GREY}">&gt; </tspan>{act}</text>')
    obs_col = RED if stall else "#9aa5b1"
    body.append(f'<text x="{LOG_X + 16}" y="{y + 21}" font-family="{MONO}" font-size="12" fill="{obs_col}" fill-opacity="{0.85 if stall else 1}">{obs}</text></g>')

    # outcome-only: +1 for everything
    appear(f"o{i}", t + 0.45, "grow")
    css.append(f".o{i}{{transform-origin:{COL_O}px 0;transform-box:view-box}}")
    body.append(f'<rect class="o{i}" x="{COL_O}" y="{y - 6}" width="{UNIT}" height="12" rx="2" fill="{GREY}" fill-opacity="0.55"/>')
    appear(f"ol{i}", t + 0.6)
    body.append(f'<text class="ol{i}" x="{COL_O + UNIT + 8}" y="{y + 4}" font-family="{MONO}" font-size="11" fill="{GREY}">+1</text>')

    # branch-aware: verifier signal
    w = abs(sig) * UNIT
    x = COL_B if sig > 0 else COL_B - w
    col = ORANGE if sig > 0 else RED
    appear(f"b{i}", t + 0.9, "grow")
    css.append(f".b{i}{{transform-origin:{COL_B}px 0;transform-box:view-box}}")
    body.append(f'<rect class="b{i}" x="{x:.1f}" y="{y - 6}" width="{w:.1f}" height="12" rx="2" fill="{col}"/>')
    appear(f"bl{i}", t + 1.05)
    lx = COL_B + w + 8 if sig > 0 else COL_B - w - 8
    anchor = "start" if sig > 0 else "end"
    body.append(f'<text class="bl{i}" x="{lx:.1f}" y="{y + 4}" text-anchor="{anchor}" font-family="{MONO}" font-size="11" fill="{col}">{sig:+.1f}</text>')

tend = T0 + STEP_T * len(steps)
appear("fin", tend)
fy = ROW0 + ROWH * len(steps) + 16
body.append(f'<g class="fin"><text x="{LOG_X}" y="{fy}" font-family="{SANS}" font-size="13" fill="#c9d1d9">'
            f'Trained on outcome-only credit, agents learn to stall: <tspan fill="{RED}">0.24</tspan> success vs '
            f'<tspan fill="#e6edf3">0.79</tspan> untrained. Branch-aware + hindsight: <tspan fill="{ORANGE}">1.00</tspan>.</text>'
            f'<text x="{LOG_X}" y="{fy + 22}" font-family="{MONO}" font-size="10.5" fill="#5c6570">signals auto-extracted from observation text, as in the paper: arrive +0.5, inventory change +1.0, repeated "Nothing happens." -1.0</text></g>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="An ALFWorld episode scored by outcome-only and branch-aware credit assignment">
<style>
{chr(10).join(css)}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<rect width="{W}" height="{H}" rx="14" fill="#0d1117" stroke="#21262d"/>
{chr(10).join(body)}
</svg>
'''
(Path(sys.argv[1]) / "credit.svg").write_text(svg)
print("ok", len(svg) // 1024, "KB")
