from PIL import Image, ImageDraw
import random
import math
import sys

# META
OUTPUT_DIR = "out"
# STIMULI
IMAGE_SIZE = 400
LINE_LENGTH = 10
BUFFER = 20
VALID_LINE_BEGIN_BOUNDS = LINE_LENGTH + BUFFER # NOTE: used for point random generation to avoid out of bounds lines
VALID_LINE_END_BOUNDS = IMAGE_SIZE - LINE_LENGTH - BUFFER
LINE_COLORS = ['blue', 'red']
ANGLES = [90, 45, 135, 0] # NOTE: target is located at index 0
ANGLES_WEIGHTS = [0, 33, 33, 33]

class OrientationJudgementTask:
    #rotates point by angle radians clockwise (stackoverflow)
    def rotated_about(p, angle):
        x, y = p
        return (
            round(x + LINE_LENGTH * math.cos(angle)),
            round(y + LINE_LENGTH * math.sin(angle))
        )

    def generate(stimuli_count = 10, display_size = 10):
        """
        Generates stimuli of randomly placed and rotated lines on a jpg image
        `stimuli_count` / 2 images have a target to search for
        `stimuli_count` / 2 images DO NOT have a target to search for
        """
        for ii in range(stimuli_count // 2):
            image = OrientationJudgementTask.generate_stimuli(display_size, target_present = True)
            image.save(f"{OUTPUT_DIR}/target_present/{ii}.jpg")
        for ii in range(stimuli_count // 2):
            image = OrientationJudgementTask.generate_stimuli(display_size, target_present = False)
            image.save(f"{OUTPUT_DIR}/target_not_present/{ii}.jpg")

    def generate_stimuli(display_size, target_present) -> Image:
        image = Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE), "white")
        # first color will be target, second will be distractor
        line_colors = [*LINE_COLORS]
        random.shuffle(line_colors)
        seen_target = not target_present
        angles_weights = [*ANGLES_WEIGHTS]
        if target_present:
            angles_weights[0] = sys.maxsize
        for ii in range(display_size):
            if seen_target: angles_weights[0] = 0
            # generate random origin point for line, then rotate and find point 2
            point1 = (random.randrange(VALID_LINE_BEGIN_BOUNDS, VALID_LINE_END_BOUNDS), random.randrange(VALID_LINE_BEGIN_BOUNDS, VALID_LINE_END_BOUNDS))
            rotation = random.choices(ANGLES, weights=angles_weights)[0]
            # if you happened to pick the random target (index 0), then make sure it doesn't show again
            if rotation == ANGLES[0]: seen_target = True
            point2 = OrientationJudgementTask.rotated_about(point1, math.radians(rotation))
            # first color is target, second is distractor so assign weights for line color accordingly
            color = random.choices(line_colors, weights=[70, 30])[0]
            draw = ImageDraw.Draw(image)
            draw.line([point1, point2], width=3, fill=color)
        return image

if __name__ == '__main__':
    OrientationJudgementTask.generate(stimuli_count = 10, display_size = 25)
