#!/usr/bin/env python3
"""Make the 25-minute movie's English voice-over with ElevenLabs text-to-speech.

    python voiceover.py cost                what each model would cost for the script; spends nothing
    python voiceover.py voices              the voices your account can use, and your credits
    python voiceover.py sample VOICE_ID     one segment, to choose a voice (a few hundred characters)
    python voiceover.py make VOICE_ID       all 74 segments; says the cost and asks first

The API key comes from the ELEVENLABS_API_KEY environment variable, or you're asked for it. It
is only sent to ElevenLabs, never written anywhere. Run this on your own machine; it needs
nothing but Python 3.

The script it reads is narration/en-core/manifest.csv: one row per slide of the core movie, written
the way it should be spoken, with a few audio tags in square brackets that direct the delivery:
[curious], [dry amusement], [short pause]. Eleven v4, the default, follows them (so does v3). For
any other model they're taken out before the text is sent, and the subtitles never show them.

It writes narration/en-core/<file>.mp3 and fills in each row's seconds. Files already there are
skipped, so an interrupted run carries on where it stopped; delete a file (and run make again) to
redo just that one. The voice, model and settings of the first file go in voice.json there, and make
won't mix another voice into the same narration. Samples go to narration/samples/, which isn't
committed. Then build.py --core --movie cuts the narrated movie.

What a model costs depends on your plan; `cost` asks ElevenLabs and compares it with your credits.
If the whole script doesn't fit, make --partial makes the segments that do, in order, and the same
command finishes the rest after your credits refill.
"""

import argparse
import csv
import getpass
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE / "narration" / "en-core"
MANIFEST = FOLDER / "manifest.csv"
LOCK = FOLDER / "voice.json"
SAMPLES = HERE / "narration" / "samples"
API = "https://api.elevenlabs.io/v1"
FORMAT = "mp3_44100_128"  # constant bit rate, so a file's length gives its duration
MODEL = "eleven_v4"
SAMPLE_STEM = "Ch00ColdOpen-09"
# Spelled for the ear, in what's sent only: the manifest and the subtitles keep the real spelling.
SAY = [(r"\bimec\b", "eye-mek"), (r"\bDELTA\b", "Delta"), (r"\bCFET", "C-FET")]


def untagged(text):
    """A narration line without its audio tags, as the subtitles show it."""
    return re.sub(r"\s+([,.;:?!])", r"\1", " ".join(re.sub(r"\[[^\]]*\]", " ", text).split()))


def takes_tags(model):
    return model.startswith(("eleven_v3", "eleven_v4"))


def spoken(text, model):
    text = text if takes_tags(model) else untagged(text)
    for pattern, sound in SAY:
        text = re.sub(pattern, sound, text)
    return text


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


def credits_used_and_left(key):
    sub = call(key, "/user/subscription")
    return sub["character_count"], sub["character_limit"] - sub["character_count"]


def speech_models(key):
    """{model_id: credits per character} for every model the account can speak with."""
    out = {}
    for m in call(key, "/models"):
        if m.get("can_do_text_to_speech"):
            rates = m.get("model_rates") or {}
            out[m["model_id"]] = (float(rates.get("character_cost_multiplier", 1.0))
                                  * float(rates.get("cost_discount_multiplier", 1.0)))
    return out


def costs(table, todo, model, rate):
    return [len(spoken(table[i]["text"], model)) * rate for i in todo]


def speak(key, voice, model, text, stability, speed, previous_text=None, next_text=None):
    if takes_tags(model):  # v3 and v4 have only these two settings
        if model.startswith("eleven_v3"):
            stability = min((0.0, 0.5, 1.0), key=lambda v: abs(v - stability))  # v3's three steps
        settings = {"stability": stability, "similarity_boost": 0.75}
    else:
        settings = {"stability": stability, "similarity_boost": 0.75, "style": 0.0,
                    "use_speaker_boost": True, "speed": speed}
    body = {"text": text, "model_id": model, "voice_settings": settings,
            "seed": 1947}  # the same text and settings give the same take, as far as the model allows
    if "multilingual" not in model and "monolingual" not in model:  # those don't take a language code
        body["language_code"] = "en"
    # The neighbouring lines keep the delivery continuous from one file to the next (not on v3).
    if not model.startswith("eleven_v3"):
        if previous_text:
            body["previous_text"] = previous_text
        if next_text:
            body["next_text"] = next_text
    return call(key, f"/text-to-speech/{voice}?output_format={FORMAT}", body, audio=True)


def seconds_of(mp3):
    return round(mp3.stat().st_size * 8 / 128000, 1)


