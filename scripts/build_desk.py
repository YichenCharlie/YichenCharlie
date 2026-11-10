"""Generate the pixel desk scene (desk.svg) for the GitHub profile README.

Usage:
    python scripts/build_desk.py                 # day/night from Houston time
    python scripts/build_desk.py --mode night    # force a mode
    python scripts/build_desk.py --mode day --out desk-day.svg
"""
import argparse
import datetime as dt
import random
from pathlib import Path
from xml.sax.saxutils import escape

from couple import COUPLE, COUPLE_COLORS

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None

ROOT = Path(__file__).resolve().parent.parent
W, H = 320, 180

PALETTES = {
    "night": {
        "wall": "#38344d", "wall_dark": "#2e2a41", "trim": "#2a2639",
        "sky": ["#151a33", "#1c2244", "#252d57", "#2f3a68"],
        "city": "#10132a", "city_win": "#f4cf78", "city_win_off": "#1d2242",
        "glow": "#ffe2a3", "frame": "#6b4a35", "frame_dark": "#523726",
    },
    "day": {
        "wall": "#ecdcc2", "wall_dark": "#e0ceb1", "trim": "#d2bd9c",
        "sky": ["#86c0e6", "#9dcdec", "#b6daf1", "#cde6f5"],
        "city": "#8094ae", "city_win": "#d5e1ec", "city_win_off": "#9aabc1",
        "glow": "#fff6dc", "frame": "#8a6246", "frame_dark": "#6e4c35",
    },
}

OWL = [
    "..BB......BB..",
    "..BBB....BBB..",
    "..BBBBBBBBBB..",
    ".BBWWWBBWWWBB.",
    ".BWWOOWWOOWWB.",
    ".BWOKOWWOKOWB.",
    ".BWWOOWWOOWWB.",
    ".BBWWWYYWWWBB.",
    ".BBBBBYYBBBBB.",
    ".BBLLBBBBLLBB.",
    "BBLLLLBBLLLLBB",
    "BBLDLLLLLLDLBB",
    "BBLLLDLLDLLLBB",
    ".BBLLLLLLLLBB.",
    "..BBBBBBBBBB..",
    "...YY....YY...",
]
OWL_COLORS = {"B": "#9a6a3c", "W": "#f3dfbd", "O": "#ef8a2c", "K": "#1d1410",
              "Y": "#e7b23c", "L": "#e9c48f", "D": "#8a5a30"}


def read_now(path):
    data = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def clip(text, n):
    text = str(text)
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


