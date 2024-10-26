import pyttsx3

from config import settings


speaker = pyttsx3.init()
voices = speaker.getProperty('voices')
for voice in voices:
    if voice.name == 'Microsoft Irina Desktop - Russian':
        speaker.setProperty('voice', voice.id)
speaker.setProperty('rate', settings.voice_speed_rate)
speaker.runAndWait()
