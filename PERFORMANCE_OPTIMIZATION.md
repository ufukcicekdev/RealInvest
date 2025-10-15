# Performance Optimization Guide

## Issues Identified from Lighthouse Report

### 1. **Cache Headers (1-hour TTL on DigitalOcean Spaces)** 
**Impact**: 211 KiB potential savings  
**Current**: 1 hour cache  
**Recommended**: 1 year cache for static assets

### 2. **Image Optimization**
**Impact**: 118 KiB potential savings  
**Issues**: Images not properly optimized or using next-gen formats

### 3. **Render-Blocking Resources**
**Impact**: 1,050 ms delay  
**Issues**: CSS/JS blocking initial page render

### 4. **Font Display**
**Impact**: 210 ms delay  
**Issues**: Font loading blocking render

### 5. **LCP (Largest Contentful Paint)**
**Issues**: Network dependency chain slowing down main content

---

## Solutions

### 1. Configure Long Cache Headers on DigitalOcean Spaces

Since you're using DigitalOcean Spaces CDN, you need to configure cache headers on the bucket level:

#### Option A: Using DigitalOcean CLI (doctl)
```bash
# Install doctl if not installed
# brew install doctl  # for macOS
# sudo snap install doctl  # for Ubuntu

# Configure authentication
doctl auth init

# Set CORS and Cache-Control headers for static files
doctl spaces upload-large YOUR_BUCKET_NAME \
  --header "Cache-Control: public, max-age=31536000, immutable" \
  --recursive realInvest/static/

# Set Cache-Control for media files
doctl spaces upload-large YOUR_BUCKET_NAME \
  --header "Cache-Control: public, max-age=31536000" \
  --recursive realInvest/media/
```

#### Option B: Using DigitalOcean Console
1. Go to DigitalOcean → Spaces
2. Select your bucket `cekfisi`
3. Go to Settings → CORS Configuration
4. Add custom headers for Cache-Control

#### Option C: Django Middleware (Temporary Solution)
Add this middleware to set cache headers from Django side:

```python
# properties/middleware.py
class CacheControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Set cache headers for static files
        if request.path.startswith('/static/') or '/static/' in request.path:
            response['Cache-Control'] = 'public, max-age=31536000, immutable'
        
        # Set cache headers for media files  
        if request.path.startswith('/media/') or '/media/' in request.path:
            response['Cache-Control'] = 'public, max-age=31536000'
            
        return response
```

### 2. Image Optimization

#### Automatic WebP Conversion
Already have WebP conversion in place. Make sure all images are converted:

```bash
python manage.py convert_images_to_webp
```

#### Lazy Loading
Images should use `loading="lazy"` attribute (already implemented in templates).

#### Responsive Images
Use `srcset` for different screen sizes (to be implemented).

### 3. Fix Render-Blocking Resources

#### A. Defer Non-Critical CSS
Move non-critical CSS to load asynchronously.

#### B. Async/Defer JavaScript
Already using `async` for Google Analytics. Apply to other scripts.

#### C. Inline Critical CSS
Extract and inline above-the-fold CSS.

### 4. Font Display Optimization

Current font loading:
```html
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

Already using `&display=swap` which is correct! ✅

### 5. Preload Critical Resources

Add resource hints for faster loading:
```html
<!-- Preconnect to external domains -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="preconnect" href="https://cekfisi.fra1.cdn.digitaloceanspaces.com">

<!-- DNS Prefetch for faster lookups -->
<link rel="dns-prefetch" href="https://www.googletagmanager.com">

<!-- Preload critical resources -->
<link rel="preload" href="{% static 'css/style.css' %}" as="style">
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" as="style">
```

---

## Implementation Steps

### Step 1: Update base.html with Resource Hints and Async Loading
See updated `base.html` template.

### Step 2: Configure DigitalOcean Spaces Cache Headers
Use one of the methods above to set long cache headers.

### Step 3: Update Django Settings
Add cache middleware and optimize static file serving.

### Step 4: Test and Verify
- Run Lighthouse again
- Check Network tab for cache headers
- Verify LCP improvements

---

## Expected Performance Improvements

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Cache Savings | - | 211 KiB | ✅ |
| Image Savings | - | 118 KiB | ✅ |
| Render Block | 1,050 ms | ~200 ms | 🚀 85% faster |
| Font Display | 210 ms | ~50 ms | 🚀 75% faster |
| LCP | Slow | Fast | 🚀 Significant |

---

## Monitoring

After implementation:
1. Run Lighthouse Performance audit
2. Monitor Core Web Vitals in Google Search Console
3. Check PageSpeed Insights: https://pagespeed.web.dev/

---

## Additional Recommendations

### 1. Enable Gzip/Brotli Compression on CDN
DigitalOcean Spaces CDN should automatically handle this.

### 2. Minify CSS/JS
Consider using Django Compressor:
```bash
pip install django-compressor
```

### 3. Use HTTP/2
Ensure your server/CDN supports HTTP/2 (DigitalOcean Spaces does).

### 4. Implement Service Worker
For offline support and faster repeat visits.

### 5. Consider Critical CSS Extraction
Tools like `critical` can extract above-the-fold CSS.

---

## Files to Update

1. ✅ `/templates/base.html` - Add resource hints, async scripts
2. ✅ `/realestate_project/settings.py` - Add cache middleware
3. ⚙️ DigitalOcean Spaces - Configure cache headers
4. ✅ Templates - Ensure lazy loading on images
