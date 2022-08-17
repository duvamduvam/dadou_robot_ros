import logging

from dadou_utils.misc import Misc


class Message:
    key = None
    left_wheel = None
    right_wheel = None
    neck = None

    PREFIX = '<'
    POSTFIX = '>'

    def set(self, msg):

        self.key = None
        self.left_wheel = None
        self.right_wheel = None
        self.neck = None

        if not msg or msg.strip() == 0 or not msg.startswith(self.PREFIX) \
                or not msg.endswith(self.POSTFIX):
            return None
        else:
            msg = msg[1:len(msg) - 1].strip()
            if len(msg) == 3:
                self.left_wheel = msg[0]
                self.right_wheel = msg[1]
                self.neck = msg[2]
            elif len(msg) > 3:
                self.left_wheel = msg[0]
                self.right_wheel = msg[1]
                self.neck = msg[2]
                self.key = msg[3:5]

            else:
                self.key = msg

            if self.key and not Misc.is_input_ok(self.key):
                self.key = None
            logging.debug("message key {}".format(self.key))
        return self
