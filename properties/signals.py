"""
Django signals for automatic image optimization
"""
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import (
    Listing, ListingImage, Construction, ConstructionImage,
    BannerImage, CustomSection, ReferenceImage, SEOSettings, SiteSettings
)
from .utils import optimize_image


@receiver(pre_save, sender=Listing)
def optimize_listing_image(sender, instance, **kwargs):
    """Convert listing main image to WebP"""
    if instance.main_image and hasattr(instance.main_image, 'file'):
        if not instance.main_image.name.endswith('.webp'):
            instance.main_image = optimize_image(
                instance.main_image,
                max_width=1920,
                max_height=1080,
                quality=85
            )


@receiver(pre_save, sender=ListingImage)
def optimize_listing_gallery_image(sender, instance, **kwargs):
    """Convert listing gallery images to WebP"""
    if instance.image and hasattr(instance.image, 'file'):
        if not instance.image.name.endswith('.webp'):
            instance.image = optimize_image(
                instance.image,
                max_width=1920,
                max_height=1080,
                quality=85
            )


@receiver(pre_save, sender=Construction)
def optimize_construction_image(sender, instance, **kwargs):
    """Convert construction main image to WebP"""
    if instance.main_image and hasattr(instance.main_image, 'file'):
        if not instance.main_image.name.endswith('.webp'):
            instance.main_image = optimize_image(
                instance.main_image,
                max_width=1920,
                max_height=1080,
                quality=85
            )


@receiver(pre_save, sender=ConstructionImage)
def optimize_construction_gallery_image(sender, instance, **kwargs):
    """Convert construction gallery images to WebP"""
    if instance.image and hasattr(instance.image, 'file'):
        if not instance.image.name.endswith('.webp'):
            instance.image = optimize_image(
                instance.image,
                max_width=1920,
                max_height=1080,
                quality=85
            )


@receiver(pre_save, sender=BannerImage)
def optimize_banner_image(sender, instance, **kwargs):
    """Convert banner images to WebP"""
    if instance.image and hasattr(instance.image, 'file'):
        if not instance.image.name.endswith('.webp'):
            instance.image = optimize_image(
                instance.image,
                max_width=1920,
                max_height=1080,
                quality=90  # Higher quality for banner images
            )


@receiver(pre_save, sender=CustomSection)
def optimize_custom_section_images(sender, instance, **kwargs):
    """Convert custom section images to WebP"""
    # Main image
    if instance.main_image and hasattr(instance.main_image, 'file'):
        if not instance.main_image.name.endswith('.webp'):
            instance.main_image = optimize_image(
                instance.main_image,
                max_width=1920,
                max_height=1080,
                quality=85
            )
    
    # Card images
    for i in range(1, 4):
        card_image = getattr(instance, f'card_image_{i}', None)
        if card_image and hasattr(card_image, 'file'):
            if not card_image.name.endswith('.webp'):
                setattr(
                    instance,
                    f'card_image_{i}',
                    optimize_image(card_image, max_width=800, max_height=600, quality=85)
                )


@receiver(pre_save, sender=ReferenceImage)
def optimize_reference_image(sender, instance, **kwargs):
    """Convert reference images to WebP"""
    if instance.image and hasattr(instance.image, 'file'):
        if not instance.image.name.endswith('.webp'):
            instance.image = optimize_image(
                instance.image,
                max_width=1920,
                max_height=1080,
                quality=85
            )


@receiver(pre_save, sender=SEOSettings)
def optimize_seo_og_image(sender, instance, **kwargs):
    """Convert SEO Open Graph images to WebP"""
    if instance.og_image and hasattr(instance.og_image, 'file'):
        if not instance.og_image.name.endswith('.webp'):
            instance.og_image = optimize_image(
                instance.og_image,
                max_width=1200,
                max_height=630,  # Standard OG image size
                quality=90
            )


@receiver(pre_save, sender=SiteSettings)
def optimize_site_settings_images(sender, instance, **kwargs):
    """Convert site settings images (logo only) to WebP - Skip favicon (.ico files)"""
    # Logo
    if instance.logo and hasattr(instance.logo, 'file'):
        if not instance.logo.name.endswith('.webp'):
            instance.logo = optimize_image(
                instance.logo,
                max_width=500,
                max_height=500,
                quality=90
            )
    
    # Favicon - DO NOT convert .ico files to WebP
    # .ico files should remain in their original format for browser compatibility
    # No conversion needed for favicon
