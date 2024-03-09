import logging

from dadou_utils.utils.time_utils import TimeUtils


class Animation:

    def __init__(self, datas, duration, animation_type):

        self.global_duration = duration
        self.animation_type = animation_type
        self.has_data = True
        self.first_animation = True
        self.last_time = None
        self.start_time = TimeUtils.current_milli_time()
        self.next_element_start_duration = 0

        if animation_type not in datas or not datas[animation_type] or len(datas[animation_type]) == 0:
            logging.debug("animation part {} is empty".format(animation_type))
            self.has_data = False
            return
        else:
            self.datas = datas[animation_type]

        self.current_pos = 0
        self.last_time = TimeUtils.current_milli_time()
        self.next_element_start_duration = None
        if self.datas[0][0] == 0:
            self.start_delay = 0
        else:
            self.start_delay = self.global_duration * self.datas[0][0]


    def next(self):
        if self.first_animation:
            if TimeUtils.is_time(self.start_time, self.start_delay):
                self.first_animation = False
                self.set_next_duration()
                return self.get(self.current_pos)
        elif self.has_data and self.current_pos != len(self.datas)-1 and TimeUtils.is_time(self.start_time, self.next_element_start_duration):
            self.current_pos = (self.current_pos + 1) % len(self.datas)
            self.set_next_duration()



            #self.current_element_duration = self.global_duration * self.datas[self.current_pos][0]
            #self.last_time = TimeUtils.current_milli_time()
            return self.get(self.current_pos)

    def set_next_duration(self):
        if self.current_pos + 1 == len(self.datas):
            self.next_element_start_duration = self.global_duration
        else:
            self.next_element_start_duration = self.global_duration * self.datas[self.current_pos+1][0]

    def get(self, index):
        logging.info("next {} index {}".format(self.animation_type, index))
        #if self.items_nb == 1:
        return self.datas[index][1]
        #if self.items_nb == 2:
        #    return [self.datas[index][1], self.datas[index][2]]
        #self.current_element_duration = self.global_duration * self.datas[index][0]
