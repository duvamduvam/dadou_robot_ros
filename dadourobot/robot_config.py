import os

import board
from dadou_utils.utils_static import AUDIOS_DIRECTORY, BASE_PATH, MSG_SIZE, NAME, SERIAL_ID, TYPE, NONE, I2C_ENABLED, \
    DEVICES, \
    STOP_ANIMATION_KEYS, \
    I2C_ENABLED, DEVICES_LIST, JSON_VISUALS, JSON_RELAYS, JSON_MAPPINGS, JSON_LIGHTS_SEQUENCE, \
    JSON_LIGHTS, JSON_FACE_SEQUENCE, JSON_EXPRESSIONS, JSON_COLORS, JSON_AUDIO_SEQUENCE, JSON_AUDIOS, JSON_CONFIG, \
    LOOP_DURATION, LEFT_ARM, REYE, LEYE, MOUTHS, RANDOM_ANIMATION_HIGH, RANDOM_ANIMATION_LOW, RANDOM_ANIMATION, \
    EYE_VISUALS_PATH, MOUTH_VISUALS_PATH, MAIN_LOOP_SLEEP, STOP_KEY, RIGHT_ARM_NB, LEFT_ARM_NB, WHEEL_RIGHT_DIR, \
    WHEEL_LEFT_DIR, WHEEL_RIGHT_PWM, WHEEL_LEFT_PWM, HEAD_PWM_NB, LORA_MISO_PIN, LORA_MOSI_PIN, LORA_SCK_PIN, \
    LORA_RESET_PIN, LORA_CS_PIN, STATUS_LED_PIN, RESTART_PIN, SHUTDOWN_PIN, CMD_RIGHT, CMD_LEFT, CMD_BACKWARD, \
    CMD_FORWARD, DIGITAL_CHANNELS_ENABLED, PWM_CHANNELS_ENABLED, LIGHTS_PIN, LIGHTS_LED_COUNT, LIGHTS_START_LED, \
    LIGHTS_END_LED, JSON_DIRECTORY, SEQUENCES_DIRECTORY, LOGGING_CONFIG_FILE, LOGGING_CONFIG_TEST_FILE, RANDOM, \
    PROFILER, CALIBRATION, LOGGING, PROCESS, LOGGING_FILE_NAME, LEFT_EYE_NB, RIGHT_EYE_NB, LOGGING_TEST_FILE_NAME

config = {}

config[I2C_ENABLED] = True
config[PWM_CHANNELS_ENABLED] = True
config[DIGITAL_CHANNELS_ENABLED] = True

config[RANDOM] = False
config[PROFILER] = False

config[CMD_FORWARD] = "g"
config[CMD_BACKWARD] = "h"
config[CMD_LEFT] = "e"
config[CMD_RIGHT] = "d"

config[CALIBRATION] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 252, 255, 251, 255, 1, 0, 232, 3, 0, 0]

########## RPI PINS #########

config[SHUTDOWN_PIN] = board.D16
config[RESTART_PIN] = board.D20
config[STATUS_LED_PIN] = board.D12

config[LIGHTS_PIN] = board.D18
config[LIGHTS_LED_COUNT] = 782
config[LIGHTS_START_LED] = 513
config[LIGHTS_END_LED] = 782

config[LORA_CS_PIN] = 0
config[LORA_RESET_PIN] = 0
config[LORA_SCK_PIN] = board.SCK
config[LORA_MOSI_PIN] = board.MOSI
config[LORA_MISO_PIN] = board.MISO

########## I2C SERVO NUMBER #########

config[HEAD_PWM_NB] = 4
config[WHEEL_LEFT_PWM] = 1
config[WHEEL_RIGHT_PWM] = 2
config[WHEEL_LEFT_DIR] = 0
config[WHEEL_RIGHT_DIR] = 3
config[LEFT_ARM_NB] = 8
config[RIGHT_ARM_NB] = 9
config[LEFT_EYE_NB] = 6
config[RIGHT_EYE_NB] = 7
config[STOP_KEY] = "Db C&"
config[MAIN_LOOP_SLEEP] = 0.001
config[MOUTH_VISUALS_PATH] = "/visuals/mouth"
config[EYE_VISUALS_PATH] = "/visuals/eye"
config[SEQUENCES_DIRECTORY] = '/json/sequences/'

config[RANDOM_ANIMATION_LOW] = 10000
config[RANDOM_ANIMATION_HIGH] = 50000
config[STOP_ANIMATION_KEYS] = ['x']

config[BASE_PATH] = os.getcwd()
config[BASE_PATH] = config[BASE_PATH].replace('/tests', '')
config[LOGGING_CONFIG_TEST_FILE] = config[BASE_PATH] + '/conf/logging-test.conf'
config[LOGGING_CONFIG_FILE] = config[BASE_PATH] + '/conf/logging.conf'
config[LOGGING_TEST_FILE_NAME] = '../../logs/robot-test.log'
config[LOGGING_FILE_NAME] = 'logs/robot.log'
config[JSON_DIRECTORY] = '/json/'
config[AUDIOS_DIRECTORY] = config[BASE_PATH] + '/audios/'

############### JSON FILES ###############

config[JSON_CONFIG] = 'robot_config.json'
config[JSON_AUDIOS] = 'audios.json'
config[JSON_AUDIO_SEQUENCE] = 'audio_sequence.json'
config[JSON_COLORS] = 'colors.json'
config[JSON_EXPRESSIONS] = 'expressions.json'
config[JSON_FACE_SEQUENCE] = 'face_sequence.json'
config[JSON_LIGHTS] = 'robot_lights.json'
config[JSON_LIGHTS_SEQUENCE] = 'lights_sequence.json'
config[JSON_MAPPINGS] = 'mappings.json'
config[JSON_RELAYS] = 'relays.json'
config[JSON_VISUALS] = 'visuals.json'

############## DEVICES ####################

config[DEVICES_LIST] = [
    {
        NAME: None,
        SERIAL_ID: "usb-Arduino__www.arduino.cc__Arduino_Mega_2560_75033303334351C01211-if00",
        MSG_SIZE: 7,
        TYPE: NONE
    },
    {
        NAME: None,
        SERIAL_ID: "usb-1a86_USB_Serial-if00-port0",
        MSG_SIZE: 7,
        TYPE: NONE
    },
    {
        NAME: None,
        SERIAL_ID: "usb-Arduino__www.arduino.cc__Arduino_Due_Prog._Port_85036313230351C0A132-if00",
        MSG_SIZE: 8,
        TYPE: NONE
    }
]




""""
[loggers]
keys=root

[logger_root]
level=INFO
handlers=screen,file

[formatters]
keys=simple,complex,color

[formatter_simple]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s

[formatter_complex]
format=%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s : %(lineno)d - %(message)s

[formatter_color]
class=colorlog.ColoredFormatter
format=%(log_color)s %(asctime)s - user:%(name)s - %(levelname)s - %(pathname)s->%(funcName)s(%(lineno)d) /// %(log_color)s%(message)s %(reset)s
datefmt=%m-%d %H:%M:%S

[handlers]
keys=file,screen

[handler_file]
class=handlers.TimedRotatingFileHandler
interval=midnight
backupCount=5
formatter=color
args=('logs/didier.log',)

[handler_screen]
class=StreamHandler
formatter=color
args=(sys.stdout,)
"""
