# Cache Optimization Guide

## Overview
This guide explains how to optimize cache headers for your static assets (images, CSS, JS files) served from DigitalOcean Spaces to improve website performance and Google PageSpeed scores.

## Problem
Google PageSpeed Insights was reporting inefficient cache lifetimes (only 1 day) for static assets. Recommended cache time is **at least 1 year** for static files.

## What Was Changed

### 1. Updated Storage Configuration (`properties/storage.py`)
- Added `get_object_parameters()` method to set proper cache headers
- **Static assets** (images, CSS, JS, fonts): `Cache-Control: public, max-age=31536000, immutable` (1 year)
- **Other files**: `Cache-Control: public, max-age=86400` (1 day)
- Added proper `Content-Type` headers for different file types

### 2. Updated Settings (`realestate_project/settings.py`)
- Added `object_parameters` with cache control headers to both media and static file storage configurations
- Cache time: 1 year (31536000 seconds) with `immutable` flag

### 3. Updated Base Template (`templates/base.html`)
- Added both `rel="icon"` and `rel="shortcut icon"` for better browser compatibility
- Ensures favicon works across all browsers

## How to Apply Changes

### Option A: For New Files (Automatic)
All **new files uploaded** to DigitalOcean Spaces will automatically get the correct cache headers.

### Option B: For Existing Files (Manual Update Required)

#### Step 1: Test First (Dry Run)
```bash
python manage.py update_s3_cache_headers --dry-run
```

This will show you what would be updated without actually making changes.

#### Step 2: Update All Files
```bash
python manage.py update_s3_cache_headers
```

This will update cache headers for all existing static assets in your S3/Spaces bucket.

**Note**: This command only works in production mode (DEBUG=False).

## What Files Are Affected

The following file types will get **1-year cache** headers:

### Images
- `.webp`, `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.ico`

### Fonts
- `.woff`, `.woff2`, `.ttf`, `.eot`, `.otf`

### Code
- `.css`, `.js`

## Cache Headers Explained

### Static Assets (1 Year Cache)
```
Cache-Control: public, max-age=31536000, immutable
```

- `public`: Can be cached by browsers and CDNs
- `max-age=31536000`: Cache for 1 year (365 days)
- `immutable`: File won't change, no need to revalidate

### Dynamic Content (1 Day Cache)
```
Cache-Control: public, max-age=86400
```

- Cache for 24 hours
- Used for files that might change more frequently

## Performance Impact

### Before
- Cache TTL: 1 day (86400 seconds)
- Browsers re-download files frequently
- Slower page loads for returning visitors

### After
- Cache TTL: 1 year (31536000 seconds)
- Browsers cache files for a long time
- Much faster page loads for returning visitors
- Better Google PageSpeed Insights score

## Important Notes

### 1. File Versioning
Since files are now cached for 1 year, if you need to update a file (like CSS or JS):
- **Rename the file** or **add a version parameter** to force browsers to download the new version
- Example: `style-v2.css` or `style.css?v=2`

### 2. CDN Cache
DigitalOcean Spaces CDN also caches files. If you need to update a file immediately:
- Upload with a new filename, or
- Use the Spaces dashboard to invalidate the CDN cache

### 3. Favicon Issues
If favicon still doesn't appear after these changes:

1. **Re-upload the favicon** in Django admin (Site Settings)
   - Remove the current favicon
   - Save
   - Upload it again
   - Save again

2. **Clear browser cache**
   - Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
   - Try incognito/private mode
   - Clear all browser cache

3. **Check S3 file directly**
   - Open the favicon URL directly in browser
   - Check if it loads correctly

## Deployment Steps

### 1. Deploy Code Changes
```bash
git add .
git commit -m "Optimize cache headers for static assets"
git push
```

### 2. Update Existing Files (Production)
```bash
# SSH into your production server
python manage.py update_s3_cache_headers --dry-run  # Test first
python manage.py update_s3_cache_headers            # Actually update
```

### 3. Re-upload Favicon
- Go to Django Admin → Site Settings
- Remove and re-upload favicon
- Save

### 4. Verify
- Check Google PageSpeed Insights
- Verify cache headers in browser DevTools (Network tab)
- Check that favicon appears correctly

## Verification

### Check Cache Headers in Browser
1. Open DevTools (F12)
2. Go to Network tab
3. Reload page
4. Click on any image/CSS/JS file
5. Look for `Cache-Control` header in Response Headers

Should show: `public, max-age=31536000, immutable`

### Check with cURL
```bash
curl -I https://cekfisi.fra1.cdn.digitaloceanspaces.com/realInvest/media/site/favicon.ico
```

Look for: `Cache-Control: public, max-age=31536000, immutable`

## Troubleshooting

### Cache headers not updating
- Make sure you ran `update_s3_cache_headers` command
- Re-upload the file to apply new headers
- Check that DEBUG=False in production

### Favicon still not showing
- Re-upload favicon in admin panel
- Clear browser cache completely
- Check file permissions in Spaces (should be public-read)
- Verify Content-Type header is `image/x-icon`

### Google PageSpeed still showing warning
- Wait 24-48 hours for CDN cache to clear
- Run the update command on all files
- Re-test with Google PageSpeed Insights

## Expected Results

After implementing these changes:
- ✅ Google PageSpeed cache warning eliminated
- ✅ Faster page loads for returning visitors
- ✅ Reduced bandwidth usage
- ✅ Better SEO performance
- ✅ Favicon working correctly across all browsers
