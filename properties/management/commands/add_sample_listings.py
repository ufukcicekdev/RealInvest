from django.core.management.base import BaseCommand
from properties.models import Listing
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Örnek emlak ilanları ekler'

    def handle(self, *args, **kwargs):
        # Örnek ilan verileri
        sample_listings = [
            {
                'title': 'Kadıköy\'de Deniz Manzaralı 3+1 Lüks Daire',
                'description': '''Kadıköy\'ün en prestijli lokasyonunda, deniz manzaralı, yeni yapılmış lüks daire. 
                
Özellikler:
- Tam deniz manzarası
- Amerikan mutfak
- Geniş balkon
- Doğal gaz kombi
- Merkezi sistem klima
- Beyaz eşya dahil
- Güvenlikli site
- Yüzme havuzu
- Fitness merkezi
- 7/24 güvenlik
                
Ulaşım:
- Metrobüs: 5 dakika
- Vapur iskelesi: 3 dakika
- AVM: 2 dakika yürüme mesafesinde
                
Bu eşsiz fırsatı kaçırmayın!''',
                'property_type': 'apartment',
                'status': 'sale',
                'price': Decimal('4500000.00'),
                'location': 'Kadıköy, İstanbul',
                'address': 'Caferağa Mahallesi, Deniz Sokak No:15',
                'bedrooms': 3,
                'bathrooms': 2,
                'area': Decimal('145.00'),
                'floor': 8,
                'building_age': 2,
                'is_featured': True,
            },
            {
                'title': 'Beşiktaş\'ta Boğaz Manzaralı 4+2 Dublex Villa',
                'description': '''Beşiktaş\'ın merkezinde, muhteşem Boğaz manzaralı dublex villa.
                
Özellikler:
- 2 katlı dublex
- Özel bahçe (200m²)
- Kapalı otopark (3 araç)
- Jakuzi
- Sauna
- Akıllı ev sistemi
- Alarm sistemi
- Yerden ısıtma
- Gömme dolap
                
Sosyal Tesisler:
- Çocuk oyun parkı
- Basketbol sahası
- Kapalı havuz
- Açık havuz
                
Konumu ile hayallerinizdeki yaşamı sunuyor!''',
                'property_type': 'villa',
                'status': 'sale',
                'price': Decimal('18500000.00'),
                'location': 'Beşiktaş, İstanbul',
                'address': 'Akaretler Mahallesi, Boğaz Caddesi No:42',
                'bedrooms': 4,
                'bathrooms': 3,
                'area': Decimal('320.00'),
                'floor': None,
                'building_age': 1,
                'is_featured': True,
            },
            {
                'title': 'Şişli Mecidiyeköy\'de Yeni Yapı 2+1 Kiralık Daire',
                'description': '''Mecidiyeköy\'ün göbeğinde, sıfır binada, modern tasarımlı kiralık daire.
                
Özellikler:
- Yeni yapı (sıfır)
- Geniş balkon
- Laminat parke
- Spot aydınlatma
- Ankastre mutfak
- Kombi doğal gaz
- Asansör
                
Konum Avantajları:
- Metro: 2 dakika
- Metrobüs: 5 dakika
- Ofis merkezlerine yakın
- AVM: 1 dakika
- Market, okul, hastane çok yakın
                
İş merkezine yakın, huzurlu yaşam!''',
                'property_type': 'apartment',
                'status': 'rent',
                'price': Decimal('25000.00'),
                'location': 'Şişli, İstanbul',
                'address': 'Mecidiyeköy Mahallesi, Şehit Ahmet Sokak No:8',
                'bedrooms': 2,
                'bathrooms': 1,
                'area': Decimal('95.00'),
                'floor': 5,
                'building_age': 0,
                'is_featured': True,
            },
            {
                'title': 'Bağdat Caddesi\'nde Satılık 180m² Dükkan',
                'description': '''Bağdat Caddesi\'nin en işlek noktasında, köşe başı satılık dükkan.
                
Özellikler:
- Köşe başı
- Geniş vitrin
- 2 katlı
- WC
- Mutfak
- Depo
- Klima
                
İş Potansiyeli:
- Günlük yüksek yaya trafiği
- Her türlü ticari faaliyete uygun
- Marka değeri yüksek lokasyon
- Metro ve otobüs hatlarına yakın
                
Yatırımın doğru adresi!''',
                'property_type': 'commercial',
                'status': 'sale',
                'price': Decimal('12000000.00'),
                'location': 'Kadıköy, İstanbul',
                'address': 'Bağdat Caddesi No:234',
                'bedrooms': 0,
                'bathrooms': 1,
                'area': Decimal('180.00'),
                'floor': 1,
                'building_age': 15,
                'is_featured': False,
            },
            {
                'title': 'Maslak\'ta A+ Plaza\'da Kiralık Ofis',
                'description': '''Maslak\'ın prestijli plazasında, modern ofis katı.
                
Özellikler:
- Açık ofis konsepti
- VRV klima sistemi
- Yerden ısıtma
- Ankastre mutfak
- Duş
- Jeneratör
- 7/24 güvenlik
- Resepsiyon
                
Plaza Olanakları:
- Restaurant
- Kafeterya
- Fitness
- Toplantı salonları
- Otopark (50+ araç)
                
Prestijli adresiniz için doğru seçim!''',
                'property_type': 'office',
                'status': 'rent',
                'price': Decimal('85000.00'),
                'location': 'Maslak, İstanbul',
                'address': 'Maslak Mahallesi, Büyükdere Caddesi No:123',
                'bedrooms': 0,
                'bathrooms': 2,
                'area': Decimal('450.00'),
                'floor': 12,
                'building_age': 5,
                'is_featured': False,
            },
            {
                'title': 'Silivri\'de Denize Sıfır 5000m² İmarlı Arsa',
                'description': '''Silivri\'de denize sıfır konumda, imar onaylı satılık arsa.
                
Özellikler:
- Denize sıfır
- İmar onaylı
- Elektrik var
- Su var
- Yol var
- Tapu temiz
                
İmar Durumu:
- Villa yapılabilir
- Otel yapılabilir
- Turizm tesisi uygun
- TAKS: 0.30
- KAKS: 0.60
                
Doğa ile iç içe yatırım fırsatı!''',
                'property_type': 'land',
                'status': 'sale',
                'price': Decimal('7500000.00'),
                'location': 'Silivri, İstanbul',
                'address': 'Kavaklı Mahallesi, Sahil Yolu',
                'bedrooms': 0,
                'bathrooms': 0,
                'area': Decimal('5000.00'),
                'floor': None,
                'building_age': None,
                'is_featured': True,
            },
            {
                'title': 'Ataşehir\'de Havuzlu Sitede 2+1 Kiralık',
                'description': '''Ataşehir\'de lüks sitede, havuz manzaralı kiralık daire.
                
Özellikler:
- Havuz manzarası
- Geniş balkon
- Laminat zemin
- Klima
- Ankastre mutfak
- Beyaz eşya
                
Site Olanakları:
- Açık yüzme havuzu
- Kapalı yüzme havuzu
- Fitness
- Sauna
- Çocuk parkı
- Güvenlik
- Otopark
                
Aileniz için güvenli, konforlu yaşam!''',
                'property_type': 'apartment',
                'status': 'rent',
                'price': Decimal('22000.00'),
                'location': 'Ataşehir, İstanbul',
                'address': 'Barbaros Mahallesi, Çamlık Sokak No:7',
                'bedrooms': 2,
                'bathrooms': 1,
                'area': Decimal('105.00'),
                'floor': 4,
                'building_age': 8,
                'is_featured': False,
            },
            {
                'title': 'Etiler\'de Müstakil Bahçeli Villa',
                'description': '''Etiler\'in sakin sokağında, özel bahçeli müstakil villa.
                
Özellikler:
- Müstakil
- Bahçe (400m²)
- Özel havuz
- Barbekü alanı
- 4 araçlık garaj
- Akıllı ev sistemi
- Güvenlik kamerası
- Jeneratör
                
İç Mekan:
- Geniş salon
- Amerikan mutfak
- Çalışma odası
- Giyinme odası
- 2 balkon
- Teras
                
Şehrin kalbinde doğa ile iç içe yaşam!''',
                'property_type': 'villa',
                'status': 'sale',
                'price': Decimal('35000000.00'),
                'location': 'Etiler, İstanbul',
                'address': 'Etiler Mahallesi, Bebek Yolu Sokak No:12',
                'bedrooms': 5,
                'bathrooms': 4,
                'area': Decimal('450.00'),
                'floor': None,
                'building_age': 10,
                'is_featured': True,
            },
        ]

        created_count = 0
        for listing_data in sample_listings:
            # Slug kontrolü - aynı başlıkta ilan varsa atlıyoruz
            slug = listing_data['title'][:50]  # İlk 50 karakter
            if not Listing.objects.filter(title=listing_data['title']).exists():
                listing = Listing.objects.create(**listing_data)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ İlan oluşturuldu: {listing.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ İlan zaten mevcut: {listing_data["title"]}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n{created_count} yeni ilan başarıyla eklendi!')
        )
