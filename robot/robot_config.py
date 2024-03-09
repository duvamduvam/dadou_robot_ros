import os

import board

from dadou_utils.misc import Misc
from dadou_utils.utils_static import AUDIOS_DIRECTORY, BASE_PATH, MSG_SIZE, NAME, SERIAL_ID, TYPE, NONE, \
    STOP_ANIMATION_KEYS, \
    I2C_ENABLED, DEVICES_LIST, JSON_RELAYS, JSON_MAPPINGS, JSON_LIGHTS_SEQUENCE, \
    JSON_LIGHTS, JSON_FACE_SEQUENCE, JSON_EXPRESSIONS, JSON_COLORS, JSON_AUDIOS, JSON_CONFIG, \
    RANDOM_ANIMATION_HIGH, RANDOM_ANIMATION_LOW, EYE_VISUALS_PATH, MOUTH_VISUALS_PATH, MAIN_LOOP_SLEEP, STOP_KEY, \
    RIGHT_ARM_NB, LEFT_ARM_NB, WHEEL_RIGHT_DIR, \
    WHEEL_LEFT_DIR, WHEEL_RIGHT_PWM, WHEEL_LEFT_PWM, HEAD_PWM_NB, LORA_MISO_PIN, LORA_MOSI_PIN, LORA_SCK_PIN, \
    LORA_RESET_PIN, LORA_CS_PIN, STATUS_LED_PIN, RESTART_PIN, SHUTDOWN_PIN, CMD_RIGHT, CMD_LEFT, CMD_BACKWARD, \
    CMD_FORWARD, DIGITAL_CHANNELS_ENABLED, PWM_CHANNELS_ENABLED, LIGHTS_PIN, LIGHTS_LED_COUNT, LIGHTS_START_LED, \
    LIGHTS_END_LED, JSON_DIRECTORY, SEQUENCES_DIRECTORY, LOGGING_CONFIG_FILE, LOGGING_CONFIG_TEST_FILE, RANDOM, \
    PROFILER, CALIBRATION, LOGGING_FILE_NAME, LEFT_EYE_NB, RIGHT_EYE_NB, LOGGING_TEST_FILE_NAME, \
    SINGLE_THREAD, JSON_LIGHTS_BASE, AUDIO_DEVICE_ID, DEFAULT_VOLUME_LEVEL, BRIGHTNESS, JSON_NOTES, JSON_AUDIOS_DATAS, \
    RANDOM_TYPE, LITTLE_MOVE, VISUAL_PATH, CONFIG_DIRECTORY, LOGGING_DIRECTORY, SRC_DIRECTORY, PROJECT_DIRECTORY, \
    MEDIAS_DIRECTORY, VISUAL_DIRECTORY

config = {}

config[I2C_ENABLED] = False
config[PWM_CHANNELS_ENABLED] = True
config[DIGITAL_CHANNELS_ENABLED] = True
config[SINGLE_THREAD] = False

config[BRIGHTNESS] = 0.05

MAX_PWM_L = 25000
MAX_PWM_R = 25000

config[RANDOM] = False
config[RANDOM_TYPE] = [LITTLE_MOVE]
config[RANDOM_ANIMATION_LOW] = 50000
config[RANDOM_ANIMATION_HIGH] = 100000

config[PROFILER] = False

config[AUDIO_DEVICE_ID] = 6
config[DEFAULT_VOLUME_LEVEL] = 50

config[CMD_FORWARD] = "g"
config[CMD_BACKWARD] = "h"
config[CMD_LEFT] = "b"
config[CMD_RIGHT] = "a"

config[CALIBRATION] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 252, 255, 251, 255, 1, 0, 232, 3, 0, 0]

########## RPI PINS #########


#if Misc.is_raspberrypi():
config[SHUTDOWN_PIN] = board.D16
config[RESTART_PIN] = board.D20
config[STATUS_LED_PIN] = board.D12

