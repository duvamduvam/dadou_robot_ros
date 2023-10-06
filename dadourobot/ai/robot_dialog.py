import logging

import openai
import whisper
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

import speech_recognition as sr
import pyttsx3

from dadou_utils.utils_static import FACE, ANIMATION, STOP


class RobotDialog:



    def __init__(self, global_receiver):
        key_file = open('../../conf/chatgpt-key.txt', 'r')
        key = key_file.read()
        key_file.close()
        openai.api_key = key
        self.recognizer = sr.Recognizer()
        self.global_receiver = global_receiver

    # Initialize the recognizer


    # Function to convert text to
    # speech
    def speakText(self, command):
        # Initialize the engine
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()

    def request(self, msg):
        response = openai.Completion.create(
            engine='text-davinci-003',  # Modèle à utiliser
            prompt=msg,
            max_tokens=100  # Limite de la réponse générée
        )
        response_text = response.choices[0].text.strip()
        logging.info(response_text)
        return response_text

    def chatgpt_request(self, text_request):
        return self.request(text_request)

    def msg_to_audio(self, msg, method='google'):
        if method == 'google':
            gTTS(text=msg, lang="fr", tld="ca").save("response.mp3")
            audio = AudioSegment.from_file('response.mp3', format='mp3')
            play(audio)
        elif method == 'whisper':
            model = whisper.load_model("base")
            #whisper_folder = os.getenv("WHISPER_FOLDER")
            #whisper = openai.Whisper(whisper_folder)
            audio_path = "output.wav"
            whisper.tts(msg, audio_path)
            audio = AudioSegment.from_file(audio_path, format='wav')
            play(audio)
            return {"duration": audio.duration_seconds}

    def listen(self):
        # Exception handling to handle
        # exceptions at the runtime
        try:
            # use the microphone as source for input.
            with sr.Microphone() as source2:

                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                self.recognizer.adjust_for_ambient_noise(source2, duration=0.2)

                # listens for the user's input
                audio2 = self.recognizer.listen(source2)

                # Using google to recognize audio
                text = self.recognizer.recognize_google(audio2, language="fr-FR")
                text = text.lower()

                logging.info("audio recognise text : {}".format(text))
                return text

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError as e:
            print("unknown error occurred {0}".format(e))

    def process(self):
        audio_input = self.listen()
        if audio_input:
            self.global_receiver.write_values({FACE: "think"})
            ai_response = self.chatgpt_request(audio_input)
            self.msg_to_audio(ai_response)
            self.global_receiver.write_values({FACE: "speak"})
            self.global_receiver.write_values({ANIMATION: STOP})


# Python program to translate
# speech to text and text to speech






# Loop infinitely for user to
# speak
