import logging


class Message:
    key = None
    left_wheel = None
    right_wheel = None
    neck = None

    PREFIX = '<'
    POSTFIX = '>'

    def __init__(self, left_wheel, right_wheel, neck, key):
        logging.info(
            "new message left wheel : " + left_wheel + " right_wheel : " + right_wheel + " head : " + neck + " key : " + key)
        self.left_wheel = self.set(left_wheel)
        self.right_wheel = self.set(right_wheel)
        self.neck = self.set(neck)
        self.key = self.set(key)

    @staticmethod
    def set(input):
        if not input or input == " ":
            return None
        else:
            return input
