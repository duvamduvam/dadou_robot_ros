import logging

import openai
import whisper
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play


class Chatgpt:

    def __init__(self):
        key_file = open('../../conf/chatgpt-key.txt', 'r')
        key = key_file.read()
        key_file.close()
        openai.api_key = key

    def request(self, msg):
        response = openai.Completion.create(
            engine='text-davinci-003',  # Modèle à utiliser
            prompt=msg,
            max_tokens=100  # Limite de la réponse générée
        )
        response_text = response.choices[0].text.strip()
        logging.info(response_text)
        return response_text

    def request_to_audio(self, msg, method='google'):
        response_txt = self.request(msg)
        if method == 'google':
            gTTS(text=response_txt, lang="fr", tld="ca").save("response.mp3")
            audio = AudioSegment.from_file('response.mp3', format='mp3')
            play(audio)
        elif method == 'whisper':
            model = whisper.load_model("base")
            #whisper_folder = os.getenv("WHISPER_FOLDER")
            #whisper = openai.Whisper(whisper_folder)
            audio_path = "output.wav"
            whisper.tts(response_txt, audio_path)
            audio = AudioSegment.from_file(audio_path, format='wav')
            play(audio)
