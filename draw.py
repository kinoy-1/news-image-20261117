#!/usr/bin/env python3
"""Draw the news-image-20261117 round-2 entry: "THE WORLD, MAPPED".

A 1024x1024 editorial front page summing up Tuesday 17 November 2026 in
35 stories: 3 features, 6 cards, a numbers strip and a 26-item "also"
list, plus a dot-matrix world map with numbered pins. Pure PIL, fully
deterministic: no randomness, no clock, no network.

Run:  python3 draw.py [out.png]     (default: entry.png)
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- palette ---------------------------------------------------------------
PAPER = (246, 241, 231)    # warm cream page
OXBLOOD = (74, 20, 32)     # masthead
GOLD = (192, 138, 43)      # rules and accents
INK = (26, 26, 26)         # main text
GREY = (90, 90, 90)        # secondary text
RED = (179, 38, 30)        # pins and numbers
NAVY = (22, 35, 61)        # map panel
DOT = (232, 223, 200)      # map dots
CREAM = (246, 241, 231)
CARD_BG = (252, 250, 244)
CARD_LINE = (216, 205, 184)
SKY = (214, 226, 238)
SEA = (47, 93, 138)

KICK = {
    "conflict": (158, 43, 37),
    "diplomacy": (31, 78, 95),
    "markets": (30, 107, 74),
    "tech": (91, 78, 138),
    "weather": (47, 93, 138),
    "culture": (138, 109, 31),
}

# --- fonts -----------------------------------------------------------------
DJ = "/usr/share/fonts/truetype/dejavu"
LB = "/usr/share/fonts/truetype/liberation"


def _f(path, size):
    return ImageFont.truetype(path, size)


def serif_b(s):
    return _f(f"{DJ}/DejaVuSerif-Bold.ttf", s)


def sans_b(s):
    return _f(f"{DJ}/DejaVuSans-Bold.ttf", s)


def sans(s):
    return _f(f"{DJ}/DejaVuSans.ttf", s)


def serif_i(s):
    return _f(f"{LB}/LiberationSerif-Italic.ttf", s)


# --- world landmask: 72 x 36 equirectangular grid, 5 degrees per cell ------
# Row r covers latitude 90-5r down to 85-5r; column c covers longitude
# -180+5c to -175+5c. Spans are (first, last) inclusive column per row,
# sketched from a plain atlas: North America cols 2-25, South America
# 20-29, Europe 34-44, Africa 33-46, Asia 44-71, Australia 59-66.
LAND = {
    0: [(26, 28)],
    1: [(26, 29)],
    2: [(19, 21), (26, 30)],
    3: [(18, 22), (25, 30)],
    4: [(17, 23), (25, 30), (38, 41)],
    5: [(3, 7), (11, 17), (25, 30), (48, 71)],
    6: [(2, 8), (10, 20), (25, 30), (32, 33), (37, 42), (48, 71)],
    7: [(2, 9), (10, 22), (25, 29), (35, 42), (47, 71)],
    8: [(3, 10), (11, 24), (26, 28), (35, 42), (46, 71)],
    9: [(4, 11), (12, 26), (36, 37), (40, 42), (46, 71)],
    10: [(6, 10), (12, 26), (40, 43), (46, 71)],
    11: [(11, 25), (41, 44), (46, 71)],
    12: [(11, 25), (41, 71)],
    13: [(11, 25), (41, 71)],
    14: [(11, 24), (41, 71)],
    15: [(11, 23), (41, 48), (50, 53), (55, 62)],
    16: [(12, 23), (41, 48), (50, 53), (54, 63)],
    17: [(12, 23), (41, 48), (50, 53), (54, 63)],
    18: [(13, 22), (41, 48), (50, 52), (54, 57), (58, 63)],
    19: [(13, 22), (42, 48), (50, 52), (54, 57), (59, 63)],
    20: [(14, 21), (42, 48), (50, 52), (55, 57), (59, 62)],
    21: [(15, 22), (42, 48), (50, 52), (55, 57), (59, 62)],
    22: [(16, 22), (43, 48), (51, 52), (55, 57), (59, 62)],
    23: [(18, 22), (43, 48), (55, 56), (59, 62)],
    24: [(19, 22), (43, 47), (59, 62)],
    25: [(20, 23), (43, 46), (59, 63), (69, 70)],
    26: [(21, 24), (44, 46), (59, 64), (69, 70)],
    27: [(21, 25), (44, 46), (59, 64)],
    28: [(22, 26), (45, 46), (60, 65)],
    29: [(22, 27), (45, 46), (60, 65)],
    30: [(23, 27), (45, 46), (60, 65)],
    31: [(23, 27), (60, 65)],
    32: [(24, 27), (60, 65)],
    33: [(24, 27), (61, 64)],
    34: [(25, 26), (61, 64)],
    35: [(25, 26)],
}

# Pin positions in grid coords (col, row) for stories 1-9.
# col = (lon + 180) / 5, row = (90 - lat) / 5.
PINS = {
    1: (43, 9),    # Kerch Strait / Crimea bridge
    2: (50, 13),   # Bahrain / Gulf
    3: (60, 15),   # Manila
    4: (21, 10),   # Washington DC (Pentagon)
    5: (62, 11),   # Okinoshima, Japan
    6: (43, 12),   # Jerusalem (Knesset)
    7: (16, 12),   # West Texas (measles outbreak origin)
    8: (57, 8),    # Ulaanbaatar, Mongolia
    9: (45, 15),   # Aden, Yemen
}

# --- story data: every item verified from Reuters / AP / The Hill / CDC --
# on 17 November 2026. Features 1-3, cards 4-9, numbers strip, also 10-35.
# features: (number, kicker, family, headline, summary)
FEATURES = [
    (1, "EUROPE · WAR IN UKRAINE", "conflict",
     "Ukraine hits the Crimea bridge a second day",
     "Kyiv struck the Kerch span again as Russia hit Kyiv's Dnipro "
     "bridges; Moscow claims a record 1,441 drones downed."),
    (2, "MIDDLE EAST · GULF", "conflict",
     "Iran fires drones at a US base in Bahrain",
     "Drones aimed at the Sheikh Isa radar site were intercepted; "
     "tankers were hit by mines near the Strait of Hormuz."),
    (3, "ASIA · DIPLOMACY", "diplomacy",
     "Trump lands in Manila to open his Asia trip",
     "Trump met regional partners at the ASEAN summit ahead of "
     "Thursday's Xi–Putin trilateral."),
]

# cards: (number, kicker, family, headline, summary, icon)
CARDS = [
    (4, "UNITED STATES · DEFENCE", "conflict",
     "Pentagon fails its ninth audit in a row",
     "Auditors could not verify accounts covering $4.8 trillion "
     "in assets.", "ledger"),
    (5, "ASIA-PACIFIC · DEFENCE", "diplomacy",
     "Japan scrambles jets as Russian planes enter",
     "Two suspected Russian aircraft violated Japanese airspace "
     "near Okinoshima.", "jet"),
    (6, "MIDDLE EAST · POLITICS", "diplomacy",
     "Knesset picks Kahana as speaker, 66–52",
     "Eisenkot's bloc installs a speaker opposed to Netanyahu's "
     "agenda; a new government is still unformed.", "parliament"),
    (7, "UNITED STATES · HEALTH", "tech",
     "US loses measles-free status after 26 years",
     "PAHO revoked the status as 2026 cases passed 5,412 — the "
     "most since 1991; the CDC pushes MMR shots.", "health"),
    (8, "ASIA · POLITICS", "diplomacy",
     "Mongolia's president resigns over graft claims",
     "Khürelsükh steps down over embezzlement claims tied to a "
     "railway project.", "scroll"),
    (9, "MIDDLE EAST · WAR IN YEMEN", "conflict",
     "Houthis advance as Yemeni forces pull back",
     "Government troops withdrew from the Red Sea coast to "
     "defend Aden against the rapid Houthi push.", "arrow"),
]

# numbers strip: (big figure, label)
NUMBERS = [
    ("1,441", "Drones Moscow says it downed — a record"),
    ("66–52", "Knesset vote that made Kahana speaker"),
    ("$4.8tn", "Pentagon assets auditors could not verify"),
    ("5,412", "US measles cases in 2026, as of 12 Nov"),
]

# "also" list, items 10-35: (number, one-line story)
ALSO = [
    (10, "France: 146,000 join a public-sector strike"),
    (11, "North Macedonia, Greece foil an Iran-linked plot"),
    (12, "US tightens AI-chip export curbs; tech shares slide"),
    (13, "Nvidia reports after the bell; board keeps Huang out"),
    (14, "UK sanctions eight Israeli settlement firms"),
    (15, "West urges Israel to open Gaza aid crossings"),
    (16, "NSA internal network goes down in maintenance"),
    (17, "White House pulls FDA nominee Heidi Overton"),
    (18, "China and Canada widen tariff relief"),
    (19, "Malaysia signs first minerals pact with France"),
    (20, "Depardieu pleads guilty to sexual assault in Paris"),
    (21, "Bolivia's García Linera confirms asylum in Mexico"),
    (22, "UN: 372 civilians killed in Ukraine in October"),
    (23, "US seeks $50.1bn to rebuild air traffic control"),
    (24, "UK gives £240m more for Ukraine's air defence"),
    (25, "Quad plans a joint maritime exercise for 2027"),
    (26, "Sudan: UN counts over 2,230 civilian deaths"),
    (27, "Prague: two passenger trains collide, riders hurt"),
    (28, "Serbia: pilot killed in a MiG-29 crash"),
    (29, "Melbourne Cup horse found dead; inquiry opened"),
    (30, "Oil prices slide on glut fears"),
    (31, "Cuba's fuel crisis turns into a US export boon"),
    (32, "Sweden gets another week of government talks"),
    (33, "All 19 crew rescued from the Gas Husky"),
    (34, "Trump brushes off the NSA outage: 'it's like that'"),
    (35, "GTA VI is almost here — AP previews the launch"),
]

# --- text helpers ----------------------------------------------------------
def _w(fnt, s):
    b = fnt.getbbox(s)
    return b[2] - b[0]


def wrap(fnt, text, max_w):
    """Greedy word wrap; every returned line fits max_w."""
    out, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if _w(fnt, trial) <= max_w or not cur:
            cur = trial
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def put_lines(d, x, y, lines, fnt, fill, step=None):
    """Draw lines top-left; returns the y just below the block."""
    if step is None:
        step = int(fnt.size * 1.18)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += step
    return y


def fit(fnt, text, max_w, max_lines):
    """Wrap to at most max_lines; ellipsize the last line if it overflows."""
    lines = wrap(fnt, text, max_w)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    while lines and _w(fnt, lines[-1] + "…") > max_w:
        lines[-1] = lines[-1][:-1].rstrip()
    lines[-1] = lines[-1].rstrip() + "…"
    return lines


def tracked(d, x, y, text, fnt, fill, gap=2):
    """Draw text with extra letter spacing; returns the width used."""
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=fnt, fill=fill)
        cx += _w(fnt, ch) + gap
    return cx - x - gap


# --- map -------------------------------------------------------------------
def draw_map(d, x0, y0, w, h):
    """Navy panel, cream dot-matrix world map, numbered red pins."""
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=10, fill=NAVY)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=10,
                        outline=GOLD, width=1)
    lab = "WHERE THE NEWS HAPPENED — NUMBERS MATCH THE STORIES"
    lf = sans_b(11)
    d.text((x0 + (w - _w(lf, lab)) // 2, y0 + 10), lab, font=lf,
           fill=(200, 190, 160))
    mx, my = x0 + 12, y0 + 34
    mw, mh = w - 24, h - 46
    cw, ch = mw / 72.0, mh / 36.0
    for r, spans in LAND.items():
        cy = my + (r + 0.5) * ch
        for a, b in spans:
            for c in range(a, b + 1):
                cx = mx + (c + 0.5) * cw
                d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=DOT)
    pf = sans_b(11)
    for num, (gc, gr) in sorted(PINS.items()):
        px = mx + (gc + 0.5) * cw
        py = my + (gr + 0.5) * ch
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=CREAM, width=2)
        s = str(num)
        d.text((px - _w(pf, s) / 2, py - 7), s, font=pf, fill=CREAM)


# --- flat vector illustrations for the three features (96 x 94) ------------
def illo_bridge(d, x, y, w, h):
    """Kerch bridge at dawn: sky, sea, towers, a deck with a gap."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + int(h * 0.60), x + w, y + h], fill=SEA)
    d.ellipse([x + 68, y + 6, x + 88, y + 26], fill=(240, 217, 168))
    # towers
    d.rectangle([x + 16, y + 20, x + 21, y + int(h * 0.60)], fill=OXBLOOD)
    d.rectangle([x + w - 21, y + 20, x + w - 16, y + int(h * 0.60)],
                fill=OXBLOOD)
    # deck: left half level, right half dropped into the water
    d.rectangle([x + 4, y + 32, x + w // 2 - 4, y + 38], fill=OXBLOOD)
    d.polygon([(x + w // 2 + 6, y + 40), (x + w - 6, y + 56),
               (x + w - 6, y + 62), (x + w // 2 + 6, y + 46)], fill=OXBLOOD)
    # smoke over the gap
    for sx, sy, r in ((44, 30, 5), (52, 24, 6), (60, 30, 4)):
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                  fill=(120, 120, 120))
    # wave marks
    for dx in (-8, 0, 8):
        d.arc([x + w // 2 + dx - 8, y + int(h * 0.68),
               x + w // 2 + dx + 8, y + int(h * 0.82)], 180, 360,
              fill=CREAM, width=2)
    # cables
    d.line([x + 18, y + 22, x + 44, y + 34], fill=INK, width=1)
    d.line([x + w - 18, y + 22, x + w - 44, y + 34], fill=INK, width=1)


def illo_drones(d, x, y, w, h):
    """Night over the Gulf: dark sky, moon, radar sweep, drone silhouettes."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for sx, sy in ((10, 12), (28, 24), (70, 10), (56, 20), (84, 28), (42, 8)):
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=DOT)
    d.ellipse([x + w - 30, y + 8, x + w - 10, y + 28], fill=(232, 223, 200))
    # radar arcs from bottom-left
    for r in (20, 34, 48):
        d.arc([x - r, y + h - r, x + r, y + h + r], 270, 360,
              fill=(120, 180, 120), width=2)
    d.line([x + 4, y + h - 6, x + 38, y + h - 44], fill=(120, 200, 120),
           width=2)
    # two drone silhouettes
    for jx, jy, s in ((52, 40, 1.0), (74, 58, 0.7)):
        d.line([x + jx - 12 * s, y + jy, x + jx + 12 * s, y + jy],
               fill=CREAM, width=2)
        d.line([x + jx, y + jy - 9 * s, x + jx, y + jy + 9 * s],
               fill=CREAM, width=2)
        d.ellipse([x + jx - 4 * s, y + jy - 4 * s, x + jx + 4 * s,
                   y + jy + 4 * s], fill=RED)
    # interceptor burst
    d.ellipse([x + 30, y + 62, x + 42, y + 74], outline=GOLD, width=2)


def illo_manila(d, x, y, w, h):
    """Manila bay at dusk: sun, skyline, three flag poles."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 217, 168))
    d.ellipse([x + 64, y + 6, x + 88, y + 30], fill=(232, 170, 60))
    d.rectangle([x, y + int(h * 0.72), x + w, y + h], fill=(120, 150, 180))
    heights = [40, 58, 34, 66, 48, 30, 54]
    bx = x + 4
    for hh in heights:
        bw = (w - 8) // len(heights)
        d.rectangle([bx, y + h - hh, bx + bw - 3, y + h], fill=OXBLOOD)
        for wy in range(y + h - hh + 6, y + h - 4, 9):
            d.rectangle([bx + 3, wy, bx + 5, wy + 3], fill=GOLD)
        bx += bw
    # three small stripe flags: US, China, Philippines
    flags = (((179, 38, 30), (246, 241, 231), (31, 78, 95)),
             ((222, 32, 32), (255, 220, 60)),
             ((246, 241, 231), (31, 78, 95), (179, 38, 30)))
    for i, cols in enumerate(flags):
        px = x + 14 + i * 32
        d.line([px, y + 8, px, y + 30], fill=INK, width=2)
        for j, c in enumerate(cols):
            d.rectangle([px + 2, y + 8 + j * 6, px + 16, y + 8 + j * 6 + 6],
                        fill=c)
        d.ellipse([px + 6, y + 12, px + 8, y + 14], fill=GOLD)


ILLOS = {1: illo_bridge, 2: illo_drones, 3: illo_manila}


# --- small card icons (54 x 54 on a navy tile) ------------------------------
def icon_tile(d, x, y, kind):
    d.rounded_rectangle([x, y, x + 54, y + 54], radius=7, fill=NAVY)
    fg, ac = CREAM, GOLD
    if kind == "ledger":
        d.rectangle([x + 12, y + 10, x + 42, y + 44], outline=fg, width=2)
        d.line([x + 12, y + 18, x + 42, y + 18], fill=fg, width=2)
        for yy in (24, 30, 36):
            d.line([x + 16, y + yy, x + 30, y + yy], fill=fg, width=2)
        d.line([x + 32, y + 40, x + 40, y + 32], fill=RED, width=3)
        d.line([x + 32, y + 32, x + 40, y + 40], fill=RED, width=3)
    elif kind == "jet":
        d.ellipse([x + 8, y + 8, x + 24, y + 24], fill=RED)
        d.polygon([(x + 14, y + 34), (x + 46, y + 24), (x + 14, y + 30),
                   (x + 22, y + 28), (x + 18, y + 42), (x + 12, y + 30)],
                  fill=fg)
    elif kind == "parliament":
        d.polygon([(x + 8, y + 22), (x + 27, y + 10), (x + 46, y + 22)],
                  fill=ac)
        for i in range(3):
            bx = x + 12 + i * 12
            d.rectangle([bx, y + 24, bx + 6, y + 42], fill=fg)
        d.rectangle([x + 8, y + 42, x + 46, y + 46], fill=fg)
    elif kind == "health":
        d.ellipse([x + 8, y + 8, x + 46, y + 46], outline=fg, width=2)
        d.rectangle([x + 23, y + 15, x + 31, y + 39], fill=RED)
        d.rectangle([x + 15, y + 23, x + 39, y + 31], fill=RED)
    elif kind == "scroll":
        d.rectangle([x + 12, y + 10, x + 42, y + 44], outline=fg, width=2)
        d.line([x + 16, y + 18, x + 38, y + 18], fill=ac, width=2)
        for yy in (25, 31, 37):
            d.line([x + 16, y + yy, x + 34, y + yy], fill=fg, width=2)
        d.ellipse([x + 36, y + 38, x + 44, y + 46], fill=RED)
    elif kind == "arrow":
        d.line([x + 12, y + 16, x + 42, y + 40], fill=fg, width=3)
        d.polygon([(x + 42, y + 40), (x + 30, y + 40), (x + 42, y + 28)],
                  fill=RED)
        d.line([x + 10, y + 44, x + 30, y + 44], fill=(140, 180, 220),
               width=2)

# --- layout ------------------------------------------------------------------
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead 0-118 (oxblood) ---
    d.rectangle([0, 0, W, 118], fill=OXBLOOD)
    tracked(d, 24, 16, "THE WORLD, MAPPED", sans_b(19), GOLD, gap=3)
    count = "35 STORIES · 6 CONTINENTS · ONE PAGE"
    cf = sans_b(13)
    d.text((W - 24 - _w(cf, count), 18), count, font=cf, fill=GOLD)
    date = "Tuesday 17 November 2026"
    df = serif_b(46)
    d.text(((W - _w(df, date)) // 2, 40), date, font=df, fill=CREAM)
    sub = "Every story on this page happened, or was first reported, on this day."
    sf = serif_i(14)
    d.text(((W - _w(sf, sub)) // 2, 94), sub, font=sf, fill=(214, 200, 170))
    d.rectangle([0, 118, W, 121], fill=GOLD)

    # --- zone A 122-420: map hero + 3 features ---
    draw_map(d, 24, 130, 596, 282)
    fx, fw = 636, 364
    for i, (num, kicker, fam, head, summ) in enumerate(FEATURES):
        y = 122 + i * 100
        ILLOS[num](d, fx, y + 2, 96, 92)
        d.rectangle([fx, y + 2, fx + 96, y + 94], outline=CARD_LINE, width=1)
        tx, tw = fx + 108, fw - 108
        kf = sans_b(10)
        d.text((tx, y + 4), kicker, font=kf, fill=KICK[fam])
        hf = serif_b(16)
        hl = fit(hf, head, tw, 2)
        yy = put_lines(d, tx, y + 20, hl, hf, INK, step=19)
        sf2 = sans(12)
        sl = fit(sf2, summ, tw, 3)
        put_lines(d, tx, yy + 2, sl, sf2, GREY, step=15)
        # red number badge on the illustration corner
        bf2 = sans_b(12)
        d.ellipse([fx + 2, y + 4, fx + 22, y + 24], fill=RED,
                  outline=CREAM, width=1)
        s = str(num)
        d.text((fx + 12 - _w(bf2, s) / 2, y + 8), s, font=bf2, fill=CREAM)
    d.line([24, 421, 1000, 421], fill=OXBLOOD, width=2)

    # --- zone B 424-694: 6 cards, 3 x 2 ---
    cw2, ch2 = 320, 131
    for i, (num, kicker, fam, head, summ, icon) in enumerate(CARDS):
        cx = 24 + (i % 3) * (cw2 + 8)
        cy = 424 + (i // 3) * (ch2 + 8)
        d.rounded_rectangle([cx, cy, cx + cw2, cy + ch2], radius=6,
                            fill=CARD_BG, outline=CARD_LINE, width=1)
        icon_tile(d, cx + 12, cy + 12, icon)
        bf2 = sans_b(11)
        d.ellipse([cx + 54, cy + 8, cx + 72, cy + 26], fill=RED,
                  outline=CREAM, width=1)
        s = str(num)
        d.text((cx + 63 - _w(bf2, s) / 2, cy + 11), s, font=bf2, fill=CREAM)
        tx, tw = cx + 76, cw2 - 88
        kf = sans_b(10)
        d.text((tx, cy + 10), kicker, font=kf, fill=KICK[fam])
        hf = serif_b(15)
        hl = fit(hf, head, tw, 2)
        yy = put_lines(d, tx, cy + 26, hl, hf, INK, step=18)
        sf2 = sans(12)
        sl = fit(sf2, summ, tw, 3)
        put_lines(d, tx, yy + 3, sl, sf2, GREY, step=15)
    d.line([24, 695, 1000, 695], fill=OXBLOOD, width=2)

    # --- zone C 698-758: BY THE NUMBERS ---
    nf = sans_b(11)
    d.text((24, 702), "BY THE NUMBERS", font=nf, fill=GREY)
    col_w = 244
    for i, (big, label) in enumerate(NUMBERS):
        x = 24 + i * col_w
        bf3 = serif_b(28)
        d.text((x, 710), big, font=bf3, fill=OXBLOOD)
        lf = sans(11)
        d.text((x, 746), label, font=lf, fill=GREY)
    d.line([24, 761, 1000, 761], fill=OXBLOOD, width=2)

    # --- zone D 762-1000: ALSO list, 2 columns x 13 rows ---
    hf = sans_b(15)
    d.text((24, 769),
           "ALSO ON TUESDAY 17 NOVEMBER — 26 MORE STORIES",
           font=hf, fill=OXBLOOD)
    af = sans(11)
    anf = sans_b(11)
    col_x = [24, 524]
    y0 = 791
    for i, (num, text) in enumerate(ALSO):
        col, row = i // 13, i % 13
        x = col_x[col]
        y = y0 + row * 16
        ns = f"{num}. "
        d.text((x, y), ns, font=anf, fill=RED)
        d.text((x + _w(anf, ns), y), text, font=af, fill=INK)

    # --- footer 1000-1022 ---
    ff = sans(10)
    foot = ("Sources: Reuters, Associated Press, The Hill, CDC, BBC, "
            "United Nations  ·  All events of Tuesday 17 November 2026  ·  "
            "Drawn entirely by code; no photographs.")
    d.text(((W - _w(ff, foot)) // 2, 1006), foot, font=ff, fill=GREY)
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = render()
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} {os.path.getsize(out)} bytes {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
