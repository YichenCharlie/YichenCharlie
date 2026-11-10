"""Generate pigeons.svg: a pixel plaza banner with pigeons walking, pecking and flying.

Usage: python scripts/build_pigeons.py [--out pigeons.svg]
"""
import argparse
import random
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
W, H = 320, 112
GROUND = 72

COLORS = {"G": "#8f96a3", "L": "#bcc1cb", "D": "#3f4352", "T": "#5d6372",
          "N": "#5f9c86", "M": "#8a6fa8", "K": "#141414", "O": "#4a403c",
          "W": "#f1efe9", "P": "#d9737d"}

STAND = [
    "..........GGG...",
    ".........GGKGO..",
    ".........GGGW...",
    "..........NM....",
    "....GGGGGGNN....",
    "..GGGLLLLGGG....",
    ".GGLLDLLDLGG....",
    "TTGLLLLLLLGG....",
    "..GGGGGGGGG.....",
    "......P..P......",
    ".....PP.PP......",
]
STEP = [
    "...........GGG..",
    "..........GGKGO.",
    "..........GGGW..",
    "..........NM....",
    "....GGGGGGNN....",
    "..GGGLLLLGGG....",
    ".GGLLDLLDLGG....",
    "TTGLLLLLLLGG....",
    "..GGGGGGGGG.....",
    ".......P.P......",
    "......PP..PP....",
]
PECK = [
    "................",
    "................",
    "................",
    "................",
    "....GGGGGG......",
    "..GGGLLLLGGN....",
    ".GGLLDLLDLGMN...",
    "TTGLLLLLLLGGNGG.",
    "..GGGGGGGGG.GKGO",
    "......P..P......",
    ".....PP.PP......",
]
FLY_UP = [
    "...GG...........",
    "...GLG..........",
    "....GLG.........",
    ".....GLG...GGG..",
    "TT..GGGGGGNGKGO.",
    ".TGGGGGGGGGG....",
    "..GGGGGGGG......",
    "................",
    "................",
]
FLY_DOWN = [
    "................",
    "................",
    "................",
    "...........GGG..",
    "TT..GGGGGGNGKGO.",
    ".TGGGLLGGGGG....",
    "..GGGLLLG.......",
    ".....GLLG.......",
    "......GG........",
]
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


def sprite(rows, colors=COLORS, cls=""):
    out = [f'<g class="{cls}">' if cls else "<g>"]
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):  # merge horizontal runs to keep the file small
            ch = row[x]
            if ch not in colors:
                x += 1
                continue
            run = 1
            while x + run < len(row) and row[x + run] == ch:
                run += 1
            out.append(f'<rect x="{x}" y="{y}" width="{run}" height="1" fill="{colors[ch]}"/>')
            x += run
    out.append("</g>")
    return "".join(out)


