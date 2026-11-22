#!/usr/bin/env python3
"""Render the Sunday 22 November 2026 world-news broadsheet (entry.png).

Fresh build for make.fun news-image-20261122 (v6). Draws a 1024x1024
newspaper front page: masthead, a world map with 13 numbered story
markers, twelve illustrated story cards, a twelve-item regional list
and a six-item ticker. Story data lives in stories.json / cards.json /
list.json / ticker.json beside this file.
"""

import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024

PAPER = (250, 246, 236)
INK = (26, 24, 22)
RULE = (120, 112, 98)
RED = (178, 34, 34)
NAVY = (27, 58, 95)
OCEAN = (176, 200, 222)
LAND = (231, 222, 198)
LAND_EDGE = (150, 138, 112)
GOLD = (184, 134, 42)
GREY = (92, 86, 76)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return json.load(fh)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, fill, leading=None, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    step = leading or (fnt.size + 3)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


# Simplified continent outlines as (lon, lat) rings, drawn fresh for v6.
NORTH_AMERICA = [(-168, 66), (-158, 71), (-140, 70), (-125, 71), (-110, 68),
                 (-95, 69), (-85, 66), (-80, 62), (-78, 58), (-72, 58),
                 (-65, 50), (-60, 46), (-66, 44), (-70, 42), (-72, 40),
                 (-74, 38), (-76, 35), (-79, 33), (-81, 31), (-81, 26),
                 (-84, 30), (-89, 29), (-94, 29), (-97, 26), (-97, 22),
                 (-94, 18), (-90, 15), (-86, 13), (-83, 9), (-79, 9),
                 (-81, 13), (-84, 15), (-88, 16), (-91, 19), (-90, 21),
                 (-87, 21), (-90, 20), (-96, 16), (-101, 18), (-105, 20),
                 (-108, 23), (-110, 24), (-112, 29), (-115, 32), (-117, 33),
                 (-120, 34), (-122, 37), (-124, 40), (-124, 46), (-123, 48),
                 (-128, 51), (-132, 54), (-137, 58), (-145, 60), (-152, 59),
                 (-158, 56), (-162, 58), (-166, 60), (-168, 66)]
SOUTH_AMERICA = [(-79, 9), (-77, 7), (-77, 4), (-79, -1), (-81, -4),
                 (-81, -6), (-78, -8), (-75, -10), (-70, -15), (-70, -18),
                 (-70, -23), (-70, -30), (-71, -38), (-73, -44), (-74, -49),
                 (-74, -52), (-68, -55), (-66, -55), (-68, -50), (-65, -45),
                 (-65, -41), (-62, -39), (-58, -34), (-52, -32), (-48, -28),
                 (-41, -23), (-39, -18), (-35, -8), (-35, -6), (-38, -5),
                 (-44, -2), (-50, 0), (-52, 5), (-58, 7), (-62, 10),
                 (-68, 11), (-72, 12), (-75, 10), (-77, 7), (-79, 9)]
AFRICA = [(-6, 35), (-10, 31), (-15, 27), (-17, 20), (-17, 15), (-16, 12),
          (-13, 8), (-8, 5), (-4, 5), (2, 6), (6, 4), (9, 4), (9, -1),
          (13, -10), (12, -18), (14, -23), (16, -29), (19, -34), (26, -34),
          (31, -29), (35, -24), (36, -18), (39, -12), (40, -6), (41, -2),
          (46, 4), (51, 11), (51, 12), (44, 11), (43, 12), (40, 15),
          (38, 20), (35, 24), (33, 27), (32, 31), (30, 31), (22, 33),
          (15, 32), (11, 34), (10, 37), (3, 37), (-2, 35), (-6, 35)]
