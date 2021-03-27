#!/usr/bin/env python

from PIL import Image, ImageDraw
import subprocess
import sys


class Exlibris:
    def __init__(self, image_path, message):
        self.message = message
        # encode message
        self.morse()

        self.image_path = image_path
        self.image = Image.open(self.image_path)
        self.output = ImageDraw.Draw(self.image)

    def save(self):
        """Save image to file."""
        self.savefile = f"results/{self.message}.png"
        self.image.save(self.savefile)

    def show(self):
        """Display image file."""
        subprocess.run(["feh", self.savefile])

    def draw(self):
        def set_ratio():
            """Calulate messagemorse length and set ratio 360/longueur."""
            longueur = 0
            for x in self.messagemorse:
                if x == "0":
                    longueur += self.short + self.halfspace
                elif x == "1":
                    longueur += self.long + self.halfspace
                elif x in [" ", "_"]:
                    longueur += 2 * self.halfspace
            self.ratio = 360 / longueur

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

        def get_image_info():
            """Get r,g,b, width, height from image object."""
            self.width, self.height = self.image.size

            # find 2 main colors
            quantized = self.image.quantize(colors=2, kmeans=3)
            convert_rgb = quantized.convert("RGB")
            colors = convert_rgb.getcolors(self.width * self.height)
            self.r, self.g, self.b = colors[0][1]
            self.ink = (self.r, self.g, self.b, 255)
            self.paper = (self.r, self.g, self.b, 140)

        self.cursor = -180

        self.long = 1
        self.short = 0.2
        self.halfspace = 0.08
        self.arcwidth = 8

        set_ratio()
        get_image_info()

        # draw clear cirle.
        drawarc(360, self.paper)

        # loop draw ink arcs.
        for x in self.messagemorse:
            if x == "0":
                drawarc(self.ratio * self.short, self.ink)
            elif x == "1":
                drawarc(self.ratio * self.long, self.ink)
            elif x in [" ", "_"]:
                self.cursor += self.ratio * self.halfspace

            self.cursor += self.ratio * self.halfspace

    def morse(self):
        # define messagemorse
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
        self.messagemorse = ""
        for c in self.message:
            self.messagemorse += morsedict[c] + " "


if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = sys.argv[1]
    else:
        message = "FIREFLY"

    image_path = "ressources/owlraw.png"

    exlibris = Exlibris(image_path, message)
    # result.morse()
    exlibris.draw()
    exlibris.save()
    exlibris.show()
