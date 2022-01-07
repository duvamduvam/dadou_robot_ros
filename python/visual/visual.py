import glob
import logging.config
import imageio

from python.visual.image_mapping import ImageMapping


class Visual:
    name: {}
    rgb: []

    def __init__(self, name, path):
        self.name = name
        self.rgb = ImageMapping.inverse_bottom_image(Image.get_rgb_from_image(path))
        #self.rgb = Image.get_rgb_from_image(path)


    @staticmethod
    def get_file_name(path: str) -> str:
        path = path.replace(Image.visual_rep, "")
        path = path.replace(Image.visual_ext, "")
        path = path.replace(Image.up, "")
        return path

    @staticmethod
    def get_visual(name, visuals):
        for visual in visuals:
            if visual.name == name:
                return visual
        logging.error("no visual name : " + name)

class Image:
    visual_rep = "visuals/"
    visual_ext = ".png"
    # for test
    up = "../"
    visuals = []

    def __init__(self):
        logging.info("create new image")
        self.load_images()

    def __init__(self, visuals_path):
        logging.info("create new image")
        self.visual_rep = visuals_path

    def load_images(self):
        logging.info("load visuals")
        images_path = glob.glob(self.visual_rep + "*")
        logging.info(self.visual_rep + " content : ")
        logging.info(images_path)
        visual_nb = len(images_path)
        self.visuals = [0 for i in range(visual_nb)]
        i = 0
        for p in images_path:
            rgb = self.get_rgb_from_image(p)
            self.visuals[i] = Visual(p, rgb)
            logging.info("load image : " + self.visuals[i].name)
            i = i + 1

    @staticmethod
    def get_rgb_from_image(path):
        rgb = imageio.imread(path)
        # logging.info(rgb)
        return rgb
        # arr[20, 30] # 3-vector for a pixel
        # arr[20, 30, 1] # green value for a pixel