EURASIA = [(-9, 37), (-9, 43), (-2, 44), (-1, 46), (-5, 48), (-2, 50),
           (0, 51), (2, 51), (5, 53), (8, 55), (8, 57), (10, 57),
           (12, 56), (18, 56), (21, 55), (24, 58), (28, 59), (30, 60),
           (28, 63), (25, 66), (22, 70), (30, 70), (40, 68), (50, 69),
           (60, 70), (70, 72), (80, 73), (90, 75), (100, 77), (110, 74),
           (120, 73), (130, 72), (140, 72), (150, 70), (160, 69),
           (170, 67), (178, 66), (178, 65), (170, 60), (162, 60),
           (158, 53), (156, 51), (150, 59), (142, 54), (140, 48),
           (138, 46), (132, 43), (129, 40), (126, 38), (122, 38),
           (120, 34), (120, 30), (118, 25), (110, 20), (108, 16),
           (107, 11), (104, 8), (103, 5), (100, 6), (98, 9), (97, 15),
           (94, 17), (92, 20), (89, 22), (86, 20), (80, 15), (77, 8),
           (73, 16), (72, 20), (68, 23), (66, 25), (61, 25), (57, 26),
           (56, 27), (54, 26), (51, 28), (50, 29), (48, 30), (48, 28),
           (50, 26), (52, 25), (55, 24), (58, 23), (59, 22), (57, 19),
           (55, 17), (52, 15), (45, 12), (43, 12), (42, 15), (39, 20),
           (38, 24), (36, 28), (35, 29), (34, 31), (36, 36), (36, 36),
           (30, 36), (27, 37), (27, 40), (23, 40), (19, 42), (15, 38),
           (16, 40), (18, 40), (15, 44), (12, 44), (10, 44), (7, 44),
           (3, 43), (3, 42), (0, 39), (-2, 37), (-6, 36), (-9, 37)]
SE_ASIA_ISLANDS = [(95, 5), (103, 1), (109, -2), (113, -3), (119, -3),
                   (125, -2), (131, -3), (136, -2), (141, -3), (146, -6),
                   (150, -9), (147, -9), (142, -8), (136, -4), (130, -3),
                   (124, -3), (118, -4), (112, -6), (105, -6), (99, -1),
                   (95, 5)]
AUSTRALIA = [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33),
             (129, -32), (133, -32), (136, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -30), (153, -26), (151, -24),
             (149, -20), (146, -19), (145, -15), (143, -12), (142, -11),
             (141, -13), (141, -17), (139, -17), (136, -15), (135, -12),
             (132, -11), (130, -12), (126, -14), (122, -17), (118, -20),
             (114, -21), (113, -22)]
GREENLAND = [(-45, 60), (-42, 65), (-50, 68), (-54, 70), (-56, 72),
             (-58, 76), (-55, 79), (-45, 80), (-32, 80), (-22, 76),
             (-20, 72), (-22, 70), (-28, 68), (-32, 65), (-40, 60),
             (-45, 60)]
UK = [(-5, 50), (-3, 53), (-5, 55), (-3, 58), (-6, 58), (-8, 55),
      (-6, 52), (-5, 50)]
JAPAN = [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (141, 44),
         (142, 45), (140, 42), (139, 38), (136, 35), (132, 33), (130, 31)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24),
              (45, -25), (44, -20), (44, -16)]
NZ = [(167, -46), (170, -44), (172, -41), (174, -39), (176, -38),
      (178, -38), (175, -36), (173, -35), (172, -40), (169, -43),
      (167, -46)]

CONTINENTS = [NORTH_AMERICA, SOUTH_AMERICA, AFRICA, EURASIA,
              SE_ASIA_ISLANDS, AUSTRALIA, GREENLAND, UK, JAPAN,
              MADAGASCAR, NZ]


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 180) / 360 * (x1 - x0)
    y = y0 + (85 - lat) / 150 * (y1 - y0)
    return x, y


def draw_map(draw, box, markers):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=OCEAN, outline=NAVY, width=2)
    # graticule
    for lon in range(-150, 181, 30):
        gx, _ = project(lon, 0, box)
        draw.line([(gx, y0), (gx, y1)], fill=(150, 176, 202), width=1)
    for lat in range(-60, 81, 30):
        _, gy = project(0, lat, box)
        draw.line([(x0, gy), (x1, gy)], fill=(150, 176, 202), width=1)
    for ring in CONTINENTS:
        pts = [project(lon, lat, box) for lon, lat in ring]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    num = font(SANS_B, 11)
    for m in markers:
        cx, cy = project(m["lon"], m["lat"], box)
        r = 9
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
                     outline=(255, 255, 255), width=2)
        label = str(m["n"])
        tw = draw.textlength(label, font=num)
        draw.text((cx - tw / 2, cy - 6), label, font=num, fill=(255, 255, 255))


# ---- small scene painters for the twelve cards -------------------------

