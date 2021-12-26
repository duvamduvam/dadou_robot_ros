import board
import neopixel

from python.json_manager import JsonManager
from python.visual import Visual


class Face:

    visuals = []
    json_manager = JsonManager()

    mouth_start = 0
    mouth_end = 382
    pixels = neopixel.NeoPixel(board.D18, 8 * 6 * 8, auto_write=False)
    pixels.brightness = 0.1

    def __init__(self):
        self.load_visual()

    def load_visual(self):
        visuals_path = self.json_manager.get_all_visual()
        for visual_path in visuals_path:
            self.visuals.append(Visual(visual_path.name, visual_path.path))

    def fill_matrix(self, start, end, visual):
        i = start
        for rgb in visual.rgb:
            self.pixels[i] = rgb
            ++i

    def fill_mouth(self, visual):
        self.fill_matrix(self.mouth_start, self.mouth_end, visual)

    def update(self, key):
        toto = 45
