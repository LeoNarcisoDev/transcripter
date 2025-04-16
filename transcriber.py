import os
import speech_recognition as sr
import pydub

# Força explicitamente o caminho do ffmpeg para o pydub
pydub.AudioSegment.converter = r"C:\Users\leoon\Documents\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe"
from pydub import AudioSegment  # só importa depois de setar o converter

def transcrever_audio(caminho_audio, idioma='pt-BR'):
    reconhecedor = sr.Recognizer()
    caminho_wav = caminho_audio

    # Converter para WAV se necessário
    if not caminho_audio.endswith('.wav'):
        audio = AudioSegment.from_file(caminho_audio)
        caminho_wav = caminho_audio.rsplit('.', 1)[0] + '.wav'
        audio.export(caminho_wav, format='wav')

    try:
        with sr.AudioFile(caminho_wav) as fonte:
            audio = reconhecedor.record(fonte)

        texto = reconhecedor.recognize_google(audio, language=idioma)
        return texto

    except sr.UnknownValueError:
        return "Não foi possível entender o áudio."
    except sr.RequestError:
        return "Erro ao acessar o serviço de reconhecimento."

    finally:
        if os.path.exists(caminho_audio):
            os.remove(caminho_audio)
        if caminho_wav != caminho_audio and os.path.exists(caminho_wav):
            os.remove(caminho_wav)
