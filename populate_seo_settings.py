#!/usr/bin/env python
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realestate_project.settings')
django.setup()

from properties.models import SEOSettings
from django.db import IntegrityError

def populate_seo_settings():
    seo_data = {
        'home': {
            'meta_title': 'Emlak ve Gayrimenkul Hizmetleri | Ana Sayfa',
            'meta_description': 'Profesyonel emlak danışmanlığı ile hayalinizdeki evi bulun. Satılık ve kiralık konut, işyeri, arsa. Güvenilir gayrimenkul hizmetleri.',
            'meta_keywords': 'emlak, gayrimenkul, satılık ev, kiralık daire, satılık arsa, emlak ofisi, gayrimenkul danışmanlığı',
            'og_title': 'Emlak ve Gayrimenkul Hizmetleri',
            'og_description': 'Profesyonel emlak danışmanlığı ile hayalinizdeki evi bulun. Satılık ve kiralık konut, işyeri ve arsa ilanlarını keşfedin.',
            'og_image_alt': 'Emlak ofisi logosu ve modern konut görseli',
            'og_type': 'website',
            'twitter_card': 'summary_large_image',
            'robots': 'index,follow'
        },
        'listings': {
            'meta_title': 'Satılık ve Kiralık İlanlar | Gayrimenkul İlanları',
            'meta_description': 'Binlerce satılık ve kiralık gayrimenkul ilanı. Konut, işyeri, arsa. Detaylı fotoğraflar ve bilgilerle hayalinizdeki mülkü bulun.',
            'meta_keywords': 'satılık ev, kiralık daire, satılık villa, kiralık işyeri, satılık arsa, emlak ilanları, gayrimenkul ilanları',
            'og_title': 'Satılık ve Kiralık Gayrimenkul İlanları',
            'og_description': 'Binlerce satılık ve kiralık gayrimenkul ilanını inceleyin. Konut, işyeri, arsa ve daha fazlası için detaylı bilgi.',
            'og_image_alt': 'Çeşitli gayrimenkul ilanları ve modern konutlar',
            'og_type': 'website',
            'twitter_card': 'summary_large_image',
            'robots': 'index,follow'
        },
        'construction': {
            'meta_title': 'Devam Eden İnşaat Projeleri | Yeni Konut Projeleri',
            'meta_description': 'Devam eden inşaat projelerimizi keşfedin. Modern mimari, kaliteli malzeme. Teslim öncesi satış avantajları ile rezervasyon yapın.',
            'meta_keywords': 'inşaat projeleri, yeni konut projeleri, satılık daireler, yeni binalar, inşaat firması, konut projesi',
            'og_title': 'Devam Eden İnşaat Projeleri',
            'og_description': 'Modern mimari ve kaliteli malzeme ile inşa edilen yeni konut projelerimizi keşfedin. Teslim öncesi satış avantajları.',
            'og_image_alt': 'Modern inşaat projesi ve şantiye görselleri',
            'og_type': 'website',
            'twitter_card': 'summary_large_image',
            'robots': 'index,follow'
        },
        'references': {
            'meta_title': 'Referanslarımız | Tamamlanan Projeler ve Müşteri Yorumları',
            'meta_description': 'Tamamlanan projelerimiz ve mutlu müşteri yorumları. Yılların deneyimi ve güvenilir hizmet anlayışımızla sizlere hizmet veriyoruz.',
            'meta_keywords': 'emlak referansları, müşteri yorumları, tamamlanan projeler, emlak deneyimi, güvenilir emlak',
            'og_title': 'Referanslarımız ve Tamamlanan Projeler',
            'og_description': 'Tamamlanan projelerimize ve mutlu müşterilerimizin yorumlarına göz atın. Yılların deneyimi ve güvenilir hizmet.',
            'og_image_alt': 'Tamamlanan projeler ve mutlu müşteri görselleri',
            'og_type': 'website',
            'twitter_card': 'summary_large_image',
            'robots': 'index,follow'
        },
        'contact': {
            'meta_title': 'İletişim | Bize Ulaşın',
            'meta_description': 'Gayrimenkul ihtiyaçlarınız için bizimle iletişime geçin. Profesyonel ekibimiz size yardımcı olmak için hazır. Telefon, e-posta veya ziyaret.',
            'meta_keywords': 'emlak iletişim, gayrimenkul iletişim, emlak ofisi telefon, emlak ofisi adres, emlak danışman',
            'og_title': 'İletişim - Bize Ulaşın',
            'og_description': 'Gayrimenkul ihtiyaçlarınız için bizimle iletişime geçin. Profesyonel ekibimiz size yardımcı olmak için hazır.',
            'og_image_alt': 'İletişim bilgileri ve ofis konumu',
            'og_type': 'website',
            'twitter_card': 'summary_large_image',
            'robots': 'index,follow'
        }
    }
    
    created_count = 0
    updated_count = 0
    
    for page_type, data in seo_data.items():
        seo_obj, created = SEOSettings.objects.get_or_create(page_type=page_type)
        
        if created:
            created_count += 1
            print(f"Created SEO settings for {page_type}")
        else:
            updated_count += 1
            print(f"Updating SEO settings for {page_type}")
        
        # Update all fields
        seo_obj.meta_title = data['meta_title']
        seo_obj.meta_description = data['meta_description']
        seo_obj.meta_keywords = data.get('meta_keywords', '')
        seo_obj.og_title = data['og_title']
        seo_obj.og_description = data['og_description']
        seo_obj.og_image_alt = data['og_image_alt']
        seo_obj.og_type = data.get('og_type', 'website')
        seo_obj.twitter_card = data.get('twitter_card', 'summary_large_image')
        seo_obj.robots = data.get('robots', 'index,follow')
        seo_obj.save()
        
        print(f"  ✓ Meta title: {data['meta_title']}")
        print(f"  ✓ Meta description: {data['meta_description'][:50]}...")
        print(f"  ✓ Meta keywords: {data.get('meta_keywords', 'N/A')[:50]}...")
        print(f"  ✓ OG title: {data['og_title']}")
        print(f"  ✓ OG description: {data['og_description'][:50]}...")
        print(f"  ✓ OG image alt: {data['og_image_alt']}")
        print(f"  ✓ OG type: {data.get('og_type', 'website')}")
        print(f"  ✓ Twitter card: {data.get('twitter_card', 'summary_large_image')}")
        print(f"  ✓ Robots: {data.get('robots', 'index,follow')}")
        print()
    
    print(f"\nSummary: Created {created_count} new, Updated {updated_count} existing SEO settings")

if __name__ == "__main__":
    populate_seo_settings()