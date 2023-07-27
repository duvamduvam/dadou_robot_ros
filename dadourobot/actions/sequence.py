from dadou_utils.utils.time_utils import TimeUtils


class Sequence:
    duration = 0
    loop = False
    elements = []
    current_element = {}
    pos = 0
    start_time = TimeUtils.current_milli_time()

    def __init__(self, duration, loop, elements, duration_position):
        self.duration = duration
        self.duration_position = duration_position
        self.loop = loop
        self.elements = elements
        self.current_element = elements[self.pos]
        self.start_time = TimeUtils.current_milli_time()

    def get_current_element(self):
        return self.elements[self.pos]

    def next(self):
        self.start_time = TimeUtils.current_milli_time()
        self.pos = (self.pos + 1) % len(self.elements)

    def time_to_switch(self):
        return TimeUtils.is_time(self.start_time, self.elements[self.pos][self.duration_position])
