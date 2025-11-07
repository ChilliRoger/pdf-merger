# PDF Tools - Merge & Edit PDFs Online

A powerful web application built with Flask that allows users to merge multiple PDF files and edit existing PDFs by removing or inserting pages. Features a clean, modern interface with easy-to-use tools for all your PDF needs.

## 🚀 Features

### 📄 PDF Merger
- **Multiple PDF Upload**: Upload and merge 2-50 PDF files at once
- **Large File Support**: Handle PDFs up to 100MB per file (500MB total)
- **Duplicate File Support**: Upload the same PDF file multiple times in different positions
- **Flexible Ordering**: Files are merged in the order they are uploaded
- **Progress Indicators**: Real-time upload and merge progress tracking
- **Chunked Upload**: Optimized handling for large files
- **Download Merged PDF**: Get your combined PDF instantly

### ✂️ PDF Editor (Remove/Insert Pages)
- **Page Preview**: View all pages as thumbnails before editing
- **Large PDF Support**: Edit PDFs up to 100MB with optimized loading
- **Remove Pages**: Click the "- Remove" button to delete unwanted pages
- **Insert Pages**: Click the "+ Insert After" button to add new PDF pages at any position
- **Drag & Drop Reordering**: Rearrange pages by dragging them
- **Multiple Insertions**: Insert multiple PDF files at different positions
- **Visual Feedback**: See which pages are marked for removal in real-time
- **Progress Tracking**: Visual progress for uploads and edits
- **Download Edited PDF**: Get your modified PDF with all changes applied

### 🎨 User Interface
- **Clean Design**: Professional, light-colored interface without gradients
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile devices
- **Help System**: Built-in help button (?) with detailed usage instructions
- **Easy Navigation**: Back buttons on every page for seamless navigation
- **Progress Bars**: Real-time visual feedback for all operations
- **File Size Validation**: Automatic checking of file sizes before upload
- **Success Pages**: Clear confirmation pages after operations complete
- **Error Handling**: User-friendly error messages with helpful guidance


## 📁 Project Structure

```
pdf-merger/
├── api/
│   └── app.py                  # Main Flask application with all routes
├── templates/
│   ├── index.html              # Home page with feature selection and help
│   ├── upload.html             # File upload interface for merging
│   ├── result.html             # Success page for merged PDFs
│   ├── upload_for_edit.html    # PDF upload page for editing
│   ├── edit_pages.html         # Page editor with preview and controls
│   └── edit_success.html       # Success page for edited PDFs
├── uploads/                    # Temporary upload directory
├── merged/                     # Output directory for merged files
├── edit_sessions/              # Temporary storage for editing sessions
├── requirements.txt            # Python dependencies
├── vercel.json                 # Vercel deployment configuration
├── LICENSE                     # MIT License
└── README.md                   # This file
```

## Installation

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd pdf-merger
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python api/app.py
   ```

6. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

### Dependencies

The application requires the following Python packages:

- **Flask**: Web framework for building the application
- **PyPDF2**: Library for PDF manipulation and merging
- **PyMuPDF (fitz)**: High-performance PDF rendering for page previews
- **Pillow**: Python Imaging Library for image processing
- **Werkzeug**: WSGI utility library (included with Flask)

## 📖 Usage

### Merging PDFs

1. **Select Feature**: Click "📄 Merge Multiple PDFs" on the home page
2. **Enter Count**: Specify how many PDF files you want to merge (2-50)
3. **Upload Files**: Select PDF files for each slot
   - You can upload the same file multiple times if needed
   - Files will be merged in the order of the slots
4. **Merge**: Click "Merge PDFs" to combine them
5. **Download**: Download your merged PDF or start a new merge

### Editing PDFs (Remove/Insert Pages)

1. **Select Feature**: Click "✂️ Edit PDF (Remove/Insert Pages)" on the home page
2. **Upload PDF**: Select the PDF file you want to edit
3. **View Pages**: All pages will be displayed as thumbnails
4. **Remove Pages**: 
   - Click the "- Remove" button on any page to mark it for removal
   - Click again to undo the removal
5. **Insert Pages**:
   - Click the "+ Insert After" button on any page
   - Upload one or more PDF files to insert at that position
   - You can insert at multiple positions
6. **Apply Changes**: Click "Apply Changes & Download"
7. **Download**: Download your edited PDF

### Getting Help

- Click the **"?" button** in the top-right corner of the home page
- Read the detailed instructions for each feature
- Learn tips and best practices

## 🔌 API Endpoints

### Merging Routes
- `GET /`: Home page with feature selection
- `POST /`: Process file count and redirect to upload page
- `POST /merge`: Handle PDF file uploads and merging
- `GET /download`: Download the merged PDF file
- `GET /restart`: Return to the home page for a new merge

### Editing Routes
- `GET /edit-mode`: Show PDF upload page for editing
- `POST /process-upload-for-edit`: Process uploaded PDF and create editing session
- `GET /page-image/<session_id>/<page_num>`: Generate and serve page preview images
- `POST /apply-edits`: Apply page removals and insertions
- `GET /download-edited/<session_id>`: Download the edited PDF file

## Deployment

### Vercel Deployment

The application is configured for Vercel deployment using the `vercel.json` configuration file:

```json
{
    "version": 2,
    "builds": [
      {
        "src": "api/app.py",
        "use": "@vercel/python"
      }
    ],
    "routes": [
      {
        "src": "/(.*)",
        "dest": "api/app.py"
      }
    ]
}
```

To deploy on Vercel:

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel
   ```

