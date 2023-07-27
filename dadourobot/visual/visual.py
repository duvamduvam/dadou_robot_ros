import logging.config
import os

import imageio.v2 as imageio

from dadourobot.visual.image_mapping import ImageMapping


class Visual:
    name: ""
    rgb: []

    """def __init__(self, name, path):
        self.name = name
        self.rgb = ImageMapping.inverse_bottom_image(Image.get_rgb_from_image(path))
        #self.rgb = Image.get_rgb_from_image(path)
    """

    def __init__(self, path, inverse_bottom: bool):
        self.name = os.path.basename(path)
        #self.name = os.path.splitext(self.name)
        #self.name = self.name[0]
        image = Image(path)
        if inverse_bottom:
            self.rgb = ImageMapping.inverse_bottom_image(image.get_rgb_from_image(path))
        else:
            self.rgb = image.get_rgb_from_image(path)
            #self.rgb = Image.get_rgb_from_image(path)


    @staticmethod
    def get_file_name(path: str) -> str:
        path = path.replace(Image.visual_rep, "")
        path = path.replace(Image.visual_ext, "")
        path = path.replace(Image.up, "")
        return path

class Image:
    visual_rep = "visuals/"
    visual_ext = ".png"
    # for test
    up = "../"
    visuals = []

    matrix_width = 24
    matrix_height = 16

    matrix_height_nb = 2
    matrix_width_nb = 3



    def __init__(self, path):
        logging.debug("create new image")
        #self.load_images()
        self.path = path
    #def __init__(self, visuals_path):
    #    logging.info("create new image")
    #    self.visual_rep = visuals_path


    def mapping(self, image, start_pixel):
        #pixels.insert(0, 10) = image
        #pixels[start_pixel:len(image)] = image
        pixels = []
        for y in range(len(image)):
            for x in range(len(image[y])):
                xpos = x % self.matrix_width

                matrix = (x // self.matrix_width) * (self.matrix_width * self.matrix_height)
                if y > self.matrix_height - 1:
                    matrix += self.matrix_width * self.matrix_height * self.matrix_width_nb

                ypos = (y * self.matrix_width)  # % (self.matrix_height * self.matrix_width)
                if ypos > (self.matrix_height * self.matrix_width):
                    ypos -= self.matrix_height * self.matrix_width

                index = xpos + matrix + ypos

                # logging.debug("pixel[" + str(index) + "] = image[" + str(y) + "][" + str(x) + "] xpos  -> " + str(
                #    xpos) + " matrix  -> " + str(matrix) + " ypos  -> " + str(ypos))
                pixels.append(image[y][x])
        return pixels

    def get_rgb_from_image(self, path):
        rgb = imageio.imread(path)
        #rgb = self.mapping(rgb, 0)
        # logging.info(rgb)
        return rgb
        # arr[20, 30] # 3-vector for a pixel
        # arr[20, 30, 1] # green value for a pixel"""
