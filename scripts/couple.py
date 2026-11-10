"""Hand-drawn pixel portrait of Yichen and his girlfriend (34 x 30), used in the desk photo frame."""

COUPLE_COLORS = {
    ".": "#f4d8cf",  # warm backdrop
    ",": "#ecc7bd",  # backdrop shade
    "h": "#1d1b21", "H": "#3b3742",          # his hair
    "g": "#2c211e", "G": "#4c3832",          # her hair
    "f": "#f3c3a5", "s": "#e2a486",          # skin, shadow
    "e": "#1a1414", "w": "#ffffff",          # eyes, catchlight
    "b": "#f2a092", "m": "#c8675f",          # blush, smile
    "T": "#24242a", "t": "#d9d4cb",          # his tee + print
    "k": "#a07a52", "K": "#7f5d3d", "c": "#b8916a",  # her shirt
}

COUPLE = [
    ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,",
    ",,,,,,hhhhhhh,,,,,,,,,,,,,,,,,,,,,",
    "....hhhhhhhhhhh...................",
    "...hhhHHhhhhhhhh....ggggggg.......",
    "..hhhhHhhhhhhhhhh.ggggGGgggggg....",
    "..hhhhhhhhhhhhhhhgggGGggggggggg...",
    "..hhhhhhhhhhhhhhhggggggggggggggg..",
    "..hhfhhhhhhhhhhhhgggfffggggggggg..",
    "..hhffhhfffhhhhfhggffffffgggggggg.",
    "..hfffffffffffffhgffffffffffggggg.",
    "..hfeeffffffeefffgffffffffffffgggg",
    "..ffewffffffewfffgfeeffffffeefgggg",
    "..fffffffffffffffgfewffffffewfgggg",
    "..fbbffffffffbbffgffffffffffffgggg",
    "...ffffffsfffffffgfbbffffffbbfgggg",
    "...ffffffffffffffgffffffsffffffggg",
    "....ffmffffmffff.gffffffffffffgggg",
    "....fffmmmmfffff.gffffmffffmffgggg",
    ".....ffffffffff..ggfffffmmmmffgggg",
    "......ffffffff...gggfffffffffggggg",
    ".......ssssss....ggggsffffffsggggg",
    "........ffff.....gggg.ssssss.ggggg",
    "....TTTTffffTTTT.gggg.ffffff..gggg",
    "..TTTTTTTTTTTTTTTgggcccffffcccgggg",
    ".TTTTTTTTTTTTTTTTggkkkcckkcckkgggg",
    ".TTTTTTTTTTTTTTTTgkkkkkcckkkkkkggg",
    "TTTTTtTtTtTTTTTTTkkkkkkkkkKkkkkggk",
    "TTTTTTttTTTTTTTTkkkkkkkkkkKkkkkkkk",
    "TTTTTTTTTTTTTTTTkkkkkkkkkkKkkkkkkk",
    "TTTTTTTTTTTTTTTTkkkkkkkkkkKkkkkkkk",
]

assert all(len(r) == 34 for r in COUPLE), [len(r) for r in COUPLE]
