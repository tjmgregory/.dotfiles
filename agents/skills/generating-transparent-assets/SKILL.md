---
name: generating-transparent-assets
description: Generates design assets with real transparent backgrounds by prompting an image model (OpenRouter, gpt-image family) for a flat chroma-key background, then keying it out deterministically with bundled scripts. Use when the user wants a PNG asset with a transparent background, wants to remove or key out a background from AI-generated art, mentions "transparent background", "cut out", "chroma key", "green screen", or complains that a generated "transparent" image has a baked-in checkerboard.
---

# Generating Transparent Assets

Image models reached through OpenRouter chat completions CANNOT return real alpha. Asked for "transparent background", they paint a fake grey-white checkerboard into the RGB pixels. Never trust the look; verify. The reliable path is: generate on a flat chroma color, key it out locally.

All scripts are pure Python 3 stdlib (no PIL). They handle 8-bit RGB/RGBA PNGs only.

## Workflow

1. **Generate on a chroma background** (needs `OPENROUTER_API_KEY`):

   ```bash
   python3 scripts/generate_chroma.py out-greenscreen.png "warm golden lantern icon, minimal illustration" --bg green
   ```

   - `--ref existing.png` sends an image and asks for it back unchanged except the background swap. Use this to make an existing render keyable. Expect small composition drift; the model redraws.
   - `--bg green` (default) for warm/neutral art. `--bg magenta` if the art contains real greens. `--bg black` only when the art has no near-black pixels.
   - `--dry-run` prints the prompt without calling the API.
   - The prompt already demands "no gradient, no glow, no noise, uniform color up to the subject edges" — this matters; models otherwise add atmospheric glow that ruins the key.

2. **Verify the background is actually flat** before keying. Sample it:

   ```bash
   python3 -c "
   import sys; sys.path.insert(0, 'scripts')
   from pngutil import decode_png
   w,h,bpp,px = decode_png('out-greenscreen.png')
   vals=[(px[(y*w+x)*bpp+1]-max(px[(y*w+x)*bpp],px[(y*w+x)*bpp+2])) for y in range(0,h//3,9) for x in range(0,w,9)]
   print('bg green-dominance min:', min(vals))  # want >= ~180
   "
   ```

   A good green screen shows dominance 200+ in the background while warm art stays at or below ~2. If separation is poor, regenerate.

3. **Key it**:

   ```bash
   python3 scripts/key_chroma.py out-greenscreen.png asset.png --bg green --soften 2 --checks ./checks
   ```

   Writes a real-alpha PNG plus `checks/asset-on-white.png` and `checks/asset-on-dark.png`.

4. **Review the checks over BOTH backgrounds, zoomed.** Magenta/white composites expose leftover dark haze; dark composites expose bright fringes. Zoom into soft edges (hair, grass, glow) with sips:

   ```bash
   sips -c <h> <w> --cropOffset <y> <x> checks/asset-on-white.png --out zoom.png && sips -z <3h> <3w> zoom.png
   ```

5. **Trim transparent padding** (top only by default, `--sides all` for full bounding box):

   ```bash
   python3 scripts/trim_transparent.py asset.png asset.png --sides all --margin 8
   ```

## Hard-won rules

- **Fake transparency check**: `pngutil.has_real_alpha(path)` — a checkerboard-looking image with color type 2 (RGB) is fake. Also exposed via `sips -g hasAlpha`.
- **Never unpremultiply/divide channels during de-spill.** Dividing r,b by an estimated alpha inflates them and paints red fringes on edges. Keep original colors and clamp the chroma channel instead (`g = min(g, max(r,b)+2)` for green). This is what `key_chroma.py` does.
- **Chroma spill is real**: the model lights subject edges with the background color. The spill clamp removes it losslessly for art that contains no legitimate chroma-colored content. If the art legitimately contains the chroma color, switch chroma (`--bg magenta`).
- **Black backgrounds key trivially** (`max(r,g,b) <= 6` after the model returns literally pure black) but produce harder, sometimes artifacty edges around soft/thin shapes; green gives softer, cleaner edges. Prefer green.
- **Luminance cannot separate dark art from dark background** — measured overlap is total (soil p50 lum 23 vs sky-remnant p50 25). Do not attempt threshold/flood keying of dark-on-dark renders; regenerate on chroma instead. That rabbit hole is deep.
- **Soft edges**: 2 passes of radius-1 alpha box blur (~gaussian sigma 1.5) reads as a natural anti-aliased edge. More looks blurry.
- **Alpha edits that scan and write in one pass cascade** (each cleared row makes the next row a boundary). Any custom feathering must read from a snapshot of the alpha and write to a copy.
