import os

import board
from dadou_utils.utils_static import MSG_SIZE,  NAME, SERIAL_ID, TYPE, NONE

I2C_ENABLED = True
PWM_CHANNELS_ENABLED = True
DIGITAL_CHANNELS_ENABLED = False

CMD_FORWARD = "g"
CMD_BACKWARD = "h"
CMD_LEFT = "e"
CMD_RIGHT = "d"

########## RPI PINS #########

SHUTDOWN_PIN = board.D16
RESTART_PIN = board.D20
STATUS_LED_PIN = board.D12

LIGHTS_PIN = board.D18

LORA_CS_PIN = 0
LORA_RESET_PIN = 0
LORA_SCK_PIN = board.SCK
LORA_MOSI_PIN = board.MOSI
LORA_MISO_PIN = board.MISO

########## I2C SERVO NUMBER #########

HEAD_PWM_NB = 4
WHEEL_LEFT_PWM = 1
WHEEL_RIGHT_PWM = 2
WHEEL_LEFT_DIR = 0
WHEEL_RIGHT_DIR = 3
LEFT_ARM_NB = 8
RIGHT_ARM_NB = 9

STOP_KEY = "Db"
MAIN_LOOP_SLEEP = 0.001
MOUTH_VISUALS_PATH = "/../visuals/mouth"
EYE_VISUALS_PATH = "/../visuals/eye"

RANDOM_ANIMATION = 60000
RANDOM_ANIMATION_LOW = 50000
RANDOM_ANIMATION_HIGH = 150000
STOP_ANIMATION_KEYS = ['x']

BASE_PATH = os.getcwd()
if "tests" in BASE_PATH:
    BASE_PATH = BASE_PATH.replace('/tests', '')
    LOGGING_CONFIG_FILE = BASE_PATH+'/../conf/logging-test.conf'
else:
    LOGGING_CONFIG_FILE = BASE_PATH+'/../conf/logging.conf'

############### PATH ###############

#LOGGING_CONFIG_FILE = '/../conf/logging.conf'
#TEST_LOGGING_CONFIG_FILE = '/../../conf/logging-test.conf'
JSON_DIRECTORY = '/../json/'
AUDIOS_DIRECTORY = '../audios/'
SEQUENCES_DIRECTORY = '/../json/sequences/'

############### KEYS ###############

MOUTHS = 'mouths'
LEYE = 'left_eyes'
REYE = 'right_eyes'

DEVICES = 'devices'
HEAD_MEGA = 'head_mega'
RADIO_MEGA = 'radio_mega'
MAIN_DUE = 'main_due'
LEFT_ARM = 'left_arm'
RIGHT_ARM = 'right_arm'

LOOP_DURATION = 'loop_duration'

############### JSON FILES ###############

JSON_CONFIG = 'robot_config.json'
JSON_AUDIOS = 'audios.json'
JSON_AUDIO_SEQUENCE = 'audio_sequence.json'
JSON_COLORS = 'colors.json'
JSON_EXPRESSIONS = 'expressions.json'
JSON_FACE_SEQUENCE = 'face_sequence.json'
JSON_LIGHTS = 'lights.json'
JSON_LIGHTS_SEQUENCE = 'lights_sequence.json'
JSON_MAPPINGS = 'mappings.json'
JSON_RELAYS = 'relays.json'
JSON_VISUALS = 'visuals.json'

############## DEVICES ####################

DEVICES_LIST = [
    {
        NAME: HEAD_MEGA,
        SERIAL_ID: "usb-Arduino__www.arduino.cc__Arduino_Mega_2560_75033303334351C01211-if00",
        MSG_SIZE: 7,
        TYPE: NONE
    },
    {
        NAME: RADIO_MEGA,
        SERIAL_ID: "usb-1a86_USB_Serial-if00-port0",
        MSG_SIZE: 7,
        TYPE: NONE
    },
    {
        NAME: MAIN_DUE,
        SERIAL_ID: "usb-Arduino__www.arduino.cc__Arduino_Due_Prog._Port_85036313230351C0A132-if00",
        MSG_SIZE: 8,
        TYPE: NONE
    }
]