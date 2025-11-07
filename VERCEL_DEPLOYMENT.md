# Vercel Deployment Guide - Large File Handling

## 🚨 **IMPORTANT: Vercel Limitations**

Your code is now optimized for Vercel, but you must understand these critical limitations:

### **Vercel Plan Limits**

| Feature | Hobby (Free) | Pro ($20/month) |
|---------|--------------|-----------------|
| **Request Body Size** | 4.5MB | 100MB |
| **Function Timeout** | 10 seconds | 60 seconds |
| **Memory** | 1024MB | 3008MB |
| **Bandwidth** | 100GB/month | 1TB/month |

### **Current Configuration**

Your app is now configured with:
- **50MB per file limit** (safe for Pro plan)
- **100MB total limit** 
- **60 second timeout**
- **3008MB memory** (requires Pro plan)

---

## 📋 **Deployment Checklist**

### **Before Deploying:**

✅ **1. Check Your Vercel Plan**
```bash
vercel whoami
```
If you're on Hobby plan, you'll be limited to 4.5MB files!

✅ **2. Files Ready**
- `vercel.json` - Updated with function config
- `requirements.txt` - All dependencies listed
- `api/app.py` - Optimized for Vercel
- All templates updated

✅ **3. Test Locally First**
```bash
python api/app.py
```
Visit http://localhost:5000 and test with files under 50MB

---

## 🚀 **Deployment Steps**

### **Option 1: Using Vercel CLI**

1. **Install Vercel CLI** (if not installed)
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   cd e:\pdf-merger
   vercel --prod
   ```

4. **Follow prompts:**
   - Link to existing project: Yes (your pdfs-merger project)
   - Deploy: Yes

### **Option 2: Git Push (Recommended)**

1. **Commit all changes**
   ```bash
   git add .
   git commit -m "Add large file handling support"
   git push origin main
   ```

2. **Vercel auto-deploys** from your GitHub repository

---

## ⚙️ **Vercel Configuration Explained**

### **vercel.json**

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/app.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"  // Allows larger function packages
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/app.py"
    }
  ],
  "functions": {
    "api/app.py": {
      "memory": 3008,      // Maximum memory (Pro plan)
      "maxDuration": 60    // Maximum timeout (Pro plan)
    }
  }
}
```

### **What This Does:**

- **maxLambdaSize**: Increases deployment package size limit
- **memory**: 3008MB (requires Pro plan, default is 1024MB)
- **maxDuration**: 60 seconds (requires Pro plan, default is 10s)

---

## 🔧 **File Size Limits**

### **Current Settings:**

```python
# api/app.py
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB total
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB per file
```

### **Adjusting Limits:**

#### **For Hobby Plan (4.5MB limit):**

In `api/app.py`, change:
```python
app.config['MAX_CONTENT_LENGTH'] = 4.5 * 1024 * 1024  # 4.5MB
MAX_FILE_SIZE = 4 * 1024 * 1024  # 4MB per file
```

In templates (`upload.html` and `upload_for_edit.html`):
```javascript
const maxSize = 4 * 1024 * 1024; // 4MB
infoDiv.textContent = `⚠️ File too large! Max 4MB (${sizeMB} MB)`;
```

#### **For Pro Plan (100MB limit):**

Current settings are optimal! No changes needed.

---

## 🧪 **Testing on Vercel**

### **After Deployment:**

1. **Visit your site**: https://pdfs-merger.vercel.app/

2. **Test with small files first** (< 5MB)
   - Merge 2-3 small PDFs
   - Edit a small PDF
   - Check if downloads work

3. **Test with larger files** (10-40MB)
   - Upload progressively larger files
   - Monitor for timeouts
   - Check Vercel logs for errors

4. **Check Vercel Logs**
   ```bash
   vercel logs pdfs-merger
   ```
   Or visit: https://vercel.com/dashboard → Your Project → Logs

### **Expected Behavior:**

✅ **What Should Work:**
- Files up to 50MB (on Pro plan)
- PDFs with 100+ pages
- Multiple file uploads (total < 100MB)
- Progress indicators
- File size validation

❌ **What Will Fail:**
- Files > 50MB (will get rejected)
- Very complex PDFs taking > 60s to process
- Concurrent large file uploads (memory limits)

---

## 🐛 **Common Issues & Solutions**

### **1. "413 Payload Too Large"**

**Problem:** File exceeds Vercel's request size limit

**Solutions:**
- **On Hobby Plan**: Use files < 4.5MB
- **On Pro Plan**: Files should be < 50MB
- Check if you're really on Pro plan: https://vercel.com/account/billing

### **2. "Function Execution Timed Out"**

**Problem:** Operation took > 60 seconds

**Solutions:**
- Reduce file sizes
- Simplify operations (fewer pages to merge)
- Optimize PDF processing:
  ```python
  # In api/app.py, reduce image quality further
  pix = page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5), alpha=False)
  img_data = pix.tobytes("jpeg", jpg_quality=50)
  ```

