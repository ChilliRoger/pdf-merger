from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import os
import uuid
from werkzeug.utils import secure_filename
import io
from PIL import Image
import fitz  # PyMuPDF
import json

app = Flask(__name__, template_folder='../templates')
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['MERGED_FOLDER'] = '/tmp/merged'
app.config['EDIT_FOLDER'] = '/tmp/edit_sessions'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MERGED_FOLDER'], exist_ok=True)
os.makedirs(app.config['EDIT_FOLDER'], exist_ok=True)

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


# PDF EDITING ROUTES

@app.route('/edit-mode', methods=['GET'])
def edit_mode():
    """Show the upload page for PDF editing"""
    return render_template('upload_for_edit.html')


@app.route('/process-upload-for-edit', methods=['POST'])
def process_upload_for_edit():
    """Process uploaded PDF and show page editor"""
    pdf_file = request.files.get('pdf_file')
    
    if not pdf_file or pdf_file.filename == '':
        return redirect(url_for('edit_mode'))
    
    # Create unique session ID
    session_id = uuid.uuid4().hex
    session_dir = os.path.join(app.config['EDIT_FOLDER'], session_id)
    os.makedirs(session_dir, exist_ok=True)
    
    # Save uploaded PDF
    pdf_path = os.path.join(session_dir, 'original.pdf')
    pdf_file.save(pdf_path)
    
    # Get total pages
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    
    return render_template('edit_pages.html', 
                          session_id=session_id, 
                          total_pages=total_pages)


@app.route('/page-image/<session_id>/<int:page_num>', methods=['GET'])
def page_image(session_id, page_num):
    """Generate and serve page preview image"""
    try:
        pdf_path = os.path.join(app.config['EDIT_FOLDER'], session_id, 'original.pdf')
        
        # Check if file exists
        if not os.path.exists(pdf_path):
            return "PDF not found", 404
        
        # Open PDF with PyMuPDF
        doc = fitz.open(pdf_path)
        
        # Validate page number
        if page_num < 1 or page_num > len(doc):
            doc.close()
            return "Invalid page number", 404
        
        page = doc[page_num - 1]  # PyMuPDF uses 0-based indexing
        
        # Render page to image with lower quality for faster loading
        # Reduced from 1.5 to 1.0 for faster generation and smaller file size
        pix = page.get_pixmap(matrix=fitz.Matrix(1.0, 1.0), alpha=False)
        
        # Convert to JPEG for smaller file size (faster loading)
        img_data = pix.tobytes("jpeg", jpg_quality=75)
        
        doc.close()
        
        return send_file(
            io.BytesIO(img_data),
            mimetype='image/jpeg',
            as_attachment=False,
            download_name=f'page_{page_num}.jpg'
        )
    except Exception as e:
        print(f"Error generating page image for page {page_num}: {e}")
        import traceback
        traceback.print_exc()
        return f"Error generating image: {str(e)}", 500


@app.route('/apply-edits', methods=['POST'])
def apply_edits():
    """Apply page removals and insertions, then show success page"""
    try:
        session_id = request.form.get('session_id')
        removed_pages_json = request.form.get('removed_pages', '[]')
        removed_pages = set(json.loads(removed_pages_json))
        
        # Load original PDF
        pdf_path = os.path.join(app.config['EDIT_FOLDER'], session_id, 'original.pdf')
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        # Collect all insertion keys from the request
        all_insertion_keys = []
        for key in request.files.keys():
            if key.startswith('insert_after_'):
                all_insertion_keys.append(key)
        
        # Process each page
        for page_num in range(1, len(reader.pages) + 1):
            # Skip removed pages
            if page_num not in removed_pages:
                writer.add_page(reader.pages[page_num - 1])
            
            # Check for insertions after this page (including nested ones)
            page_insert_keys = [k for k in all_insertion_keys if k.startswith(f'insert_after_{page_num}')]
            
            for insert_key in page_insert_keys:
                if insert_key in request.files:
                    insert_files = request.files.getlist(insert_key)
                    for insert_file in insert_files:
                        if insert_file.filename != '':
                            # Read the inserted PDF
                            insert_reader = PdfReader(insert_file.stream)
                            # Add all pages from inserted PDF
                            for insert_page in insert_reader.pages:
                                writer.add_page(insert_page)
        
        # Save edited PDF
        output_path = os.path.join(app.config['EDIT_FOLDER'], session_id, 'edited.pdf')
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        # Return success page instead of direct download
        return render_template('edit_success.html', session_id=session_id)
        
    except Exception as e:
        print(f"Error applying edits: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/download-edited/<session_id>', methods=['GET'])
def download_edited(session_id):
    """Download the edited PDF"""
    try:
        output_path = os.path.join(app.config['EDIT_FOLDER'], session_id, 'edited.pdf')
        return send_file(output_path, as_attachment=True, download_name='edited.pdf')
    except Exception as e:
        print(f"Error downloading edited PDF: {e}")
        return "Error downloading file", 500


if __name__ == '__main__':
    app.run(debug=True)
