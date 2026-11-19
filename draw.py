#!/usr/bin/env python3
"""Draw 'The World in One Image - 18 November 2026'.

A single editorial front-page image, 1024x1024 PNG, drawn with PIL only.
Deterministic: fixed geometry, no randomness, no timestamps, no network.
Run: python3 draw.py  ->  writes entry.png beside this file.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

PAPER = (246, 241, 231)
NAVY = (22, 35, 63)
RED = (163, 22, 33)
INK = (20, 20, 20)
GOLD = (198, 158, 60)
GREY = (90, 90, 90)
SEA = (24, 68, 104)
SEA_D = (16, 48, 78)
FLAME = (232, 116, 28)
SMOKE = (70, 70, 70)
GREEN = (26, 127, 75)
SAND = (234, 223, 195)
SKY = (188, 214, 232)
SUN = (242, 193, 78)
CLOUD = (255, 255, 255)
STORM = (52, 68, 92)
RAIN = (140, 170, 205)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def flow(text, face, limit):
    """Greedy word wrap; returns lines that fit inside limit pixels."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if face.getlength(trial) <= limit:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def mid(d, y, text, face, fill, x0=0, x1=W):
    w = face.getlength(text)
    d.text(((x0 + x1 - w) / 2, y), text, font=face, fill=fill)


def star5(d, cx, cy, ro, ri, fill):
    pts = []
    for i in range(10):
        r = ro if i % 2 == 0 else ri
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def puff(d, x, y, s):
    """A small flat-bottomed cloud from overlapping ellipses."""
    d.ellipse([x, y, x + 34 * s, y + 16 * s], fill=CLOUD)
    d.ellipse([x + 10 * s, y - 8 * s, x + 34 * s, y + 10 * s], fill=CLOUD)
    d.ellipse([x + 22 * s, y - 2 * s, x + 46 * s, y + 14 * s], fill=CLOUD)
    d.rectangle([x, y + 8 * s, x + 46 * s, y + 16 * s], fill=CLOUD)


def gull(d, x, y, s):
    """A tiny two-stroke gull, drawn as one polyline per wing."""
    d.line([(x, y), (x + 6 * s, y - 5 * s), (x + 12 * s, y)],
           fill=INK, width=2)
    d.line([(x + 12 * s, y), (x + 18 * s, y - 5 * s), (x + 24 * s, y)],
           fill=INK, width=2)


def tick_icon(d, idx, cx, cy):
    """One small gold icon per 'THE DAY IN BRIEF' item, centred on (cx, cy)."""
    g = GOLD
    if idx == 0:  # Kerch Bridge: arc deck with two posts
        d.arc([cx - 9, cy - 4, cx + 9, cy + 12], 180, 360, fill=g, width=2)
        d.line([cx - 9, cy + 4, cx + 9, cy + 4], fill=g, width=2)
        d.line([cx - 6, cy + 4, cx - 6, cy + 9], fill=g, width=2)
        d.line([cx + 6, cy + 4, cx + 6, cy + 9], fill=g, width=2)
    elif idx == 1:  # Nvidia chip: square die with pins on each side
        d.rectangle([cx - 6, cy - 6, cx + 6, cy + 6], outline=g, width=2)
        for px in (cx - 4, cx, cx + 4):
            d.line([px, cy - 10, px, cy - 6], fill=g, width=2)
            d.line([px, cy + 6, px, cy + 10], fill=g, width=2)
        for py in (cy - 4, cy, cy + 4):
            d.line([cx - 10, py, cx - 6, py], fill=g, width=2)
            d.line([cx + 6, py, cx + 10, py], fill=g, width=2)
    elif idx == 2:  # Myanmar verdict: scales of justice
        d.line([cx, cy - 9, cx, cy + 9], fill=g, width=2)
        d.line([cx - 9, cy - 6, cx + 9, cy - 6], fill=g, width=2)
        d.arc([cx - 11, cy - 2, cx - 3, cy + 6], 0, 180, fill=g, width=2)
        d.arc([cx + 3, cy - 2, cx + 11, cy + 6], 0, 180, fill=g, width=2)
    elif idx == 3:  # Measles: spiked virus ball
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=g)
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            d.line([(cx + 6 * math.cos(a), cy + 6 * math.sin(a)),
                    (cx + 10 * math.cos(a), cy + 10 * math.sin(a))],
                   fill=g, width=2)
    elif idx == 4:  # Ebola: three-lobed hazard mark
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=g, width=2)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=g)
        for dx, dy in [(-5, -5), (5, -5), (0, 6)]:
            d.ellipse([cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2],
                      fill=g)
    elif idx == 5:  # Senate seat: capitol dome on columns
        d.arc([cx - 8, cy - 8, cx + 8, cy + 2], 180, 360, fill=g, width=2)
        d.line([cx, cy - 10, cx, cy - 8], fill=g, width=2)
        d.line([cx - 8, cy + 2, cx + 8, cy + 2], fill=g, width=2)
        for px in (cx - 6, cx, cx + 6):
            d.line([px, cy + 2, px, cy + 9], fill=g, width=2)
        d.line([cx - 9, cy + 9, cx + 9, cy + 9], fill=g, width=2)
    else:  # Dhoni retires: cricket bat with a ball
        d.line([cx - 6, cy + 8, cx + 4, cy - 8], fill=g, width=4)
        d.line([cx - 8, cy + 6, cx - 2, cy + 10], fill=g, width=2)
        d.ellipse([cx + 4, cy + 2, cx + 10, cy + 8], fill=g)


