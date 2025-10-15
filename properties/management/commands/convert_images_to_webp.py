"""
Management command to convert existing images to WebP format
"""
from django.core.management.base import BaseCommand
from django.core.files import File
from properties.models import (
    Listing, ListingImage, Construction, ConstructionImage,
    BannerImage, CustomSection, ReferenceImage, SEOSettings, SiteSettings
)
from properties.utils import optimize_image
import os


class Command(BaseCommand):
    help = 'Convert all existing images to WebP format for better performance'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be converted without actually converting',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        total_converted = 0
        
        # Convert Listing images
        self.stdout.write('Converting Listing images...')
        total_converted += self.convert_model_images(
            Listing.objects.all(),
            ['main_image'],
            dry_run
        )
        
        # Convert ListingImage
        self.stdout.write('Converting Listing gallery images...')
        total_converted += self.convert_model_images(
            ListingImage.objects.all(),
            ['image'],
            dry_run
        )
        
        # Convert Construction images
        self.stdout.write('Converting Construction images...')
        total_converted += self.convert_model_images(
            Construction.objects.all(),
            ['main_image'],
            dry_run
        )
        
        # Convert ConstructionImage
        self.stdout.write('Converting Construction gallery images...')
        total_converted += self.convert_model_images(
            ConstructionImage.objects.all(),
            ['image'],
            dry_run
        )
        
        # Convert BannerImage
        self.stdout.write('Converting Banner images...')
        total_converted += self.convert_model_images(
            BannerImage.objects.all(),
            ['image'],
            dry_run,
            quality=90
        )
        
        # Convert CustomSection images
        self.stdout.write('Converting Custom Section images...')
        total_converted += self.convert_model_images(
            CustomSection.objects.all(),
            ['main_image', 'card_image_1', 'card_image_2', 'card_image_3'],
            dry_run
        )
        
        # Convert ReferenceImage
        self.stdout.write('Converting Reference images...')
        total_converted += self.convert_model_images(
            ReferenceImage.objects.all(),
            ['image'],
            dry_run
        )
        
        # Convert SEOSettings OG images
        self.stdout.write('Converting SEO Open Graph images...')
        total_converted += self.convert_model_images(
            SEOSettings.objects.all(),
            ['og_image'],
            dry_run,
            max_width=1200,
            max_height=630,
            quality=90
        )
        
        # Convert SiteSettings images
        self.stdout.write('Converting Site Settings images...')
        total_converted += self.convert_model_images(
            SiteSettings.objects.all(),
            ['logo', 'favicon'],
            dry_run,
            max_width=500,
            max_height=500,
            quality=90
        )
        
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'Would convert {total_converted} images to WebP format')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully converted {total_converted} images to WebP format')
            )

    def convert_model_images(self, queryset, image_fields, dry_run, max_width=1920, max_height=1080, quality=85):
        """Convert images for a given model queryset"""
        converted = 0
        
        for instance in queryset:
            for field_name in image_fields:
                image_field = getattr(instance, field_name, None)
                
                if not image_field:
                    continue
                
                # Skip if already WebP
                if image_field.name.endswith('.webp'):
                    continue
                
                try:
                    if dry_run:
                        self.stdout.write(f'  Would convert: {image_field.name}')
                        converted += 1
                    else:
                        # Convert to WebP
                        webp_image = optimize_image(
                            image_field,
                            max_width=max_width,
                            max_height=max_height,
                            quality=quality
                        )
                        
                        if webp_image:
                            # Save the converted image
                            setattr(instance, field_name, webp_image)
                            instance.save()
                            
                            self.stdout.write(
                                self.style.SUCCESS(f'  ✓ Converted: {image_field.name} -> {webp_image.name}')
                            )
                            converted += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Failed to convert {image_field.name}: {str(e)}')
                    )
        
        return converted
