import openai
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

# Ouvre le fichier en mode lecture
key_file = open('../../conf/chatgpt-key.txt', 'r')
key = key_file.read()
key_file.close()

openai.api_key = key
response = openai.Completion.create(
    engine='text-davinci-003',  # Modèle à utiliser
    prompt='l ai est elle dangeureuse ?',
    max_tokens=100  # Limite de la réponse générée
)

response_text = response.choices[0].text.strip()
print(response_text)  # Affiche la réponse générée

gTTS(text=response_text, lang="fr", tld="ca").save("response.mp3")


audio = AudioSegment.from_file('response.mp3', format='mp3')
play(audio)


