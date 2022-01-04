from python.utils import Utils


class Sequence:
    duration = 0
    start_time = Utils.current_milli_time()
    loop = False
    frames = []
    current_frame = {}
    pos = 0

    def __init__(self, duration, loop, frames):
        self.duration = duration
        self.loop = loop
        self.frames = frames
        self.current_frame = frames[self.pos]

    def next(self):
        self.pos = (self.pos + 1) % len(self.frames)
        self.current_frame = self.frames[self.pos]
