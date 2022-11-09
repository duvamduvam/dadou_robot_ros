import logging

from dadou_utils.time.time_utils import TimeUtils


class Sequence:
    duration = 0
    loop = False
    elements = []
    current_element = {}
    pos = 0
    start_time = TimeUtils.current_milli_time()

    def __init__(self, duration, loop, elements, start_pixel):
        self.start_pixel = start_pixel
        self.duration = duration
        self.element_duration = elements[self.pos][1]
        self.loop = loop
        self.elements = elements
        self.current_element = elements[self.pos][0]
        self.start_time = TimeUtils.current_milli_time()

    def get_current_element(self):
        return self.elements[self.pos]

    def next(self):
        self.start_time = TimeUtils.current_milli_time()
        self.pos = (self.pos + 1) % len(self.elements)
        self.element_duration = self.elements[self.pos][1]
        self.current_element = self.elements[self.pos][0]

    def time_to_switch(self):
        duration = self.element_duration * self.duration
        #logging.debug("change face part millis {} duration {}".format(TimeUtils.current_milli_time(), duration))
        return TimeUtils.is_time(self.start_time, duration)