config[LIGHTS_PIN] = board.D18
config[LIGHTS_LED_COUNT] = 1000
config[LIGHTS_START_LED] = 513
config[LIGHTS_END_LED] = 673

config[LORA_CS_PIN] = 0
config[LORA_RESET_PIN] = 0

if Misc.is_raspberrypi():
    config[LORA_SCK_PIN] = board.SCK
    config[LORA_MOSI_PIN] = board.MOSI
    config[LORA_MISO_PIN] = board.MISO

########## I2C SERVO NUMBER #########

config[HEAD_PWM_NB] = 5
config[WHEEL_LEFT_PWM] = 1
config[WHEEL_RIGHT_PWM] = 2
config[WHEEL_LEFT_DIR] = 0
config[WHEEL_RIGHT_DIR] = 3
config[LEFT_ARM_NB] = 4
config[RIGHT_ARM_NB] = 15
config[LEFT_EYE_NB] = 8
config[RIGHT_EYE_NB] = 9

base = "robot/"

config[STOP_KEY] = "L"
config[MAIN_LOOP_SLEEP] = 0.001

config[STOP_ANIMATION_KEYS] = ['x']

#config[BASE_PATH] = os.getcwd()
config[BASE_PATH] = "/root/ros2_ws/"
config[BASE_PATH] = config[BASE_PATH].replace('/tests', '')
config[SRC_DIRECTORY] = config[BASE_PATH] + "src/"
config[PROJECT_DIRECTORY] = config[SRC_DIRECTORY] + "robot/"

config[CONFIG_DIRECTORY] = config[PROJECT_DIRECTORY] + "conf/"
config[JSON_DIRECTORY] = config[PROJECT_DIRECTORY] + "json/"
config[MEDIAS_DIRECTORY] = config[PROJECT_DIRECTORY] + 'medias/'

config[AUDIOS_DIRECTORY] = config[MEDIAS_DIRECTORY] + 'audios/'
config[VISUAL_DIRECTORY] = config[MEDIAS_DIRECTORY] + 'visuals/'

config[SEQUENCES_DIRECTORY] = config[JSON_DIRECTORY]+'sequences/'
config[LOGGING_DIRECTORY] = config[CONFIG_DIRECTORY] + "logging/"

config[LOGGING_CONFIG_TEST_FILE] = config[LOGGING_DIRECTORY] + 'logging-test.conf'
config[LOGGING_CONFIG_FILE] = config[LOGGING_DIRECTORY] + 'logging.conf'

config[LOGGING_TEST_FILE_NAME] = '../../logs/robot-test.log'
config[LOGGING_FILE_NAME] = '/root/ros2_ws/log/robot.log'
config[LOGGING_TEST_FILE_NAME] = '../../logs/robot-test.log'

config[MOUTH_VISUALS_PATH] = config[VISUAL_DIRECTORY] + "mouth"
config[EYE_VISUALS_PATH] = config[VISUAL_DIRECTORY] + "eye"

############### JSON FILES ###############

config[JSON_CONFIG] = 'robot_config.json'
config[JSON_AUDIOS] = 'audios.json'
config[JSON_AUDIOS_DATAS] = 'audios-data.json'
#config[JSON_AUDIO_SEQUENCE] = 'audio_sequence.json'
config[JSON_COLORS] = 'colors.json'
config[JSON_EXPRESSIONS] = 'expressions.json'
config[JSON_FACE_SEQUENCE] = 'face_sequence.json'
config[JSON_LIGHTS] = 'robot_lights.json'
config[JSON_LIGHTS_BASE] = 'lights_base.json'
config[JSON_LIGHTS_SEQUENCE] = 'lights_sequence.json'
config[JSON_MAPPINGS] = 'mappings.json'
config[JSON_NOTES] = 'piano.json'
config[JSON_RELAYS] = 'relays.json'
#config[JSON_VISUALS] = 'visuals.json'

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
