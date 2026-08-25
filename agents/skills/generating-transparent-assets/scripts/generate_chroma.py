"""Generate (or regenerate) an asset on a flat chroma background via OpenRouter.

Usage:
  OPENROUTER_API_KEY=... python3 generate_chroma.py OUTPUT.png "subject prompt" [--bg green|black|magenta] [--ref IMAGE.png] [--dry-run]

With --ref, the model is told to return the reference image unchanged except for
the background swap (use this to re-key an existing render). Without --ref, it
generates the subject from scratch on the chroma background.
"""
import argparse, base64, json, os, sys, urllib.request

BGS = {
    "green": ("#00FF00", "pure solid green #00FF00, like a chroma-key green screen"),
    "magenta": ("#FF00FF", "pure solid magenta #FF00FF, like a chroma-key screen"),
    "black": ("#000000", "pure solid black #000000"),
}

p = argparse.ArgumentParser()
p.add_argument("output")
p.add_argument("prompt")
p.add_argument("--bg", choices=BGS, default="green")
p.add_argument("--ref")
p.add_argument("--model", default="openai/gpt-5.4-image-2")
p.add_argument("--dry-run", action="store_true")
args = p.parse_args()

hexcode, bgdesc = BGS[args.bg]
if args.ref:
    prompt = (
        "Give me back this exact image, unchanged, with only this edit: replace the "
        f"entire background (everything that is not the subject, including gaps inside "
        f"and between parts of the subject) with {bgdesc}. No gradient, no glow, no "
        f"noise in the background, uniform {hexcode} right up to the subject edges. "
        "Keep the subject's shapes, textures, colors and lighting exactly as they are. "
        "Same composition, same size. Subject: " + args.prompt
    )
else:
    prompt = (
        args.prompt + " The entire background must be " + bgdesc + ": no gradient, "
        f"no glow, no noise, uniform {hexcode} right up to the subject edges."
    )

if args.dry_run:
    print(prompt)
    sys.exit(0)

key = os.environ["OPENROUTER_API_KEY"]
content = [{"type": "text", "text": prompt}]
if args.ref:
    b64 = base64.b64encode(open(args.ref, "rb").read()).decode()
    content.append({"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}})

body = {"model": args.model, "modalities": ["image", "text"],
        "messages": [{"role": "user", "content": content}]}
req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps(body).encode(),
    headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
)
resp = json.load(urllib.request.urlopen(req, timeout=600))
msg = resp["choices"][0]["message"]
images = msg.get("images") or []
if not images:
    print("NO IMAGE returned. Message:", json.dumps(msg)[:1500])
    sys.exit(1)
data = base64.b64decode(images[0]["image_url"]["url"].split(",", 1)[1])
open(args.output, "wb").write(data)
print("saved", args.output, len(data), "bytes")
