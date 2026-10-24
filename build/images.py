"""Swaps website pictures for the ones linked in the Google Sheet.

The 'PICTURES' rows in the Sheet hold one link per picture (a Google Drive share
link, or any direct image link). When a link changes, the picture is downloaded,
resized and saved over the old file in assets/img/. An empty cell keeps the
current picture. build/images.json remembers which link each file came from.

Run from the repo root:  python3 build/images.py
"""
import csv
import io
import json
import re
import sys
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "build" / "content.csv"
LOCK = ROOT / "build" / "images.json"

# file name -> (label in the Sheet, largest width in pixels)
PICTURES = {
    "cassandra": ("About: photo of Cassandra", 1000),
    "peppar-website": ("Header + Project 1: website screenshot", 1600),
    "peppar-instagram": ("Project 1: phone screenshot", 600),
    "pohjola-instagram": ("Header + Project 2: first phone screenshot", 600),
    "nordjobb-reel": ("Header + Project 2: second phone screenshot", 600),
    "blog-hitachi": ("Project 3: first article screenshot", 1600),
    "blog-spot": ("Project 3: second article screenshot", 1600),
}


def direct_link(url):
    """Turns a Google Drive or Dropbox share link into a download link."""
    m = re.search(r"drive\.google\.com/(?:file/d/|open\?id=|uc\?(?:.*&)?id=)([\w-]+)", url)
    if m:
        return f"https://drive.usercontent.google.com/download?id={m.group(1)}&export=download&confirm=t"
    if "dropbox.com" in url:
        return re.sub(r"([?&])dl=0", r"\1dl=1", url) if "dl=0" in url else url + ("&" if "?" in url else "?") + "dl=1"
    return url


def fetch(url):
    req = urllib.request.Request(direct_link(url), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def links():
    if not CSV.exists():
        return {}
    out = {}
    with open(CSV, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = [h.strip().lower() for h in next(reader)]
        idc = next(i for i, h in enumerate(header) if h.startswith("id"))
        en = header.index("english")
        for row in reader:
            if len(row) > idc and row[idc].strip().startswith("image."):
                name = row[idc].strip()[6:]
                link = row[en].strip() if en < len(row) else ""
                if name in PICTURES and link.startswith("http"):
                    out[name] = link
    return out


def main():
    lock = json.loads(LOCK.read_text()) if LOCK.exists() else {}
    failed = False
    for name, link in links().items():
        if lock.get(name) == link:
            continue
        try:
            im = Image.open(io.BytesIO(fetch(link)))
            im = ImageOps.exif_transpose(im).convert("RGB")
        except Exception as e:  # not an image, not shared, or not reachable
            print(f"::warning::Could not use the picture for '{PICTURES[name][0]}'. "
                  f"Check the link and that it is shared as 'Anyone with the link'. ({e})")
            failed = True
            continue
        max_w = PICTURES[name][1]
        if im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        im.save(ROOT / "assets" / "img" / f"{name}.webp", "WEBP", quality=85, method=6)
        lock[name] = link
        print(f"updated {name}.webp ({im.width}x{im.height})")
    LOCK.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n")
    return failed


if __name__ == "__main__":
    main()
