"""Checks the track files and writes them into one list.

    python tools/check_tracks.py                 # check tracks/*.json
    python tools/check_tracks.py --out tracks.json

The PitLogger reads the single files from its SD card (folder tracks); the list is for other tools.
"""
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tracks")
ID = re.compile(r"^[a-z]{2}-[a-z0-9-]{2,40}$")


def gate(t, key, errors):
    g = t.get(key)
    if not isinstance(g, dict):
        errors.append(f"'{key}' missing")
        return
    lat, lon, course = g.get("lat"), g.get("lon"), g.get("course")
    if not all(isinstance(v, (int, float)) for v in (lat, lon, course)):
        errors.append(f"'{key}' needs lat, lon and course as numbers")
        return
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        errors.append(f"'{key}' is not a position")
    if not 0 <= course < 360:
        errors.append(f"'{key}'.course must be 0 ... 360")


def check(path):
    errors = []
    try:
        with open(path, encoding="utf-8") as f:
            t = json.load(f)
    except ValueError as e:
        return None, [f"not valid JSON: {e}"]
    tid = t.get("id", "")
    if not ID.match(tid):
        errors.append("'id' must look like 'de-some-track'")
    if os.path.basename(path) != tid + ".json":
        errors.append(f"file name must be {tid}.json")
    if not isinstance(t.get("name"), str) or not 0 < len(t["name"]) <= 47:
        errors.append("'name' must be 1 ... 47 characters")
    if not re.match(r"^[A-Z]{2}$", t.get("country", "")):
        errors.append("'country' must be a two-letter code")
    if not tid.startswith(t.get("country", "").lower() + "-"):
        errors.append("'id' must start with the country code")
    if t.get("type") not in ("circuit", "sprint"):
        errors.append("'type' must be 'circuit' or 'sprint'")
    gate(t, "start", errors)
    if t.get("type") == "sprint":
        gate(t, "finish", errors)
    elif "finish" in t:
        errors.append("a circuit has no 'finish' (start is start and finish)")
    if not t.get("source"):
        errors.append("'source' missing: where do the lines come from?")
    return t, errors


def main():
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    tracks, failed = [], False
    for name in sorted(os.listdir(ROOT)):
        if not name.endswith(".json"):
            continue
        t, errors = check(os.path.join(ROOT, name))
        for e in errors:
            print(f"{name}: {e}")
        failed |= bool(errors)
        if t and not errors:
            tracks.append(t)
    if len({t["id"] for t in tracks}) != len(tracks):
        print("two tracks with the same id")
        failed = True
    print(f"{len(tracks)} tracks ok" + (", errors above" if failed else ""))
    if out and not failed:
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"tracks": tracks}, f, ensure_ascii=False, indent=1)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