def paint_flag(d, kind, x, y, w=84, h=50):
    """Paint a small national flag: kind is 'us', 'cn' or 'ru'."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK)
    if kind == "us":
        for i in range(7):
            if i % 2 == 0:
                sy = y + i * h / 7
                d.rectangle([x, sy, x + w, sy + h / 7], fill=(178, 34, 52))
        d.rectangle([x, y, x + w * 0.4, y + h * 0.55], fill=(30, 50, 110))
        for r in range(3):
            for c in range(4):
                px, py = x + 5 + c * 8, y + 5 + r * 8
                d.ellipse([px, py, px + 3, py + 3], fill=(255, 255, 255))
    elif kind == "cn":
        d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK)
        star5(d, x + 16, y + 15, 11, 4.5, (255, 222, 0))
        for sx, sy in [(34, 8), (42, 15), (42, 25), (34, 31)]:
            star5(d, x + sx, y + sy, 4.5, 1.8, (255, 222, 0))
    else:  # ru
        d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3],
                    fill=(0, 57, 166))
        d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def lead_art(d, x0, y0, w, h):
    """Strait of Hormuz at dusk: jets overhead, a burning tanker below."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA_D, outline=INK, width=2)
    # dusk sky: dark blue up top, burning orange at the horizon
    d.rectangle([x0 + 2, y0 + 2, x0 + w - 2, y0 + 90], fill=(28, 44, 74))
    d.rectangle([x0 + 2, y0 + 90, x0 + w - 2, y0 + 150], fill=(96, 74, 88))
    d.rectangle([x0 + 2, y0 + 150, x0 + w - 2, y0 + 168], fill=(214, 120, 58))
    # low sun sinking into the haze, right of centre
    sx, sy = x0 + w - 90, y0 + 132
    d.ellipse([sx - 26, sy - 26, sx + 26, sy + 26], fill=(242, 150, 60))
    # two fighter jets crossing the sky, with white contrails
    for jx, jy, s in [(x0 + 78, y0 + 52, 1.0), (x0 + 210, y0 + 30, 0.8)]:
        d.line([(jx - 58, jy + 18), (jx - 20, jy + 4)], fill=CLOUD, width=2)
        d.polygon([(jx, jy - 6), (jx + 26, jy), (jx, jy + 6),
                   (jx + 6, jy)], fill=(200, 200, 200))
        d.polygon([(jx - 4, jy - 12), (jx + 4, jy - 4), (jx - 2, jy)],
                  fill=(160, 160, 160))
        d.polygon([(jx - 4, jy + 12), (jx + 4, jy + 4), (jx - 2, jy)],
                  fill=(160, 160, 160))
    # a missile arcs down toward the sea, leaving a smoke trail
    mx, my = x0 + 300, y0 + 66
    pts = []
    for t in [i / 10 for i in range(11)]:
        px = x0 + 120 + t * (mx - x0 - 120)
        py = y0 + 18 + t * t * (my - y0 - 18)
        pts.append((px, py))
    d.line(pts, fill=(220, 220, 220), width=3)
    d.polygon([(mx, my - 5), (mx + 10, my), (mx, my + 5)], fill=RED)
    # the sea: deep blue with pale wave lines
    base = y0 + 168
    d.rectangle([x0 + 2, base, x0 + w - 2, y0 + h - 34], fill=SEA)
    for wy in range(base + 14, y0 + h - 40, 16):
        for wx in range(x0 + 10, x0 + w - 30, 46):
            d.arc([wx, wy, wx + 26, wy + 10], 180, 360,
                  fill=(90, 140, 180), width=2)
    # the tanker: long black hull, white bridge tower, red waterline
    hx, hy = x0 + 34, y0 + h - 92
    d.rectangle([hx, hy, hx + 300, hy + 40], fill=(18, 18, 18))
    d.rectangle([hx, hy + 32, hx + 300, hy + 40], fill=RED)
    d.rectangle([hx + 252, hy - 34, hx + 292, hy], fill=(230, 230, 230))
    d.rectangle([hx + 258, hy - 44, hx + 286, hy - 34], fill=(200, 200, 200))
    for wy in range(hy - 30, hy - 4, 9):
        d.rectangle([hx + 258, wy, hx + 264, wy + 5], fill=(40, 80, 140))
        d.rectangle([hx + 272, wy, hx + 278, wy + 5], fill=(40, 80, 140))
    # fire and smoke rising from the tanker's deck, mid-ship
    fx, fy = hx + 130, hy - 6
    for (ox, oy, r) in [(-16, -8, 12), (0, -18, 16), (16, -8, 12),
                        (-6, -30, 10), (8, -28, 9)]:
        d.ellipse([fx + ox - r, fy + oy - r, fx + ox + r, fy + oy + r],
                  fill=FLAME)
    d.ellipse([fx - 6, fy - 16, fx + 6, fy - 4], fill=(255, 214, 80))
    for (ox, oy, r) in [(-24, -44, 12), (-8, -58, 15), (12, -48, 11),
                        (2, -72, 9)]:
        d.ellipse([fx + ox - r, fy + oy - r, fx + ox + r, fy + oy + r],
                  fill=SMOKE)
    # dark band with the dateline label, clear of the flames
    d.rectangle([x0, y0 + h - 34, x0 + w, y0 + h], fill=INK)
    mid(d, y0 + h - 27, "STRAIT OF HORMUZ", fnt(SANS_B, 18),
        (255, 255, 255), x0, x0 + w)


