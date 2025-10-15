"""
Utility functions for the properties app
"""
import os
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def convert_to_webp(image_field, quality=85):
    """
    Convert uploaded image to WebP format
    
    Args:
        image_field: Django ImageField instance
        quality: WebP quality (1-100, default 85)
    
    Returns:
        InMemoryUploadedFile: Converted WebP image
    """
    if not image_field:
        return None
    
    # Skip if already WebP
    if image_field.name.lower().endswith('.webp'):
        return image_field
    
    # Open the image
    img = Image.open(image_field)
    
    # Convert RGBA to RGB if necessary (WebP supports RGBA but some tools prefer RGB)
    if img.mode in ('RGBA', 'LA', 'P'):
        # Create a white background
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Create output buffer
    output = BytesIO()
    
    # Save as WebP
    img.save(output, format='WEBP', quality=quality, method=6)
    output.seek(0)
    
    # Generate new filename
    original_name = os.path.splitext(image_field.name)[0]
    new_name = f"{original_name}.webp"
    
    # Create InMemoryUploadedFile
    return InMemoryUploadedFile(
        output,
        'ImageField',
        new_name,
        'image/webp',
        sys.getsizeof(output),
        None
    )


def optimize_image(image_field, max_width=1920, max_height=1080, quality=85):
    """
    Optimize and resize image while converting to WebP
    
    Args:
        image_field: Django ImageField instance
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
        quality: WebP quality (1-100)
    
    Returns:
        InMemoryUploadedFile: Optimized WebP image
    """
    if not image_field:
        return None
    
    # Skip if already WebP
    if image_field.name.lower().endswith('.webp'):
        return image_field
    
    # Open the image
    img = Image.open(image_field)
    
    # Resize if larger than max dimensions
    if img.width > max_width or img.height > max_height:
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    
    # Convert RGBA to RGB if necessary
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Create output buffer
    output = BytesIO()
    
    # Save as WebP
    img.save(output, format='WEBP', quality=quality, method=6)
    output.seek(0)
    
    # Generate new filename
    original_name = os.path.splitext(os.path.basename(image_field.name))[0]
    new_name = f"{original_name}.webp"
    
    # Create InMemoryUploadedFile
    return InMemoryUploadedFile(
        output,
        'ImageField',
        new_name,
        'image/webp',
        sys.getsizeof(output),
        None
    )
