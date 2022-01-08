import logging

from python.json_manager import JsonManager


class Config:
    LIGHTS_PIN = 0
    FACE_PIN = 0
    LEFT_PWM_PIN = 0
    LEFT_DIR_PIN = 0
    RIGHT_PWM_PIN = 0
    RIGHT_DIR_PIN = 0
    NECK_PIN = 0

    def __init__(self, json_manager: JsonManager):
        self.json_config = json_manager.get_config()

    def load(self):
        self.load_pins()
        logging.debug(self)

    def reload(self):
        self.json_config = JsonManager().get_config()
        self.load()

    def load_pins(self):
        self.LIGHTS_PIN = self.json_config['pins']['lights']
        self.FACE_PIN = self.json_config['pins']['face']
        self.LEFT_PWM_PIN = self.json_config['pins']['left_pwm']
        self.LEFT_DIR_PIN = self.json_config['pins']['left_dir']
        self.RIGHT_PWM_PIN = self.json_config['pins']['right_pwm']
        self.RIGHT_DIR_PIN = self.json_config['pins']['right_dir']
        self.NECK_PIN = self.json_config['pins']['neck']
