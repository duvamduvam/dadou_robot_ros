from enum import Enum

from dadou_utils_ros.utils.time_utils import TimeUtils
from dadou_utils_ros.utils_static import DURATION, MOUTHS


class LedPart(Enum):
    LEYE = 1
    REYE = 2
    MOUTH = 3


class FaceSequence:

    EYE_FOLDER = "eye/"
    MOUTH_FOLDER = "mouth/"

    leyes_pos = 0
    reyes_pos = 0
    mouths_pos = 0

    leyes_time = 0
    reyes_time = 0
    mouths_time = 0

    current_element = None

    def __init__(self, json):
        self.mouths = json[MOUTHS]
        self.leyes = json[RIGHTS_EYES]
        self.reyes = json[LEFT_EYES]
        self.duration = json[DURATION]
        self.loop = json[DURATION]
        self.start_time = TimeUtils.current_milli_time()

    def get_pos(self, part: LedPart):
        if part == LedPart.LEYE:
            return self.leyes_pos
        if part == LedPart.REYE:
            return self.reyes_pos
        if part == LedPart.MOUTH:
            return self.mouths_pos

    def get_frames(self, part: LedPart):
        if part == LedPart.LEYE:
            return self.leyes
        if part == LedPart.REYE:
            return self.reyes
        if part == LedPart.MOUTH:
            return self.mouths

    def get_current_frame(self, part: LedPart):
        frames = self.get_frames(part)
        pos = self.get_pos(part)
        return frames[pos]

    def get_part_time(self, part: LedPart):
        if part == LedPart.LEYE:
            return self.leyes_time
        if part == LedPart.REYE:
            return self.reyes_time
        if part == LedPart.MOUTH:
            return self.mouths_time

    def time_to_switch(self, part: LedPart):
        pos = self.get_pos(part)
        frames = self.get_frames(part)
        time = self.get_part_time(part)
        return TimeUtils.is_time(time, frames[pos][0])

    def folder(self, part: LedPart):
        if part == LedPart.LEYE or part == LedPart.REYE:
            return self.EYE_FOLDER
        if part == LedPart.MOUTH:
            return self.MOUTH_FOLDER

    def next(self, part: LedPart):
        pos = self.get_pos(part)
        frames = self.get_frames(part)
        return (pos + 1) % len(frames)
