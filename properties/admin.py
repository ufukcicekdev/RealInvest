from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Listing, ListingImage, Construction, ConstructionImage, ContactMessage, About

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


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    """
    Hakkımızda sayfası için admin yapılandırması (tekil)
    """
    fieldsets = (
        ('Ana İçerik', {
            'fields': ('title', 'subtitle', 'content', 'mission', 'vision')
        }),
        ('Medya', {
            'fields': ('main_image', 'image_alt_text')
        }),
        ('İletişim Bilgileri', {
            'fields': ('phone', 'email', 'address'),
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
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Sadece örnek yoksa eklemeye izin ver
        return not About.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Silmeye izin verme
        return False
