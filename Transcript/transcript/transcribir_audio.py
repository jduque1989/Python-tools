import speech_recognition as sr
from pydub import AudioSegment

# Ruta del archivo de audio M4A
audio_file_path = "AUDIO-2024-08-08-07-37-20.m4a"

# Convertir archivo M4A a WAV
audio = AudioSegment.from_file(audio_file_path, format="m4a")
wav_file_path = audio_file_path.replace(".m4a", ".wav")
audio.export(wav_file_path, format="wav")

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()

# Transcribir el archivo de audio a texto
with sr.AudioFile(wav_file_path) as source:
    audio_data = recognizer.record(source)
    text = recognizer.recognize_google(audio_data, language="es-ES")

print(text)

