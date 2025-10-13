from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Listing(models.Model):
    """
    Real estate property listing model
    """
    PROPERTY_TYPES = (
        ('apartment', 'Daire'),
        ('house', 'Ev'),
        ('villa', 'Villa'),
        ('land', 'Arsa'),
        ('commercial', 'Ticari'),
        ('office', 'Ofis'),
    )
    
    STATUS_CHOICES = (
        ('sale', 'Satılık'),
        ('rent', 'Kiralık'),
    )
    
    title = models.CharField(max_length=255, verbose_name="Başlık", help_text="SEO için optimize edilmiş emlak başlığı")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="URL Yolu")
    description = models.TextField(verbose_name="Açıklama", help_text="Detaylı emlak açıklaması")
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES, default='apartment', verbose_name="Emlak Tipi")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sale', verbose_name="Durum")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Fiyat", help_text="Türk Lirası cinsinden fiyat")
    location = models.CharField(max_length=255, verbose_name="Konum", help_text="Emlak konumu (şehir, ilçe)")
    address = models.CharField(max_length=500, blank=True, null=True, verbose_name="Adres")
    
    # Property details
    bedrooms = models.IntegerField(default=0, verbose_name="Yatak Odası Sayısı", help_text="Yatak odası adedi")
    bathrooms = models.IntegerField(default=0, verbose_name="Banyo Sayısı", help_text="Banyo adedi")
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Alan (m²)", help_text="Metrekare cinsinden alan")
    floor = models.IntegerField(blank=True, null=True, verbose_name="Kat", help_text="Kat numarası")
    building_age = models.IntegerField(blank=True, null=True, verbose_name="Bina Yaşı", help_text="Bina yaşı (yıl)")
    
    # Media
    main_image = models.ImageField(upload_to='listings/', verbose_name="Ana Resim", help_text="Ana emlak resmi")
    image_alt_text = models.CharField(max_length=255, blank=True, verbose_name="Resim Alt Yazısı", help_text="Ana resim için SEO alt yazısı")
    
    # Meta information
    is_active = models.BooleanField(default=True, verbose_name="Aktif", help_text="Web sitesinde göster")
    is_featured = models.BooleanField(default=False, verbose_name="Öne Çıkan", help_text="Ana sayfada göster")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Oluşturma Tarihi")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    # SEO fields
    meta_title = models.CharField(max_length=60, blank=True, verbose_name="Meta Başlık", help_text="SEO meta başlığı")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="Meta Açıklama", help_text="SEO meta açıklaması")
    
    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Emlak İlanı'
        verbose_name_plural = 'Emlak İlanları'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.image_alt_text:
            self.image_alt_text = f"{self.title} - {self.location}"
        if not self.meta_title:
            self.meta_title = self.title[:60]
        if not self.meta_description:
            self.meta_description = self.description[:160]
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('listing_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title


class ListingImage(models.Model):
    """
    Emlak ilanları için ek resimler
    """
    listing = models.ForeignKey(Listing, related_name='images', on_delete=models.CASCADE, verbose_name="İlan")
    image = models.ImageField(upload_to='listings/gallery/', verbose_name="Resim")
    alt_text = models.CharField(max_length=255, blank=True, verbose_name="Alt Yazı")
    order = models.IntegerField(default=0, verbose_name="Sıra")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Yüklenme Tarihi")
    
    class Meta:
        ordering = ['order']
        verbose_name = 'İlan Resmi'
        verbose_name_plural = 'İlan Resimleri'
    
    def __str__(self):
        return f"{self.listing.title} resmi"


class Construction(models.Model):
    """
    Devam eden veya tamamlanmış inşaat projeleri modeli
    """
    STATUS_CHOICES = (
        ('planning', 'Planlamada'),
        ('ongoing', 'Devam Ediyor'),
        ('completed', 'Tamamlandı'),
    )
    
    project_name = models.CharField(max_length=255, verbose_name="Proje Adı", help_text="İnşaat proje adı")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="URL Yolu")
    description = models.TextField(verbose_name="Proje Açıklaması", help_text="Proje açıklaması")
    location = models.CharField(max_length=255, verbose_name="Konum", help_text="Proje konumu")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing', verbose_name="Durum")
    
    start_date = models.DateField(verbose_name="Başlangıç Tarihi")
    end_date = models.DateField(blank=True, null=True, verbose_name="Bitiş Tarihi")
    
    # Media
    main_image = models.ImageField(upload_to='construction/', verbose_name="Ana Resim", help_text="Ana proje resmi")
    image_alt_text = models.CharField(max_length=255, blank=True, verbose_name="Resim Alt Yazısı")
    
    # Meta
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Oluşturma Tarihi")
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True, verbose_name="Meta Başlık")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="Meta Açıklama")
    
    class Meta:
        ordering = ['-created_date']
        verbose_name = 'İnşaat Projesi'
        verbose_name_plural = 'İnşaat Projeleri'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.project_name)
        if not self.image_alt_text:
            self.image_alt_text = f"{self.project_name} - {self.location}"
        if not self.meta_title:
            self.meta_title = self.project_name[:60]
        if not self.meta_description:
            self.meta_description = self.description[:160]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.project_name


