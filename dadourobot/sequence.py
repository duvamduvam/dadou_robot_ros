from dadourobot.utils import Utils


class Sequence:
    duration = 0
    loop = False
    elements = []
    current_element = {}
    pos = 0
    start_time = Utils.current_milli_time()

    def __init__(self, duration, loop, elements):
        self.duration = duration
        self.loop = loop
        self.elements = elements
        self.current_element = elements[self.pos]
        self.start_time = Utils.current_milli_time()

    def next(self):
        self.pos = (self.pos + 1) % len(self.elements)
        self.current_element = self.elements[self.pos]
