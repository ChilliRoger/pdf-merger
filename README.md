# PDF Merger

A web application built with Flask that allows users to merge multiple PDF files into a single document. 
## Features

- **Multiple PDF Upload**: Upload and merge 2-50 PDF files at once
- **Responsive Design**: Modern, mobile-friendly interface with gradient backgrounds
- **File Management**: Automatic cleanup of uploaded files after processing
- **Download Support**: Direct download of merged PDF files


## Project Structure

```
pdf-merger/
├── api/
│   └── app.py              # Main Flask application
├── templates/
│   ├── index.html          # Home page with file count input
│   ├── upload.html         # File upload interface
│   └── result.html         # Success page with download options
├── uploads/                # Temporary upload directory
├── merged/                 # Output directory for merged files
├── requirements.txt        # Python dependencies
├── vercel.json            # Vercel deployment configuration
└── venv/                  # Virtual environment (not included in deployment)
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

## Usage

1. **Start the Process**: Enter the number of PDF files you want to merge (2-50)
2. **Upload Files**: Select PDF files for each slot in the upload interface
3. **Merge**: Click "Merge PDFs" to process the files
4. **Download**: Download the merged PDF file or start a new merge process

## API Endpoints

- `GET /`: Home page with file count input form
- `POST /`: Process file count and redirect to upload page
- `POST /merge`: Handle PDF file uploads and merging
- `GET /download`: Download the merged PDF file
- `GET /restart`: Return to the home page for a new merge

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

## Technical Details

### File Handling

- Uploaded files are temporarily stored in `/tmp/uploads` during processing
- Merged files are saved to `/tmp/merged` directory
- All uploaded files are automatically cleaned up after merging
- The application uses PyPDF2's `PdfMerger` class for efficient PDF merging

### Security Considerations

- File uploads are restricted to PDF files only (`accept="application/pdf"`)
- Temporary files are cleaned up immediately after processing
- No persistent storage of user files

### Browser Compatibility

The application uses modern CSS features including:
- CSS Grid for responsive layouts
- Flexbox for component alignment
- CSS gradients for visual appeal
- Media queries for mobile responsiveness

## Limitations

- Maximum file upload limit depends on server configuration
- Files are processed in the order they are uploaded
- No password protection or encryption features
- Temporary storage only (files not permanently stored)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.


