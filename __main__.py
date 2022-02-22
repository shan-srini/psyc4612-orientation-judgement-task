from PIL import Image, ImageDraw, ImageOps
import random
import math
import sys

# META
OUTPUT_DIR = "out"
# STIMULI
IMAGE_SIZE = 1000
LINE_LENGTH = 50
BUFFER = 20
VALID_LINE_BEGIN_BOUNDS = LINE_LENGTH + BUFFER # NOTE: used for point random generation to avoid out of bounds lines
VALID_LINE_END_BOUNDS = IMAGE_SIZE - LINE_LENGTH - BUFFER
LINE_COLORS = ['blue', 'red']
ANGLES = [90, 45, 0, 135] # NOTE: target is located at index 0
ANGLES_WEIGHTS = [0, 33, 33, 33]

class OrientationJudgementTask:
    #rotates point by angle radians clockwise (stackoverflow)
    def rotated_about(p, angle):
        x, y = p
        length = LINE_LENGTH - 20
        return (
            round(x + length * math.cos(angle)),
            round(y + length * math.sin(angle))
        )

    def generate(stimuli_count = 10, display_size = 10):
        """
        Generates stimuli of randomly placed and rotated lines on a jpg image
        `stimuli_count` / 2 images have a target to search for
        `stimuli_count` / 2 images DO NOT have a target to search for
        """
        for ii in range(stimuli_count // 2):
            stimuli, target_color = OrientationJudgementTask.generate_stimuli(display_size, target_present = True)
            instructions = OrientationJudgementTask.generate_target_color_image(target_color)
            instructions.save(f"{OUTPUT_DIR}/target_present/{ii}_color.jpg")
            stimuli.save(f"{OUTPUT_DIR}/target_present/{ii}.jpg")
        for ii in range(stimuli_count // 2):
            stimuli, target_color = OrientationJudgementTask.generate_stimuli(display_size, target_present = False)
            instructions = OrientationJudgementTask.generate_target_color_image(target_color)
            instructions.save(f"{OUTPUT_DIR}/target_not_present/{ii}_color.jpg")
            stimuli.save(f"{OUTPUT_DIR}/target_not_present/{ii}.jpg")

    def generate_target_color_image(target_color):
        image = Image.new("RGB", (100, 100), "white")
        draw = ImageDraw.Draw(image)
        draw.text((40, 40), target_color, fill="black")
        return image.resize((IMAGE_SIZE, IMAGE_SIZE))

    def generate_stimuli(display_size, target_present) -> Image:
        grid = [[False for _ in range(IMAGE_SIZE // LINE_LENGTH)] for _ in range(IMAGE_SIZE// LINE_LENGTH)]
        image = Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE), "white")
        # first color will be target, second will be distractor
        line_colors = [*LINE_COLORS]
        random.shuffle(line_colors)
        seen_target = not target_present
        angles_weights = [*ANGLES_WEIGHTS]
        if target_present:
            angles_weights[0] = sys.maxsize
        target_color = line_colors[0]
        for ii in range(display_size):
            if seen_target: angles_weights[0] = 33
            # generate random origin point for line, then rotate and find point 2
            point1 = None
            while point1 is None:
                x, y = (random.randrange(IMAGE_SIZE // LINE_LENGTH), random.randrange(IMAGE_SIZE // LINE_LENGTH))
                if not grid[x][y]: point1 = (x * LINE_LENGTH, y * LINE_LENGTH)
            grid[x][y] = True
            # first color is target, second is distractor so assign weights for line color accordingly
            color = random.choices(line_colors, weights=[70, 40])[0]
            rotation = random.choices(ANGLES, weights=angles_weights)[0]
            # Distractors should still be allowed to be vertical, but targets shouldn't
            while seen_target and rotation == ANGLES[0] and color == target_color:
                rotation = random.choices(ANGLES, weights=angles_weights)[0]
            point2 = OrientationJudgementTask.rotated_about(point1, math.radians(rotation))
            # if you happened to pick the random target (index 0), then make sure it doesn't show again
            if rotation == ANGLES[0] and color == target_color:
                seen_target = True
                color = line_colors[0] # manually override color for target
            draw = ImageDraw.Draw(image)
            draw.line([point1, point2], width=3, fill=color)
        return ImageOps.expand(image, border = 100, fill = 'white'), target_color

if __name__ == '__main__':
    OrientationJudgementTask.generate(stimuli_count = 10, display_size = 100)
