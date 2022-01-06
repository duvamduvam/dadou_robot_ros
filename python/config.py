from python.json_manager import JsonManager


class Config:
    LIGHTS_PIN, FACE_PIN, LEFT_PWM_PIN, LEFT_DIR_PIN, RIGHT_PWM_PIN, RIGHT_DIR_PIN, NECK_PIN = {}

    def __int__(self, json_manager: JsonManager):
        json_config = json_manager.get_config()

        self.LIGHTS_PIN = json_config['pins']['lights']
        self.FACE_PIN = json_config['pins']['face']
        self.LEFT_PWM_PIN = json_config['pins']['left_pwm_']
        self.LEFT_DIR_PIN = json_config['pins']['left_dir']
        self.RIGHT_PWM_PIN = json_config['pins']['right_pwm']
        self.RIGHT_DIR_PIN = json_config['pins']['right_dir']
        self.NECK_PIN = json_config['pins']['neck']
