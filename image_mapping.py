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
                pixels[index] = image[y][x]

    def inverse_bottom_image(image):
        new_image = image

        for y in range(abs(len(image) / 2)):
            for x in range(len(image[0])):
                xpos = x % len(image[0])
                new_image[abs(len(image) / 2) + (abs(len(image) / 2) - y)][len(image[0]) - x] = image[y][x]
        return new_image
