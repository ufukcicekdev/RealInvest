from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django import forms
from django.db import models
from .widgets import ColorPickerWidget, CustomSectionForm
from .models import (
    Listing, ListingImage, Construction, ConstructionImage, ContactMessage, 
    About, SiteSettings, CustomSection, BannerImage, Reference, ReferenceImage, 
    ReferenceVideo, SEOSettings, VisibleCustomSection, NewsletterSubscriber, 
    Newsletter, PopupSettings, NewsletterLog
)

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
        return obj.get_formatted_price()
    price_display.short_description = 'Fiyat'
    price_display.admin_order_field = 'price'
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'slug', 'description', 'property_type', 'status', 'price', 'currency', 'location', 'address')
        }),
        ('Gayrimenkul Detayları', {
            'fields': ('bedrooms', 'bathrooms', 'area', 'floor', 'building_age'),
            'description': 'NOT: Yatak odası, banyo, kat ve bina yaşı alanları arsa ve ticari gayrimenkuller için boş bırakılabilir. Bu alanlar sadece daire, ev, villa ve ofis için doldurulmalıdır.'
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
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 3, 'cols': 60})},
    }
    
    fieldsets = (
        ('Marka ve Kimlik', {
            'fields': ('logo', 'favicon'),
            'description': 'Sitenizin logosunu ve faviconunu buraya yükleyin.'
        }),
        ('İletişim Bilgileri', {
            'fields': ('phone', 'email', 'address', 'contact_email_recipients', 'tax_number', 'tax_office'),
            'description': 'Şirketinizin iletişim bilgilerini buraya girin. Bu bilgiler web sitenizin farklı bölümlerinde gösterilecektir. İletişim formu alıcı e-postaları: Birden fazla e-posta için virgül ile ayırın.'
        }),
        ('Email SMTP Ayarları', {
            'fields': (
                ('smtp_host', 'smtp_port'),
                'smtp_username',
                'smtp_password',
                ('smtp_use_tls', 'email_from')
            ),
            'description': 'İletişim formundan email göndermek için SMTP ayarlarını buraya girin. Gmail kullanıyorsanız: Google Hesabı → Güvenlik → 2 Adımlı Doğrulama → Uygulama Şifreleri ile 16 haneli şifre oluşturun.',
            'classes': ('collapse',)
        }),
        ('Harita Konumu', {
            'fields': ('map_embed_code', 'map_latitude', 'map_longitude', 'google_maps_api_key'),
            'description': 'Google Maps konumunuzu buraya ekleyin. Embed kodu veya enlem/boylam koordinatlarını girebilirsiniz.'
        }),
        ('Sosyal Medya', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'linkedin_url'),
            'description': 'Sosyal medya hesaplarınızı buraya ekleyin. Boş bırakılan alanlar web sitesinde gösterilmeyecektir.'
        }),
        ('WhatsApp ve Telefon İkonları', {
            'fields': (
                ('show_whatsapp', 'whatsapp_number', 'whatsapp_position'),
                ('show_phone', 'phone_number', 'phone_position')
            ),
            'description': 'Sayfada sabit whatsapp ve telefon ikonlarını göster. Kullanıcılar bu ikonlara tıklayarak sizi arayabilir veya WhatsApp\'tan yazabilir.'
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


class BannerImageForm(forms.ModelForm):
    """
    Custom form for BannerImage model with color picker widgets
    """
    class Meta:
        model = BannerImage
        fields = '__all__'
        widgets = {
            'button_background_color': ColorPickerWidget(),
            'button_text_color': ColorPickerWidget(),
            'alt_text_color': ColorPickerWidget(),
        }


@admin.register(BannerImage)
class BannerImageAdmin(admin.ModelAdmin):
    """
    Banner image admin configuration
    """
    form = BannerImageForm  # Use custom form with color pickers
    
    list_display = ('image_preview', 'alt_text', 'button_text', 'is_active', 'order', 'created_date')
    list_filter = ('is_active', 'created_date')
    search_fields = ('alt_text', 'button_text')
    list_editable = ('is_active', 'order')
    date_hierarchy = 'created_date'
    
    fieldsets = (
        ('Görsel', {
            'fields': ('image', 'alt_text', 'alt_text_position', 'alt_text_color'),
            'description': 'Önerilen boyut: 1920x1080 piksel (16:9 en-boy oranı). Tüm banner görselleri aynı boyutta olmalıdır.'
        }),
        ('Buton Ayarları', {
            'fields': ('button_text', 'button_link', 'button_position', 'button_background_color', 'button_text_color'),
            'description': 'Banner üzerinde buton göstermek istiyorsanız bu alanları doldurun.'
        }),
        ('Görünüm Ayarları', {
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
    
    list_display = ('title', 'layout', 'is_active', 'created_date')
    list_filter = ('layout', 'is_active', 'created_date')
    search_fields = ('title', 'subtitle', 'content')
    list_editable = ('is_active',)
    date_hierarchy = 'created_date'
    
    def get_readonly_fields(self, request, obj=None):
        """
        Sabit bölümler için alanları read-only yap
        """
        readonly_fields = []
        if obj and obj.layout in [
            'search_bar', 'stats_section', 'featured_listings', 
            'features_section', 'testimonials', 'recent_listings', 
            'contact_info', 'social_media'
        ]:
            # Sabit bölümler için tüm alanları read-only yap
            readonly_fields = [field.name for field in obj._meta.fields]
        return readonly_fields
    
    def has_change_permission(self, request, obj=None):
        """
        Sabit bölümler için düzenleme iznini kaldır
        """
        if obj and obj.layout in [
            'search_bar', 'stats_section', 'featured_listings', 
            'features_section', 'testimonials', 'recent_listings', 
            'contact_info', 'social_media'
        ]:
            return False
        return super().has_change_permission(request, obj)
    
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
            'fields': ('is_active',)
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
        ('Temel Meta Etiketleri', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('Sayfa Ayarları', {
            'fields': ('canonical_url', 'robots'),
            'description': 'Canonical URL ve arama motoru bot ayarları'
        }),
        ('Open Graph (Facebook, LinkedIn)', {
            'fields': ('og_type', 'og_title', 'og_description', 'og_image', 'og_image_alt'),
            'description': 'Sosyal medya platformlarında paylaşım için Open Graph ayarları. İdeal görsel boyutu: 1200x630px'
        }),
        ('Twitter Card', {
            'fields': ('twitter_card', 'twitter_site', 'twitter_creator'),
            'description': 'Twitter paylaşımları için özel ayarlar'
        }),
        ('Yapılandırılmış Veri', {
            'fields': ('structured_data',),
            'description': 'JSON-LD formatında yapılandırılmış veri (gelişmiş kullanıcılar için)'
        }),
    )
    
    def page_type_display(self, obj):
        return obj.get_page_type_display()
    page_type_display.short_description = 'Sayfa Türü'
    page_type_display.admin_order_field = 'page_type'


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    """
    Newsletter subscribers admin
    """
    list_display = ('email', 'name', 'phone', 'is_active', 'subscribed_date', 'subscriber_status')
    list_filter = ('is_active', 'subscribed_date')
    search_fields = ('email', 'name', 'phone')
    readonly_fields = ('subscribed_date', 'unsubscribed_date', 'ip_address', 'unsubscribe_token')
    list_editable = ('is_active',)
    date_hierarchy = 'subscribed_date'
    
    fieldsets = (
        ('Abone Bilgileri', {
            'fields': ('email', 'name', 'phone', 'is_active')
        }),
        ('Tarihler', {
            'fields': ('subscribed_date', 'unsubscribed_date')
        }),
        ('Teknik Bilgiler', {
            'fields': ('ip_address', 'unsubscribe_token'),
            'classes': ('collapse',)
        }),
    )
    
    def subscriber_status(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Aktif</span>')
        else:
            return format_html('<span style="color: red;">✗ Pasif</span>')
    subscriber_status.short_description = 'Durum'
    
    actions = ['activate_subscribers', 'deactivate_subscribers']
    
    def activate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=True, unsubscribed_date=None)
        self.message_user(request, f'{updated} abone aktifleştirildi.')
    activate_subscribers.short_description = 'Seçili aboneleri aktifleştir'
    
    def deactivate_subscribers(self, request, queryset):
        from django.utils import timezone
        for subscriber in queryset:
            subscriber.is_active = False
            subscriber.unsubscribed_date = timezone.now()
            subscriber.save()
        self.message_user(request, f'{queryset.count()} abone pasifleştirildi.')
    deactivate_subscribers.short_description = 'Seçili aboneleri pasifleştir'


class NewsletterLogInline(admin.TabularInline):
    """
    Inline admin for newsletter logs
    """
    model = NewsletterLog
    extra = 0
    readonly_fields = ('log_type', 'message', 'subscriber_email', 'error_details', 'created_date')
    can_delete = False
    max_num = 0  # Prevent adding new logs through admin
    
    fields = ('created_date', 'log_type', 'message', 'subscriber_email')
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """
    Newsletter campaigns admin with send functionality
    """
    list_display = ('title', 'status', 'scheduled_date', 'sent_date', 'total_recipients', 'sent_count', 'status_badge')
    list_filter = ('status', 'scheduled_date', 'sent_date')
    search_fields = ('title', 'subject', 'content')
    readonly_fields = ('sent_date', 'total_recipients', 'sent_count', 'failed_count', 'created_date', 'updated_date')
    date_hierarchy = 'created_date'
    inlines = [NewsletterLogInline]  # Add log inline
    
    fieldsets = (
        ('Bülten Bilgileri', {
            'fields': ('title', 'subject', 'content')
        }),
        ('Zamanlama', {
            'fields': ('status', 'scheduled_date', 'sent_date'),
            'description': 'Gönderim zamanı boş bırakılırsa "Gönder" butonuna basıldığında hemen gönderilir.'
        }),
        ('İstatistikler', {
            'fields': ('total_recipients', 'sent_count', 'failed_count'),
            'classes': ('collapse',)
        }),
        ('Tarihler', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'draft': 'gray',
            'scheduled': 'blue',
            'sending': 'orange',
            'sent': 'green',
            'failed': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Durum'
    
    actions = ['send_newsletter']
    
    def send_newsletter(self, request, queryset):
        from django.core.mail import EmailMultiAlternatives, get_connection
        from django.template.loader import render_to_string
        from django.utils import timezone
        
        for newsletter in queryset:
            if newsletter.status in ['sent', 'sending']:
                self.message_user(request, f'"{newsletter.title}" zaten gönderilmiş veya gönderiliyor.', level='warning')
                continue
            
            # Log: Starting newsletter send
            NewsletterLog.log_info(newsletter, f'Bülten gönderimi başlatıldı: {newsletter.title}')
            
            # Get active subscribers
            subscribers = NewsletterSubscriber.objects.filter(is_active=True)
            newsletter.total_recipients = subscribers.count()
            
            if newsletter.total_recipients == 0:
                NewsletterLog.log_error(newsletter, 'Aktif abone bulunamadı')
                self.message_user(request, 'Aktif abone bulunamadı!', level='error')
                continue
            
            NewsletterLog.log_info(newsletter, f'Toplam {newsletter.total_recipients} aboneye gönderilecek')
            
            newsletter.status = 'sending'
            newsletter.save()
            
            sent_count = 0
            failed_count = 0
            
            # Get SMTP settings from SiteSettings
            site_settings = SiteSettings.objects.first()
            
            if not site_settings:
                NewsletterLog.log_error(newsletter, 'Site ayarları bulunamadı')
                self.message_user(request, 'Site ayarları bulunamadı! Lütfen önce Site Ayarlarını yapılandırın.', level='error')
                newsletter.status = 'failed'
                newsletter.save()
                continue
            
            # Check if SMTP settings are configured
            if not site_settings.smtp_host or not site_settings.smtp_username:
                NewsletterLog.log_error(newsletter, 'SMTP ayarları yapılandırılmamış')
                self.message_user(
                    request, 
                    'SMTP ayarları yapılandırılmamış! Lütfen Site Ayarları > Email SMTP Ayarları bölümünü doldurun.',
                    level='error'
                )
                newsletter.status = 'failed'
                newsletter.save()
                continue
            
            # Create custom email connection with SiteSettings SMTP config
            try:
                connection = get_connection(
                    backend='django.core.mail.backends.smtp.EmailBackend',
                    host=site_settings.smtp_host,
                    port=site_settings.smtp_port,
                    username=site_settings.smtp_username,
                    password=site_settings.smtp_password,
                    use_tls=site_settings.smtp_use_tls,
                    fail_silently=False,
                )
                NewsletterLog.log_success(newsletter, f'SMTP bağlantısı kuruldu: {site_settings.smtp_host}:{site_settings.smtp_port}')
            except Exception as e:
                error_msg = f'SMTP bağlantısı kurulamadı: {str(e)}'
                NewsletterLog.log_error(newsletter, error_msg, error_details=str(e))
                self.message_user(request, error_msg, level='error')
                newsletter.status = 'failed'
                newsletter.save()
                continue
            
            for subscriber in subscribers:
                try:
                    # Prepare unsubscribe link
                    unsubscribe_url = request.build_absolute_uri(
                        reverse('newsletter_unsubscribe', args=[subscriber.unsubscribe_token])
                    )
                    
                    # Generate absolute logo URL for email
                    logo_url = None
                    if site_settings.logo:
                        # Logo URL is already absolute from CDN, use it directly
                        logo_url = site_settings.logo.url
                        NewsletterLog.log_info(newsletter, f'Logo URL from storage: {logo_url}')
                        # If it's a relative path, make it absolute
                        if not logo_url.startswith('http'):
                            logo_url = request.build_absolute_uri(logo_url)
                            NewsletterLog.log_info(newsletter, f'Logo URL converted to absolute: {logo_url}')
                        else:
                            NewsletterLog.log_info(newsletter, f'Logo URL is already absolute: {logo_url}')
                    
                    # Render email template with context
                    import datetime
                    context = {
                        'newsletter': newsletter,
                        'subscriber': subscriber,
                        'site_settings': site_settings,
                        'unsubscribe_url': unsubscribe_url,
                        'logo_url': logo_url,
                        'current_year': datetime.datetime.now().year,
                    }
                    
                    html_content = render_to_string('emails/newsletter.html', context)
                    
                    # Plain text version (strip HTML tags)
                    from django.utils.html import strip_tags
                    plain_content = strip_tags(newsletter.content)
                    
                    # Send email using custom SMTP connection
                    email = EmailMultiAlternatives(
                        subject=newsletter.subject,
                        body=plain_content,
                        from_email=site_settings.email_from if site_settings.email_from else site_settings.email,
                        to=[subscriber.email],
                        connection=connection  # Use custom SMTP connection
                    )
                    email.attach_alternative(html_content, "text/html")
                    email.send()
                    
                    sent_count += 1
                    NewsletterLog.log_success(
                        newsletter, 
                        f'Email başarıyla gönderildi', 
                        subscriber_email=subscriber.email
                    )
                    
                except Exception as e:
                    failed_count += 1
                    error_msg = f'Email gönderilemedi: {str(e)}'
                    NewsletterLog.log_error(
                        newsletter,
                        error_msg,
                        subscriber_email=subscriber.email,
                        error_details=str(e)
                    )
                    print(f"Failed to send to {subscriber.email}: {str(e)}")
            
            # Close connection
            try:
                connection.close()
            except:
                pass
            
            # Update newsletter stats and status
            newsletter.sent_count = sent_count
            newsletter.failed_count = failed_count
            newsletter.sent_date = timezone.now()
            
            # Determine final status
            if sent_count == 0:
                # No emails sent at all
                newsletter.status = 'failed'
                status_message = f'❌ "{newsletter.title}" bülteni hiçbir aboneye gönderilemedi! ({failed_count} başarısız)'
                message_level = 'error'
                NewsletterLog.log_error(newsletter, f'Bülten gönderimi başarısız: Hiçbir email gönderilemedi ({failed_count} hata)')
            elif failed_count == 0:
                # All emails sent successfully
                newsletter.status = 'sent'
                status_message = f'✅ "{newsletter.title}" bülteni {sent_count}/{newsletter.total_recipients} aboneye başarıyla gönderildi!'
                message_level = 'success'
                NewsletterLog.log_success(newsletter, f'Bülten başarıyla gönderildi: {sent_count}/{newsletter.total_recipients} email')
            else:
                # Partial success
                newsletter.status = 'sent'  # Mark as sent if at least some went through
                status_message = f'⚠️ "{newsletter.title}" bülteni {sent_count}/{newsletter.total_recipients} aboneye gönderildi. ({failed_count} başarısız)'
                message_level = 'warning'
                NewsletterLog.log_warning(newsletter, f'Kısmi başarı: {sent_count} başarılı, {failed_count} başarısız')
            
            newsletter.save()
            
            self.message_user(request, status_message, level=message_level)
    
    send_newsletter.short_description = 'Seçili bültenleri gönder'


@admin.register(PopupSettings)
class PopupSettingsAdmin(admin.ModelAdmin):
    """
    Newsletter popup settings admin (singleton)
    """
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'class': 'vTextField'})},
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 3})},
    }
    
    fieldsets = (
        ('Popup Ayarları', {
            'fields': ('enabled', 'title', 'description')
        }),
        ('Görüntüleme Ayarları', {
            'fields': ('delay_seconds', 'show_on_mobile')
        }),
        ('Stil Ayarları', {
            'fields': ('button_text', 'button_color'),
            'description': 'Buton rengi için hex kod kullanın (orn: #007bff)'
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not PopupSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


class NewsletterLogInline(admin.TabularInline):
    """
    Inline admin for newsletter logs
    """
    model = NewsletterLog
    extra = 0
    readonly_fields = ('log_type', 'message', 'subscriber_email', 'error_details', 'created_date')
    can_delete = False
    max_num = 0  # Prevent adding new logs through admin
    
    fields = ('created_date', 'log_type', 'message', 'subscriber_email')
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(NewsletterLog)
class NewsletterLogAdmin(admin.ModelAdmin):
    """
    Newsletter log admin for viewing send history
    """
    list_display = ('created_date', 'newsletter', 'log_type_badge', 'message_preview', 'subscriber_email')
    list_filter = ('log_type', 'created_date', 'newsletter')
    search_fields = ('message', 'subscriber_email', 'error_details', 'newsletter__title')
    readonly_fields = ('newsletter', 'log_type', 'message', 'subscriber_email', 'error_details', 'created_date')
    date_hierarchy = 'created_date'
    
    fieldsets = (
        ('Log Bilgileri', {
            'fields': ('newsletter', 'log_type', 'created_date')
        }),
        ('Mesaj', {
            'fields': ('message', 'subscriber_email')
        }),
        ('Hata Detayları', {
            'fields': ('error_details',),
            'classes': ('collapse',)
        }),
    )
    
    def log_type_badge(self, obj):
        colors = {
            'info': '#17a2b8',
            'success': '#28a745',
            'warning': '#ffc107',
            'error': '#dc3545'
        }
        color = colors.get(obj.log_type, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_log_type_display()
        )
    log_type_badge.short_description = 'Tip'
    
    def message_preview(self, obj):
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    message_preview.short_description = 'Mesaj'
    
    def has_add_permission(self, request):
        # Don't allow manual log creation
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Allow deletion for cleanup
        return True