def build():
    rng = random.Random(3)
    p = []
    add = p.append

    # sky + distant city
    for i, col in enumerate(("#cfe4f2", "#d9eaf4", "#e3eff5", "#ecf3f4")):
        add(f'<rect x="0" y="{i*14}" width="{W}" height="15" fill="{col}"/>')
    add(f'<rect x="0" y="56" width="{W}" height="{GROUND-56}" fill="#ecf3f4"/>')
    x = 0
    while x < W:
        bw, bh = rng.randint(10, 22), rng.randint(6, 17)
        add(f'<rect x="{x}" y="{GROUND-bh}" width="{bw}" height="{bh}" fill="#c3d0dc"/>')
        x += bw + rng.randint(0, 3)
    for cx, cy in ((40, 12), (196, 20)):
        add(f'<g class="cloud"><rect x="{cx}" y="{cy}" width="22" height="3" fill="#fff"/>'
            f'<rect x="{cx+5}" y="{cy-2}" width="10" height="2" fill="#fff"/></g>')

    # plaza tiles
    add(f'<rect x="0" y="{GROUND}" width="{W}" height="{H-GROUND}" fill="#d9cdb8"/>')
    add(f'<rect x="0" y="{GROUND}" width="{W}" height="1" fill="#bfae92"/>')
    for row, y in enumerate(range(GROUND + 7, H, 7)):
        add(f'<rect x="0" y="{y}" width="{W}" height="1" fill="#cbbda5"/>')
        off = 0 if row % 2 else 7
        for tx in range(off, W, 14):
            add(f'<rect x="{tx}" y="{y-6}" width="1" height="6" fill="#cbbda5"/>')

    # name block
    add('<text x="14" y="30" class="serif" font-size="17" font-weight="bold" fill="#1f3550">Yichen Feng</text>')
    add('<text x="15" y="41" class="mono" font-size="5.4" fill="#4f6378">incoming ECE @ Rice · ML systems · LLM inference</text>')
    add('<text x="15" y="49" class="mono" font-size="4.6" fill="#7a8a99">(the pigeons are colleagues. the owl is management.)</text>')

    # lamppost with the owl on top
    add(f'<rect x="286" y="43" width="4" height="{GROUND-43+2}" fill="#3c4250"/>')
    add('<rect x="278" y="40" width="20" height="3" fill="#3c4250"/>')
    add(f'<rect x="283" y="{GROUND}" width="10" height="3" fill="#3c4250"/>')
    add('<g transform="translate(274 8) scale(2)">' + sprite(OWL, OWL_COLORS)
        + '<g class="lid"><rect x="2" y="4" width="4" height="3" fill="#9a6a3c"/>'
          '<rect x="8" y="4" width="4" height="3" fill="#9a6a3c"/></g></g>')

    # bench
    add('<rect x="140" y="66" width="56" height="3" fill="#8a5b3b"/>')
    add('<rect x="140" y="70" width="56" height="2" fill="#7a4f33"/>')
    add('<rect x="143" y="72" width="3" height="9" fill="#3c4250"/><rect x="190" y="72" width="3" height="9" fill="#3c4250"/>')

    # crumbs
    for cx in (236, 241, 247, 252, 258, 230, 244):
        add(f'<rect x="{cx}" y="{GROUND+29+(cx%3)}" width="1" height="1" fill="#e8c27a"/>')

    # pigeon 1: walks across the plaza
    add(f'<g class="walker"><g transform="translate(0 {GROUND-6}) scale(2)">'
        + sprite(STAND, cls="fa") + sprite(STEP, cls="fb") + "</g></g>")
    # pigeon 2: pecking at crumbs
    add(f'<g transform="translate(222 {GROUND+10}) scale(2)">' + sprite(STAND, cls="pa") + sprite(PECK, cls="pb") + "</g>")
    # pigeon 3: facing left, bobbing its head
    add(f'<g transform="translate(206 {GROUND+16}) scale(-2 2)">' + sprite(STAND, cls="pa2") + sprite(PECK, cls="pb2") + "</g>")
    # pigeon 4: resting on the bench
    add('<g transform="translate(152 48) scale(2)">' + sprite(STAND[:9]) + "</g>")
    # pigeon 5: flying over
    add('<g class="flyer"><g transform="scale(2)">' + sprite(FLY_UP, cls="fa fast") + sprite(FLY_DOWN, cls="fb fast") + "</g></g>")

    style = """
  .mono{font-family:'Courier New',Courier,monospace}
  .serif{font-family:Georgia,'Times New Roman',serif;letter-spacing:-.4px}
  .fa{animation:fa .5s steps(1) infinite}.fb{animation:fb .5s steps(1) infinite}
  .fast{animation-duration:.3s}
  @keyframes fa{0%{opacity:1}50%{opacity:0}}
  @keyframes fb{0%{opacity:0}50%{opacity:1}}
  .walker{animation:walk 22s linear infinite}
  @keyframes walk{from{transform:translateX(-40px)}to{transform:translateX(330px)}}
  .flyer{animation:fly 13s linear infinite}
  @keyframes fly{0%{transform:translate(-40px,50px)}45%{transform:translate(340px,-4px)}100%{transform:translate(340px,-4px)}}
  .pa{animation:pa 3.2s steps(1) infinite}.pb{animation:pb 3.2s steps(1) infinite}
  @keyframes pa{0%{opacity:1}40%{opacity:0}50%{opacity:1}60%{opacity:0}70%{opacity:1}}
  @keyframes pb{0%{opacity:0}40%{opacity:1}50%{opacity:0}60%{opacity:1}70%{opacity:0}}
  .pa2{animation:pa 4.6s steps(1) infinite 1.3s}.pb2{opacity:0;animation:pb 4.6s steps(1) infinite 1.3s}
  .lid{opacity:0;animation:blink 5s infinite}
  @keyframes blink{0%,92%,100%{opacity:0}94%,97%{opacity:1}}
  .cloud{animation:drift 50s linear infinite alternate}
  @keyframes drift{to{transform:translateX(24px)}}
  @media (prefers-reduced-motion:reduce){*{animation:none!important}.fb,.pb,.pb2,.lid{opacity:0}.walker{transform:translateX(60px)}.flyer{display:none}}
"""
    label = "Yichen Feng: a pixel plaza with pigeons walking, pecking and flying, and an owl on a lamppost"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W*3}" height="{H*3}" '
            f'shape-rendering="crispEdges" role="img" aria-label="{escape(label)}">\n'
            f"<title>{escape(label)}</title>\n<style>{style}</style>\n" + "\n".join(p) + "\n</svg>\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "pigeons.svg"))
    args = ap.parse_args()
    Path(args.out).write_text(build(), encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
