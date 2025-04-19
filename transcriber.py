import whisper
from deep_translator import GoogleTranslator
import os

def transcrever_audio(caminho_arquivo, idioma='pt'):
    try:
        # Carregar o modelo apenas quando a função for chamada (economiza memória)
        model = whisper.load_model("tiny")  # modelos: tiny, base, small, medium, large

        # Executa a transcrição
        resultado = model.transcribe(caminho_arquivo, language=idioma)

        texto = resultado["text"].strip()

        # Tradução para português BR (se necessário)
        if idioma != "pt" and texto:
            translator = GoogleTranslator(source=idioma, target="pt")
            traducao = translator.translate(texto)
        else:
            traducao = texto  # já está em pt

        return texto, traducao

    except Exception as e:
        print(f"[ERRO] Falha na transcrição: {e}")
        return "Erro ao transcrever", "Erro ao traduzir"
