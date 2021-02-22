#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFilter
import random
import subprocess
import sys


morsedict = {
    "A": "01",
    "B": "1000",
    "C": "1010",
    "D": "100",
    "E": "0",
    "F": "0010",
    "G": "110",
    "H": "0000",
    "I": "00",
    "J": "0111",
    "K": "101",
    "L": "0100",
    "M": "11",
    "N": "10",
    "O": "111",
    "P": "0110",
    "Q": "1101",
    "R": "010",
    "S": "000",
    "T": "1",
    "U": "001",
    "V": "0001",
    "W": "011",
    "X": "1001",
    "Y": "1011",
    "Z": "1100",
    "1": "01111",
    "2": "00111",
    "3": "00011",
    "4": "00001",
    "5": "00000",
    "6": "10000",
    "7": "11000",
    "8": "11100",
    "9": "11110",
    "0": "11111",
    ",": "110011",
    ".": "010101",
    "?": "001100",
    "/": "10010",
    "-": "100001",
    "(": "10110",
    ")": "101101",
    " ": "_",
}


def getpalette(image_path):
    """return palette and size."""
    image = Image.open(image_path)
    width, height = image.size
    quantized = image.quantize(colors=2, kmeans=3)
    convert_rgb = quantized.convert("RGB")
    colors = convert_rgb.getcolors(width * height)
    print(width, height)
    return (width, height, colors)


def drawarc(length, width, color):
    global cursor
    draw.arc(dimension, start=cursor, end=cursor + length, fill=color, width=width)
    cursor = cursor + length


def morse(message):
    messagemorse = ""
    for c in messageclear:
        print(c, morsedict[c])
        messagemorse += morsedict[c] + " "
    return messagemorse


def longueur_message(messagemorse):
    global short
    global long
    global halfspace

    longueur = 0
    for x in messagemorse:
        if x == "0":
            longueur += short + halfspace
        elif x == "1":
            longueur += long + halfspace
        elif x in [" ", "_"]:
            longueur += 2 * halfspace
    return longueur


short = 0.2
long = 2
halfspace = 0.08
pen_width = 8
cursor = -180

if len(sys.argv) > 1:
    messageclear = sys.argv[1]
else:
    messageclear = "FIREFLY"

messagemorse = morse(messageclear)
longueur = longueur_message(messagemorse)

ratio = 360 / longueur

filepath = "ressources/owlraw.png"
owl = Image.open(filepath)
width, height, palette = getpalette(filepath)

draw = ImageDraw.Draw(owl)

r, g, b = palette[0][1]

ink = (r + 10, g + 10, b + 10, 240)
paper = (r, g, b, 30)
dimension = (0, 0, width, height)

# draw clear circle
drawarc(360, pen_width, paper)

for x in messagemorse:
    if x == "0":
        drawarc(ratio * short, pen_width, ink)
    elif x == "1":
        drawarc(ratio * long, pen_width, ink)
    elif x == " ":
        cursor += ratio * halfspace
    cursor += ratio * halfspace

filename = f"results/{messageclear}.png"
owl.save(filename)
subprocess.run(["feh", "-B", "black", filename])
