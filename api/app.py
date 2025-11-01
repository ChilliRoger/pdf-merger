from flask import Flask, render_template, request, send_file, redirect, url_for
from PyPDF2 import PdfMerger
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='../templates')
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['MERGED_FOLDER'] = '/tmp/merged'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MERGED_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_files = int(request.form['num_files'])
        return render_template('upload.html', num_files=num_files)
    return render_template('index.html')


@app.route('/merge', methods=['POST'])
def merge_pdfs():
    merger = PdfMerger()
    uploaded_files = request.files.getlist('pdf_files')

    file_paths = []
    for idx, file in enumerate(uploaded_files):
        if file.filename != '':
            # Create unique filename to allow same file in multiple slots
            original_filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{idx}_{original_filename}"
            path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(path)
            file_paths.append(path)

    for path in file_paths:
        merger.append(path)

    output_path = os.path.join(app.config['MERGED_FOLDER'], 'merged.pdf')
    merger.write(output_path)
    merger.close()

    # Clean uploaded files
    for path in file_paths:
        os.remove(path)

    return render_template('result.html')


@app.route('/download', methods=['GET'])
def download():
    output_path = os.path.join(app.config['MERGED_FOLDER'], 'merged.pdf')
    return send_file(output_path, as_attachment=True)


@app.route('/restart', methods=['GET'])
def restart():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
