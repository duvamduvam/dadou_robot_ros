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
        self.left_wheel = left_wheel
        self.right_wheel = right_wheel
        self.neck = neck
        self.key = key

