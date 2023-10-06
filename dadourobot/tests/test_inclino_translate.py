import unittest

from dadourobot.move.anglo_meter_translator import AngloMeterTranslator


class MyTestCase(unittest.TestCase):

    def test_anglo_translate(self):
        anglo_meter_translator = AngloMeterTranslator()
        left, right = anglo_meter_translator.joystickToDiff(y=1, x=20)
        print("left {} right {}".format(left, right))


if __name__ == '__main__':
    unittest.main()
