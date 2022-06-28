import logging

from dadourobot.files.robot_json_manager import RobotJsonManager


class RobotConfig:

    BASE_PATH = None
    HEAD_MEGA_ID = None
    RADIO_MEGA_ID = None

    FACE_PIN = 0
    NECK_PIN = 0
    LIGHTS_PIN = 0
    LEFT_PWM_PIN = 0
    LEFT_DIR_PIN = 0
    RIGHT_PWM_PIN = 0
    RIGHT_DIR_PIN = 0

    json_config = None

    def __init__(self, json_manager: RobotJsonManager):
        self.json_manager = json_manager
        self.load()

    def load(self):
        self.json_config = self.json_manager.get_config()
        self.load_pins()
        self.load_serials()
        logging.debug(self.__dict__)

    def reload(self):
        self.json_config = self.json_manager.get_config()
        self.load()

    def load_pins(self):
        self.NECK_PIN = self.json_config['pins']['neck']
        self.LIGHTS_PIN = self.json_config['pins']['lights']
        self.FACE_PIN = self.json_config['pins']['face']
        self.LEFT_PWM_PIN = self.json_config['pins']['left_pwm']
        self.LEFT_DIR_PIN = self.json_config['pins']['left_dir']
        self.RIGHT_PWM_PIN = self.json_config['pins']['right_pwm']
        self.RIGHT_DIR_PIN = self.json_config['pins']['right_dir']

    def load_serials(self):
        self.HEAD_MEGA_ID = self.json_config['head_mega_id']
        self.RADIO_MEGA_ID = self.json_config['radio_mega_id']
