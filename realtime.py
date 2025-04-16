import speech_recognition as sr

def transcrever_ao_vivo():
    reconhecedor = sr.Recognizer()

    try:
        with sr.Microphone() as fonte:
            print("🎙️ Fale algo... (pressione CTRL+C para encerrar)")
            reconhecedor.adjust_for_ambient_noise(fonte)
            while True:
                try:
                    print("⏺️ Aguardando sua fala...")
                    audio = reconhecedor.listen(fonte)
                    texto = reconhecedor.recognize_google(audio, language="pt-BR")
                    print("📝 Você disse:", texto)
                except sr.UnknownValueError:
                    print("🤔 Não entendi o que foi dito.")
                except sr.RequestError:
                    print("❌ Erro ao acessar o serviço de transcrição (verifique sua internet).")
    except KeyboardInterrupt:
        print("\n⏹️ Transcrição encerrada pelo usuário.")
    except OSError as e:
        print(f"❌ Erro de microfone: {e}. Verifique se há um dispositivo padrão conectado.")

if __name__ == "__main__":
    transcrever_ao_vivo()
