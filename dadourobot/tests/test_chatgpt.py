import unittest

from dadourobot.ai.chat_gpt import Chatgpt


class TestChatgpt(unittest.TestCase):

    chatgpt = Chatgpt()
    def test_simple_request_google_audio(self):
        self.chatgpt.request_to_audio("c'est l'histoire dans la révolutino francaise en 5 lignes?", "google")

    def test_simple_request_whisper_audio(self):
        self.chatgpt.request_to_audio("c'est quoi l'histoire du funk ?")

if __name__ == '__main__':
    unittest.main()
