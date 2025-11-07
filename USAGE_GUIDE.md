# PDF Merger - Large File Handling Guide

## Quick Start Guide for Large Files

### 🚀 New Features

#### 1. Large File Support
- **Single File**: Up to 100MB per PDF
- **Total Upload**: Up to 500MB for merging multiple PDFs
- **Optimized Processing**: Chunked uploads and processing

#### 2. Real-Time Progress Tracking
- Visual progress bars during upload
- Status updates during processing
- Estimated completion feedback

#### 3. File Size Validation
- Automatic size checking before upload
- Warning messages for oversized files
- Clear error messages with guidance

---

## Merging Large PDFs

### Step-by-Step Process

1. **Select "Merge Multiple PDFs"**
   - Click on the merge button from home page
   - Enter the number of PDFs to merge (2-50)

2. **Upload Files**
   - Choose PDF files (max 100MB each)
   - See file size displayed in MB
   - Get warnings if file is too large
   - Files are automatically validated

3. **Track Progress**
   - Progress bar appears automatically
   - Shows upload percentage (0-100%)
   - Displays current stage (uploading/merging)
   - Completes with success message

4. **Download**
   - Automatic redirect to success page
   - Click "Download Merged PDF" button
   - File is automatically cleaned up after download

### Tips for Best Performance

✅ **Do:**
- Keep individual files under 50MB when possible
- Use modern browsers (Chrome, Firefox, Edge, Safari)
- Ensure stable internet connection for large uploads
- Wait for progress bar to complete

❌ **Don't:**
- Upload password-protected PDFs (not supported)
- Close browser during upload
- Upload more than 500MB total
- Refresh page during processing

---

## Editing Large PDFs

### Step-by-Step Process

1. **Select "Edit PDF"**
   - Click on edit button from home page
   - Upload a single PDF file (max 100MB)

2. **Upload & Process**
   - File size is checked automatically
   - Progress bar shows upload status
   - PDF pages are analyzed
   - Thumbnails are generated progressively

3. **Edit Operations**
   - **Remove Pages**: Click "-" button on unwanted pages
   - **Reorder Pages**: Drag and drop pages to new positions
   - **Insert Pages**: Click "+" to insert PDFs after any page
   - All changes are tracked in real-time

4. **Apply Changes**
   - Click "Apply Changes & Download"
   - Progress bar shows processing status
   - Edits are applied to PDF
   - Automatic redirect to success page

5. **Download**
   - Click "Download Edited PDF"
   - Session files are automatically cleaned up

### Tips for Large PDF Editing

✅ **Best Practices:**
- Pages load progressively (200-250ms delay)
- Larger PDFs take longer to load thumbnails
- Wait for all thumbnails to load before editing
- Use retry button if page fails to load

⚠️ **Performance Notes:**
- PDFs with 100+ pages may take 20-30 seconds to load
- Thumbnail quality is optimized for speed
- Drag-drop may be slower on very large PDFs
- Browser performance varies by device

---

## Technical Details

### File Size Validation

**Pre-Upload Checks:**
- File size calculated before upload
- Warning displayed if over 100MB
- Upload prevented for invalid files

**Server-Side Validation:**
- Double-check on server
- 500MB total limit enforced
- Detailed error messages returned

### Progress Indicators

**Upload Stage (10-70%):**
- File transfer to server
- Chunked upload in 8KB blocks
- Progress simulated for smooth UX

**Processing Stage (70-100%):**
- PDF analysis and processing
- Page extraction/merging
- File generation

### Optimizations Applied

**Backend:**
- Chunked file reading (8KB)
- Memory-efficient processing
- Progressive page rendering
- Automatic cleanup

**Frontend:**
- Async AJAX requests
- Non-blocking operations
- Smooth progress animations
- Error recovery

---

## Troubleshooting

### Common Issues

#### 1. "File too large" Error
**Problem:** PDF exceeds 100MB
**Solution:**
- Compress PDF using online tools
- Split PDF into smaller parts
- Try a different PDF