def _sky(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    steps = 24
    for i in range(steps):
        t = i / (steps - 1)
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
        yy = y0 + (y1 - y0) * i / steps
        draw.rectangle([x0, yy, x1, yy + (y1 - y0) / steps + 1], fill=col)


def art_summit(draw, box):
    x0, y0, x1, y1 = box
    _sky(draw, box, (96, 140, 190), (200, 220, 240))
    # sun and a broken gavel line
    draw.ellipse([x1 - 52, y0 + 8, x1 - 22, y0 + 38], fill=(250, 205, 80))
    # conference table rows
    for row in range(3):
        yy = y1 - 12 - row * 14
        draw.rectangle([x0 + 10 + row * 8, yy, x1 - 10 - row * 8, yy + 8],
                       fill=(70, 60, 48))
    # flags crossed out
    for fx in (x0 + 22, x0 + 52, x0 + 82):
        draw.line([(fx, y0 + 12), (fx, y1 - 52)], fill=(60, 60, 60), width=2)
        draw.rectangle([fx, y0 + 12, fx + 20, y0 + 24], fill=(90, 140, 90))
    draw.line([(x0 + 14, y0 + 8), (x0 + 112, y0 + 34)], fill=RED, width=4)
    draw.line([(x0 + 14, y0 + 34), (x0 + 112, y0 + 8)], fill=RED, width=4)


def art_tanker(draw, box):
    x0, y0, x1, y1 = box
    _sky(draw, box, (70, 90, 120), (150, 170, 190))
    sea_y = y0 + (y1 - y0) * 0.62
    draw.rectangle([x0, sea_y, x1, y1], fill=(30, 70, 110))
    for i in range(6):
        wy = sea_y + 6 + i * 6
        draw.line([(x0 + 6, wy), (x1 - 6, wy)], fill=(90, 140, 180), width=1)
    # tanker hull
    hy = sea_y - 14
    draw.polygon([(x0 + 14, hy), (x1 - 26, hy), (x1 - 14, hy + 14),
                  (x0 + 22, hy + 14)], fill=(40, 40, 46))
    draw.rectangle([x0 + 26, hy - 10, x0 + 44, hy], fill=(200, 90, 40))
    draw.rectangle([x1 - 48, hy - 14, x1 - 32, hy], fill=(220, 220, 220))
    # fire plume
    cx = x0 + 70
    draw.polygon([(cx - 12, hy), (cx + 12, hy), (cx + 4, hy - 30),
                  (cx - 6, hy - 38)], fill=(240, 120, 30))
    draw.polygon([(cx - 6, hy), (cx + 6, hy), (cx + 2, hy - 18)],
                 fill=(250, 200, 60))


def art_city(draw, box):
    x0, y0, x1, y1 = box
    _sky(draw, box, (40, 44, 60), (110, 100, 100))
    # apartment blocks
    for i, (bx, bh) in enumerate([(x0 + 12, 58), (x0 + 52, 74), (x0 + 96, 50),
                                  (x0 + 132, 66)]):
        draw.rectangle([bx, y1 - bh, bx + 32, y1 - 8], fill=(58, 54, 58))
        for wy in range(y1 - bh + 8, y1 - 16, 10):
            for wx in range(bx + 5, bx + 28, 8):
                lit = (wx * 7 + wy * 3) % 5 == 0
                draw.rectangle([wx, wy, wx + 4, wy + 5],
                               fill=(250, 220, 130) if lit else (30, 30, 36))
    # missile streaks
    for sx, sy in [(x0 + 30, y0 + 10), (x0 + 80, y0 + 6), (x0 + 128, y0 + 14)]:
        draw.line([(sx, sy), (sx + 26, sy + 30)], fill=(250, 180, 60), width=3)
        draw.ellipse([sx + 22, sy + 26, sx + 32, sy + 36], fill=(250, 120, 40))


def art_ship(draw, box):
    x0, y0, x1, y1 = box
    _sky(draw, box, (120, 150, 180), (205, 220, 230))
    sea_y = y0 + (y1 - y0) * 0.66
    draw.rectangle([x0, sea_y, x1, y1], fill=(44, 84, 120))
    hy = sea_y - 12
    draw.polygon([(x0 + 10, hy), (x1 - 18, hy), (x1 - 8, hy + 12),
                  (x0 + 18, hy + 12)], fill=(52, 52, 60))
    # cargo containers
    for i, col in enumerate([(190, 70, 50), (60, 120, 170), (200, 150, 50)]):
        draw.rectangle([x0 + 22 + i * 30, hy - 12, x0 + 48 + i * 30, hy],
                       fill=col)
    # smoke column
    for i in range(5):
        r = 6 + i * 3
        cx = x0 + 70 + i * 7
        cy = hy - 16 - i * 9
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 68, 70))


