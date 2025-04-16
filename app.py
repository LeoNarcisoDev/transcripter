from flask import Flask, render_template, request, send_file, redirect, url_for
from transcriber import transcrever_audio
from werkzeug.utils import secure_filename
from datetime import datetime
import os, json, uuid
from flask import jsonify

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
HISTORICO_ARQ = 'historico.json'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# carregar histórico
if os.path.exists(HISTORICO_ARQ):
    with open(HISTORICO_ARQ, 'r', encoding='utf-8') as f:
        historico = json.load(f)
else:
    historico = []

@app.route('/', methods=['GET', 'POST'])
def index():
    texto = ''
    traducao = ''
    if request.method == 'POST':
        if 'audio' in request.files:
            arquivo = request.files['audio']
            idioma = request.form.get('idioma', 'pt-BR')
            if arquivo.filename != '':
                nome_seguro = secure_filename(arquivo.filename)
                caminho = os.path.join(app.config['UPLOAD_FOLDER'], nome_seguro)
                arquivo.save(caminho)

                texto, traducao = transcrever_audio(caminho, idioma=idioma)

                id_transcricao = str(uuid.uuid4())
                registro = {
                    'id': id_transcricao,
                    'arquivo': nome_seguro,
                    'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'idioma': idioma,
                    'texto': texto,
                    'traducao': traducao
                }

                historico.append(registro)
                with open(HISTORICO_ARQ, 'w', encoding='utf-8') as f:
                    json.dump(historico, f, ensure_ascii=False, indent=4)

    return render_template('index.html', texto_original=texto, traducao=traducao)

@app.route('/historico')
def ver_historico():
    return render_template('historico.html', historico=historico)

@app.route('/baixar/<id>')
def baixar_transcricao(id):
    for registro in historico:
        if registro['id'] == id:
            nome_arquivo = f"{registro['arquivo'].rsplit('.', 1)[0]}_{registro['data'].replace(':','-')}.txt"
            caminho_txt = os.path.join("uploads", nome_arquivo)
            with open(caminho_txt, 'w', encoding='utf-8') as f:
                f.write(f"Transcrição original ({registro['idioma']}):\n{registro['texto']}\n\n")
                f.write(f"Tradução para pt-BR:\n{registro['traducao']}")
            return send_file(caminho_txt, as_attachment=True)
    return "Transcrição não encontrada", 404

@app.route('/ao-vivo')
def ao_vivo():
    return render_template('ao_vivo.html')

@app.route('/transcrever', methods=['POST'])
def transcrever_microfone():
    import speech_recognition as sr

    reconhecedor = sr.Recognizer()
    try:
        with sr.Microphone() as fonte:
            reconhecedor.adjust_for_ambient_noise(fonte)
            audio = reconhecedor.listen(fonte)
            texto = reconhecedor.recognize_google(audio, language="pt-BR")
            return jsonify({"texto": texto})
    except sr.UnknownValueError:
        return jsonify({"texto": "🤔 Não entendi o que foi dito."})
    except Exception as e:
        return jsonify({"texto": f"Erro: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
