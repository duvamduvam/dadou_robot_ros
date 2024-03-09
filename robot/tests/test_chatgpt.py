import unittest

from robot.ai.robot_dialog import RobotDialog


class TestChatgpt(unittest.TestCase):

    robot_dialog = RobotDialog(None)
    def test_simple_request_google_audio(self):
        self.chatgpt.request_to_audio("c'est l'histoire dans la révolutino francaise en 5 lignes?", "google")

    def test_simple_request_whisper_audio(self):
        self.chatgpt.request_to_audio("c'est quoi l'histoire du funk ?")

    def test_listen(self):
        while 1:
            self.robot_dialog.process()

    def test_translate(self):
        f = open("/home/dadou/tmp/chaco-modif3.txt", "r")
        print(f.read())
        self.robot_dialog.translate(f.read())

if __name__ == '__main__':
    unittest.main()
