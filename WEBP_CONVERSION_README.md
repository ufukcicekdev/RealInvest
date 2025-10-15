# Automatic WebP Image Conversion

This Django project now includes automatic WebP image conversion for better performance.

## Features

✅ **Automatic Conversion**: All uploaded images are automatically converted to WebP format
✅ **Image Optimization**: Images are resized and optimized for web performance
✅ **Quality Control**: Different quality settings for different image types
✅ **Backward Compatible**: Existing images can be converted using a management command

## What Gets Converted

All images in these models are automatically converted to WebP:

- **Listings**: Main image and gallery images
- **Construction Projects**: Main image and gallery images
- **Banner Images**: Homepage banner carousel images
- **Custom Sections**: Main images and card images
- **References**: Reference gallery images
- **SEO Settings**: Open Graph (social media) images
- **Site Settings**: Logo and favicon

## Image Sizes and Quality

| Image Type | Max Size | Quality |
|------------|----------|---------|
| Listing Images | 1920x1080 | 85% |
| Construction Images | 1920x1080 | 85% |
| Banner Images | 1920x1080 | 90% (higher quality) |
| Custom Section Images | 1920x1080 | 85% |
| Card Images | 800x600 | 85% |
| Reference Images | 1920x1080 | 85% |
| OG Images (Social Media) | 1200x630 | 90% |
| Logo | 500x500 | 90% |
| Favicon | 256x256 | 90% |

## How It Works

### For New Images (Automatic)

When you upload a new image through the Django admin panel:

1. Image is uploaded
2. Automatically converted to WebP format
3. Resized if larger than maximum dimensions
4. Optimized for web performance
5. Saved with `.webp` extension

**No action required** - it happens automatically!

### For Existing Images (Manual Command)

To convert existing images that were uploaded before this feature was added:

```bash
# Dry run (see what would be converted without making changes)
python manage.py convert_images_to_webp --dry-run

# Actually convert all images
python manage.py convert_images_to_webp
```

## Benefits

- **Faster Page Load**: WebP images are 25-35% smaller than JPEG/PNG
- **Better SEO**: Faster loading improves search rankings
- **Less Bandwidth**: Reduces server bandwidth usage
- **Better UX**: Images load faster for users

## Technical Details

### Files Added

1. **properties/utils.py** - Image conversion utilities
2. **properties/signals.py** - Django signals for automatic conversion
3. **properties/management/commands/convert_images_to_webp.py** - Management command

### Configuration

The conversion happens in `properties/signals.py`. You can adjust quality settings there:

```python
# Example: Change banner image quality
instance.image = optimize_image(
    instance.image,
    max_width=1920,
    max_height=1080,
    quality=90  # Adjust this (1-100)
)
```

## Browser Support

WebP is supported by all modern browsers:
- Chrome ✅
- Firefox ✅
- Safari ✅ (iOS 14+, macOS Big Sur+)
- Edge ✅
- Opera ✅

## Notes

- Already WebP images will not be re-converted
- Original images are replaced with WebP versions
- RGBA/PNG transparency is handled by adding white background
- Images maintain aspect ratio when resized

## Troubleshooting

If images aren't converting:

1. Check that Pillow is installed: `pip install Pillow`
2. Verify signals are registered in `properties/apps.py`
3. Check Django logs for errors
4. Ensure file permissions allow writing to media directory

## Performance Impact

Expected improvements:
- **Image Size**: 25-35% smaller files
- **Page Load**: 20-40% faster
- **Bandwidth**: 30-40% reduction
- **Mobile Performance**: Significant improvement on slow connections
