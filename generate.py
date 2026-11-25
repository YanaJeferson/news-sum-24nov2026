"""Render entry.png: an editorial front page summing up Tuesday 24 November 2026.

Authoring tool only. The graded program is main.ts, which copies entry.png.
Run: /tmp/imgvenv/bin/python generate.py
"""
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
PAPER = (242, 235, 221)
INK = (20, 17, 15)
RED = (200, 39, 30)
MUTED = (107, 98, 90)
CREAM = (245, 239, 226)

SERIF_B = "/usr/share/fonts/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def text(x, y, s, f, fill=INK):
    d.text((x, y), s, font=f, fill=fill)


def wrap(s, f, width):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(x, y, s, f, width, leading, fill=INK):
    for line in wrap(s, f, width):
        text(x, y, line, f, fill)
        y += leading
    return y


# ---------------------------------------------------------------- header
text(30, 18, "THE WORLD TODAY", font(SERIF_B, 60))
text(748, 14, "24", font(SANS_B, 74), RED)
text(838, 30, "NOV", font(SANS_B, 30), INK)
text(838, 60, "2026", font(SANS_B, 30), INK)
text(30, 96, "TUESDAY 24 NOVEMBER 2026   ·   ONE DAY OF WORLD NEWS", font(SANS_B, 21), RED)
d.rectangle([30, 132, 994, 135], fill=INK)
d.rectangle([30, 135, 994, 139], fill=RED)

# ---------------------------------------------------------------- tiles
MARGE, GAP = 30, 14
TW = (W - 2 * MARGE - 2 * GAP) // 3  # 310
ROW1, ROW2, TH = 152, 516, 350
ICON_H = 160


def tile(x, y, bg, region, headline, detail, icon):
    d.rectangle([x, y, x + TW, y + TH], fill=CREAM)
    d.rectangle([x, y, x + TW, y + ICON_H], fill=bg)
    icon(x, y)
    # region tag
    text(x + 16, y + ICON_H + 12, region, font(SANS_B, 14), RED)
    # headline
    fh = font(SANS_B, 30)
    yy = y + ICON_H + 32
    for line in wrap(headline, fh, TW - 30):
        text(x + 16, yy, line, fh, INK)
        yy += 33
    # detail
    yy += 6
    fd = font(SERIF, 15)
    for line in wrap(detail, fd, TW - 30)[:3]:
        text(x + 16, yy, line, fd, MUTED)
        yy += 18


def icon_ukraine(x, y):
    # night sky, damaged apartment block, smoke, missile streak
    d.ellipse([x + 196, y + 16, x + 216, y + 36], fill=(214, 205, 180))
    # missile
    d.line([x + 24, y + 34, x + 96, y + 92], fill=(240, 138, 46), width=5)
    d.polygon([(x + 20, y + 30), (x + 34, y + 34), (x + 26, y + 44)], fill=(255, 196, 92))
    # block
    bx, by = x + 84, y + 58
    d.rectangle([bx, by, bx + 150, y + 146], fill=(226, 216, 194))
    d.rectangle([bx, by, bx + 150, by + 14], fill=(200, 190, 168))
    # broken top right
    d.polygon([(bx + 96, by), (bx + 150, by), (bx + 150, by + 10),
               (bx + 128, by + 16), (bx + 112, by + 8), (bx + 96, by + 20)], fill=(30, 42, 56))
    for r in range(3):
        for c in range(6):
            wx, wy = bx + 12 + c * 22, by + 26 + r * 30
            if r == 2 and c > 3:
                continue
            d.rectangle([wx, wy, wx + 12, wy + 16], fill=(40, 52, 66))
    # smoke
    for cx, cy, r in [(bx + 160, y + 52, 20), (bx + 184, y + 36, 15), (bx + 202, y + 58, 12)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 100, 104))
    # rubble
    d.polygon([(bx + 110, y + 146), (bx + 140, y + 146), (bx + 132, y + 132),
               (bx + 120, y + 138)], fill=(200, 190, 168))


def icon_china(x, y):
    # big star under inspection
    cx, cy, R, r = x + 135, y + 82, 58, 23
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=CREAM)
    # magnifier
    mx, my, mr = x + 214, y + 54, 30
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=CREAM, width=7)
    d.ellipse([mx - mr + 7, my - mr + 7, mx + mr - 7, my + mr - 7], fill=(220, 96, 80))
    d.line([mx + 22, my + 22, mx + 48, my + 48], fill=CREAM, width=9)


def icon_huawei(x, y):
    # gavel and sounding block
    d.rounded_rectangle([x + 92, y + 108, x + 218, y + 128], radius=7, fill=CREAM)
    # handle
    d.line([x + 118, y + 100, x + 168, y + 44], fill=CREAM, width=16)
    # head (rotated)
    hx, hy = x + 178, y + 36
    ang = math.radians(40)
    ca, sa = math.cos(ang), math.sin(ang)
    corners = []
    for dx, dy in [(-38, -20), (38, -20), (38, 20), (-38, 20)]:
        corners.append((hx + dx * ca - dy * sa, hy + dx * sa + dy * ca))
    d.polygon(corners, fill=CREAM)
    d.line([hx - 32 * ca, hy - 32 * sa, hx + 32 * ca, hy + 32 * sa], fill=(22, 50, 79), width=5)