#### 2. "Upload Failed" Error
**Problem:** Network interruption or server timeout
**Solution:**
- Check internet connection
- Refresh page and try again
- Try with smaller file first
- Clear browser cache

#### 3. Slow Page Loading
**Problem:** Large PDF with many pages
**Solution:**
- Wait for all pages to load
- Don't close browser
- Pages load progressively
- Use retry button if needed

#### 4. Browser Freezing
**Problem:** Browser running out of memory
**Solution:**
- Close other tabs
- Try a different browser
- Restart browser
- Update browser to latest version

### Error Messages Explained

| Error Message | Meaning | Solution |
|--------------|---------|----------|
| "File size exceeds 100MB limit" | Individual file too large | Compress or split PDF |
| "No files uploaded" | No file selected | Choose a PDF file |
| "Session not found" | Session expired | Upload again |
| "Invalid page number" | Internal error | Retry operation |
| "Error generating image" | Thumbnail creation failed | Use retry button |

---

## Performance Benchmarks

### Expected Processing Times

**Merging:**
- 2-5 small PDFs (< 10MB): 2-5 seconds
- 5-10 medium PDFs (10-50MB): 5-15 seconds
- 10+ large PDFs (50-100MB): 15-30 seconds

**Editing:**
- Small PDF (< 20 pages): 5-10 seconds
- Medium PDF (20-100 pages): 10-30 seconds
- Large PDF (100+ pages): 30-60 seconds

*Times may vary based on:*
- Internet speed
- Server load
- Browser performance
- Device specifications

---

## Browser Compatibility

### Recommended Browsers

✅ **Fully Supported:**
- Google Chrome 90+
- Microsoft Edge 90+
- Mozilla Firefox 88+
- Safari 14+

⚠️ **Partial Support:**
- Older browser versions (may be slower)
- Mobile browsers (may have memory limits)

❌ **Not Supported:**
- Internet Explorer (all versions)
- Very old browsers without Fetch API

---

## Security & Privacy

### Data Handling

✅ **Secure Processing:**
- All files processed on server
- No data sent to third parties
- Automatic file deletion after download
- Session isolation per user

✅ **Privacy:**
- Files stored temporarily only
- No permanent storage
- No file content analysis
- No tracking or logging

### Best Practices

- Don't upload sensitive documents on public computers
- Download files immediately
- Clear browser cache after use
- Use HTTPS connection (ensure URL starts with https://)

---

## FAQ

**Q: Can I upload the same PDF multiple times?**
A: Yes! The merge feature allows duplicate files in different positions.

**Q: What happens to my files after download?**
A: They are automatically deleted from the server immediately.

**Q: Can I edit password-protected PDFs?**
A: No, password-protected PDFs are not currently supported.

**Q: Is there a limit on the number of pages?**
A: No specific page limit, but larger PDFs (100+ pages) may be slower.

**Q: Can I cancel an upload in progress?**
A: Yes, close the browser or refresh the page to cancel.

**Q: Will my edits be saved if I refresh the page?**
A: No, you'll need to start over. Complete all edits before closing.

**Q: Can I use this on mobile?**
A: Yes, but performance may vary. Desktop browsers recommended for large files.

**Q: Is there a daily usage limit?**
A: No usage limits currently implemented.

---

## Support

If you encounter issues:

1. **Check this guide** - Most issues covered above
2. **Refresh the page** - Try the operation again
3. **Try smaller files** - Test with a small PDF first
4. **Update browser** - Ensure you're using latest version
5. **Contact support** - Open an issue on GitHub

---

## Version History

### v2.0 - Large File Support
- Added 100MB per file support
- Implemented progress tracking
- Added file size validation
- Optimized processing
- Improved error handling

### v1.0 - Initial Release
- Basic merge functionality
- Basic edit functionality
- Up to 50MB files

---

**Live Demo**: [https://pdf-merger-eta-rust.vercel.app/](https://pdf-merger-eta-rust.vercel.app/)

**GitHub**: Report issues or contribute improvements