class ConstructionImage(models.Model):
    """
    İnşaat projeleri için çoklu resimler
    """
    construction = models.ForeignKey(Construction, related_name='images', on_delete=models.CASCADE, verbose_name="İnşaat Projesi")
    image = models.ImageField(upload_to='construction/gallery/', verbose_name="Resim")
    alt_text = models.CharField(max_length=255, blank=True, verbose_name="Alt Yazı")
    caption = models.CharField(max_length=255, blank=True, verbose_name="Başlık")
    order = models.IntegerField(default=0, verbose_name="Sıra")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Yüklenme Tarihi")
    
    class Meta:
        ordering = ['order']
        verbose_name = 'İnşaat Resmi'
        verbose_name_plural = 'İnşaat Resimleri'
    
    def __str__(self):
        return f"{self.construction.project_name} resmi"


class ContactMessage(models.Model):
    """
    İletişim formu gönderimleri
    """
    name = models.CharField(max_length=100, verbose_name="Ad Soyad")
    email = models.EmailField(verbose_name="E-posta")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    subject = models.CharField(max_length=200, blank=True, verbose_name="Konu")
    message = models.TextField(verbose_name="Mesaj")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Gönderim Tarihi")
    is_read = models.BooleanField(default=False, verbose_name="Okundu")
    
    class Meta:
        ordering = ['-created_date']
        verbose_name = 'İletişim Mesajı'
        verbose_name_plural = 'İletişim Mesajları'
    
    def __str__(self):
        return f"{self.name} mesajı - {self.created_date.strftime('%Y-%m-%d')}"


class SiteSettings(models.Model):
    """
    Global site settings (singleton model - only one instance)
    """
    # Branding
    logo = models.ImageField(
        upload_to='site/', 
        blank=True, 
        verbose_name="Site Logosu",
        help_text="Sitenizin logosunu yükleyin"
    )
    favicon = models.ImageField(
        upload_to='site/', 
        blank=True, 
        verbose_name="Favicon",
        help_text="Tarayıcı sekmesinde görünen favicon (genellikle 32x32 piksel)"
    )
    
    # Contact information
    phone = models.CharField(max_length=200, blank=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="E-posta")
    address = models.CharField(max_length=500, blank=True, verbose_name="Adres")
    
    # Tax information
    tax_number = models.CharField(max_length=20, blank=True, verbose_name="Vergi Numarası")
    tax_office = models.CharField(max_length=100, blank=True, verbose_name="Vergi Dairesi")
    
    # Map location
    map_embed_code = models.TextField(
        blank=True, 
        verbose_name="Harita Embed Kodu",
        help_text="Google Maps embed kodunu buraya yapıştırın"
    )
    map_latitude = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name="Enlem (Latitude)",
        help_text="Harita konumunun enlem değeri"
    )
    map_longitude = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name="Boylam (Longitude)",
        help_text="Harita konumunun boylam değeri"
    )
    google_maps_api_key = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Google Maps API Anahtarı",
        help_text="Google Maps API anahtarınızı buraya ekleyin"
    )
    
    # Social media
    facebook_url = models.URLField(blank=True, verbose_name="Facebook URL")
    instagram_url = models.URLField(blank=True, verbose_name="Instagram URL")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter URL")
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn URL")
    
    # Google tools
    google_search_console_verification = models.CharField(
        max_length=500, 
        blank=True, 
        verbose_name="Google Search Console Doğrulama Kodu",
        help_text="Google Search Console için meta tag veya HTML doğrulama kodu"
    )
    google_analytics_id = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name="Google Analytics ID",
        help_text="Google Analytics için izleme ID (örn: UA-XXXXXXXX-X veya G-XXXXXXXXXX)"
    )
    
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    class Meta:
        verbose_name = 'Site Ayarları'
        verbose_name_plural = 'Site Ayarları'
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError('Only one SiteSettings instance is allowed')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return "Site Ayarları"


