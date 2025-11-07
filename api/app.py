from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import os
import uuid
from werkzeug.utils import secure_filename
import io
from PIL import Image
import fitz  # PyMuPDF
import json
import warnings

# Suppress PyPDF2 warnings about malformed PDFs
warnings.filterwarnings("ignore", category=UserWarning, module="PyPDF2")

app = Flask(__name__, template_folder='../templates')
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['MERGED_FOLDER'] = '/tmp/merged'
app.config['EDIT_FOLDER'] = '/tmp/edit_sessions'
# Note: Vercel has limits - Free: 4.5MB, Pro: 100MB
# Local development can handle up to 500MB
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB for Vercel Pro compatibility
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for development

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
    try:
        merger = PdfMerger()
        uploaded_files = request.files.getlist('pdf_files')

        if not uploaded_files or len(uploaded_files) == 0:
            return jsonify({'error': 'No files uploaded'}), 400

        file_paths = []
        total_size = 0
        
        # Adjusted for Vercel limits (50MB per file for safety)
        MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB per file
        
        for idx, file in enumerate(uploaded_files):
            if file.filename != '':
                # Validate file size (individual file should not exceed 100MB)
                file.seek(0, os.SEEK_END)
                file_size = file.tell()
                file.seek(0)
                
                if file_size > MAX_FILE_SIZE:
                    return jsonify({'error': f'File {file.filename} exceeds {MAX_FILE_SIZE/(1024*1024)}MB limit'}), 400
                
                total_size += file_size
                
                # Create unique filename to allow same file in multiple slots
                original_filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{idx}_{original_filename}"
                path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                
                # Save in chunks for large files
                with open(path, 'wb') as f:
                    while True:
                        chunk = file.read(8192)  # 8KB chunks
                        if not chunk:
                            break
                        f.write(chunk)
                
                file_paths.append(path)

        # Merge PDFs with better memory management
        for path in file_paths:
            try:
                merger.append(path)
            except Exception as e:
                # Clean up on error
                for p in file_paths:
                    if os.path.exists(p):
                        os.remove(p)
                return jsonify({'error': f'Error merging PDF: {str(e)}'}), 500

        output_filename = f"merged_{uuid.uuid4().hex}.pdf"
        output_path = os.path.join(app.config['MERGED_FOLDER'], output_filename)
        merger.write(output_path)
        merger.close()

        # Clean uploaded files
        for path in file_paths:
            if os.path.exists(path):
                os.remove(path)

        return jsonify({'success': True, 'filename': output_filename})
    
    except Exception as e:
        print(f"Error in merge_pdfs: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    try:
        # Sanitize filename to prevent directory traversal
        safe_filename = secure_filename(filename)
        output_path = os.path.join(app.config['MERGED_FOLDER'], safe_filename)
        
        if not os.path.exists(output_path):
            return "File not found", 404
        
        response = send_file(output_path, as_attachment=True, download_name='merged.pdf')
        
        # Clean up after download
        try:
            os.remove(output_path)
        except:
            pass
            
        return response
    except Exception as e:
        print(f"Error in download: {e}")
        return "Error downloading file", 500


@app.route('/restart', methods=['GET'])
def restart():
    return redirect(url_for('index'))


@app.route('/merge-result', methods=['GET'])
def merge_result():
    """Show merge success page"""
    filename = request.args.get('filename', 'merged.pdf')
    return render_template('result.html', filename=filename)


# PDF EDITING ROUTES

@app.route('/edit-mode', methods=['GET'])
def edit_mode():
    """Show the upload page for PDF editing"""
    return render_template('upload_for_edit.html')


@app.route('/edit-pages', methods=['GET'])
def edit_pages():
    """Show the page editor"""
    session_id = request.args.get('session_id')
    total_pages = request.args.get('total_pages', 0, type=int)
    
    if not session_id or total_pages == 0:
        return redirect(url_for('edit_mode'))
    
    return render_template('edit_pages.html', 
                          session_id=session_id, 
                          total_pages=total_pages)


@app.route('/process-upload-for-edit', methods=['POST'])
def process_upload_for_edit():
    """Process uploaded PDF and show page editor"""
    try:
        pdf_file = request.files.get('pdf_file')
        
        if not pdf_file or pdf_file.filename == '':
            return jsonify({'error': 'No file uploaded'}), 400
        
        # Check file size
        pdf_file.seek(0, os.SEEK_END)
        file_size = pdf_file.tell()
        pdf_file.seek(0)
        
        MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB for Vercel compatibility
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': f'File size exceeds {MAX_FILE_SIZE/(1024*1024)}MB limit'}), 400
        
        # Create unique session ID
        session_id = uuid.uuid4().hex
        session_dir = os.path.join(app.config['EDIT_FOLDER'], session_id)
        os.makedirs(session_dir, exist_ok=True)
        
        # Save uploaded PDF in chunks for large files
        pdf_path = os.path.join(session_dir, 'original.pdf')
        with open(pdf_path, 'wb') as f:
            while True:
                chunk = pdf_file.read(8192)  # 8KB chunks
                if not chunk:
                    break
                f.write(chunk)
        
        # Get total pages
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'total_pages': total_pages
        })
        
    except Exception as e:
        print(f"Error in process_upload_for_edit: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/page-image/<session_id>/<int:page_num>', methods=['GET'])
def page_image(session_id, page_num):
    """Generate and serve page preview image"""
    try:
        # Sanitize session_id to prevent directory traversal
        safe_session_id = secure_filename(session_id)
        pdf_path = os.path.join(app.config['EDIT_FOLDER'], safe_session_id, 'original.pdf')
        
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
        
        # Render page to image with optimized settings for large files
        # Use lower resolution for faster generation
        pix = page.get_pixmap(matrix=fitz.Matrix(0.8, 0.8), alpha=False)
        
        # Convert to JPEG with lower quality for faster loading and smaller size
        img_data = pix.tobytes("jpeg", jpg_quality=60)
        
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
    """Apply page removals, insertions, and reordering, then show success page"""
    try:
        session_id = request.form.get('session_id')
        if not session_id:
            return jsonify({'error': 'No session ID provided'}), 400
            
        # Sanitize session_id
        safe_session_id = secure_filename(session_id)
        
        removed_pages_json = request.form.get('removed_pages', '[]')
        removed_pages = set(json.loads(removed_pages_json))
        
        # Get page order if provided
        page_order_json = request.form.get('page_order', '[]')
        page_order = json.loads(page_order_json)
        
        # Load original PDF
        pdf_path = os.path.join(app.config['EDIT_FOLDER'], safe_session_id, 'original.pdf')
        
        if not os.path.exists(pdf_path):
            return jsonify({'error': 'Session not found'}), 404
            
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        # If page order is provided, use it; otherwise use default sequential order
        if page_order and len(page_order) > 0:
            # Process pages in the order specified by drag-and-drop
            for item in page_order:
                if item['type'] == 'page':
                    page_num = int(item['value'])
                    # Skip removed pages
                    if page_num not in removed_pages:
                        writer.add_page(reader.pages[page_num - 1])
                
                elif item['type'] == 'insert':
                    insert_key = f"insert_after_{item['value']}"
                    if insert_key in request.files:
                        insert_files = request.files.getlist(insert_key)
                        for insert_file in insert_files:
                            if insert_file.filename != '':
                                # Read the inserted PDF
                                insert_reader = PdfReader(insert_file.stream)
                                # Add all pages from inserted PDF
                                for insert_page in insert_reader.pages:
                                    writer.add_page(insert_page)
        else:
            # Fallback to original logic if no page order provided
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
        output_path = os.path.join(app.config['EDIT_FOLDER'], safe_session_id, 'edited.pdf')
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        # Return success response
        return jsonify({
            'success': True,
            'session_id': safe_session_id
        })
        
    except Exception as e:
        print(f"Error applying edits: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/download-edited/<session_id>', methods=['GET'])
def download_edited(session_id):
    """Download the edited PDF"""
    try:
        # Sanitize session_id
        safe_session_id = secure_filename(session_id)
        output_path = os.path.join(app.config['EDIT_FOLDER'], safe_session_id, 'edited.pdf')
        
        if not os.path.exists(output_path):
            return "File not found", 404
        
        response = send_file(output_path, as_attachment=True, download_name='edited.pdf')
        
        # Clean up session after download
        try:
            session_dir = os.path.join(app.config['EDIT_FOLDER'], safe_session_id)
            if os.path.exists(session_dir):
                import shutil
                shutil.rmtree(session_dir)
        except Exception as cleanup_error:
            print(f"Error cleaning up session: {cleanup_error}")
        
        return response
    except Exception as e:
        print(f"Error downloading edited PDF: {e}")
        return "Error downloading file", 500


@app.route('/edit-success', methods=['GET'])
def edit_success():
    """Show edit success page"""
    session_id = request.args.get('session_id')
    if not session_id:
        return redirect(url_for('edit_mode'))
    return render_template('edit_success.html', session_id=session_id)


if __name__ == '__main__':
    app.run(debug=True)
