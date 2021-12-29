import logging


class ImageMapping:

    def __init__(self, matrix_width, matrix_height, matrix_width_nb, matrix_height_nb):
        self.matrix_width = matrix_width
        self.matrix_height = matrix_height
        self.matrix_height_nb = matrix_width_nb
        self.matrix_width_nb = matrix_width_nb

    def mapping(self, pixels, image):
        for y in range(len(image)):
            for x in range(len(image[y])):
                index = (x % self.matrix_width) + ((x // self.matrix_width) * (
                        self.matrix_width * self.matrix_height)) + (
                                (y // 2) * self.matrix_width)
                logging.debug("pixel[" + str(index) + "] = image[" + str(y) + "][" + str(x) + "]")
                pixels[index] = image[y][x]