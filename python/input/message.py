import logging


class Message:
    key = None
    left_wheel = None
    right_wheel = None
    head = None

    PREFIX = '<'
    POSTFIX = '>'

    def __self__(self, left_wheel, right_wheel, head, key):
        logging.info(
            "new message left wheel : " + left_wheel + " right_wheel : " + right_wheel + " head : " + head + " key : " + key)
        self.left_wheel = left_wheel
        self.right_wheel = right_wheel
        self.head = head
        self.key = key

    @staticmethod
    def decode(msg: str):
        if msg.startswith(Message.PREFIX) and msg.endswith(Message.POSTFIX):
            return Message(msg[1], msg[2], msg[3], msg[4] + msg[5])
        else:
            logging.error("wrong message : \"" + msg + "\"")
            return None
