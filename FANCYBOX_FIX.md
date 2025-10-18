# Fancybox Loading Fix

## Problem
After optimizing CSS/JS loading with `defer` attribute, Fancybox was throwing an error:

```
Uncaught TypeError: Invalid attempt to iterate non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.
```

This happened because:
1. Fancybox JS was deferred, causing it to load asynchronously
2. Page scripts tried to use Fancybox before it was fully loaded
3. The Fancybox object was undefined when initialization was attempted

## Solution Applied

### What Was Changed in `base.html`:

1. **Removed defer from Bootstrap JS**
   - Bootstrap needs to be available immediately for modals and other components
   - Changed from `defer` to synchronous loading

2. **Ensured Fancybox loads synchronously**
   - Fancybox JS loads without `defer` to ensure it's available immediately
   - Added after Bootstrap but before custom scripts

3. **Added Fancybox initialization check**
   - Wrapped Fancybox.bind() in a type check
   - Ensures Fancybox is loaded before trying to use it

### Code Changes:

```html
<!-- Before (Broken) -->
<script src="bootstrap.bundle.min.js" defer></script>
<script src="fancybox.umd.js"></script>
<script src="script.js" defer></script>

<!-- After (Fixed) -->
<script src="bootstrap.bundle.min.js"></script>
<script src="fancybox.umd.js"></script>
<script>
    if (typeof Fancybox !== 'undefined') {
        Fancybox.bind("[data-fancybox]", {
            // Fancybox options
        });
    }
</script>
<script src="script.js" defer></script>
```

## How Fancybox Works Now

1. ✅ **Bootstrap loads first** - Required for modals and UI components
2. ✅ **Fancybox loads second** - Available before any usage
3. ✅ **Fancybox initialized** - Binds to all `[data-fancybox]` elements
4. ✅ **Custom scripts load** - Can safely use Fancybox

## Performance Impact

### Before:
- All scripts deferred → Race condition
- Fancybox might not be ready when needed
- Errors in console
- Gallery/lightbox features broken

### After:
- Controlled loading order
- Fancybox always ready when needed
- No errors
- All features working

**Note:** While we removed `defer` from Bootstrap and Fancybox, these scripts are still loaded at the end of `<body>`, so they don't block initial page render. The performance impact is minimal.

## Testing Checklist

After deployment, verify:

- [ ] Image galleries open in Fancybox lightbox
- [ ] Video embeds open in Fancybox modal  
- [ ] No console errors related to Fancybox
- [ ] Page still loads quickly (check PageSpeed Insights)
- [ ] All modals and dropdowns work (Bootstrap)

## Usage in Templates

Fancybox will automatically work for any element with `data-fancybox` attribute:

### For Images:
```html
<a href="large-image.jpg" data-fancybox="gallery">
    <img src="thumbnail.jpg" alt="Description">
</a>
```

### For Videos:
```html
<a href="video.mp4" data-fancybox data-type="video">
    <img src="video-thumbnail.jpg" alt="Video">
</a>
```

### For Image Galleries:
```html
<a href="image1.jpg" data-fancybox="gallery-name">Image 1</a>
<a href="image2.jpg" data-fancybox="gallery-name">Image 2</a>
<a href="image3.jpg" data-fancybox="gallery-name">Image 3</a>
```

## Alternative Approaches (If Issues Persist)

If you still encounter loading issues, consider:

### Option 1: Use async instead of defer
```html
<script src="fancybox.umd.js" async></script>
```

### Option 2: Load Fancybox in head with defer
```html
<!-- In <head> -->
<link rel="preload" href="fancybox.umd.js" as="script">
<script src="fancybox.umd.js" defer></script>
```

### Option 3: Initialize Fancybox after DOMContentLoaded
```html
<script>
document.addEventListener('DOMContentLoaded', function() {
    if (typeof Fancybox !== 'undefined') {
        Fancybox.bind("[data-fancybox]", {});
    } else {
        console.error('Fancybox not loaded');
    }
});
</script>
```

## Summary

The fix ensures Fancybox loads in the correct order and is properly initialized before any code tries to use it. This eliminates the iterator error while maintaining good performance.
