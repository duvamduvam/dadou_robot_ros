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
        json_config = json_manager.get_config()

        self.LIGHTS_PIN = json_config['pins']['lights']
        self.FACE_PIN = json_config['pins']['face']
        self.LEFT_PWM_PIN = json_config['pins']['left_pwm_']
        self.LEFT_DIR_PIN = json_config['pins']['left_dir']
        self.RIGHT_PWM_PIN = json_config['pins']['right_pwm']
        self.RIGHT_DIR_PIN = json_config['pins']['right_dir']
        self.NECK_PIN = json_config['pins']['neck']
