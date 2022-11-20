import logging

from dadourobot.files.robot_json_manager import RobotJsonManager


class RobotConfig:
    STOP_KEY = None
    MAIN_LOOP_SLEEP = 0

    MOUTH_VISUALS_PATH = None
    EYE_VISUALS_PATH = None

    BASE_PATH = None
    HEAD_MEGA_ID = None
    RADIO_MEGA_ID = None
    MAIN_DUE_ID = None

    FACE_PIN, NECK_PIN, LIGHTS_PIN, LEFT_PWM_PIN, LEFT_DIR_PIN, RIGHT_PWM_PIN, RIGHT_DIR_PIN,\
        LORA_CS_PIN, LORA_RESET_PIN, LORA_SCK_PIN, LORA_MOSI_PIN, LORA_MISO_PIN = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    json_config = None

    def __init__(self, json_manager: RobotJsonManager):
        self.json_manager = json_manager
        self.load()

    def load(self):
        self.json_config = self.json_manager.get_config()
        self.load_pins()
        self.STOP_KEY = self.json_config['stop_key']
        self.MAIN_LOOP_SLEEP = self.json_config['main_loop_sleep']
        self.MOUTH_VISUALS_PATH = self.json_config['mouth_visuals_path']
        self.EYE_VISUALS_PATH = self.json_config['eye_visuals_path']
        logging.debug(self.__dict__)

    def get(self, key):
        if key not in self.json_config.keys():
            logging.error('{} key not in config'.format(key))
            return
        return self.json_config[key]

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

        self.LORA_CS_PIN = self.json_config['pins']['lora_cs']
        self.LORA_RESET_PIN = self.json_config['pins']['lora_reset']
        self.LORA_SCK_PIN = self.json_config['pins']['lora_sck']
        self.LORA_MOSI_PIN = self.json_config['pins']['lora_mosi']
        self.LORA_MISO_PIN = self.json_config['pins']['lora_miso']

        #cs = digitalio.DigitalInOut(board.GP8)
        #reset = digitalio.DigitalInOut(board.GP9)
        #spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)

    #def load_serials(self):
    #    self.HEAD_MEGA_ID = self.json_config['head_mega_id']
    #    self.RADIO_MEGA_ID = self.json_config['radio_mega_id']
    #    self.MAIN_DUE_ID = self.json_config['main_due_id']
