from dadourobot.robot_config import I2C_ENABLED, PWM_CHANNELS_ENABLED, LEFT_ARM, LEFT_ARM_NB

from dadou_utils.utils_static import NECK, KEY
from dadou_utils.actions.servo_abstract import ServoAbstract


MIN_PWM = 5000
MAX_PWM = 65530

DEFAULT_POS = 180


class LeftArm(ServoAbstract):

    SERVO_MIN = 0
    SERVO_MAX = 180
    DEFAULT_POS = 0

    def __init__(self):

        super().__init__(LEFT_ARM, LEFT_ARM_NB, self.DEFAULT_POS, self.SERVO_MAX, I2C_ENABLED, PWM_CHANNELS_ENABLED)