class About(models.Model):
    """
    Homepage settings and content (singleton model - only one instance)
    """
    HOMEPAGE_TEMPLATES = (
        ('template1', 'Template 1 - Large Banner'),
        ('template2', 'Template 2 - Minimal'),
        ('template3', 'Template 3 - Featured Focus'),
        ('template4', 'Template 4 - Content Rich'),
    )
    
    # Template selection
    homepage_template = models.CharField(
        max_length=20, 
        choices=HOMEPAGE_TEMPLATES, 
        default='template1',
        verbose_name="Anasayfa Şablonu",
        help_text="Anasayfa için kullanılacak şablonu seçin"
    )
    
    # Banner images
    banner_images = models.ManyToManyField(
        'BannerImage',
        blank=True,
        verbose_name="Banner Görselleri",
        help_text="Anasayfa banner'ında gösterilmesini istediğiniz görselleri seçin"
    )
    
    # Navigation visibility options
    show_listings_page = models.BooleanField(default=True, verbose_name="İlanlar Sayfasını Göster", help_text="Header menüsünde İlanlar sayfası linkini göster")
    show_construction_page = models.BooleanField(default=True, verbose_name="İnşaatlar Sayfasını Göster", help_text="Header menüsünde İnşaatlar sayfası linkini göster")
    show_references_page = models.BooleanField(default=True, verbose_name="Referanslar Sayfasını Göster", help_text="Header menüsünde Referanslar sayfası linkini göster")
    show_contact_page = models.BooleanField(default=True, verbose_name="İletişim Sayfasını Göster", help_text="Header menüsünde İletişim sayfası linkini göster")
    
    # General section visibility options (not tied to specific content)
    show_search_bar = models.BooleanField(default=True, verbose_name="Arama Çubuğunu Göster")
    show_stats_section = models.BooleanField(default=True, verbose_name="İstatistikleri Göster")
    show_featured_listings = models.BooleanField(default=True, verbose_name="Öne Çıkan İlanları Göster")
    show_features_section = models.BooleanField(default=True, verbose_name="Özellikler Bölümünü Göster")
    show_testimonials = models.BooleanField(default=True, verbose_name="Müşteri Yorumlarını Göster")
    show_recent_listings = models.BooleanField(default=True, verbose_name="Son İlanları Göster")
    show_contact_info = models.BooleanField(default=True, verbose_name="İletişim Bilgilerini Göster")
    show_social_media = models.BooleanField(default=True, verbose_name="Sosyal Medya Bağlantılarını Göster")
    
    # Custom sections visibility with ordering
    # visible_custom_sections = models.ManyToManyField(
    #     'CustomSection',
    #     through='VisibleCustomSection',
    #     blank=True,
    #     verbose_name="Görünür Özel Bölümler",
    #     help_text="Anasayfada gösterilmesini istediğiniz özel bölümleri seçin"
    # )
    
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    class Meta:
        verbose_name = 'Ana Sayfa Ayarları'
        verbose_name_plural = 'Ana Sayfa Ayarları'
    
    def save(self, *args, **kwargs):
        if not self.pk and About.objects.exists():
            # Ensure only one instance exists
            raise ValueError('Only one About instance is allowed')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return "Ana Sayfa Ayarları"


