#!/usr/bin/env python

from PIL import Image, ImageDraw
import random
import subprocess
import sys


class exlibris:
    def __init__(self, image_path, message):
        self.message = message
        self.image_path = image_path

        self.morsedict = {
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

    def save(self):
        # savefile
        self.savefile = f"results/{self.message}.png"
        self.image.save(self.savefile)

    def show(self):
        # subprocess.run(["feh", "-B", "white", self.filename])
        subprocess.run(["feh", self.savefile])

    def get_image_info(self):
        """return palette"""
        self.width, self.height = self.image.size

        quantized = self.image.quantize(colors=2, kmeans=3)
        convert_rgb = quantized.convert("RGB")
        self.colors = convert_rgb.getcolors(self.width * self.height)
        self.r, self.g, self.b = self.colors[0][1]

    def draw(self):
        # encode message
        self.morse()

        self.image = Image.open(self.image_path)
        self.cursor = -180

        self.long = 1
        self.short = 0.2
        self.halfspace = 0.08

        self.output = ImageDraw.Draw(self.image)

        self.set_ratio()
        self.get_image_info()

        self.arcwidth = 8

        ink = (self.r, self.g, self.b, 255)
        paper = (self.r, self.g, self.b, 150)

        def drawarc(arclength, color):
            # draw arc and update cursor
            self.output.arc(
                (0, 0, self.width, self.height),
                start=self.cursor,
                end=self.cursor + arclength,
                fill=color,
                width=self.arcwidth,
            )
            self.cursor = self.cursor + arclength

        # draw cirle
        drawarc(360, paper)
        # loop draw arc.
        for x in self.messagemorse:
            if x == "0":
                drawarc(self.ratio * self.short, ink)
            elif x == "1":
                drawarc(self.ratio * self.long, ink)
            elif x in [" ", "_"]:
                self.cursor += self.ratio * self.halfspace

            self.cursor += self.ratio * self.halfspace

    def morse(self):
        # define messagemorse
        self.messagemorse = ""
        for c in self.message:
            self.messagemorse += self.morsedict[c] + " "

    def set_ratio(self):
        # define ratio
        longueur = 0
        for x in self.messagemorse:
            if x == "0":
                longueur += self.short + self.halfspace
            elif x == "1":
                longueur += self.long + self.halfspace
            elif x in [" ", "_"]:
                longueur += 2 * self.halfspace
        self.ratio = 360 / longueur


if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = sys.argv[1]
    else:
        message = "FIREFLY"

    image_path = "ressources/owlraw.png"

    result = exlibris(image_path, message)
    # result.morse()
    result.draw()
    result.save()
    result.show()
