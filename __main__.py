from PIL import Image, ImageDraw
from random import randrange
import math

class OrientationJudgementTask:
    def __main__(self):
        self.lines = set()

    #rotates point `A` about point `B` by `angle` radians clockwise.
    def rotated_about(self, p, angle):
        x, y = p
        radius = 10
        # angle += math.atan2(ay-by, ax-bx)
        return (
            round(x + radius * math.cos(angle)),
            round(y + radius * math.sin(angle))
        )

    def generate(self):
        image = Image.new("RGB", (400, 400), "white")
        for ii in range(25):
            p1 = (randrange(400), randrange(400))
            p2 = (p1[0] + 100, p1[1] + 100)
            draw = ImageDraw.Draw(image)
            draw.line((p1, self.rotated_about(p1, math.radians(randrange(90)))), width=3, fill='blue')

        image.save('test.jpg')

if __name__ == '__main__':
    OrientationJudgementTask().generate()