def show_costs(table, todo, models, left, only_fitting=False):
    for model, rate in sorted(models.items(), key=lambda m: (not takes_tags(m[0]), sum(costs(table, todo, *m)))):
        cost = sum(costs(table, todo, model, rate))
        if only_fitting and cost > left:
            continue
        print(f"  {model:<28} {cost:>9,.0f} credits   {'fits' if cost <= left else 'too many':<9}"
              f"{'follows the tags' if takes_tags(model) else 'tags taken out'}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=("cost", "voices", "sample", "make"))
    ap.add_argument("voice", nargs="?", help="a voice_id from 'voices'")
    ap.add_argument("--model", default=MODEL, help=f"default {MODEL}; see 'cost' for the others")
    ap.add_argument("--stability", type=float, default=0.5,
                    help="0 to 1; lower is more expressive, higher more even (default 0.5)")
    ap.add_argument("--speed", type=float, default=1.0, help="0.7 to 1.2, for models without tags (v4 has no speed)")
    ap.add_argument("--segment", default=SAMPLE_STEM, help=f"for sample: which line (default {SAMPLE_STEM})")
    ap.add_argument("--partial", action="store_true", help="make what your credits cover now, the rest later")
    ap.add_argument("--yes", action="store_true", help="don't ask before spending credits")
    args = ap.parse_args()
    key = api_key()
    table = rows()
    todo = [i for i, r in enumerate(table) if not (FOLDER / r["file"]).exists()]

    if args.command == "voices":
        for v in sorted(call(key, "/voices")["voices"], key=lambda v: v["name"]):
            labels = ", ".join(f"{k}: {val}" for k, val in (v.get("labels") or {}).items())
            print(f"{v['voice_id']}  {v['name']:<22} {v.get('category', ''):<12} {labels}")
        print(f"\nCredits left: {credits_used_and_left(key)[1]:,}")
        return

    models = speech_models(key)
    left = credits_used_and_left(key)[1]
    if args.command == "cost":
        print(f"{len(todo)} of {len(table)} segments still to make. You have {left:,} credits. Each model:")
        show_costs(table, todo, models, left)
        return

    if not args.voice:
        sys.exit("Give a voice_id (see: python voiceover.py voices).")
    if args.model not in models:
        sys.exit(f"No text-to-speech model called {args.model} on this account. See: python voiceover.py cost")
    if takes_tags(args.model) and args.speed != 1.0:
        print(f"{args.model} has no speed setting; --speed is left out.")
    rate = models[args.model]

    if args.command == "sample":
        row = next((r for r in table if Path(r["file"]).stem == args.segment), None)
        if not row:
            sys.exit(f"No segment called {args.segment}; the names are in {MANIFEST.relative_to(HERE)}.")
        text = spoken(row["text"], args.model)
        print(f"Sample: {len(text)} characters, about {len(text) * rate:,.0f} credits ({left:,} left).")
        SAMPLES.mkdir(parents=True, exist_ok=True)
        out = SAMPLES / f"{args.segment}-{args.voice}-{args.model}-s{args.stability:g}.mp3"
        used = credits_used_and_left(key)[0]
        out.write_bytes(speak(key, args.voice, args.model, text, args.stability, args.speed))
        now_used, now_left = credits_used_and_left(key)
        if now_used > used:
            print(f"It used {now_used - used:,} credits; {now_left:,} left.")
        print(f"Wrote {out.relative_to(HERE)}. Listen; when you like it: python voiceover.py make {args.voice}"
              + ("" if args.model == MODEL else f" --model {args.model}")
              + ("" if args.stability == 0.5 else f" --stability {args.stability:g}"))
        return

    setup = {"voice": args.voice, "model": args.model, "stability": args.stability,
             "speed": 1.0 if takes_tags(args.model) else args.speed}
    made = len(table) - len(todo)
    if made and LOCK.exists() and json.loads(LOCK.read_text()) != setup:
        sys.exit(f"The {made} files already made used {LOCK.read_text().strip()}. Make the rest with the same "
                 f"settings, or delete narration/en-core/*.mp3 and voice.json to start over.")
    if not todo:
        print(f"All {len(table)} segments are already there. Delete a file to remake it.")
        return
    each = costs(table, todo, args.model, rate)
    print(f"{len(todo)} segments to make: about {sum(each):,.0f} credits with {args.model}. You have {left:,}.")
    if sum(each) > left:
        fit, spent = 0, 0.0
        while fit < len(each) and spent + each[fit] <= left:
            spent += each[fit]
            fit += 1
        if not args.partial or not fit:
            print("Not enough credits for all of them. These models would fit:")
            show_costs(table, todo, models, left, only_fitting=True)
            sys.exit(f"Or make the first {fit} now with --partial, and run the same command again after your "
                     "credits refill: it carries on where it stopped.")
        todo, each = todo[:fit], each[:fit]
        print(f"Making the first {fit} now, about {sum(each):,.0f} credits.")
    if not args.yes and input("Go ahead? [y/N] ").strip().lower() != "y":
        sys.exit("Nothing spent.")
    LOCK.write_text(json.dumps(setup) + "\n")
    used = credits_used_and_left(key)[0]
    for n, i in enumerate(todo, 1):
        row = table[i]
        # The neighbours are context only, so they go without tags.
        before = spoken(untagged(table[i - 1]["text"]), args.model) if i > 0 else None
        after = spoken(untagged(table[i + 1]["text"]), args.model) if i + 1 < len(table) else None
        out = FOLDER / row["file"]
        out.write_bytes(speak(key, args.voice, args.model, spoken(row["text"], args.model),
                              args.stability, args.speed, before, after))
        row["seconds"] = f"{seconds_of(out)}"
        save_rows(table)  # after every file, so an interrupted run keeps what it made
        print(f"  {n:2d}/{len(todo)}  {row['file']:<34} {row['seconds']:>6} s")
    now_used, now_left = credits_used_and_left(key)
    total = sum(float(r["seconds"] or 0) for r in table)
    print(f"Done: {total / 60:.1f} minutes of narration so far."
          + (f" That used {now_used - used:,} credits." if now_used > used else "") + f" {now_left:,} left.")
    rest = sum(1 for r in table if not (FOLDER / r["file"]).exists())
    if rest:
        print(f"{rest} segments still to make: run the same command again when your credits refill.")
    else:
        print("Commit narration/en-core/ (the .mp3 files, manifest.csv and voice.json) and push.")


if __name__ == "__main__":
    main()
