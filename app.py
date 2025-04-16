from flask import Flask, render_template, request, send_file
from transcriber import transcrever_audio
import os
from werkzeug.utils import secure_filename
import warnings


warnings.filterwarnings("ignore", category=RuntimeWarning)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# variável global para armazenar o texto transcrito
texto_transcrito = ''

@app.route('/', methods=['GET', 'POST'])
def index():
    global texto_transcrito
    texto = ''
    if request.method == 'POST':
        if 'audio' in request.files:
            arquivo = request.files['audio']
            if arquivo.filename != '':
                idioma = request.form.get('idioma', 'pt-BR')
                caminho = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(arquivo.filename))
                arquivo.save(caminho)
                texto = transcrever_audio(caminho, idioma=idioma)
                texto_transcrito = texto
    return render_template('index.html', texto=texto)

@app.route('/download_txt')
def download_txt():
    global texto_transcrito
    with open('transcricao.txt', 'w', encoding='utf-8') as f:
        f.write(texto_transcrito)
    return send_file('transcricao.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
