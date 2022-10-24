import logging

from dadou_utils.misc import Misc
from dadou_utils.time.time_utils import TimeUtils


class Animation:

    def __init__(self, datas, duration, animation_type, items_nb):
        self.datas = datas
        self.global_duration = duration
        self.animation_type = animation_type
        self.has_data = True
        self.last_time = None
        self.current_element_duration = 0
        #self.time_pos = time_pos
        self.items_nb = items_nb
        #self.current_action_done = False

        if not (self.datas and len(self.datas) > 0):
            logging.warning("animation part {} is empty".format(animation_type))
            self.has_data = False
            return

        self.current_pos = 0
        self.last_time = TimeUtils.current_milli_time()
        self.set_current_duration()

    def next(self):
        if self.has_data and TimeUtils.is_time(self.last_time, self.current_element_duration):
            self.current_pos = (self.current_pos + 1) % len(self.datas)
            self.last_time = TimeUtils.current_milli_time()
            self.set_current_duration()
            logging.info("next {} pos {}".format(self.animation_type, self.current_pos))
            if self.items_nb == 1:
                return self.datas[self.current_pos][0]
            if self.items_nb == 2:
                return [self.datas[self.current_pos][0], self.datas[self.current_pos][1]]

    def set_current_duration(self):
        self.current_element_duration = self.global_duration * Misc.cast_float(self.datas[self.current_pos][0])
