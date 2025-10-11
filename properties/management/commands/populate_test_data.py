import os
import django
from django.core.management.base import BaseCommand
from django.utils import timezone
from properties.models import Listing, Construction, About
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Populate database with test data'

    def handle(self, *args, **options):
        # Clear existing data
        Listing.objects.all().delete()
        Construction.objects.all().delete()
        About.objects.all().delete()
        
        # Create About page data
        about = About.objects.create(
            title="Hakkımızda",
            subtitle="Profesyonel Emlak Hizmetleri",
            content="2005 yılından bu yana İstanbul ve çevre illerde gayrimenkul sektöründe hizmet veren şirketimiz, alanında uzman ekibiyle siz değerli müşterilerimize en kaliteli hizmeti sunmayı amaçlamaktadır. Bugüne kadar yüzlerce başarılı işlem gerçekleştiren ekibimiz, her geçen gün tecrübe ve bilgi birikimini artırarak hizmet kalitesini yükseltmektedir.",
            mission="Müşterilerimizin gayrimenkul ihtiyaçlarını en doğru ve hızlı şekilde karşılamak, şeffaf ve güvenilir hizmet anlayışıyla sektörde örnek bir kurum olmak.",
            vision="Gayrimenkul sektöründe yenilikçi ve müşteri odaklı hizmet anlayışıyla Türkiye'nin önde gelen emlak danışmanlığı şirketlerinden biri olmak.",
            phone="+90 212 123 45 67",
            email="info@emlak.com",
            address="Örnek Mahallesi, Emlak Cad. No:123, İstanbul",
            facebook_url="https://facebook.com/emlak",
            instagram_url="https://instagram.com/emlak",
            twitter_url="https://twitter.com/emlak",
            linkedin_url="https://linkedin.com/company/emlak"
        )
        self.stdout.write(self.style.SUCCESS('Successfully created About data'))
        
        # Create sample listings
        property_types = ['apartment', 'house', 'villa', 'land', 'commercial', 'office']
        locations = ['Beşiktaş, İstanbul', 'Şişli, İstanbul', 'Kadıköy, İstanbul', 'Üsküdar, İstanbul', 'Bakırköy, İstanbul']
        
        for i in range(20):
            is_featured = i < 6  # First 6 listings are featured
            listing = Listing.objects.create(
                title=f"Şık {random.choice(['Daire', 'Ev', 'Villa'])} - {i+1}",
                description=f"Harika konumda lüks {random.choice(['daire', 'ev', 'villa'])}. Modern iç tasarım, lüks malzemeler ve şık detaylarla donatılmıştır. Sessiz ve güvenli bir mahalleye sahiptir.",
                property_type=random.choice(property_types),
                status=random.choice(['sale', 'rent']),
                price=random.randint(500000, 5000000),
                location=random.choice(locations),
                address=f"Örnek Mahallesi {i+1}. Cadde No:{i+10}, İstanbul",
                bedrooms=random.randint(1, 5),
                bathrooms=random.randint(1, 3),
                area=random.randint(80, 300),
                floor=random.randint(1, 10),
                building_age=random.randint(0, 20),
                is_active=True,
                is_featured=is_featured
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully created 20 sample listings'))
        
        # Create sample construction projects
        statuses = ['planning', 'ongoing', 'completed']
        construction_locations = ['Ataşehir, İstanbul', 'Bağcılar, İstanbul', 'Avcılar, İstanbul']
        
        for i in range(10):
            start_date = date.today() - timedelta(days=random.randint(30, 365))
            end_date = start_date + timedelta(days=random.randint(180, 730)) if random.choice([True, False]) else None
            
            construction = Construction.objects.create(
                project_name=f"Lüks Konut Projesi - {i+1}",
                description=f"Şehir merkezinde yer alan bu lüks konut projesi, modern mimarisi ve çevreye duyarlı yaklaşımıyla dikkat çekmektedir. Proje içerisinde alışveriş merkezi, spor tesisleri ve çocuk oyun alanları da bulunmaktadır.",
                location=random.choice(construction_locations),
                status=random.choice(statuses),
                start_date=start_date,
                end_date=end_date
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully created 10 sample construction projects'))
        self.stdout.write(self.style.SUCCESS('All test data populated successfully!'))