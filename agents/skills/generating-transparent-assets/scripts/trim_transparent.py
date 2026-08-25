"""Trim fully-transparent border rows/columns from an RGBA PNG.

Usage:
  python3 trim_transparent.py INPUT.png OUTPUT.png [--sides top|all] [--margin 8]

Default trims only the top (common for ground/footer assets that must stay
anchored to the other edges). --margin keeps N transparent pixels as padding.
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pngutil import decode_png, encode_png

p = argparse.ArgumentParser()
p.add_argument("input")
p.add_argument("output")
p.add_argument("--sides", choices=("top", "all"), default="top")
p.add_argument("--margin", type=int, default=8)
args = p.parse_args()

w, h, bpp, px = decode_png(args.input)
assert bpp == 4, "input must be RGBA"

def row_empty(y):
    base = y * w * 4
    return all(px[base + x * 4 + 3] == 0 for x in range(w))

def col_empty(x):
    return all(px[(y * w + x) * 4 + 3] == 0 for y in range(h))

top = 0
while top < h - 1 and row_empty(top):
    top += 1
bottom, left, right = h, 0, w
if args.sides == "all":
    while bottom > top + 1 and row_empty(bottom - 1):
        bottom -= 1
    while left < w - 1 and col_empty(left):
        left += 1
    while right > left + 1 and col_empty(right - 1):
        right -= 1

top = max(0, top - args.margin)
bottom = min(h, bottom + args.margin)
left = max(0, left - args.margin)
right = min(w, right + args.margin)

nw, nh = right - left, bottom - top
out = bytearray(nw * nh * 4)
for y in range(nh):
    src = ((y + top) * w + left) * 4
    out[y * nw * 4:(y + 1) * nw * 4] = px[src:src + nw * 4]
encode_png(args.output, nw, nh, 4, out)
print(f"saved {args.output} {nw}x{nh} (was {w}x{h}, cut top {top}, left {left})")