class Canvas:
    def __init__(self):
        self.parts = []

    def rect(self, x, y, w, h, fill, extra=""):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{extra}/>')

    def raw(self, s):
        self.parts.append(s)

    def sprite(self, rows, colors, ox, oy):
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch in colors:
                    self.rect(ox + x, oy + y, 1, 1, colors[ch])

    def disc(self, cx, cy, r, fill):
        """Pixel circle drawn as horizontal spans."""
        for dy in range(-r, r + 1):
            span = int((r * r - dy * dy) ** 0.5 + 0.5)
            self.rect(cx - span, cy + dy, span * 2 + 1, 1, fill)

    def text(self, x, y, s, size, fill, cls="mono", weight="normal", anchor="start"):
        self.parts.append(
            f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')


def build(mode, now):
    p = PALETTES[mode]
    night = mode == "night"
    rng = random.Random(7)
    c = Canvas()

    # ---- wall ---------------------------------------------------------
    c.rect(0, 0, W, H, p["wall"])
    for x in range(0, W, 16):  # subtle wallpaper stripes
        c.rect(x, 0, 8, 132, p["wall_dark"], ' opacity=".35"')
    c.rect(0, 126, W, 6, p["trim"])

    # ---- window -------------------------------------------------------
    wx, wy, ww, wh = 24, 14, 100, 70
    gx, gy, gw, gh = wx + 4, wy + 4, ww - 8, wh - 8
    band = gh // len(p["sky"])
    for i, col in enumerate(p["sky"]):
        c.rect(gx, gy + i * band, gw, band + 1, col)
    if night:
        c.disc(gx + 14, gy + 10, 5, "#f3ecd2")
        c.disc(gx + 16, gy + 8, 4, p["sky"][0])  # crescent bite
        for i in range(16):
            sx, sy = gx + rng.randint(2, gw - 3), gy + rng.randint(2, 30)
            c.rect(sx, sy, 1, 1, "#fff6d8", f' class="star s{i % 4}"')
    else:
        c.disc(gx + 76, gy + 12, 5, "#fff1b8")
        for cx0, cy0 in ((gx + 10, gy + 10), (gx + 44, gy + 18)):
            c.raw(f'<g class="cloud">')
            c.rect(cx0, cy0, 16, 3, "#ffffff")
            c.rect(cx0 + 3, cy0 - 2, 8, 2, "#ffffff")
            c.raw("</g>")
    # skyline
    x = gx
    while x < gx + gw:
        bw = rng.randint(7, 14)
        bh = rng.randint(14, 30)
        bw = min(bw, gx + gw - x)
        top = gy + gh - bh
        c.rect(x, top, bw, bh, p["city"])
        for wy2 in range(top + 3, gy + gh - 2, 4):
            for wx2 in range(x + 2, x + bw - 2, 3):
                on = rng.random() < (0.45 if night else 0.3)
                c.rect(wx2, wy2, 1, 2, p["city_win"] if on else p["city_win_off"])
        x += bw + 1
    # frame + mullions
    c.rect(wx, wy, ww, 4, p["frame"]); c.rect(wx, wy + wh - 4, ww, 4, p["frame"])
    c.rect(wx, wy, 4, wh, p["frame"]); c.rect(wx + ww - 4, wy, 4, wh, p["frame"])
    c.rect(wx + ww // 2 - 1, wy, 3, wh, p["frame"]); c.rect(wx, wy + wh // 2 - 1, ww, 3, p["frame"])
    c.rect(wx - 4, wy + wh, ww + 8, 4, p["frame_dark"])  # sill

    # ---- owl on the sill ---------------------------------------------
    # drawn at 2x so the mascot reads clearly at README size
    ox, oy = wx + 10, wy + wh - 32
    c.raw(f'<g class="owl"><g transform="translate({ox} {oy}) scale(2)">')
    c.sprite(OWL, OWL_COLORS, 0, 0)
    c.raw('<g class="lid">')
    c.rect(2, 4, 4, 3, OWL_COLORS["B"]); c.rect(8, 4, 4, 3, OWL_COLORS["B"])
    c.raw("</g></g></g>")

    # ---- Rice pennant + shelf -----------------------------------------
    c.raw('<g transform="translate(0 -12)">')
    c.raw('<g class="pennant">')
    c.raw('<polygon points="232,22 286,28 232,34" fill="#00205b"/>')
    c.rect(230, 20, 2, 16, "#5a4030")
    c.text(236, 30.5, "RICE", 5, "#c1c6c8", cls="mono", weight="bold")
    c.raw("</g>")
    c.rect(222, 62, 86, 3, p["frame"])
    c.rect(226, 65, 2, 4, p["frame_dark"]); c.rect(302, 65, 2, 4, p["frame_dark"])
    bx = 228
    for col, bh in (("#b5523b", 14), ("#3c6e8f", 16), ("#d3a640", 12), ("#5a7d4a", 15),
                    ("#7a4f8c", 13), ("#c9c1b0", 16)):
        c.rect(bx, 62 - bh, 5, bh, col); c.rect(bx + 1, 62 - bh + 3, 3, 1, "#ffffff", ' opacity=".35"')
        bx += 6
    c.raw(f'<polygon points="{bx},62 {bx+3},50 {bx+8},50 {bx+5},62" fill="#8e7a5c"/>')
    # plant
    c.rect(286, 54, 10, 8, "#b86b44"); c.rect(285, 53, 12, 2, "#c97b52")
    for lx, ly, lw, lh in ((288, 44, 2, 9), (291, 40, 2, 13), (294, 45, 2, 8), (285, 47, 3, 2), (295, 43, 3, 2)):
        c.rect(lx, ly, lw, lh, "#5b8f4e")

    c.raw('</g>')

    # ---- desk lamp + glow ---------------------------------------------
    if night:
        c.raw(f'<polygon points="30,96 52,96 76,132 6,132" fill="{p["glow"]}" opacity=".16" class="lampglow"/>')
    c.rect(18, 128, 18, 4, "#3d3d48"); c.rect(25, 104, 3, 24, "#4a4a58")
    c.rect(25, 102, 14, 3, "#4a4a58")
    c.raw('<polygon points="34,92 52,92 48,100 38,100" fill="#d85f4a"/>')
    c.rect(38, 100, 10, 1, p["glow"] if night else "#e9e2cf")

    # ---- desk -----------------------------------------------------------
    c.rect(0, 132, W, 8, "#a8774f")
    c.rect(0, 132, W, 1, "#c18f63")
    c.rect(0, 140, W, 40, "#7c5134")
    c.rect(0, 140, W, 2, "#5f3c26")
    for gx2 in range(10, W, 37):
        c.rect(gx2, 146 + (gx2 % 5), 18, 1, "#6d462d")

    # ---- drawers on the desk front -----------------------------------------
    for dx in (20, 170):
        c.rect(dx, 150, 130, 22, "#5f3c26")
        c.rect(dx + 1, 151, 128, 20, "#86583a")
        c.rect(dx + 1, 151, 128, 1, "#9a6a47")
        c.rect(dx + 59, 159, 12, 3, "#d8b46a"); c.rect(dx + 59, 161, 12, 1, "#a8843f")

    # ---- mug + steam ---------------------------------------------------
    mgx = 42
    c.rect(mgx, 122, 10, 10, "#e8e1d3"); c.rect(mgx, 122, 10, 2, "#cfc6b4")
    c.rect(mgx + 10, 124, 3, 1, "#e8e1d3"); c.rect(mgx + 12, 124, 1, 5, "#e8e1d3"); c.rect(mgx + 10, 128, 3, 1, "#e8e1d3")
    c.rect(mgx + 2, 126, 6, 3, "#c25d47")
    for i, (sx, sy) in enumerate(((mgx + 3, 118), (mgx + 6, 115), (mgx + 4, 112))):
        c.rect(sx, sy, 1, 3, "#ffffff", f' class="steam t{i}" opacity="0"')

    # ---- framed photo of the two of them --------------------------------
    fx, fy = 62, 95
    fw, fh = len(COUPLE[0]) + 6, len(COUPLE) + 6
    c.rect(fx + 1, fy + 1, fw, fh, "#000000", ' opacity=".18"')
    c.rect(fx, fy, fw, fh, "#8a5a3a")
    c.rect(fx, fy, fw, 1, "#a8774f"); c.rect(fx, fy, 1, fh, "#a8774f")
    c.rect(fx + 2, fy + 2, fw - 4, fh - 4, "#f6efe2")  # mat
    c.sprite(COUPLE, COUPLE_COLORS, fx + 3, fy + 3)
    c.rect(fx + 4, fy + 4, 6, 1, "#ffffff", ' opacity=".35"')  # glass glint
    c.rect(fx + 4, fy + 5, 3, 1, "#ffffff", ' opacity=".35"')
    heart = [".X.X.", "XXXXX", ".XXX.", "..X.."]
    c.raw(f'<g class="heart"><g transform="translate({fx + fw // 2 - 2} {fy - 7})">')
    c.sprite(heart, {"X": "#e2566a"}, 0, 0)
    c.raw("</g></g>")

    # ---- monitor (links to the website) ---------------------------------
    mx, my, mw, mh = 116, 66, 92, 58
    c.rect(mx, my, mw, mh, "#2b2b33")
    c.rect(mx + 1, my + 1, mw - 2, 1, "#45454f")
    sx0, sy0, sw0, sh0 = mx + 4, my + 4, mw - 8, mh - 10
    c.rect(sx0, sy0, sw0, sh0, "#fffefa")
    c.rect(sx0, sy0, sw0, 10, "#143e80")
    c.text(sx0 + 3, sy0 + 7.5, "yichen", 6.5, "#ffffff", cls="serif", weight="bold")
    c.text(sx0 + 25, sy0 + 7.5, ".space", 6.5, "#cedeed", cls="serif")
    c.rect(sx0 + 49, sy0 + 2, 1, 1, "#f4ce91"); c.rect(sx0 + 48, sy0 + 3, 3, 1, "#f4ce91"); c.rect(sx0 + 49, sy0 + 4, 1, 1, "#f4ce91")
    c.rect(sx0, sy0 + 10, sw0, 3, "#6595bd")
    c.rect(sx0 + 3, sy0 + 16, 18, 22, "#d8e5ef")  # sidebar
    c.rect(sx0 + 3, sy0 + 16, 18, 3, "#6494bd")
    c.rect(sx0 + 24, sy0 + 16, sw0 - 27, 3, "#f5d6b3")
    for i, lw in enumerate((50, 44, 52, 30)):
        c.rect(sx0 + 24, sy0 + 22 + i * 3, lw, 1, "#c9ced3")
    c.text(sx0 + 24, sy0 + 42, "> visit my site", 4.6, "#204f89")
    c.rect(sx0 + 67, sy0 + 38.5, 3, 4, "#204f89", ' class="cursor"')
    c.rect(mx, my + mh - 6, mw, 6, "#2b2b33")
    c.rect(mx + mw // 2 - 1, my + mh - 4, 2, 2, "#7fd17a", ' class="led"')
    c.rect(mx + mw // 2 - 6, my + mh, 12, 6, "#3a3a44")
    c.rect(mx + mw // 2 - 16, 130, 32, 2, "#3a3a44")
    if night:  # screen glow on the desk
        c.raw(f'<polygon points="{mx+6},132 {mx+mw-6},132 {mx+mw+14},140 {mx-14},140" fill="#cfe3ff" opacity=".12"/>')

    # keyboard + mouse
    c.rect(126, 134, 64, 5, "#d9d6cf"); c.rect(126, 138, 64, 1, "#b9b5ad")
    for kx in range(128, 188, 4):
        c.rect(kx, 135, 3, 1, "#b9b5ad"); c.rect(kx + 1, 136, 3, 1, "#c4c0b8")
    c.rect(196, 134, 6, 5, "#d9d6cf"); c.rect(198, 134, 2, 2, "#b9b5ad")

    # ---- record player (now playing) ------------------------------------
    c.rect(222, 120, 48, 12, "#5b3a28"); c.rect(222, 120, 48, 1, "#7b5139")
    c.rect(225, 123, 4, 6, "#2a1c15"); c.rect(263, 123, 4, 6, "#2a1c15")
    c.raw('<g class="vinyl">')
    c.disc(246, 108, 11, "#16161b")
    c.disc(246, 108, 8, "#24242c")
    c.disc(246, 108, 6, "#16161b")
    c.disc(246, 108, 3, "#e0703f")
    c.rect(246, 108, 1, 1, "#16161b")
    c.rect(240, 100, 3, 1, "#5a5a68")  # sheen that shows the spin
    c.rect(238, 101, 2, 1, "#5a5a68")
    c.raw("</g>")
    c.rect(234, 118, 24, 2, "#3a2a20")  # stand lip
    for i, (nx, ny) in enumerate(((261, 112), (266, 106), (257, 104))):
        c.text(nx, ny, "♪", 7, "#f4cf78" if night else "#a05a2c", cls=f"mono note n{i}")

    # ---- handheld console (now playing game) ----------------------------
    c.rect(278, 126, 30, 7, "#c8434a")
    c.rect(280, 120, 26, 7, "#d4545b")
    c.rect(285, 121, 16, 5, "#26323f")
    c.rect(287, 123, 2, 2, "#8de06b", ' class="blip"')
    c.rect(281, 122, 2, 1, "#2a2a30"); c.rect(282, 121, 1, 3, "#2a2a30")
    c.rect(303, 122, 2, 2, "#2a2a30")

    # ---- corkboard with the two notes, right above their objects --------
    cbx, cby, cbw, cbh = 216, 58, 98, 37
    c.rect(cbx, cby, cbw, cbh, "#7a5236")
    c.rect(cbx + 2, cby + 2, cbw - 4, cbh - 4, "#c79a64")
    for i in range(40):  # cork speckles
        c.rect(cbx + 3 + rng.randint(0, cbw - 7), cby + 3 + rng.randint(0, cbh - 7), 1, 1, "#b0844f")

    def wrap(text, width):
        lines, cur = [], ""
        for word in str(text).split():
            if cur and len(cur) + 1 + len(word) > width:
                lines.append(cur); cur = word
            else:
                cur = f"{cur} {word}".strip()
        lines.append(cur)
        if len(lines) > 2:
            lines = [lines[0], clip(" ".join(lines[1:]), width)]
        return [clip(l, width) for l in lines]

    def note(x, y, w, h, angle, paper, pin, icon, title, main, sub):
        cx, cy = x + w / 2, y + h / 2
        c.raw(f'<g transform="rotate({angle} {cx} {cy})">')
        c.rect(x + 1, y + 1, w, h, "#000000", ' opacity=".22"')
        c.rect(x, y, w, h, paper)
        c.rect(x, y + h - 3, w, 3, "#000000", ' opacity=".05"')
        c.sprite(icon, {"X": "#4a3a2c", "o": "#e0703f", "r": "#d85f4a", "b": "#3c6e8f"}, x + 3, y + 3)
        c.text(x + 10, y + 7.2, title, 3.6, "#8a6a3a", weight="bold")
        c.rect(x + 3, y + 9, w - 6, 1, "#000000", ' opacity=".12"')
        ty = y + 15
        for line in wrap(main, 16):
            c.text(x + 3, ty, line, 4.4, "#2f2a26", weight="bold")
            ty += 5.4
        c.text(x + 3, y + h - 3.5, sub, 3.8, "#6a5a48")
        c.raw("</g>")
        c.rect(int(cx) - 1, y - 1, 3, 3, pin); c.rect(int(cx) - 1, y - 1, 1, 1, "#ffffff")

    vinyl_icon = [".XXX.", "XXoXX", "XoXoX", "XXoXX", ".XXX."]
    pad_icon = ["XXXXX", "XrXbX", "XXXXX", "X...X"]
    song = clip(now.get("song", "—"), 34)
    artist = clip(now.get("artist", ""), 17)
    game = clip(now.get("game", "—"), 34)
    hours = now.get("game_hours", "")
    note(cbx + 4, cby + 4, 45, 29, -2, "#fbeeb0", "#d85f4a", vinyl_icon, "SPINNING", song, artist)
    note(cbx + 51, cby + 4, 43, 29, 2, "#d6ecf6", "#3c6e8f", pad_icon, "PLAYING", game,
         f"{hours} hrs" if hours else "")

    style = """
  .mono{font-family:'Courier New',Courier,monospace}
  .serif{font-family:Georgia,'Times New Roman',serif}
  .lid{opacity:0;animation:blink 5s infinite}
  @keyframes blink{0%,92%,100%{opacity:0}94%,97%{opacity:1}}
  .owl{animation:bob 6s steps(1) infinite}
  @keyframes bob{0%,70%,100%{transform:translateY(0)}72%,80%{transform:translateY(-1px)}}
  .cursor{animation:cur 1s steps(1) infinite}
  @keyframes cur{50%{opacity:0}}
  .vinyl{transform-box:fill-box;transform-origin:center;animation:spin 3s linear infinite}
  @keyframes spin{to{transform:rotate(360deg)}}
  .note{opacity:0;animation:float 3.6s linear infinite}
  .n1{animation-delay:1.2s}.n2{animation-delay:2.4s}
  @keyframes float{0%{opacity:0;transform:translateY(4px)}20%{opacity:1}80%{opacity:.8}100%{opacity:0;transform:translateY(-8px)}}
  .steam{animation:steam 2.4s linear infinite}
  .t1{animation-delay:.8s}.t2{animation-delay:1.6s}
  @keyframes steam{0%{opacity:0;transform:translateY(2px)}30%{opacity:.8}100%{opacity:0;transform:translateY(-6px)}}
  .star{animation:tw 3s steps(1) infinite}
  .s1{animation-delay:.7s}.s2{animation-delay:1.5s}.s3{animation-delay:2.2s}
  @keyframes tw{0%,100%{opacity:1}50%{opacity:.25}}
  .cloud{animation:drift 40s linear infinite alternate}
  @keyframes drift{to{transform:translateX(18px)}}
  .blip{animation:cur .8s steps(1) infinite}
  .led{animation:cur 2.5s steps(1) infinite}
  .heart{opacity:0;animation:heart 7s ease-out infinite 2s}
  @keyframes heart{0%{opacity:0;transform:translateY(3px)}8%{opacity:1}30%{opacity:1;transform:translateY(-4px)}40%,100%{opacity:0;transform:translateY(-6px)}}
  @media (prefers-reduced-motion:reduce){*{animation:none!important}.lid,.note,.steam,.heart{opacity:0}}
"""
    title = f"Yichen's desk: listening to {song} by {artist}; playing {game}"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W*3}" height="{H*3}" '
        f'shape-rendering="crispEdges" role="img" aria-label="{escape(title)}">\n'
        f"<title>{escape(title)}</title>\n<style>{style}</style>\n"
        + "\n".join(c.parts) + "\n</svg>\n"
    )


def houston_mode():
    if ZoneInfo is None:
        return "night"
    hour = dt.datetime.now(ZoneInfo("America/Chicago")).hour
    return "day" if 7 <= hour < 19 else "night"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["day", "night", "auto"], default="auto")
    ap.add_argument("--now", default=str(ROOT / "now.yml"))
    ap.add_argument("--out", default=str(ROOT / "desk.svg"))
    args = ap.parse_args()
    mode = houston_mode() if args.mode == "auto" else args.mode
    svg = build(mode, read_now(Path(args.now)))
    Path(args.out).write_text(svg, encoding="utf-8")
    print(f"wrote {args.out} ({mode})")


if __name__ == "__main__":
    main()
