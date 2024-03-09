import copy
import logging

class ImageMapping:

    def __init__(self, start_pixel, global_width, global_height, matrix_width, matrix_height, matrix_width_nb, matrix_height_nb):
        self.start_pixel = start_pixel
        self.global_width = global_width
        self.global_height = global_height
        self.matrix_width = matrix_width
        self.matrix_height = matrix_height
        self.matrix_height_nb = matrix_height_nb
        self.matrix_width_nb = matrix_width_nb

        self.index_order = []

    def mapping(self, pixels, image, start_pixel):
        #pixels.insert(0, 10) = image
        #pixels[start_pixel:len(image)] = image
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
                pixels[index+start_pixel] = image[y][x]

    def create_matrix_horizontal_index2(self):
        led_index = 0
        rows, cols = (self.global_height*self.matrix_height_nb, self.global_width * self.matrix_width_nb)
        self.index_order = [[0 for i in range(cols)] for j in range(rows)]

        for panel_width_nb in range(self.matrix_width_nb):
            x_min = (panel_width_nb * self.matrix_width)
            x_max = (panel_width_nb * self.matrix_width) + self.matrix_width - 1
            for y in range(self.matrix_height):
                if not y % 2:
                    increment = 1
                    x = x_min
                else:
                    increment = -1
                    x = x_max
                while x_min <= x <= x_max:
                    self.index_order[y][x] = led_index

                    x += increment
                    led_index += 1


    def create_matrix_vertical_index(self):
        led_index = 0
        rows, cols = (self.matrix_height*self.matrix_height_nb, self.matrix_width * self.matrix_width_nb)

        self.index_order = [[0 for i in range(cols)] for j in range(rows)]

        for panel_height_nb in range(self.matrix_height_nb):
            y_min = (panel_height_nb * self.matrix_height)
            y_max = (panel_height_nb * self.matrix_height) + self.matrix_height - 1
            for x in range(self.matrix_width):
                if not x % 2:
                    increment = 1
                    y = y_min
                else:
                    increment = -1
                    y = y_max
                while y_min <= y <= y_max:
                    self.index_order[y][x] = led_index

                    y += increment
                    led_index += 1


    def fill_image(self, pixels, image):
        for y in range(len(image)):
            for x in range(len(image[y])):
                pixels[self.index_order[y][x]] = image[y][x]

    def print_index(self):
        for y in range(len(self.index_order)):
            print(self.index_order[y])

    def inverse_bottom_image(image):
        new_image = copy.copy(image)
        logging.debug("inverse image")
        for y in range(int(len(image) / 2), len(image)):
            for x in range(0, len(image[0])):
                ypos = len(image) + (int(len(image) / 2) - (y + 1))
                xpos = (len(image[0]) - 1) - x
                #logging.debug(
                #    "new_image[" + str(y) + "][" + str(x) + "] = image[" + str(ypos) + "][" + str(xpos) + "] => " + str(
                #        image[ypos][xpos]))

                new_image[y][x] = image[ypos][xpos]
                #new_image[y][x] = ORANGE

        return new_image

    def create_matrix_horizontal_index(self):

        rows, cols = (self.matrix_height * self.matrix_height_nb, self.matrix_width * self.matrix_width_nb)
        self.index_order = [[0 for i in range(cols)] for j in range(rows)]

        width = self.matrix_width * self.matrix_width_nb
        height = self.matrix_height * self.matrix_height_nb
        for y in range(height):
            for x in range(width):
                xpos = x % self.matrix_width
                matrix = (x // self.matrix_width) * (self.matrix_width * self.matrix_height)
                if y > self.matrix_height - 1:
                    matrix += self.matrix_width * self.matrix_height * self.matrix_width_nb

                ypos = (y * self.matrix_width)  # % (self.matrix_height * self.matrix_width)
                if ypos > (self.matrix_height * self.matrix_width):
                    ypos -= self.matrix_height * self.matrix_width

                index = xpos + matrix + ypos

                self.index_order[y][x] = index + self.start_pixel