def apec_art(d, x0, y0, w, h):
    """APEC in Shenzhen: three flags over a tech-city skyline."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SKY, outline=INK, width=2)
    d.rectangle([x0 + 2, y0 + 2, x0 + w - 2, y0 + 46], fill=(146, 190, 220))
    puff(d, x0 + 12, y0 + 14, 0.7)
    puff(d, x0 + 220, y0 + 8, 0.6)
    # three flagpoles with the US, Chinese and Russian flags
    for fx, kind in [(x0 + 22, "us"), (x0 + 128, "cn"), (x0 + 234, "ru")]:
        d.line([fx + 3, y0 + 44, fx + 3, y0 + h - 26], fill=INK, width=3)
        d.ellipse([fx, y0 + 40, fx + 6, y0 + 46], fill=GOLD)
        paint_flag(d, kind, fx + 5, y0 + 46, 64, 38)
    # tech skyline along the bottom, windows lit
    base = y0 + h
    for bx, bh in [(0, 22), (36, 34), (76, 26), (116, 40), (160, 28),
                   (200, 36), (244, 24), (284, 32)]:
        d.rectangle([x0 + bx, base - bh, x0 + bx + 34, base],
                    fill=(90, 107, 125))
        for wy in range(base - bh + 6, base - 4, 11):
            d.rectangle([x0 + bx + 6, wy, x0 + bx + 11, wy + 5],
                        fill=(242, 193, 78))
            d.rectangle([x0 + bx + 20, wy, x0 + bx + 25, wy + 5],
                        fill=(242, 193, 78))
    d.line([x0 + 116 + 17, base - 40, x0 + 116 + 17, base - 50],
           fill=INK, width=2)
    d.ellipse([x0 + 116 + 14, base - 53, x0 + 116 + 20, base - 47],
              fill=RED)
    # red carpet strip with the city name
    d.rectangle([x0, base - 26, x0 + w, base], fill=RED)
    mid(d, base - 22, "SHENZHEN", fnt(SANS_B, 16), (255, 255, 255),
        x0, x0 + w)


def ipo_art(d, x0, y0, w, h):
    """Anthropic IPO: $83 a share, bars climbing, $81.3bn raised."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(238, 244, 238),
                outline=INK, width=2)
    d.text((x0 + 12, y0 + 8), "$83", font=fnt(SANS_B, 30), fill=GREEN)
    d.text((x0 + 96, y0 + 16), "A SHARE", font=fnt(SANS_B, 18), fill=INK)
    base = y0 + h - 12
    for gy in (base - 32, base - 64, base - 96):
        d.line([x0 + 10, gy, x0 + w - 10, gy], fill=(205, 220, 205),
               width=1)
    heights = [26, 42, 58, 74, 96]
    for i, bh in enumerate(heights):
        bx = x0 + 18 + i * 58
        col = GREEN if i == 4 else (110, 168, 110)
        d.rectangle([bx, base - bh, bx + 38, base], fill=col)
        d.ellipse([bx + 15, base - bh - 4, bx + 23, base - bh + 4],
                  fill=GREEN)
    d.line([x0 + 10, base, x0 + w - 10, base], fill=INK, width=2)
    # "$81.3bn raised" chip, top right
    d.rounded_rectangle([x0 + 196, y0 + 10, x0 + w - 10, y0 + 34],
                        radius=10, fill=GREEN)
    d.text((x0 + 206, y0 + 13), "$81.3bn", font=fnt(SANS_B, 15),
           fill=(255, 255, 255))
    # red growth arrow over the bars
    d.line([x0 + 104, y0 + 72, x0 + 205, y0 + 40], fill=RED, width=4)
    d.polygon([(x0 + 205, y0 + 40), (x0 + 187, y0 + 38),
               (x0 + 197, y0 + 54)], fill=RED)
    d.text((x0 + 14, y0 + 48), "NASDAQ: ANT", font=fnt(SANS_B, 13), fill=GREEN)


