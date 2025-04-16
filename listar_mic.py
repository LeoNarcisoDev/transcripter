import speech_recognition as sr

print("\n🔊 Dispositivos de entrada de áudio disponíveis:\n")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{index}: {name}")