### **3. "Out of Memory"**

**Problem:** Function exceeded memory limit

**Solutions:**
- Ensure you're on Pro plan (3008MB memory)
- Process files sequentially, not in parallel
- Add memory cleanup:
  ```python
  import gc
  gc.collect()  # After processing each file
  ```

### **4. "Module Not Found"**

**Problem:** Dependencies not installed

**Solutions:**
- Verify `requirements.txt` is correct:
  ```
  flask
  PyPDF2
  PyMuPDF
  Pillow
  ```
- Check Vercel build logs
- Clear deployment cache and redeploy

### **5. "File Not Found" on Download**

**Problem:** `/tmp` storage cleared between function invocations

**Solutions:**
- This shouldn't happen with current code
- Session files are created and used in same invocation
- If it happens, files may be too large for `/tmp` (512MB limit)

---

## 📊 **Monitoring Performance**

### **Vercel Analytics**

1. Go to https://vercel.com/dashboard
2. Select your project
3. Click "Analytics" tab
4. Monitor:
   - Function Duration (should be < 60s)
   - Memory Usage (should be < 3008MB)
   - Status Codes (watch for 413, 504 errors)

### **Key Metrics to Watch:**

- **Average Duration**: < 30 seconds is good
- **Error Rate**: < 1% is acceptable
- **Memory Usage**: < 80% of limit (2400MB/3008MB)

---

## 💰 **Cost Considerations**

### **Pro Plan Pricing:**

- **$20/month** base cost
- **$40/month** for team features
- Additional costs for:
  - Bandwidth over 1TB/month
  - Function invocations over 1M/month

### **Optimizing Costs:**

1. **Cache static assets** (already done)
2. **Compress PDFs** before processing
3. **Limit concurrent users** during peak times
4. **Monitor bandwidth usage** in Vercel dashboard

### **Free Alternatives:**

If Pro plan is too expensive, consider:

1. **Railway.app** - More generous free tier
2. **Render.com** - 750 hours free/month
3. **Heroku** - Free tier with 550 hours/month
4. **Self-hosting** - DigitalOcean, AWS, etc.

---

## 🔄 **Updating the Deployment**

### **Method 1: Git Push (Automatic)**

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Vercel auto-deploys in ~2 minutes
```

### **Method 2: Vercel CLI (Manual)**

```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

### **Rollback if Needed:**

```bash
# List deployments
vercel ls

# Promote a previous deployment
vercel promote <deployment-url>
```

---

## ✅ **Pre-Deployment Checklist**

Before pushing to production:

- [ ] Tested locally with various file sizes
- [ ] Verified all file size limits are correct
- [ ] Checked vercel.json configuration
- [ ] Confirmed Pro plan is active (if using > 4.5MB)
- [ ] Updated README with correct limits
- [ ] Tested merge and edit features
- [ ] Verified progress bars work
- [ ] Checked error messages are user-friendly
- [ ] Reviewed Vercel logs for any warnings
- [ ] Tested on mobile devices

---

## 🎯 **Recommended Settings**

### **For Production (Pro Plan):**

```python
# api/app.py
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB per file
```

```json
// vercel.json
"functions": {
  "api/app.py": {
    "memory": 3008,
    "maxDuration": 60
  }
}
```

### **For Hobby Plan:**

```python
# api/app.py
app.config['MAX_CONTENT_LENGTH'] = 4.5 * 1024 * 1024  # 4.5MB
MAX_FILE_SIZE = 4 * 1024 * 1024  # 4MB per file
```

```json
// vercel.json
"functions": {
  "api/app.py": {
    "memory": 1024,
    "maxDuration": 10
  }
}
```

---

## 📱 **Support & Troubleshooting**

### **Check Deployment Status:**
```bash
vercel inspect <deployment-url>
```

### **View Real-Time Logs:**
```bash
vercel logs --follow
```

### **Vercel Support:**
- Documentation: https://vercel.com/docs
- Community: https://github.com/vercel/vercel/discussions
- Email: support@vercel.com (Pro plan only)

---

## 🎉 **Success Criteria**

Your deployment is successful when:

✅ Website loads without errors
✅ Merge feature works with 2+ PDFs (< 50MB each)
✅ Edit feature works with PDFs (< 50MB)
✅ Progress bars display correctly
✅ Downloads work properly
✅ File size validation works
✅ No 413 or 504 errors in logs
✅ Response times < 60 seconds

---

## 📝 **Quick Deploy Command**

```bash
cd e:\pdf-merger
git add .
git commit -m "Add large file handling - optimized for Vercel Pro"
git push origin main
# Wait 2-3 minutes for auto-deployment
# Visit https://pdfs-merger.vercel.app/
```

---

**Your site:** https://pdfs-merger.vercel.app/

**Remember:** You're currently configured for **Vercel Pro plan** (50MB files). If you're on Hobby plan, reduce limits to 4MB!
