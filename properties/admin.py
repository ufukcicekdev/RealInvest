from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .widgets import ColorPickerWidget, CustomSectionForm
from .models import Listing, ListingImage, Construction, ConstructionImage, ContactMessage, About, SiteSettings, CustomSection, BannerImage, Reference, ReferenceImage, ReferenceVideo, SEOSettings, VisibleCustomSection

# Register your models here.

class ListingImageInline(admin.TabularInline):
    """
    İlan resimleri için inline admin
    """
    model = ListingImage
    extra = 1
    fields = ('image', 'alt_text', 'order')
    verbose_name = "İlan Resmi"
    verbose_name_plural = "İlan Resimleri"


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    """
    Gayrimenkul İlanları için admin yapılandırması
    """
    list_display = ('title', 'property_type', 'status', 'price_display', 'location', 'is_active', 'is_featured', 'created_date')
    list_filter = ('property_type', 'status', 'is_active', 'is_featured', 'created_date')
    search_fields = ('title', 'description', 'location', 'address')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active', 'is_featured')
    date_hierarchy = 'created_date'
    inlines = [ListingImageInline]
    
    def price_display(self, obj):
        return f"₺{obj.price:,.0f}"
    price_display.short_description = 'Fiyat'
    price_display.admin_order_field = 'price'
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'slug', 'description', 'property_type', 'status', 'price', 'location', 'address')
        }),
        ('Gayrimenkul Detayları', {
            'fields': ('bedrooms', 'bathrooms', 'area', 'floor', 'building_age')
        }),
        ('Medya', {
            'fields': ('main_image', 'image_alt_text')
        }),
        ('Görüntüleme Seçenekleri', {
            'fields': ('is_active', 'is_featured')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )


class ConstructionImageInline(admin.TabularInline):
    """
    İnşaat resimleri için inline admin
    """
    model = ConstructionImage
    extra = 1
    fields = ('image', 'alt_text', 'caption', 'order')
    verbose_name = "İnşaat Resmi"
    verbose_name_plural = "İnşaat Resimleri"


@admin.register(Construction)
class ConstructionAdmin(admin.ModelAdmin):
    """
    İnşaat Projeleri için admin yapılandırması
    """
    list_display = ('project_name', 'location', 'status', 'start_date', 'end_date', 'is_active')
    list_filter = ('status', 'is_active', 'start_date')
    search_fields = ('project_name', 'description', 'location')
    prepopulated_fields = {'slug': ('project_name',)}
    list_editable = ('is_active',)
    date_hierarchy = 'start_date'
    inlines = [ConstructionImageInline]
    
    fieldsets = (
        ('Proje Bilgileri', {
            'fields': ('project_name', 'slug', 'description', 'location', 'status')
        }),
        ('Zaman Çizelgesi', {
            'fields': ('start_date', 'end_date')
        }),
        ('Medya', {
            'fields': ('main_image', 'image_alt_text')
        }),
        ('Görüntüleme Seçenekleri', {
            'fields': ('is_active',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    İletişim mesajları için admin yapılandırması
    """
    list_display = ('name', 'email', 'subject', 'created_date', 'is_read')
    list_filter = ('is_read', 'created_date')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('is_read',)
    date_hierarchy = 'created_date'
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_date')
    
    fieldsets = (
        ('İletişim Bilgileri', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Mesaj', {
            'fields': ('subject', 'message', 'created_date')
        }),
        ('Durum', {
            'fields': ('is_read',)
        }),
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    Site-wide settings configuration (singleton)
    """
    fieldsets = (
        ('Marka ve Kimlik', {
            'fields': ('logo', 'favicon'),
            'description': 'Sitenizin logosunu ve faviconunu buraya yükleyin.'
        }),
        ('İletişim Bilgileri', {
            'fields': ('phone', 'email', 'address', 'tax_number', 'tax_office'),
            'description': 'Şirketinizin iletişim bilgilerini buraya girin. Bu bilgiler web sitenizin farklı bölümlerinde gösterilecektir.'
        }),
        ('Harita Konumu', {
            'fields': ('map_embed_code', 'map_latitude', 'map_longitude', 'google_maps_api_key'),
            'description': 'Google Maps konumunuzu buraya ekleyin. Embed kodu veya enlem/boylam koordinatlarını girebilirsiniz.'
        }),
        ('Sosyal Medya', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'linkedin_url'),
            'description': 'Sosyal medya hesaplarınızı buraya ekleyin. Boş bırakılan alanlar web sitesinde gösterilmeyecektir.'
        }),
        ('Google Araçları', {
            'fields': ('google_search_console_verification', 'google_analytics_id'),
            'description': 'Google Search Console ve Google Analytics ayarlarını buraya ekleyin. Bu alanlar SEO ve analiz için önemlidir.'
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


@admin.register(BannerImage)
class BannerImageAdmin(admin.ModelAdmin):
    """
    Banner image admin configuration
    """
    list_display = ('image_preview', 'alt_text', 'button_text', 'is_active', 'order', 'created_date')
    list_filter = ('is_active', 'created_date')
    search_fields = ('alt_text', 'button_text')
    list_editable = ('is_active', 'order')
    date_hierarchy = 'created_date'
    
    fieldsets = (
        ('Görsel', {
            'fields': ('image', 'alt_text'),
            'description': 'Önerilen boyut: 1920x1080 piksel (16:9 en-boy oranı). Tüm banner görselleri aynı boyutta olmalıdır.'
        }),
        ('Buton Ayarları', {
            'fields': ('button_text', 'button_link', 'button_position'),
            'description': 'Banner üzerinde buton göstermek istiyorsanız bu alanları doldurun.'
        }),
        ('Görüntüleme Seçenekleri', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "Görsel Yok"
    image_preview.short_description = 'Önizleme'


class VisibleCustomSectionInline(admin.TabularInline):
    """
    Inline admin for ordering visible custom sections
    """
    model = VisibleCustomSection
    extra = 1
    fields = ('custom_section', 'order')
    verbose_name = "Görünür Özel Bölüm"
    verbose_name_plural = "Görünür Özel Bölümler"


@admin.register(About)
class HomepageSettingsAdmin(admin.ModelAdmin):
    """
    Ana Sayfa Ayarları (tekil model)
    """
    inlines = [VisibleCustomSectionInline]
    
    fieldsets = (
        ('Şablon Seçimi', {
            'fields': ('homepage_template',)
        }),
        ('Banner Ayarları', {
            'fields': ('banner_images',)
        }),
        ('Menü Görünürlüğü', {
            'fields': (
                'show_listings_page', 'show_construction_page', 
                'show_references_page', 'show_contact_page'
            ),
            'description': 'Header menüsünde gösterilmesini istediğiniz sayfaları seçin.'
        }),
        ('Bölüm Görünürlüğü', {
            'fields': (
                'show_search_bar', 'show_stats_section', 'show_featured_listings',
                'show_features_section', 'show_testimonials', 'show_recent_listings',
                'show_contact_info', 'show_social_media'
            ),
            'description': 'Anasayfada gösterilmesini istediğiniz bölümleri seçin.'
        }),
    )
    
    def has_add_permission(self, request):
        # Sadece örnek yoksa eklemeye izin ver
        return not About.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Silmeye izin verme
        return False


@admin.register(CustomSection)
class CustomSectionAdmin(admin.ModelAdmin):
    """
    Custom content sections admin configuration
    """
    form = CustomSectionForm  # Use custom form with color pickers
    
    list_display = ('title', 'layout', 'is_active', 'order', 'created_date')
    list_filter = ('layout', 'is_active', 'created_date')
    search_fields = ('title', 'subtitle', 'content')
    list_editable = ('is_active', 'order')
    date_hierarchy = 'created_date'
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'subtitle', 'content')
        }),
        ('Düzen ve Stil', {
            'fields': ('layout', 'text_alignment', 'background_color', 'text_color')
        }),
        ('Resimler', {
            'fields': ('main_image', 'image_alt_text')
        }),
        ('Kartlar (Sadece Kart Düzeni İçin)', {
            'fields': (
                'card_title_1', 'card_content_1', 'card_image_1',
                'card_title_2', 'card_content_2', 'card_image_2',
                'card_title_3', 'card_content_3', 'card_image_3'
            ),
            'classes': ('collapse',)
        }),
        ('Görüntüleme Seçenekleri', {
            'fields': ('is_active', 'order')
        }),
    )


class ReferenceImageInline(admin.TabularInline):
    """
    Reference images inline admin
    """
    model = ReferenceImage
    extra = 1
    fields = ('image', 'alt_text', 'order')
    verbose_name = "Referans Resmi"
    verbose_name_plural = "Referans Resimleri"


class ReferenceVideoInline(admin.TabularInline):
    """
    Reference videos inline admin
    """
    model = ReferenceVideo
    extra = 1
    fields = ('video', 'title', 'order')
    verbose_name = "Referans Videosu"
    verbose_name_plural = "Referans Videoları"


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    """
    Reference items admin configuration
    """
    list_display = ('title', 'is_active', 'order', 'created_date')
    list_filter = ('is_active', 'created_date')
    search_fields = ('title', 'subtitle', 'description')
    list_editable = ('is_active', 'order')
    date_hierarchy = 'created_date'
    inlines = [ReferenceImageInline, ReferenceVideoInline]
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'subtitle', 'description')
        }),
        ('Görüntüleme Seçenekleri', {
            'fields': ('is_active', 'order')
        }),
    )


@admin.register(SEOSettings)
class SEOSettingsAdmin(admin.ModelAdmin):
    """
    SEO settings admin configuration
    """
    list_display = ('page_type_display', 'meta_title', 'updated_date')
    list_filter = ('page_type', 'updated_date')
    search_fields = ('meta_title', 'meta_description')
    date_hierarchy = 'updated_date'
    
    fieldsets = (
        ('Sayfa Türü', {
            'fields': ('page_type',)
        }),
        ('Meta Etiketleri', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Open Graph (Sosyal Medya)', {
            'fields': ('og_title', 'og_description', 'og_image', 'og_image_alt')
        }),
        ('Yapılandırılmış Veri', {
            'fields': ('structured_data',)
        }),
    )
    
    def page_type_display(self, obj):
        return obj.get_page_type_display()
    page_type_display.short_description = 'Sayfa Türü'
    page_type_display.admin_order_field = 'page_type'