class BannerImage(models.Model):
    """
    Model for homepage banner images with optional buttons
    """
    image = models.ImageField(
        upload_to='banner/',
        verbose_name="Banner Görseli",
        help_text="Banner olarak kullanılacak görsel. Önerilen boyut: 1920x1080 piksel (16:9 en-boy oranı). Tüm banner görselleri aynı boyutta olmalıdır."
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Alternatif Metin",
        help_text="Görsel için erişilebilirlik metni"
    )
    
    # Button options
    button_text = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Buton Metni",
        help_text="Banner üzerinde gösterilecek buton metni (boş bırakılırsa buton gösterilmez)"
    )
    button_link = models.URLField(
        blank=True,
        verbose_name="Buton Bağlantısı",
        help_text="Butonun yönlendireceği URL"
    )
    button_position = models.CharField(
        max_length=20,
        choices=[
            ('top-left', 'Üst Sol'),
            ('top-center', 'Üst Orta'),
            ('top-right', 'Üst Sağ'),
            ('middle-left', 'Orta Sol'),
            ('middle-center', 'Orta'),
            ('middle-right', 'Orta Sağ'),
            ('bottom-left', 'Alt Sol'),
            ('bottom-center', 'Alt Orta'),
            ('bottom-right', 'Alt Sağ'),
        ],
        default='middle-center',
        verbose_name="Buton Konumu",
        help_text="Butonun banner üzerindeki konumu"
    )
    
    # Display options
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    order = models.IntegerField(default=0, verbose_name="Sıra")
    
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Oluşturma Tarihi")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Banner Görseli'
        verbose_name_plural = 'Banner Görselleri'
    
    def save(self, *args, **kwargs):
        if not self.alt_text and self.image:
            # Generate alt text from image name if not provided
            self.alt_text = self.image.name.split('/')[-1].split('.')[0].replace('-', ' ').replace('_', ' ').title()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Banner Görseli - {self.alt_text}"


class CustomSection(models.Model):
    """
    Custom content sections for homepage and other pages
    """
    LAYOUT_CHOICES = (
        ('text_only', 'Sadece Metin'),
        ('image_left', 'Resim Solda'),
        ('image_right', 'Resim Sağda'),
        ('image_center', 'Resim Ortada'),
        ('cards', 'Kartlar'),
        ('about_section', 'Hakkımızda Bölümü'),  # Added new layout for About section
        ('services', 'Hizmetler'),  # Added new layout for Services section
    )
    
    ALIGNMENT_CHOICES = (
        ('left', 'Sol'),
        ('center', 'Orta'),
        ('right', 'Sağ'),
    )
    
    title = models.CharField(max_length=255, verbose_name="Başlık")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Alt Başlık")
    content = models.TextField(blank=True, verbose_name="İçerik")
    layout = models.CharField(max_length=20, choices=LAYOUT_CHOICES, default='text_only', verbose_name="Düzen")
    text_alignment = models.CharField(max_length=10, choices=ALIGNMENT_CHOICES, default='left', verbose_name="Metin Hizalama")
    
    # Images
    main_image = models.ImageField(upload_to='custom_sections/', blank=True, null=True, verbose_name="Ana Resim")
    image_alt_text = models.CharField(max_length=255, blank=True, verbose_name="Resim Alt Yazısı")
    
    # Cards (for card layout)
    card_title_1 = models.CharField(max_length=100, blank=True, verbose_name="Kart 1 Başlık")
    card_content_1 = models.TextField(blank=True, verbose_name="Kart 1 İçerik")
    card_image_1 = models.ImageField(upload_to='custom_sections/cards/', blank=True, null=True, verbose_name="Kart 1 Resim")
    
    card_title_2 = models.CharField(max_length=100, blank=True, verbose_name="Kart 2 Başlık")
    card_content_2 = models.TextField(blank=True, verbose_name="Kart 2 İçerik")
    card_image_2 = models.ImageField(upload_to='custom_sections/cards/', blank=True, null=True, verbose_name="Kart 2 Resim")
    
    card_title_3 = models.CharField(max_length=100, blank=True, verbose_name="Kart 3 Başlık")
    card_content_3 = models.TextField(blank=True, verbose_name="Kart 3 İçerik")
    card_image_3 = models.ImageField(upload_to='custom_sections/cards/', blank=True, null=True, verbose_name="Kart 3 Resim")
    
    # Display options
    background_color = models.CharField(max_length=20, blank=True, verbose_name="Arka Plan Rengi", help_text="HEX renk kodu (örn: #ffffff)")
    text_color = models.CharField(max_length=20, blank=True, verbose_name="Metin Rengi", help_text="HEX renk kodu (örn: #000000)")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    order = models.IntegerField(default=0, verbose_name="Sıra")
    
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Oluşturma Tarihi")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Özel Bölüm'
        verbose_name_plural = 'Özel Bölümler'
    
    def __str__(self):
        return self.title


