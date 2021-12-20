import unittest
from python.mapping import Mapping
from python.audio import Audio


class AudioTests(unittest.TestCase):
    mapping = Mapping()
    audio = Audio()

    def play(self):
        #self.assertEqual(True, False)  # add assertion here
        audio_path = self.mapping.get_audio_file("A5")
        if audio_path:
            self.audio.play_sound(audio_path)


if __name__ == '__main__':
    unittest.main()
