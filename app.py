from flask import Flask, request, render_template, send_file
from utils import convert_pdf_to_ssp_format
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    uploaded_pdf = request.files['voter_pdf']
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input.pdf')
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'ssp_output.pdf')
    uploaded_pdf.save(input_path)

    convert_pdf_to_ssp_format(input_path, output_path)
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