def icon_gaza(x, y):
    # city skyline under a targeting reticle
    for bx, bw, bh in [(x + 46, 34, 44), (x + 88, 44, 62), (x + 140, 30, 38), (x + 178, 48, 54),
                       (x + 234, 34, 30)]:
        d.rectangle([bx, y + 146 - bh, bx + bw, y + 146], fill=(36, 46, 36))
    cx, cy = x + 155, y + 72
    d.ellipse([cx - 56, cy - 56, cx + 56, cy + 56], outline=CREAM, width=4)
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=CREAM, width=4)
    d.line([cx - 74, cy, cx + 74, cy], fill=CREAM, width=4)
    d.line([cx, cy - 74, cx, cy + 74], fill=CREAM, width=4)


def icon_sanofi(x, y):
    # capsule and deal value
    d.rounded_rectangle([x + 40, y + 62, x + 168, y + 102], radius=20, fill=CREAM)
    d.rounded_rectangle([x + 104, y + 62, x + 168, y + 102], radius=20, fill=(220, 96, 80))
    d.rectangle([x + 104, y + 62, x + 132, y + 102], fill=(220, 96, 80))
    text(x + 184, y + 56, "$41B", font(SANS_B, 34), CREAM)
    text(x + 42, y + 112, "SANOFI · INSMED", font(SANS_B, 14), (170, 210, 205))


def icon_bitcoin(x, y):
    # coin with B and two strokes, falling line
    cx, cy, R = x + 96, y + 76, 50
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=CREAM, width=5)
    text(cx - 15, cy - 28, "B", font(SANS_B, 52), CREAM)
    d.rectangle([cx - 15, cy - 38, cx - 9, cy + 34], fill=CREAM)
    d.rectangle([cx + 12, cy - 38, cx + 18, cy + 34], fill=CREAM)
    # falling chart
    pts = [(x + 176, y + 46), (x + 198, y + 66), (x + 216, y + 58), (x + 236, y + 94),
           (x + 256, y + 86), (x + 276, y + 118)]
    d.line(pts, fill=(240, 138, 46), width=6)
    ax, ay = x + 276, y + 118
    d.polygon([(ax, ay), (ax - 16, ay - 4), (ax - 6, ay - 20)], fill=(240, 138, 46))


tiles = [
    (MARGE, ROW1, (30, 42, 56), "EUROPE  ·  WAR",
     "9 KILLED IN RUSSIAN STRIKES",
     "Attacks across Ukraine; a Zaporizhzhia apartment block hit, 81 hurt.", icon_ukraine),
    (MARGE + TW + GAP, ROW1, (179, 38, 30), "CHINA  ·  POLITICS",
     "POLITBURO MEMBER PROBED",
     "Shanghai party chief Chen Jining investigated for serious violations.", icon_china),
    (MARGE + 2 * (TW + GAP), ROW1, (22, 50, 79), "UNITED STATES  ·  COURTS",
     "HUAWEI GUILTY IN US CASE",
     "Federal jury in Brooklyn convicts on 10 of 12 trade-secrets counts.", icon_huawei),
    (MARGE, ROW2, (36, 46, 36), "GAZA  ·  MIDDLE EAST",
     "HAMAS SECURITY CHIEF KILLED",
     "Naim Abu Nahal dies in an Israeli air strike on Gaza City.", icon_gaza),
    (MARGE + TW + GAP, ROW2, (15, 92, 92), "BUSINESS  ·  PHARMA",
     "SANOFI BUYS INSMED",
     "A $41bn cash deal at $175 a share, announced before markets opened.", icon_sanofi),
    (MARGE + 2 * (TW + GAP), ROW2, (26, 26, 26), "MARKETS  ·  CRYPTO",
     "BITCOIN FALLS BELOW $60,000",
     "The token slid below the level; the Nasdaq fell 1.5% as chips dropped.", icon_bitcoin),
]

for args in tiles:
    tile(*args)

# ---------------------------------------------------------------- briefs
d.rectangle([30, 880, 994, 883], fill=INK)
briefs = [
    (30, "AFRICA", "Sports court restores Senegal's AFCON title"),
    (360, "OCEANIA", "Solomon Islands lets its China pact lapse"),
    (690, "SPACE", "Ariane 6 launches 36 Amazon satellites"),
]
for bx, tag, line in briefs:
    text(bx, 892, tag, font(SANS_B, 13), RED)
    para(bx, 910, line, font(SANS_B, 16), 300, 19, INK)

# ---------------------------------------------------------------- ticker
d.rectangle([0, 956, W, H], fill=INK)
text(30, 968, "ALSO TODAY", font(SANS_B, 15), RED)
text(30, 990, "Dow closes above 50,000  ·  13 killed in a UAE bus crash  ·  "
              "England records 5,258 heat deaths  ·  Real Madrid 5-1 PSV",
     font(SANS, 14), CREAM)

img.save("entry.png", optimize=True)
print("wrote entry.png")
