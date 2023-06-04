import logging

from dadou_utils.misc import Misc
from dadou_utils.utils.time_utils import TimeUtils


class Animation:

    def __init__(self, datas, duration, animation_type):

        self.global_duration = duration
        self.animation_type = animation_type
        self.has_data = True
        self.first_animation = True
        self.last_time = None
        self.current_element_duration = 0

        if animation_type not in datas or not datas[animation_type] or len(datas[animation_type]) == 0:
            logging.debug("animation part {} is empty".format(animation_type))
            self.has_data = False
            return
        else:
            self.datas = datas[animation_type]

        self.current_pos = 0
        self.last_time = TimeUtils.current_milli_time()
        self.current_element_duration = self.global_duration * self.datas[self.current_pos][0]

    def next(self):
        if self.first_animation:
            self.first_animation = False
            return self.get(self.current_pos)
        if self.has_data and self.current_pos != len(self.datas)-1 and TimeUtils.is_time(self.last_time, self.current_element_duration):
            self.current_pos = (self.current_pos + 1) % len(self.datas)
            self.last_time = TimeUtils.current_milli_time()
            return self.get(self.current_pos)

    def get(self, index):
        logging.info("next {} index {}".format(self.animation_type, index))
        #if self.items_nb == 1:
        return self.datas[index][1]
        #if self.items_nb == 2:
        #    return [self.datas[index][1], self.datas[index][2]]
        #self.current_element_duration = self.global_duration * self.datas[index][0]
