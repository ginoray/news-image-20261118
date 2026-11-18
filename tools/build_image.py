#!/usr/bin/env python3
"""Render the entry image for make.fun's news-image-20261118 bounty.

The image sums up the world news of Wednesday, 18 November 2026 on one
1024x1024 newspaper-style poster: a masthead naming the day, one lead
story, eight regional/field cards and an "also today" strip. Every
story below was cross-checked against at least two independent news
reports published on 18 November 2026 (Reuters, BBC, Al Jazeera, AP and
the day's news digests that cite them).

The render is deterministic: fixed data, fixed fonts, no clock, no
network. It writes a preview at assets/entry.png and the shipped
asset at assets/entry.png.b64 (the same PNG, base64-encoded on one
line, so the repository stays plain text); the shipped program
(main.py) decodes that asset and writes /output/entry.png.
"""

import base64
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "entry.png"
OUT_B64 = ROOT / "assets" / "entry.png.b64"

FONT_DIR = Path("/usr/share/fonts/truetype/liberation")
SERIF_BOLD = str(FONT_DIR / "LiberationSerif-Bold.ttf")
SANS = str(FONT_DIR / "LiberationSans-Regular.ttf")
SANS_BOLD = str(FONT_DIR / "LiberationSans-Bold.ttf")

PAPER = (250, 246, 238)
CARD = (255, 253, 246)
INK = (23, 32, 54)
GREY = (84, 88, 96)
NAVY = (20, 38, 63)
GOLD = (227, 179, 65)
RED = (179, 35, 42)
BORDER = (216, 210, 196)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


LEAD = {
    "kicker": "APEC SUMMIT · SHENZHEN, CHINA",
    "headline": "Xi urges open trade as Trump and Putin arrive for summit talks",
    "sub": "The three leaders meet Thursday on trade, AI and two wars.",
}

CARDS = [
    ("MIDDLE EAST", (179, 35, 42),
     "US hits Iran's Qeshm Island; Iran drones Bahrain & Kuwait"),
    ("UKRAINE WAR", (64, 92, 140),
     "Ukrainian strike collapses part of Kerch Bridge"),
    ("AMERICAS", (46, 110, 78),
     "Peltola flips Alaska — Democrats reach 56 Senate seats"),
    ("HEALTH", (122, 78, 158),
     "US loses measles-free status after 26 years"),
    ("AFRICA", (178, 106, 27),
     "Ebola in DR Congo doubles — 11,000 cases, UN says"),
    ("EUROPE", (64, 92, 140),
     "EU fast-tracks permits for clean energy and grids"),
    ("MARKETS", (31, 122, 109),
     "Shares slide on Fed fears; Nvidia's sales double"),
    ("CULTURE", (160, 58, 107),
     "GTA VI goes on sale worldwide at midnight"),
]

ALSO = ("Cyclone Xavier, a Category-5 storm, hits the Cook Islands · "
        "Russian military plane crash in Siberia kills 19 · "
        "Deadly cold grips Gaza's tent camps")
SOURCES = "Compiled from reports by Reuters, BBC, Al Jazeera and AP — 18 November 2026"


def draw_masthead(draw):
    draw.rectangle([0, 0, W, 148], fill=NAVY)
    centered(draw, W / 2, 18, "THE WORLD TODAY", font(SERIF_BOLD, 63), (255, 255, 255))
    centered(draw, W / 2, 94, "Wednesday, 18 November 2026", font(SANS_BOLD, 37), GOLD)
    draw.rectangle([0, 148, W, 154], fill=GOLD)


def draw_lead(draw):
    x0, y0, x1, y1 = 24, 166, W - 24, 352
    draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=BORDER, width=2)
    draw.rectangle([x0, y0, x0 + 10, y1], fill=RED)
    tx = x0 + 30
    draw.text((tx, y0 + 13), LEAD["kicker"], font=font(SANS_BOLD, 26), fill=RED)
    y = y0 + 46
    for line in wrap(draw, LEAD["headline"], font(SANS_BOLD, 42), x1 - tx - 20):
        draw.text((tx, y), line, font=font(SANS_BOLD, 42), fill=INK)
        y += 48
    draw.text((tx, y0 + 148), LEAD["sub"], font=font(SANS, 24), fill=GREY)


def draw_card(draw, x0, y0, x1, y1, tag, color, headline):
    draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=BORDER, width=2)
    draw.rectangle([x0, y0, x1, y0 + 6], fill=color)
    chip_f = font(SANS_BOLD, 20)
    tw = draw.textlength(tag, font=chip_f)
    draw.rectangle([x0 + 14, y0 + 16, x0 + 14 + tw + 18, y0 + 46], fill=color)
    draw.text((x0 + 23, y0 + 20), tag, font=chip_f, fill=(255, 255, 255))
    y = y0 + 54
    for line in wrap(draw, headline, font(SANS_BOLD, 27), x1 - x0 - 28):
        draw.text((x0 + 14, y), line, font=font(SANS_BOLD, 27), fill=INK)
        y += 32


def draw_footer(draw):
    y = 938
    draw.text((24, y), "ALSO TODAY", font=font(SANS_BOLD, 22), fill=RED)
    tx = 24 + draw.textlength("ALSO TODAY  ", font=font(SANS_BOLD, 22))
    lines = wrap(draw, ALSO, font(SANS, 22), W - tx - 24)
    rest = ALSO
    if lines:
        draw.text((tx, y), lines[0], font=font(SANS, 22), fill=INK)
        rest = ALSO[len(lines[0]):].strip()
    for i, line in enumerate(wrap(draw, rest, font(SANS, 22), W - 48)[:1]):
        draw.text((24, y + 27), line, font=font(SANS, 22), fill=INK)
    centered(draw, W / 2, 994, SOURCES, font(SANS, 20), GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead(draw)
    grid_top, card_h, gap = 364, 133, 10
    col_w = (W - 48 - gap) // 2
    for i, (tag, color, headline) in enumerate(CARDS):
        row, col = divmod(i, 2)
        x0 = 24 + col * (col_w + gap)
        y0 = grid_top + row * (card_h + gap)
        draw_card(draw, x0, y0, x0 + col_w, y0 + card_h, tag, color, headline)
    draw_footer(draw)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    OUT_B64.write_text(base64.b64encode(OUT.read_bytes()).decode("ascii") + "\n",
                       encoding="ascii")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, {W}x{H})")
    print(f"wrote {OUT_B64} ({OUT_B64.stat().st_size} bytes, base64)")


if __name__ == "__main__":
    main()
