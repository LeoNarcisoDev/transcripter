import os
import whisper
from datetime import datetime
from deep_translator import GoogleTranslator

model = whisper.load_model("base")  # pode usar "small", "medium" ou "large"

def transcrever_audio(caminho_audio, idioma='pt'):
    try:
        resultado = model.transcribe(caminho_audio)

        texto = resultado['text'].strip()
        idioma_detectado = resultado['language']

        # Traduz para português se não for pt
        if idioma_detectado != 'pt':
            traducao = GoogleTranslator(source=idioma_detectado, target="pt").translate(texto)
        else:
            traducao = texto

        return texto, traducao

    except Exception as e:
        return f"[Erro na transcrição: {e}]", ""
    finally:
        if os.path.exists(caminho_audio):
            os.remove(caminho_audio)
