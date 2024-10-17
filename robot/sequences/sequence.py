from dadou_utils.utils.time_utils import TimeUtils


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
        self.loop = loop
        self.elements = elements
        if len(self.elements) == 1:
            self.element_duration = self.duration
        else:
            self.element_duration = (elements[1][0] * self.duration) - (elements[0][0] * self.duration)
        self.current_element = elements[self.pos][1]
        self.start_time = TimeUtils.current_milli_time()
        #self.started = True

    def get_current_element(self):
        return self.elements[self.pos]

    def next(self):
        self.start_time = TimeUtils.current_milli_time()
        if len(self.elements) == 1:
            return 0
        self.pos = (self.pos + 1) % len(self.elements)
        if self.pos == 0:
            self.element_duration = int(self.elements[self.pos][0] * self.duration)
        else:
            self.element_duration = int(self.elements[self.pos][0] * self.duration - self.elements[self.pos-1][0] * self.duration)
        self.current_element = self.elements[self.pos][1]

    def time_to_switch(self):
        #if self.started:
        #    self.started = False
        #    return True
        #logging.debug("change face part millis {} duration {}".format(TimeUtils.current_milli_time(), duration))
        return TimeUtils.is_time(self.start_time, self.element_duration)
