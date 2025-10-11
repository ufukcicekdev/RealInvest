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


class About(models.Model):
    """
    Hakkımızda sayfa içeriği (tekil model - sadece bir örnek)
    """
    title = models.CharField(max_length=255, default="Hakkımızda", verbose_name="Başlık")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Alt Başlık")
    content = models.TextField(verbose_name="İçerik", help_text="Ana hakkımızda sayfa içeriği")
    mission = models.TextField(blank=True, verbose_name="Misyon", help_text="Şirket misyon beyanı")
    vision = models.TextField(blank=True, verbose_name="Vizyon", help_text="Şirket vizyonu")
    
    # Images
    main_image = models.ImageField(upload_to='about/', verbose_name="Ana Resim", help_text="Ana hakkımızda sayfa resmi")
    image_alt_text = models.CharField(max_length=255, blank=True, verbose_name="Resim Alt Yazısı")
    
    # Contact details
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="E-posta")
    address = models.CharField(max_length=500, blank=True, verbose_name="Adres")
    
    # Social media
    facebook_url = models.URLField(blank=True, verbose_name="Facebook URL")
    instagram_url = models.URLField(blank=True, verbose_name="Instagram URL")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter URL")
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn URL")
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True, verbose_name="Meta Başlık")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="Meta Açıklama")
    
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    class Meta:
        verbose_name = 'Hakkımızda Sayfası'
        verbose_name_plural = 'Hakkımızda Sayfası'
    
    def save(self, *args, **kwargs):
        if not self.pk and About.objects.exists():
            # Ensure only one instance exists
            raise ValueError('Only one About instance is allowed')
        if not self.image_alt_text:
            self.image_alt_text = self.title
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_description:
            self.meta_description = self.content[:160]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