def cyclone_art(d, x0, y0, w, h):
    """Cyclone Akvan: a great spiral over a rain-lashed coast."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=STORM, outline=INK, width=2)
    # the spiral: concentric arcs winding into the eye
    cx, cy = x0 + w - 92, y0 + 58
    for r, a0, a1 in [(52, 200, 470), (40, 140, 410), (28, 80, 350),
                      (16, 20, 290)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1,
              fill=(200, 215, 235), width=4)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(240, 244, 250))
    # rain slanting across the left half of the panel
    for rx in range(x0 + 12, x0 + 170, 22):
        for ry in range(y0 + 12, y0 + 76, 18):
            d.line([(rx, ry), (rx - 6, ry + 12)], fill=RAIN, width=2)
    # coastline and houses at the bottom, with an evacuation arrow
    base = y0 + h
    d.polygon([(x0, base), (x0, base - 26), (x0 + 120, base - 40),
               (x0 + 220, base - 30), (x0 + w, base - 18), (x0 + w, base)],
              fill=(44, 84, 60))
    for hx, hy in [(x0 + 18, base - 34), (x0 + 58, base - 40),
                   (x0 + 100, base - 32)]:
        d.rectangle([hx, hy, hx + 26, hy + 18], fill=(200, 170, 110))
        d.polygon([(hx - 3, hy), (hx + 13, hy - 12), (hx + 29, hy)],
                  fill=(150, 60, 50))
    d.line([x0 + 180, base - 8, x0 + 260, base - 8], fill=GOLD, width=4)
    d.polygon([(x0 + 260, base - 8), (x0 + 244, base - 16),
               (x0 + 244, base)], fill=GOLD)
    d.text((x0 + 176, base - 30), "EVACUATE", font=fnt(SANS_B, 13), fill=GOLD)


def panel(d, x0, y0, w, headline, body, art_fn):
    """One story panel: art on top, headline, then body text."""
    art_h = 130
    art_fn(d, x0, y0, w, art_h)
    ty = y0 + art_h + 10
    for line in flow(headline, fnt(SANS_B, 26), w):
        d.text((x0, ty), line, font=fnt(SANS_B, 26), fill=INK)
        ty += 30
    ty += 4
    for line in flow(body, fnt(SANS, 19), w):
        d.text((x0, ty), line, font=fnt(SANS, 19), fill=(40, 40, 40))
        ty += 24


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=NAVY, width=4)

    # masthead
    d.rectangle([0, 0, W, 88], fill=NAVY)
    mid(d, 16, "THE WORLD IN ONE IMAGE", fnt(SERIF_B, 50),
        (255, 255, 255))
    # red date band, edged with a thin gold rule
    d.rectangle([0, 88, W, 134], fill=RED)
    d.rectangle([0, 134, W, 137], fill=GOLD)
    mid(d, 96, "WEDNESDAY 18 NOVEMBER 2026", fnt(SANS_B, 34),
        (255, 255, 255))

    # lead story
    lead_art(d, 24, 146, 372, 302)
    tx = 420
    d.text((tx, 150), "WAR IN THE GULF", font=fnt(SANS_B, 22), fill=RED)
    y = 184
    for line in flow("US JETS STRIKE IRAN AS MISSILES HIT THE GULF",
                     fnt(SERIF_B, 36), 580):
        d.text((tx, y), line, font=fnt(SERIF_B, 36), fill=INK)
        y += 44
    d.line([tx, y + 6, 1000, y + 6], fill=RED, width=3)
    y += 22
    sub = ("US jets hit a Guards missile site on Qeshm Island after "
           "Iran attacked a US base in Bahrain. Iran fired on Kuwait "
           "and Bahrain; oil nears $93.")
    for line in flow(sub, fnt(SANS, 22), 580):
        d.text((tx, y), line, font=fnt(SANS, 22), fill=(40, 40, 40))
        y += 29
    d.text((tx, 416), "STRAIT OF HORMUZ  \u2022  18 NOVEMBER 2026",
           font=fnt(SANS_B, 18), fill=GREY)

    # divider
    d.line([24, 466, 1000, 466], fill=INK, width=2)

    # three panels
    panel(d, 24, 478, 320,
          "APEC OPENS IN SHENZHEN",
          "Xi chairs the meeting as Xi and Putin meet ahead of "
          "Thursday's trilateral with Trump.",
          apec_art)
    panel(d, 352, 478, 320,
          "ANTHROPIC PRICES RECORD $83 IPO",
          "Priced at $83 a share, $81.3bn raised - the biggest IPO "
          "ever. ANT starts on Nasdaq tomorrow.",
          ipo_art)
    panel(d, 680, 478, 320,
          "CYCLONE AKVAN NEARS INDIA",
          "A severe storm heads for the Andhra coast, landfall due "
          "Friday. 47,000+ evacuated in Odisha.",
          cyclone_art)

    # divider
    d.line([24, 770, 1000, 770], fill=INK, width=2)

    # ticker
    d.rectangle([0, 782, W, H], fill=NAVY)
    d.text((24, 796), "THE DAY IN BRIEF", font=fnt(SANS_B, 24), fill=GOLD)
    d.line([24, 824, 240, 824], fill=GOLD, width=2)
    # dotted world-map strip in the empty navy space, right of the heading
    dots = [(700, 760, 796, 808), (720, 745, 810, 820),
            (830, 855, 796, 804), (835, 865, 806, 820),
            (880, 970, 796, 812), (930, 960, 816, 822)]
    for mx0, mx1, my0, my1 in dots:
        for mx in range(mx0, mx1, 8):
            for my in range(my0, my1, 6):
                if (mx + my) // 8 % 3:
                    d.rectangle([mx, my, mx + 3, my + 3], fill=GOLD)
    items = [
        "Kerch Bridge hit again - part of road span collapses",
        "Nvidia's record $115.8bn quarter; board rejects Huang's return",
        "World Court to deliver Myanmar genocide verdict on Thursday",
        "US loses measles-free status after 26 years",
        "Ebola in DR Congo passes 11,000 cases",
        "Peltola wins Alaska Senate seat; Democrats take 56-44 majority",
        "MS Dhoni retires from the IPL",
    ]
    y = 832
    for i, it in enumerate(items):
        tick_icon(d, i, 34, y + 10)
        d.text((48, y), it, font=fnt(SANS, 19), fill=(255, 255, 255))
        y += 26

    img.save(OUT, format="PNG")


if __name__ == "__main__":
    main()
    print("wrote", OUT)

