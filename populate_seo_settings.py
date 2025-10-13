#!/usr/bin/env python
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realestate_project.settings')
django.setup()

from properties.models import SEOSettings
from django.db import IntegrityError

def populate_seo_settings():
    page_types = ['home', 'listings', 'construction', 'references', 'contact']
    created_count = 0
    
    for page_type in page_types:
        try:
            SEOSettings.objects.create(page_type=page_type)
            created_count += 1
            print(f"Created SEO settings for {page_type}")
        except IntegrityError:
            print(f"SEO settings for {page_type} already exist")
    
    print(f"Created {created_count} SEO settings objects")

if __name__ == "__main__":
    populate_seo_settings()