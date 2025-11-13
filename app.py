# app.py
import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import PyPDF2
from ai_processor import classify_email, suggest_response

app = Flask(__name__)

# Configuração para upload de arquivos
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def read_pdf(file_path):
    """Extrai texto de um arquivo PDF."""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
            return text
    except Exception as e:
        print(f"Erro ao ler PDF: {e}")
        return None

@app.route('/')
def index():
    """Renderiza a página HTML principal."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Endpoint da API para analisar o email."""
    email_text = ""

    # Verifica se o texto foi enviado diretamente no formulário
    if 'email_text' in request.form and request.form['email_text'].strip():
        email_text = request.form['email_text']
    # Senão, verifica se um arquivo foi enviado
    elif 'email_file' in request.files:
        file = request.files['email_file']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            if filename.lower().endswith('.txt'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        email_text = f.read()
                except Exception as e:
                    return jsonify({"error": f"Erro ao ler arquivo de texto: {e}"}), 500
            elif filename.lower().endswith('.pdf'):
                email_text = read_pdf(file_path)
                if email_text is None:
                    return jsonify({"error": "Não foi possível extrair texto do arquivo PDF."}), 500

            # Limpa o arquivo após o processamento para economizar espaço
            os.remove(file_path)

    if not email_text or not email_text.strip():
        return jsonify({"error": "Nenhum texto ou arquivo válido foi enviado."}), 400

    # Usa nosso módulo de IA para processar o texto
    category = classify_email(email_text)
    response = suggest_response(email_text, category)

    return jsonify({
        "category": category,
        "suggested_response": response
    })

if __name__ == '__main__':
    # Para desenvolvimento local, use o servidor do Flask.
    # Para produção, use 'gunicorn app:app'.
    app.run(host='0.0.0.0', port=5000, debug=True)