def art_race(draw, box):
    x0, y0, x1, y1 = box
    _sky(draw, box, (24, 26, 52), (70, 70, 110))
    # neon strip lights
    for i in range(7):
        lx = x0 + 10 + i * 24
        draw.ellipse([lx, y0 + 8, lx + 10, y0 + 18], fill=(250, 220, 120))
    # track
    ty = y1 - 26
    draw.rectangle([x0, ty, x1, y1], fill=(34, 34, 38))
    for i in range(8):
        draw.rectangle([x0 + i * 22, ty + 12, x0 + i * 22 + 12, ty + 15],
                       fill=(240, 240, 240))
    # car silhouette
    cx, cy = x0 + 52, ty - 12
    draw.polygon([(cx - 34, cy + 8), (cx - 20, cy), (cx + 6, cy - 2),
                  (cx + 26, cy + 2), (cx + 40, cy + 8)], fill=(200, 30, 40))
    draw.rectangle([cx + 30, cy - 8, cx + 44, cy - 4], fill=(200, 30, 40))
    draw.rectangle([cx - 38, cy - 10, cx - 30, cy], fill=(30, 30, 30))
    for wx in (cx - 24, cx + 24):
        draw.ellipse([wx - 8, cy + 4, wx + 8, cy + 20], fill=(16, 16, 16),
                     outline=(180, 180, 180))
    # chequer flag
    fx, fy = x1 - 30, y0 + 26
    for r in range(4):
        for c in range(4):
            col = (20, 20, 20) if (r + c) % 2 == 0 else (245, 245, 245)
            draw.rectangle([fx + c * 5, fy + r * 5, fx + c * 5 + 5,
                            fy + r * 5 + 5], fill=col)


def art_chart(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(20, 24, 34))
    # grid
    for gx in range(x0 + 16, x1 - 8, 16):
        draw.line([(gx, y0 + 8), (gx, y1 - 10)], fill=(52, 60, 78), width=1)
    for gy in range(y0 + 16, y1 - 8, 14):
        draw.line([(x0 + 8, gy), (x1 - 8, gy)], fill=(52, 60, 78), width=1)
    # plunging line
    pts = [(x0 + 12, y0 + 22), (x0 + 44, y0 + 30), (x0 + 72, y0 + 26),
           (x0 + 100, y0 + 44), (x0 + 128, y0 + 58), (x0 + 156, y0 + 78),
           (x1 - 12, y1 - 16)]
    draw.line(pts, fill=(250, 80, 70), width=4)
    # arrow head
    ax, ay = pts[-1]
    draw.polygon([(ax, ay), (ax - 12, ay - 3), (ax - 4, ay - 12)],
                 fill=(250, 80, 70))
    pct = font(SANS_B, 15)
    draw.text((x0 + 10, y0 + 6), "-5.3%", font=pct, fill=(250, 120, 100))


def art_capture(draw, box):
    x0, y0, x1, y1 = box
    _sky(draw, box, (30, 32, 48), (90, 84, 96))
    # helicopter searchlight
    hx, hy = x0 + 120, y0 + 22
    draw.polygon([(hx, hy), (x0 + 34, y1 - 6), (x0 + 84, y1 - 6)],
                 fill=(250, 240, 170))
    draw.ellipse([hx - 16, hy - 8, hx + 16, hy + 6], fill=(20, 20, 24))
    draw.line([(hx - 22, hy - 10), (hx + 22, hy - 10)], fill=(20, 20, 24),
              width=3)
    draw.line([(hx + 16, hy), (hx + 30, hy - 4)], fill=(20, 20, 24), width=3)
    # roadblock silhouettes
    for bx in (x0 + 16, x0 + 56, x0 + 96):
        draw.rectangle([bx, y1 - 18, bx + 30, y1 - 6], fill=(24, 22, 26))
    # handcuff ring
    draw.ellipse([x0 + 18, y0 + 16, x0 + 40, y0 + 38], outline=(230, 230, 230),
                 width=3)
    draw.ellipse([x0 + 34, y0 + 22, x0 + 54, y0 + 42], outline=(230, 230, 230),
                 width=3)


