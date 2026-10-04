#!/usr/bin/env python3
"""Make the 25-minute movie's English voice-over with ElevenLabs text-to-speech.

    python voiceover.py voices              list the voices your account can use
    python voiceover.py sample VOICE_ID     one short sample, to choose a voice (about 100 credits)
    python voiceover.py make VOICE_ID       all 74 segments; says the cost and asks first

The API key comes from the ELEVENLABS_API_KEY environment variable, or you're asked for it. It
is only sent to ElevenLabs, never written anywhere. Run this on your own machine; it needs
nothing but Python 3.

The script it reads is narration/en-core/manifest.csv: one row per slide of the core movie, the
text already written the way it should be spoken. It writes narration/en-core/<file>.mp3 and fills
in each row's seconds. Files already there are skipped, so an interrupted run carries on where it
stopped; delete a file (and run make again) to redo just that one. Samples go to narration/samples/,
which isn't committed. Then build.py --core --movie cuts the narrated movie.

The default model, Flash v2.5, costs about half a credit per character: about 8,300 credits for
the whole script. Multilingual v2 (--model eleven_multilingual_v2) sounds a little richer but costs
a full credit per character, about 16,600. The script checks your balance before it spends.
"""

import argparse
import csv
import getpass
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE / "narration" / "en-core"
MANIFEST = FOLDER / "manifest.csv"
SAMPLES = HERE / "narration" / "samples"
API = "https://api.elevenlabs.io/v1"
FORMAT = "mp3_44100_128"  # constant bit rate, so a file's length gives its duration
SAMPLE_STEM = "Ch05Boltzmann-06"


def api_key():
    key = os.environ.get("ELEVENLABS_API_KEY") or getpass.getpass("ElevenLabs API key (not shown): ")
    if not key.strip():
        sys.exit("No API key.")
    return key.strip()


def call(key, path, body=None, audio=False):
    req = urllib.request.Request(API + path, data=None if body is None else json.dumps(body).encode(),
                                 headers={"xi-api-key": key, "Content-Type": "application/json",
                                          "Accept": "audio/mpeg" if audio else "application/json"},
                                 method="GET" if body is None else "POST")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
                return data if audio else json.loads(data)
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:400]
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(5 * (attempt + 1))
                continue
            sys.exit(f"ElevenLabs said {e.code} for {path}: {detail}")
        except urllib.error.URLError as e:
            if attempt < 3:
                time.sleep(5 * (attempt + 1))
                continue
            sys.exit(f"Couldn't reach ElevenLabs: {e.reason}")


def rows():
    with open(MANIFEST, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_rows(table):
    with open(MANIFEST, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file", "seconds", "text"], lineterminator="\n")
        w.writeheader()
        w.writerows(table)


def credits_left(key):
    sub = call(key, "/user/subscription")
    return sub["character_limit"] - sub["character_count"]


def cost_multiplier(key, model):
    for m in call(key, "/models"):
        if m.get("model_id") == model:
            return float((m.get("model_rates") or {}).get("character_cost_multiplier", 1.0))
    sys.exit(f"No model called {model} on this account.")


def speak(key, voice, model, text, previous_text=None, next_text=None, speed=1.0):
    body = {
        "text": text,
        "model_id": model,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.0,
                           "use_speaker_boost": True, "speed": speed},
        "seed": 1947,  # the same text and settings give the same take
    }
    if "v2_5" in model:  # only the v2.5 models take a language code
        body["language_code"] = "en"
    # The neighbouring sentences keep the delivery continuous from one file to the next.
    if previous_text:
        body["previous_text"] = previous_text
    if next_text:
        body["next_text"] = next_text
    return call(key, f"/text-to-speech/{voice}?output_format={FORMAT}", body, audio=True)


def seconds_of(mp3):
    return round(mp3.stat().st_size * 8 / 128000, 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=("voices", "sample", "make"))
    ap.add_argument("voice", nargs="?", help="a voice_id from 'voices'")
    ap.add_argument("--model", default="eleven_flash_v2_5", help="default eleven_flash_v2_5 (half a credit per character)")
    ap.add_argument("--speed", type=float, default=1.0, help="0.7 to 1.2; 1.0 is the voice's own pace")
    ap.add_argument("--yes", action="store_true", help="don't ask before spending credits")
    args = ap.parse_args()
    key = api_key()

    if args.command == "voices":
        for v in sorted(call(key, "/voices")["voices"], key=lambda v: v["name"]):
            labels = ", ".join(f"{k}: {val}" for k, val in (v.get("labels") or {}).items())
            print(f"{v['voice_id']}  {v['name']:<22} {v.get('category', ''):<12} {labels}")
        print(f"\nCredits left: {credits_left(key):,}")
        return

    if not args.voice:
        sys.exit("Give a voice_id (see: python voiceover.py voices).")
    table = rows()
    mult = cost_multiplier(key, args.model)
    left = credits_left(key)

    if args.command == "sample":
        text = next(r["text"] for r in table if Path(r["file"]).stem == SAMPLE_STEM)
        print(f"Sample: {len(text)} characters, about {len(text) * mult:.0f} credits ({left:,} left).")
        SAMPLES.mkdir(parents=True, exist_ok=True)
        out = SAMPLES / f"sample-{args.voice}-{args.model}.mp3"
        out.write_bytes(speak(key, args.voice, args.model, text, speed=args.speed))
        print(f"Wrote {out.relative_to(HERE)}. Listen, then run: python voiceover.py make {args.voice}")
        return

    todo = [i for i, r in enumerate(table) if not (FOLDER / r["file"]).exists()]
    if not todo:
        print("All 74 segments are already there. Delete a file to remake it.")
        return
    chars = sum(len(table[i]["text"]) for i in todo)
    cost = chars * mult
    print(f"{len(todo)} segments to make, {chars:,} characters: about {cost:,.0f} credits with {args.model}. "
          f"You have {left:,}.")
    if cost > left:
        sys.exit("Not enough credits for all of them. Use a cheaper model, or wait for the credits to refill.")
    if not args.yes and input("Go ahead? [y/N] ").strip().lower() != "y":
        sys.exit("Nothing spent.")
    for n, i in enumerate(todo, 1):
        row = table[i]
        prev_text = table[i - 1]["text"] if i > 0 else None
        next_text = table[i + 1]["text"] if i + 1 < len(table) else None
        out = FOLDER / row["file"]
        out.write_bytes(speak(key, args.voice, args.model, row["text"], prev_text, next_text, args.speed))
        row["seconds"] = f"{seconds_of(out)}"
        save_rows(table)  # after every file, so an interrupted run keeps what it made
        print(f"  {n:2d}/{len(todo)}  {row['file']:<34} {row['seconds']:>6} s")
    total = sum(float(r["seconds"] or 0) for r in table)
    print(f"Done: {total / 60:.1f} minutes of narration. Credits left: {credits_left(key):,}.")
    print("Commit narration/en-core/ (the .mp3 files and manifest.csv) and push.")


if __name__ == "__main__":
    main()
