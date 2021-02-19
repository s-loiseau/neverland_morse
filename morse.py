from PIL import Image, ImageDraw
import random
import subprocess

im = Image.new("RGB", (500, 500), (200, 200, 200))
draw = ImageDraw.Draw(im)

# draw.rectangle((25, 75, 175, 150), fill=(255, 0, 0), width=15, outline=15)

message = 100 * "101101011100110110111010101010110110110101101101010011"
message = message[:360]
print(message)

for x in range(0, 360, 5):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    if message[x] == "0":
        color = (170, 170, 170)
    else:
        color = (190, 190, 190)
    draw.arc((25, 25, 475, 475), start=x, end=x + 10, fill=color, width=8)
im.save("morse.jpg")
subprocess.run(["feh", "morse.jpg"])