def art_quake(draw, box):
    x0, y0, x1, y1 = box
    _sky(draw, box, (120, 150, 190), (215, 225, 235))
    # Andes ridge
    ridge = [(x0, y1 - 40), (x0 + 34, y0 + 30), (x0 + 66, y1 - 52),
             (x0 + 100, y0 + 22), (x0 + 134, y1 - 48), (x1, y1 - 34),
             (x1, y1), (x0, y1)]
    draw.polygon(ridge, fill=(110, 96, 84))
    draw.polygon([(x0 + 26, y0 + 40), (x0 + 34, y0 + 30), (x0 + 42, y0 + 40)],
                 fill=(245, 245, 245))
    draw.polygon([(x0 + 92, y0 + 32), (x0 + 100, y0 + 22), (x0 + 108, y0 + 32)],
                 fill=(245, 245, 245))
    # crack
    crack = [(x0 + 30, y1 - 8), (x0 + 52, y1 - 22), (x0 + 70, y1 - 12),
             (x0 + 94, y1 - 26), (x0 + 116, y1 - 14), (x0 + 140, y1 - 24)]
    draw.line(crack, fill=(30, 24, 20), width=4)
    # seismograph trace
    trace = []
    for i in range(25):
        tx = x0 + 8 + i * 6
        amp = 3 if i < 10 else (14 if i < 18 else 5)
        ty = y0 + 16 + ((i * 37) % (2 * amp + 1)) - amp
        trace.append((tx, ty))
    draw.line(trace, fill=RED, width=2)


def art_front(draw, box):
    x0, y0, x1, y1 = box
    _sky(draw, box, (150, 140, 110), (220, 205, 170))
    # savanna
    draw.rectangle([x0, y1 - 34, x1, y1], fill=(170, 150, 96))
    # acacia
    tx = x0 + 130
    draw.line([(tx, y1 - 30), (tx, y1 - 56)], fill=(80, 60, 40), width=4)
    draw.ellipse([tx - 34, y1 - 72, tx + 34, y1 - 52], fill=(90, 120, 60))
    # armoured vehicle silhouette
    vx, vy = x0 + 26, y1 - 30
    draw.rectangle([vx, vy - 16, vx + 56, vy], fill=(56, 62, 48))
    draw.rectangle([vx + 14, vy - 24, vx + 36, vy - 16], fill=(56, 62, 48))
    draw.line([(vx + 36, vy - 20), (vx + 62, vy - 24)], fill=(40, 44, 34),
              width=3)
    for wx in (vx + 10, vx + 30, vx + 48):
        draw.ellipse([wx - 6, vy - 4, wx + 6, vy + 8], fill=(26, 26, 26))
    # dust
    for i in range(4):
        r = 5 + i * 3
        draw.ellipse([vx - 8 - i * 8 - r, vy - r, vx - 8 - i * 8 + r, vy + r],
                     fill=(190, 172, 128))


def art_virus(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(244, 238, 226))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = 30
    # spikes
    for k in range(12):
        ang = k * math.pi / 6
        sx = cx + math.cos(ang) * (r + 12)
        sy = cy + math.sin(ang) * (r + 12)
        draw.line([(cx, cy), (sx, sy)], fill=(190, 60, 60), width=3)
        draw.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(190, 60, 60))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 90, 90),
                 outline=(160, 44, 44), width=3)
    for dx, dy, rr in [(-12, -8, 6), (10, 4, 7), (-4, 14, 5), (14, -12, 4)]:
        draw.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr],
                     fill=(170, 50, 50))
    # syringe
    sx, sy = x1 - 40, y1 - 26
    draw.line([(sx, sy), (sx + 18, sy - 18)], fill=(90, 90, 100), width=5)
    draw.line([(sx + 18, sy - 18), (sx + 26, sy - 26)], fill=(60, 60, 70),
              width=2)


