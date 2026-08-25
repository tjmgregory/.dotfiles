"""Key a flat chroma background out of a render into a real-alpha PNG.

Usage:
  python3 key_chroma.py INPUT.png OUTPUT.png [--bg green|magenta|black] [--soften 1] [--checks DIR]

green/magenta: alpha from chroma dominance, spill clamped (never divides channels).
black: alpha=0 where max channel <= 6, 6px unpremultiplied edge band (only safe
when the art has no near-black; sample first).
--soften N: N passes of radius-1 box blur on alpha (2 passes ~ gaussian sigma 1.5).
--checks DIR: writes INPUT-on-white.png and INPUT-on-dark.png composites for review.
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pngutil import decode_png, encode_png


def box_blur(a, w, h, r):
    tmp = [0] * (w * h)
    for y in range(h):
        base = y * w
        s = sum(a[base:base + r + 1]) + a[base] * r
        n = 2 * r + 1
        for x in range(w):
            tmp[base + x] = s // n
            xl = max(0, x - r); xr = min(w - 1, x + r + 1)
            s += a[base + xr] - a[base + xl]
    out = [0] * (w * h)
    for x in range(w):
        s = sum(tmp[yy * w + x] for yy in range(r + 1)) + tmp[x] * r
        n = 2 * r + 1
        for y in range(h):
            out[y * w + x] = s // n
            yl = max(0, y - r); yr = min(h - 1, y + r + 1)
            s += tmp[yr * w + x] - tmp[yl * w + x]
    return out


p = argparse.ArgumentParser()
p.add_argument("input")
p.add_argument("output")
p.add_argument("--bg", choices=("green", "magenta", "black"), default="green")
p.add_argument("--soften", type=int, default=2)
p.add_argument("--checks")
args = p.parse_args()

w, h, bpp, px = decode_png(args.input)
if bpp == 4:  # flatten any (probably fake) alpha
    px = bytearray(b for i in range(w * h) for b in px[i * 4:i * 4 + 3])

alpha = [0] * (w * h)
if args.bg in ("green", "magenta"):
    # dominance: how much more chroma than subject-plausible color the px has.
    # Ramp 0..150 chosen from measured data: flat chroma sky ~210+, warm art <= 2.
    for i in range(w * h):
        r, g, b = px[i * 3], px[i * 3 + 1], px[i * 3 + 2]
        dom = (g - max(r, b)) if args.bg == "green" else (min(r, b) - g)
        if dom <= 0:
            alpha[i] = 255
        elif dom >= 150:
            alpha[i] = 0
        else:
            alpha[i] = 255 - (dom * 255 // 150)
else:
    for i in range(w * h):
        if max(px[i * 3], px[i * 3 + 1], px[i * 3 + 2]) <= 6:
            alpha[i] = 0
        else:
            alpha[i] = 255

for _ in range(max(0, args.soften)):
    alpha = box_blur(alpha, w, h, 1)

out = bytearray(w * h * 4)
for i in range(w * h):
    r, g, b = px[i * 3], px[i * 3 + 1], px[i * 3 + 2]
    if args.bg == "green":
        m = max(r, b)
        if g > m + 2:
            g = m + 2  # spill suppression; do NOT unpremultiply (causes fringes)
    elif args.bg == "magenta":
        m = g
        if r > m + 2 and b > m + 2:
            r = min(r, m + 2 + (r - b if r > b else 0))
            b = min(b, m + 2 + (b - r if b > r else 0))
    o = i * 4
    out[o], out[o + 1], out[o + 2], out[o + 3] = r, g, b, alpha[i]

encode_png(args.output, w, h, 4, out)
print("saved", args.output)

if args.checks:
    os.makedirs(args.checks, exist_ok=True)
    stem = os.path.splitext(os.path.basename(args.output))[0]
    for name, BG in (("white", (255, 255, 255)), ("dark", (14, 17, 22))):
        chk = bytearray(w * h * 3)
        for i in range(w * h):
            r, g, b, a = out[i * 4:i * 4 + 4]
            chk[i * 3] = (r * a + BG[0] * (255 - a)) // 255
            chk[i * 3 + 1] = (g * a + BG[1] * (255 - a)) // 255
            chk[i * 3 + 2] = (b * a + BG[2] * (255 - a)) // 255
        path = os.path.join(args.checks, f"{stem}-on-{name}.png")
        encode_png(path, w, h, 3, chk)
        print("check:", path)
