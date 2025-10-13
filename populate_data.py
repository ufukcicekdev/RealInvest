#!/usr/bin/env python
"""
Script to populate the database with sample data for listings and constructions.
"""
import os
import sys
import django
from django.core.files.base import ContentFile
import random
from datetime import datetime, timedelta

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realestate_project.settings')
django.setup()

from properties.models import Listing, Construction
from django.utils import timezone

def create_sample_listings():
    """Create sample property listings"""
    property_types = ['apartment', 'house', 'villa', 'land', 'commercial', 'office']
    locations = [
        'İstanbul, Beşiktaş',
        'İstanbul, Kadıköy',
        'Ankara, Çankaya',
        'İzmir, Karşıyaka',
        'Antalya, Lara',
        'Bursa, Nilüfer'
    ]
    
    # Sample data for listings
    sample_listings = [
        {
            'title': 'Modern Lüks Daire',
            'description': 'Harika konumda lüks daire. 3+1, 150 m2, balkonlu, asansörlü. Emanet emlak ile sizlere sunduğumuz bu harika fırsatı kaçırmayın.',
            'property_type': 'apartment',
            'status': 'sale',
            'price': 2500000,
            'location': 'İstanbul, Beşiktaş',
            'address': 'Cumhuriyet Caddesi No:123, Beşiktaş/İstanbul',
            'bedrooms': 3,
            'bathrooms': 2,
            'area': 150.50,
            'floor': 5,
            'building_age': 2,
            'is_featured': True
        },
        {
            'title': 'Manzara Severler İçin Villa',
            'description': 'Deniz manzaralı özel villa. 5+2, 300 m2, özel havuzlu, bahçeli. Aile hayatınız için mükemmel bir yatırım.',
            'property_type': 'villa',
            'status': 'sale',
            'price': 4500000,
            'location': 'Antalya, Lara',
            'address': 'Lara Sahil Yolu No:45, Antalya',
            'bedrooms': 5,
            'bathrooms': 3,
            'area': 300.00,
            'floor': 2,
            'building_age': 1,
            'is_featured': True
        },
        {
            'title': 'Yatırım İçin Ofis',
            'description': 'Merkezi konumda kiralık ofis. 2+1, 120 m2, otoparklı. İş yeriniz için ideal konumda.',
            'property_type': 'office',
            'status': 'rent',
            'price': 15000,
            'location': 'Ankara, Çankaya',
            'address': 'Kavaklıdere Mahallesi, Çankaya/Ankara',
            'bedrooms': 2,
            'bathrooms': 1,
            'area': 120.00,
            'floor': 3,
            'building_age': 5,
            'is_featured': False
        },
        {
            'title': 'Şehir Merkezinde Daire',
            'description': 'Yeni yapılmış şehir merkezi daire. 2+1, 100 m2, doğalgazlı, klima tesisatlı. Modern yaşam alanları.',
            'property_type': 'apartment',
            'status': 'sale',
            'price': 1800000,
            'location': 'İzmir, Karşıyaka',
            'address': 'Nergiz Mahallesi, Karşıyaka/İzmir',
            'bedrooms': 2,
            'bathrooms': 1,
            'area': 100.00,
            'floor': 8,
            'building_age': 0,
            'is_featured': True
        },
        {
            'title': 'Ticari Amaçlı Arsa',
            'description': 'Yatırım için harika fırsat. 500 m2, imarlı, yol yakınında. Ticari amaçlı kullanım için ideal.',
            'property_type': 'land',
            'status': 'sale',
            'price': 3000000,
            'location': 'Bursa, Nilüfer',
            'address': 'Yıldırım Mahallesi, Nilüfer/Bursa',
            'bedrooms': 0,
            'bathrooms': 0,
            'area': 500.00,
            'floor': None,
            'building_age': None,
            'is_featured': False
        }
    ]
    
    print("Creating sample listings...")
    created_listings = []
    
    for listing_data in sample_listings:
        listing = Listing.objects.create(**listing_data)
        created_listings.append(listing)
        print(f"Created listing: {listing.title}")
    
    return created_listings

def create_sample_constructions():
    """Create sample construction projects"""
    statuses = ['planning', 'ongoing', 'completed']
    locations = [
        'İstanbul, Ataşehir',
        'Ankara, Yenimahalle',
        'İzmir, Bornova',
        'Antalya, Kepez',
        'Bursa, Osmangazi'
    ]
    
    # Sample data for constructions
    sample_constructions = [
        {
            'project_name': 'Lüks Konut Projesi',
            'description': 'Şehir merkezinde konumlanmış lüks konut projesi. 200 daire, sosyal tesisler, güvenlik sistemi ile donatılmış. Modern mimariye sahip bu proje tamamen depreme dayanıklı olarak inşa edilmektedir.',
            'location': 'İstanbul, Ataşehir',
            'status': 'ongoing',
            'start_date': timezone.now().date() - timedelta(days=365),
        },
        {
            'project_name': 'Alışveriş Merkezi',
            'description': 'Yeni nesil alışveriş merkezi projesi. 50.000 m2 kapalı alan, 200 mağaza, sinema salonları, eğlence alanları. Şehrin yeni merkezi olacak bu proje 2025 yılında tamamlanacak.',
            'location': 'Ankara, Yenimahalle',
            'status': 'ongoing',
            'start_date': timezone.now().date() - timedelta(days=500),
            'end_date': timezone.now().date() + timedelta(days=200),
        },
        {
            'project_name': 'İş Kulesi',
            'description': '50 katlı iş kulesi projesi. Ofis alanları, konferans salonları, restoranlar ve otopark ile donatılmış. Şehrin gökyüzünü süsleyecek bu modern yapı 2024 sonunda tamamlanacak.',
            'location': 'İzmir, Bornova',
            'status': 'completed',
            'start_date': timezone.now().date() - timedelta(days=1000),
            'end_date': timezone.now().date() - timedelta(days=50),
        },
        {
            'project_name': 'Resort Otel',
            'description': 'Deniz kenarında konumlanmış 5 yıldızlı resort otel projesi. 150 oda, spa merkezi, 5 farklı restoran, özel plaj. Tatilin tadını çıkarabileceğiniz bu lüks tesis 2026 yazında hizmete açılacak.',
            'location': 'Antalya, Kepez',
            'status': 'planning',
            'start_date': timezone.now().date() + timedelta(days=100),
        },
        {
            'project_name': 'Tasarım Ofis Binası',
            'description': 'Yaratıcı sektör çalışanları için tasarlanmış ofis binası. Açık alanlar, yeşil alanlar, kreatif çalışma alanları. Modern mimari ve sürdürülebilir malzemelerle inşa edilen bu proje 2025 başı itibariyle kullanıma açılacak.',
            'location': 'Bursa, Osmangazi',
            'status': 'ongoing',
            'start_date': timezone.now().date() - timedelta(days=200),
        }
    ]
    
    print("Creating sample construction projects...")
    created_constructions = []
    
    for construction_data in sample_constructions:
        construction = Construction.objects.create(**construction_data)
        created_constructions.append(construction)
        print(f"Created construction: {construction.project_name}")
    
    return created_constructions

def main():
    """Main function to populate database with sample data"""
    print("Starting to populate database with sample data...")
    
    # Create sample listings
    listings = create_sample_listings()
    
    # Create sample constructions
    constructions = create_sample_constructions()
    
    print(f"Successfully created {len(listings)} listings and {len(constructions)} construction projects.")
    print("Sample data population completed!")

if __name__ == '__main__':
    main()