def art_bottle(draw, box):
    x0, y0, x1, y1 = box
    _sky(draw, box, (60, 66, 60), (120, 118, 104))
    # bottles row
    for i, bx in enumerate([x0 + 26, x0 + 66, x0 + 106]):
        by = y1 - 12
        draw.rectangle([bx, by - 44, bx + 24, by], fill=(96, 130, 84))
        draw.rectangle([bx + 8, by - 56, bx + 16, by - 44], fill=(96, 130, 84))
        draw.rectangle([bx + 3, by - 34, bx + 21, by - 16], fill=(235, 230, 210))
    # skull mark
    cx, cy = x0 + 78, y0 + 24
    draw.ellipse([cx - 12, cy - 11, cx + 12, cy + 11], fill=(240, 238, 230))
    for ex in (cx - 6, cx + 3):
        draw.ellipse([ex, cy - 4, ex + 5, cy + 2], fill=(30, 30, 30))
    draw.line([(cx - 14, cy + 16), (cx + 14, cy + 24)], fill=(240, 238, 230),
              width=4)
    draw.line([(cx + 14, cy + 16), (cx - 14, cy + 24)], fill=(240, 238, 230),
              width=4)


def art_plane(draw, box):
    x0, y0, x1, y1 = box
    _sky(draw, box, (26, 34, 64), (80, 96, 140))
    # runway
    draw.rectangle([x0, y1 - 22, x1, y1], fill=(40, 42, 48))
    for i in range(6):
        draw.rectangle([x0 + 8 + i * 28, y1 - 12, x0 + 22 + i * 28, y1 - 9],
                       fill=(240, 230, 160))
    # 767 side profile
    fx, fy = x0 + 18, y1 - 48
    draw.rounded_rectangle([fx, fy, fx + 128, fy + 18], radius=8,
                           fill=(228, 230, 234))
    draw.polygon([(fx + 4, fy + 2), (fx - 6, fy - 22), (fx + 14, fy - 22),
                  (fx + 20, fy + 2)], fill=(40, 90, 160))
    draw.polygon([(fx + 60, fy + 16), (fx + 44, fy + 34), (fx + 58, fy + 34),
                  (fx + 74, fy + 16)], fill=(180, 184, 190))
    for wx in range(fx + 26, fx + 112, 10):
        draw.ellipse([wx, fy + 6, wx + 5, fy + 11], fill=(70, 110, 160))
    # deployed slide + engine smoke
    draw.polygon([(fx + 96, fy + 14), (fx + 122, y1 - 22), (fx + 110, y1 - 22),
                  (fx + 88, fy + 16)], fill=(250, 190, 60))
    draw.ellipse([fx + 66, fy + 12, fx + 84, fy + 26], fill=(60, 60, 66))
    for i in range(3):
        r = 4 + i * 3
        draw.ellipse([fx + 78 + i * 8 - r, fy - 2 - i * 6 - r,
                      fx + 78 + i * 8 + r, fy - 2 - i * 6 + r],
                     fill=(90, 90, 96))


ART = {"summit": art_summit, "tanker": art_tanker, "city": art_city,
       "ship": art_ship, "race": art_race, "chart": art_chart,
       "capture": art_capture, "quake": art_quake, "front": art_front,
       "virus": art_virus, "bottle": art_bottle, "plane": art_plane}


# ---- page assembly ------------------------------------------------------

def masthead(draw, meta):
    title = font(SERIF_B, 54)
    tw = draw.textlength(meta["paper"], font=title)
    draw.text(((W - tw) / 2, 10), meta["paper"], font=title, fill=INK)
    draw.line([(24, 76), (W - 24, 76)], fill=INK, width=3)
    draw.line([(24, 82), (W - 24, 82)], fill=INK, width=1)
    date_f = font(SERIF_B, 25)
    line = meta["date_line"]
    dw = draw.textlength(line, font=date_f)
    draw.text(((W - dw) / 2, 88), line, font=date_f, fill=RED)
    tag_f = font(SERIF, 13)
    tg = meta["tagline"] + "  ·  Vol. CCXXVI  ·  31 stories, 7 regions"
    tw2 = draw.textlength(tg, font=tag_f)
    draw.text(((W - tw2) / 2, 120), tg, font=tag_f, fill=GREY)
    draw.line([(24, 140), (W - 24, 140)], fill=RULE, width=1)


