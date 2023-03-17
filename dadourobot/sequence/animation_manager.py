import logging

from dadou_utils.files.files_utils import FilesUtils
from dadou_utils.misc import Misc
from dadou_utils.utils.time_utils import TimeUtils

from robot_factory import RobotFactory
from robot_config import RobotStatic
from sequence.animation import Animation

#TODO 2 AnimationManager ...
class AnimationManager:

    current_key = None
    playing = False
    last_time = 0
    timeout = 0
    datas = None

    necks_animation = None
    faces_animation = None
    lights_animation = None
    wheels_animation = None

    current_animation = None

    sequences = {}

    def __init__(self):
        #self.face = RobotFactory().face
        self.head = RobotFactory().head
        self.wheels = RobotFactory().wheel
        self.load_sequences()

    def load_sequences(self):
        sequences_files = FilesUtils.get_folder_files(RobotStatic.SEQUENCES_DIRECTORY)
        for sequence_file in sequences_files:
            json_sequence = FilesUtils.open_json(sequence_file, 'r')
            self.sequences[json_sequence['keys']] = json_sequence

    def update(self, key):
        if not (key and key != self.current_key and key in self.sequences):
            return

        logging.info('update animation with {}'.format(key))
        self.current_animation = self.sequences[key]
        self.playing = True

        duration = Misc.cast_float(self.current_animation['duration']) * 1000

        self.necks_animation = Animation(self.current_animation['necks'], duration, 'necks', 1)
        self.faces_animation = Animation(self.current_animation['faces'], duration, 'faces', 1)
        self.lights_animation = Animation(self.current_animation['lights'], duration, 'lights', 1)
        self.wheels_animation = Animation(self.current_animation['wheels'], duration, 'wheels', 2)

    def process(self):

        #if self.necks_animation:
        #    neck_action = self.necks_animation.next()
        #    if neck_action:
        #        self.head.send_msg(neck_action)

        if self.wheels_animation:
            wheels_action = self.wheels_animation.next()
            if wheels_action:
                self.wheels.send_msg(wheels_action)

        #if self.faces_animation:
        #    faces_action = self.wheels_animation.next()
        #    if faces_action:
        #        self.face.send_msg(faces_action)
        