# Through model for ordering visible custom sections
class Reference(models.Model):
    """
    Model for reference items with images, videos, and descriptions
    """
    title = models.CharField(max_length=255, verbose_name="Başlık")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Alt Başlık")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    
    # Display options
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    order = models.IntegerField(default=0, verbose_name="Sıra")
    
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Oluşturma Tarihi")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Referans'
        verbose_name_plural = 'Referanslar'
    
    def __str__(self):
        return self.title


class ReferenceImage(models.Model):
    """
    Model for reference images
    """
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='references/images/', verbose_name="Resim")
    alt_text = models.CharField(max_length=255, blank=True, verbose_name="Alternatif Metin")
    order = models.IntegerField(default=0, verbose_name="Sıra")
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Referans Resmi'
        verbose_name_plural = 'Referans Resimleri'
    
    def save(self, *args, **kwargs):
        if not self.alt_text and self.image:
            # Generate alt text from image name if not provided
            self.alt_text = self.image.name.split('/')[-1].split('.')[0].replace('-', ' ').replace('_', ' ').title()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.reference.title} - Resim {self.order + 1}"


class ReferenceVideo(models.Model):
    """
    Model for reference videos
    """
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='references/videos/', verbose_name="Video")
    title = models.CharField(max_length=255, blank=True, verbose_name="Video Başlığı")
    order = models.IntegerField(default=0, verbose_name="Sıra")
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Referans Videosu'
        verbose_name_plural = 'Referans Videoları'
    
    def save(self, *args, **kwargs):
        if not self.title and self.video:
            # Generate title from video name if not provided
            self.title = self.video.name.split('/')[-1].split('.')[0].replace('-', ' ').replace('_', ' ').title()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.reference.title} - Video {self.order + 1}"


class SEOSettings(models.Model):
    """
    SEO settings for different page types
    """
    PAGE_TYPES = (
        ('home', 'Anasayfa'),
        ('listings', 'İlanlar'),
        ('construction', 'İnşaatlar'),
        ('references', 'Referanslar'),
        ('contact', 'İletişim'),
    )
    
    page_type = models.CharField(max_length=20, choices=PAGE_TYPES, unique=True, verbose_name="Sayfa Türü")
    meta_title = models.CharField(max_length=60, blank=True, verbose_name="Meta Başlık", help_text="Tarayıcı sekmesinde görünen başlık (en fazla 60 karakter)")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="Meta Açıklama", help_text="Arama motorlarında görünen açıklama (en fazla 160 karakter)")
    og_title = models.CharField(max_length=60, blank=True, verbose_name="Open Graph Başlık", help_text="Sosyal medya platformlarında paylaşıldığında görünen başlık")
    og_description = models.CharField(max_length=255, blank=True, verbose_name="Open Graph Açıklama", help_text="Sosyal medya platformlarında paylaşıldığında görünen açıklama")
    og_image = models.ImageField(upload_to='seo/', blank=True, null=True, verbose_name="Open Graph Görseli", help_text="Sosyal medya platformlarında paylaşıldığında görünen görsel")
    og_image_alt = models.CharField(max_length=255, blank=True, verbose_name="Open Graph Görsel Açıklaması", help_text="Open Graph görseli için alternatif metin")
    
    # JSON-LD structured data
    structured_data = models.TextField(blank=True, verbose_name="Yapılandırılmış Veri (JSON-LD)", help_text="Sayfa için özel JSON-LD yapılandırılmış veri")
    
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    class Meta:
        verbose_name = 'SEO Ayarı'
        verbose_name_plural = 'SEO Ayarları'
    
    def __str__(self):
        return f"SEO - {self.get_page_type_display()}"


class VisibleCustomSection(models.Model):
    """
    Through model to manage visible custom sections with ordering
    """
    about = models.ForeignKey('About', on_delete=models.CASCADE)
    custom_section = models.ForeignKey('CustomSection', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, verbose_name="Görünüm Sırası")
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Görünür Özel Bölüm'
        verbose_name_plural = 'Görünür Özel Bölümler'
        unique_together = ('about', 'custom_section')
    
    def __str__(self):
        return f"{self.about} - {self.custom_section} (Sıra: {self.order})"