def lead_panel(draw, meta, box):
    x0, y0, x1, y1 = box
    lead = meta["lead"]
    region_f = font(SANS_B, 13)
    draw.text((x0, y0), lead["region"].upper() + "  —  LEAD STORY",
              font=region_f, fill=NAVY)
    head_f = font(SERIF_B, 30)
    y = draw_wrapped(draw, lead["headline"], head_f, x0, y0 + 18,
                     x1 - x0, INK, leading=33, max_lines=2)
    sub_f = font(SERIF, 13)
    y = draw_wrapped(draw, lead["sub"], sub_f, x0, y + 2, x1 - x0,
                     GREY, leading=16, max_lines=2)
    map_box = (x0, y + 6, x1, y1 - 16)
    draw_map(draw, map_box, meta["markers"])
    cap_f = font(SANS, 10)
    draw.text((x0, y1 - 13),
              "Numbered markers: the day's 13 mapped stories  ·  " +
              lead["source"], font=cap_f, fill=GREY)


def card(draw, item, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(255, 253, 248), outline=RULE, width=1)
    art_box = (x0 + 5, y0 + 4, x1 - 5, y0 + 46)
    ART[item["art"]](draw, art_box)
    draw.rectangle(art_box, outline=(60, 56, 50), width=1)
    region_f = font(SANS_B, 9)
    draw.text((x0 + 8, y0 + 49), item["region"], font=region_f, fill=NAVY)
    head_f = font(SERIF_B, 11.5)
    y = draw_wrapped(draw, item["headline"], head_f, x0 + 8, y0 + 60,
                     x1 - x0 - 16, INK, leading=13, max_lines=2)
    body_f = font(SERIF, 8.5)
    draw_wrapped(draw, item["body"], body_f, x0 + 8, y + 1,
                 x1 - x0 - 16, (52, 48, 44), leading=9.5, max_lines=4)


def list_panel(draw, items, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(246, 241, 230), outline=RULE, width=1)
    title_f = font(SANS_B, 12)
    draw.text((x0 + 8, y0 + 5), "AROUND THE WORLD — IN BRIEF",
              font=title_f, fill=NAVY)
    draw.line([(x0 + 8, y0 + 21), (x1 - 8, y0 + 21)], fill=RULE, width=1)
    cols = 3
    col_w = (x1 - x0 - 16 - (cols - 1) * 10) // cols
    head_f = font(SERIF_B, 10)
    body_f = font(SERIF, 8)
    place_f = font(SANS_B, 7.5)
    for i, item in enumerate(items):
        col = i % cols
        row = i // cols
        cx = x0 + 8 + col * (col_w + 10)
        cy = y0 + 25 + row * 36
        draw.text((cx, cy), item["place"].upper(), font=place_f, fill=RED)
        y = draw_wrapped(draw, item["headline"], head_f, cx, cy + 7,
                         col_w, INK, leading=10, max_lines=1)
        draw_wrapped(draw, item["text"], body_f, cx, y + 1, col_w,
                     (60, 56, 50), leading=8.5, max_lines=2)


def ticker(draw, items, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=INK)
    label_f = font(SANS_B, 12)
    draw.rectangle([x0, y0, x0 + 74, y1], fill=RED)
    draw.text((x0 + 8, y0 + 6), "LATEST", font=label_f, fill=(255, 255, 255))
    item_f = font(MONO, 9)
    line1 = "  ///  ".join(it["text"] for it in items[:3])
    line2 = "  ///  ".join(it["text"] for it in items[3:])
    draw.text((x0 + 84, y0 + 3), line1, font=item_f, fill=(250, 246, 236))
    draw.text((x0 + 84, y0 + 17), line2, font=item_f, fill=(250, 246, 236))


def main():
    meta = load("stories.json")
    cards = load("cards.json")
    briefs = load("list.json")
    ticks = load("ticker.json")

    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    masthead(draw, meta)
    lead_panel(draw, meta, (24, 148, W - 24, 392))

    # twelve cards: 4 columns x 3 rows
    gx0, gy0 = 24, 398
    cw = (W - 48 - 3 * 8) // 4
    ch = 126
    for i, item in enumerate(cards):
        col, row = i % 4, i // 4
        cx = gx0 + col * (cw + 8)
        cy = gy0 + row * (ch + 7)
        card(draw, item, (cx, cy, cx + cw, cy + ch))

    list_panel(draw, briefs, (24, 804, W - 24, 972))
    ticker(draw, ticks, (24, 980, W - 24, 1012))

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