3. **Follow the prompts** to configure your deployment

## 🔧 Technical Details

### File Handling

- **Merging**: Uploaded files stored in `/tmp/uploads`, merged files in `/tmp/merged`
- **Editing**: Session-based storage in `/tmp/edit_sessions` with unique session IDs
- **Auto Cleanup**: All uploaded files are automatically deleted after processing
- **Unique Filenames**: UUID-based naming prevents conflicts when uploading duplicate files
- **Chunked Processing**: Large files processed in 8KB chunks for memory efficiency
- **Session Cleanup**: Edit sessions automatically cleaned up after download

### PDF Processing

- **Merging**: Uses PyPDF2's `PdfMerger` and `PdfWriter` for efficient combining
- **Page Extraction**: PyPDF2's `PdfReader` for page-level manipulation
- **Image Rendering**: PyMuPDF (fitz) renders PDF pages as JPEG thumbnails
- **Optimization**: 0.8x zoom and 60% JPEG quality for fast loading of large PDFs
- **Large File Handling**: Optimized processing for PDFs up to 100MB
- **Progressive Loading**: Adaptive delay based on PDF size (200-250ms per page)

### Security & Performance

- **File Validation**: Only PDF files accepted with size limits (100MB per file, 500MB total)
- **Size Checking**: Pre-upload validation prevents oversized files
- **Session Isolation**: Each editing session has a unique ID with sanitized filenames
- **Directory Traversal Protection**: All filenames sanitized using `secure_filename()`
- **No Persistent Storage**: Files deleted immediately after download
- **Progressive Loading**: Page images load sequentially to avoid server overload
- **Error Recovery**: Retry mechanism for failed page loads with user-friendly messages
- **Serverless Ready**: Optimized for Vercel's serverless functions with 500MB limit
- **Memory Management**: Chunked file reading/writing for large files

### Browser Features

- **Modern CSS**: Clean, professional design without gradients
- **Responsive Grid**: Adapts to any screen size
- **Smooth Animations**: Fade-in effects and hover transitions
- **Custom Scrollbars**: Styled scrollbars for better UX
- **Modal System**: Help popup with keyboard shortcuts (ESC to close)
- **Lazy Loading**: Progressive image loading for better performance

## ⚠️ Limitations

- **File Count**: Maximum 50 PDFs can be merged at once
- **File Size**: 100MB per individual file, 500MB total for merging
- **Processing Time**: Large PDFs may take longer to process in serverless environments
- **Page Previews**: Generated on-demand with progressive loading for better performance
- **No Password Support**: Cannot process password-protected PDFs
- **Temporary Storage**: Files are not permanently stored, download immediately
- **No Encryption**: Edited/merged PDFs are not encrypted
- **Serverless Timeout**: Very large operations may timeout on some hosting platforms

## 🛠️ Future Enhancements

Potential features for future development:
- Password-protected PDF support
- Page rotation functionality
- Page reordering (drag and drop)
- PDF compression options
- Watermark addition
- PDF to image conversion
- Batch processing
- Cloud storage integration

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Flask** - Web framework
- **PyPDF2** - PDF manipulation library
- **PyMuPDF** - Fast PDF rendering
- **Vercel** - Deployment platform

## 📧 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the built-in help (? button) on the website

---

**Live Demo**: [https://pdf-merger-eta-rust.vercel.app/](https://pdf-merger-eta-rust.vercel.app/)




