from python.utils import Utils


class Sequence:
    duration = 0
    current_time = Utils.current_milli_time()
    loop = False
    frames = []
    current_frame = 0

    def __init__(self, duration, loop, frames):
        self.duration = duration
        self.loop = loop
        self.frames = frames