import os
import django
from django.core.management.base import BaseCommand
from django.utils import timezone
from properties.models import Reference, ReferenceImage, ReferenceVideo
import random

class Command(BaseCommand):
    help = 'Populate database with sample reference data'

    def handle(self, *args, **options):
        # Clear existing reference data
        Reference.objects.all().delete()
        ReferenceImage.objects.all().delete()
        ReferenceVideo.objects.all().delete()
        
        # Sample reference data
        references_data = [
            {
                'title': 'Luxury Apartment Complex',
                'subtitle': 'Modern Living Experience',
                'description': 'A stunning luxury apartment complex with panoramic city views, featuring premium amenities including a fitness center, swimming pool, and 24/7 security. This project showcases our commitment to excellence in residential development.'
            },
            {
                'title': 'Commercial Office Tower',
                'subtitle': 'Business Hub',
                'description': 'A state-of-the-art commercial office tower designed for modern businesses. The building features energy-efficient systems, flexible office spaces, and convenient downtown location. Perfect for companies looking to establish a professional presence.'
            },
            {
                'title': 'Residential Villa Development',
                'subtitle': 'Exclusive Community',
                'description': 'An exclusive residential villa development offering privacy and luxury in a serene environment. Each villa is designed with spacious layouts, private gardens, and high-end finishes. The community includes club facilities and recreational areas.'
            }
        ]
        
        # Create reference entries
        for i, ref_data in enumerate(references_data):
            reference = Reference.objects.create(
                title=ref_data['title'],
                subtitle=ref_data['subtitle'],
                description=ref_data['description'],
                is_active=True,
                order=i
            )
            
            # Add sample images for each reference
            for j in range(random.randint(2, 4)):  # 2-4 images per reference
                ReferenceImage.objects.create(
                    reference=reference,
                    alt_text=f"{ref_data['title']} - Image {j+1}",
                    order=j
                )
            
            # Add sample videos for some references
            if i < 2:  # Add videos to first two references
                for k in range(random.randint(1, 2)):  # 1-2 videos per reference
                    ReferenceVideo.objects.create(
                        reference=reference,
                        title=f"{ref_data['title']} - Video {k+1}",
                        order=k
                    )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(references_data)} sample references with multiple images and videos'))
        self.stdout.write(self.style.SUCCESS('Reference data populated successfully!'))