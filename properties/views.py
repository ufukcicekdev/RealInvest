from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import (
    Listing, Construction, About, ContactMessage, Reference, 
    SEOSettings, CustomSection, BannerImage, SiteSettings,
    NewsletterSubscriber, Newsletter, PopupSettings, VisibleCustomSection
)
from .forms import ContactForm, NewsletterSubscribeForm

# Create your views here.

def home(request):
    """
    Home page view displaying featured listings, hero section, and about info
    """
    # Get querysets for featured and recent listings
    featured_listings_qs = Listing.objects.filter(is_active=True, is_featured=True)
    featured_listings = featured_listings_qs[:6]  # Sliced for display
    
    recent_listings_qs = Listing.objects.filter(is_active=True)
    recent_listings = recent_listings_qs[:8]  # Sliced for display
    
    # DEBUG: Print featured listings info
    print("\n=== DEBUG: Featured Listings ===")
    print(f"Featured listings count: {featured_listings_qs.count()}")
    print(f"Featured listings exist: {featured_listings_qs.exists()}")
    if featured_listings_qs.exists():
        for listing in featured_listings:
            print(f"  - {listing.title} (is_featured={listing.is_featured}, is_active={listing.is_active})")
    print("================================\n")
    
    # Get about content for homepage
    try:
        about_content = About.objects.first()
    except About.DoesNotExist:
        about_content = None
    
    # Get banner images for homepage
    banner_images = about_content.banner_images.filter(is_active=True) if about_content else BannerImage.objects.none()
    # Get visible custom sections for homepage with ordering
    custom_sections = CustomSection.objects.none()
    if about_content:
        custom_sections = CustomSection.objects.filter(
            is_active=True
        ).order_by('visiblecustomsection__order')
        

    # Get SEO settings for homepage
    try:
        seo_settings = SEOSettings.objects.get(page_type='home')
        page_title = seo_settings.meta_title or 'Modern Emlak | Hayalinizdeki Gayrimenkulü Bulun'
        meta_description = seo_settings.meta_description or 'Geniş emlak ilanlarımızla hayalinizdeki gayrimenkulü bulun. Daire, ev, villa ve ticari gayrimenkullere göz atın.'
    except SEOSettings.DoesNotExist:
        page_title = 'Modern Emlak | Hayalinizdeki Gayrimenkulü Bulun'
        meta_description = 'Geniş emlak ilanlarımızla hayalinizdeki gayrimenkulü bulun. Daire, ev, villa ve ticari gayrimenkullere göz atın.'
        seo_settings = None
    
    # Create a list of sections with their order and visibility
    sections = []
    if about_content:
        # Get all visible custom sections including fixed sections
        visible_sections = VisibleCustomSection.objects.filter(about=about_content).select_related('custom_section')
        
        # Create a dictionary to track which fixed sections are added via VisibleCustomSection
        fixed_sections_added = {}
        
        for visible_section in visible_sections:
            custom_section = visible_section.custom_section
            
            # Check if this is a fixed section type
            if custom_section.layout == 'search_bar' and about_content.show_search_bar:
                sections.append({'type': 'search_bar', 'order': visible_section.order})
                fixed_sections_added['search_bar'] = True
            elif custom_section.layout == 'stats_section' and about_content.show_stats_section:
                sections.append({'type': 'stats_section', 'order': visible_section.order})
                fixed_sections_added['stats_section'] = True
            elif custom_section.layout == 'featured_listings' and about_content.show_featured_listings and featured_listings_qs.exists():
                sections.append({'type': 'featured_listings', 'order': visible_section.order, 'data': featured_listings})
                fixed_sections_added['featured_listings'] = True
                print(f"✅ Featured listings ADDED from VisibleCustomSection with order: {visible_section.order}")
            elif custom_section.layout == 'featured_listings' and not about_content.show_featured_listings:
                print(f"❌ Featured listings SKIPPED - show_featured_listings is False")
            elif custom_section.layout == 'features_section' and about_content.show_features_section:
                sections.append({'type': 'features_section', 'order': visible_section.order})
                fixed_sections_added['features_section'] = True
            elif custom_section.layout == 'testimonials' and about_content.show_testimonials:
                sections.append({'type': 'testimonials', 'order': visible_section.order})
                fixed_sections_added['testimonials'] = True
            elif custom_section.layout == 'recent_listings' and about_content.show_recent_listings and recent_listings_qs.exists():
                sections.append({'type': 'recent_listings', 'order': visible_section.order, 'data': recent_listings})
                fixed_sections_added['recent_listings'] = True
            elif custom_section.layout == 'contact_info' and about_content.show_contact_info:
                sections.append({'type': 'contact_info', 'order': visible_section.order})
                fixed_sections_added['contact_info'] = True
            elif custom_section.layout == 'social_media' and about_content.show_social_media:
                sections.append({'type': 'social_media', 'order': visible_section.order})
                fixed_sections_added['social_media'] = True
            elif custom_section.is_active:
                # Regular custom section
                section_data = {
                    'type': 'custom_section',
                    'order': visible_section.order,
                    'custom_section': custom_section
                }
                sections.append(section_data)
    
    # Sort sections by order
    sections.sort(key=lambda x: x['order'])
    
    # DEBUG: Print final sections list
    print("\n=== Final Sections List ===")
    print(f"Total sections: {len(sections)}")
    for section in sections:
        section_type = section.get('type', 'unknown')
        section_order = section.get('order', 'no order')
        if section_type == 'featured_listings':
            data_count = len(section.get('data', []))
            print(f"  - Type: {section_type}, Order: {section_order}, Data Count: {data_count}")
        else:
            print(f"  - Type: {section_type}, Order: {section_order}")
    print("===========================\n")
    context = {
        'featured_listings': featured_listings,
        'recent_listings': recent_listings,
        'about': about_content,
        'banner_images': banner_images,  # Add banner images to context
        'custom_sections': custom_sections,
        'sections': sections,
        'page_title': page_title,
        'meta_description': meta_description,
        'seo_settings': seo_settings,
    }
    return render(request, 'properties/home.html', context)


def listings(request):
    """
    Listings page with search, filter, and pagination
    """
    listings_list = Listing.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        listings_list = listings_list.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Filter by property type
    property_type = request.GET.get('type', '')
    if property_type:
        listings_list = listings_list.filter(property_type=property_type)
    
    # Filter by status (sale/rent)
    status = request.GET.get('status', '')
    if status:
        listings_list = listings_list.filter(status=status)
    
    # Pagination
    paginator = Paginator(listings_list, 9)  # 9 listings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get SEO settings for listings page
    try:
        seo_settings = SEOSettings.objects.get(page_type='listings')
        page_title = seo_settings.meta_title or 'Gayrimenkul İlanları | Tüm Gayrimenkullere Göz Atın'
        meta_description = seo_settings.meta_description or 'Kapsamlı gayrimenkul ilanlarımıza göz atın. Satılık veya kiralık daire, ev, villa ve ticari gayrimenkuller bulun.'
    except SEOSettings.DoesNotExist:
        page_title = 'Gayrimenkul İlanları | Tüm Gayrimenkullere Göz Atın'
        meta_description = 'Kapsamlı gayrimenkul ilanlarımıza göz atın. Satılık veya kiralık daire, ev, villa ve ticari gayrimenkuller bulun.'
        seo_settings = None
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'selected_type': property_type,
        'selected_status': status,
        'page_title': page_title,
        'meta_description': meta_description,
        'seo_settings': seo_settings,
    }
    return render(request, 'properties/listings.html', context)


def listing_detail(request, slug):
    """
    Individual listing detail page with inquiry form
    """
    listing = get_object_or_404(Listing, slug=slug, is_active=True)
    related_listings = Listing.objects.filter(
        is_active=True,
        location=listing.location
    ).exclude(id=listing.id)[:3]
    
    # Handle inquiry form submission
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        
        if name and email and message:
            # Save inquiry as contact message
            contact_message = ContactMessage(
                name=name,
                email=email,
                phone=phone,
                subject=f"İlan Sorgusu: {listing.title}",
                message=message
            )
            contact_message.save()
            
            # Send email notification
            try:
                site_settings = SiteSettings.objects.first()
                
                # Get email recipients
                recipient_emails = []
                if site_settings and site_settings.contact_email_recipients:
                    recipient_emails = [email.strip() for email in site_settings.contact_email_recipients.split(',') if email.strip()]
                
                if not recipient_emails and site_settings and site_settings.email:
                    recipient_emails = [site_settings.email]
                
                # Send email if SMTP configured
                if recipient_emails and site_settings and site_settings.smtp_username and site_settings.smtp_password:
                    from django.core.mail import EmailMessage
                    import smtplib
                    
                    subject = f"İlan Sorgusu: {listing.title}"
                    message_body = f"""
Yeni bir ilan sorgusu alındı:

İlan: {listing.title}
İlan Linki: {request.build_absolute_uri(listing.get_absolute_url() if hasattr(listing, 'get_absolute_url') else '')}

Müşteri Bilgileri:
Ad Soyad: {name}
E-posta: {email}
Telefon: {phone}

Mesaj:
{message}

---
Bu mesaj web sitenizin ilan detay sayfasından gönderilmiştir.
                    """
                    
                    try:
                        email_msg = EmailMessage(
                            subject=subject,
                            body=message_body,
                            from_email=site_settings.email_from or site_settings.smtp_username,
                            to=recipient_emails,
                        )
                        
                        smtp_host = site_settings.smtp_host or 'smtp.gmail.com'
                        smtp_port = site_settings.smtp_port or 587
                        
                        connection = smtplib.SMTP(smtp_host, smtp_port)
                        if site_settings.smtp_use_tls:
                            connection.starttls()
                        connection.login(site_settings.smtp_username, site_settings.smtp_password)
                        connection.send_message(email_msg.message())
                        connection.quit()
                    except Exception as smtp_error:
                        print(f"SMTP Email gönderme hatası: {smtp_error}")
            except Exception as e:
                print(f"Email gönderme hatası: {e}")
            
            messages.success(request, 'Sorgunuz başarıyla gönderildi! En kısa sürede size dönüş yapacağız.')
            return redirect('listing_detail', slug=slug)
    
    context = {
        'listing': listing,
        'related_listings': related_listings,
        'page_title': listing.meta_title or listing.title,
        'meta_description': listing.meta_description,
    }
    return render(request, 'properties/listing_detail.html', context)


def construction(request):
    """
    Construction projects page with gallery layout
    """
    projects = Construction.objects.filter(is_active=True)
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        projects = projects.filter(status=status)
    
    # Get SEO settings for construction page
    try:
        seo_settings = SEOSettings.objects.get(page_type='construction')
        page_title = seo_settings.meta_title or 'İnşaat Projeleri | Devam Eden ve Tamamlananlar'
        meta_description = seo_settings.meta_description or 'İnşaat projelerimizi keşfedin. Devam eden ve tamamlanmış emlak gelişim ve inşaat projelerini görüntüleyin.'
    except SEOSettings.DoesNotExist:
        page_title = 'İnşaat Projeleri | Devam Eden ve Tamamlananlar'
        meta_description = 'İnşaat projelerimizi keşfedin. Devam eden ve tamamlanmış emlak gelişim ve inşaat projelerini görüntüleyin.'
        seo_settings = None
    
    context = {
        'projects': projects,
        'selected_status': status,
        'page_title': page_title,
        'meta_description': meta_description,
        'seo_settings': seo_settings,
    }
    return render(request, 'properties/construction.html', context)


def about(request):
    """
    About page view
    """
    try:
        about_content = About.objects.first()
    except About.DoesNotExist:
        about_content = None
    
    # Get visible custom sections for about page with ordering
    custom_sections = CustomSection.objects.none()
    if about_content:
        custom_sections = CustomSection.objects.filter(
            visiblecustomsection__about=about_content,
            is_active=True
        ).order_by('visiblecustomsection__order')
    
    # Get SEO settings for about page
    try:
        seo_settings = SEOSettings.objects.get(page_type='about')
        page_title = seo_settings.meta_title or 'Hakkımızda'
        meta_description = seo_settings.meta_description or 'Emlak şirketimiz, misyonumuz ve ekibimiz hakkında daha fazla bilgi edinin.'
    except SEOSettings.DoesNotExist:
        page_title = 'Hakkımızda'
        meta_description = 'Emlak şirketimiz, misyonumuz ve ekibimiz hakkında daha fazla bilgi edinin.'
        seo_settings = None
    
    context = {
        'about': about_content,
        'custom_sections': custom_sections,
        'page_title': page_title,
        'meta_description': meta_description,
        'seo_settings': seo_settings,
    }
    return render(request, 'properties/about.html', context)


def contact(request):
    """
    Contact page with form submission
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the contact message
            contact_message = ContactMessage(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data.get('phone', ''),
                subject=form.cleaned_data.get('subject', ''),
                message=form.cleaned_data['message']
            )
            contact_message.save()
            
            # Send email notification to admin
            try:
                # Get admin emails and SMTP settings from SiteSettings
                site_settings = SiteSettings.objects.first()
                
                # Get email recipients from contact_email_recipients field
                recipient_emails = []
                if site_settings and site_settings.contact_email_recipients:
                    # Split by comma and clean whitespace
                    recipient_emails = [email.strip() for email in site_settings.contact_email_recipients.split(',') if email.strip()]
                
                # Fallback to regular email field if no recipients specified
                if not recipient_emails and site_settings and site_settings.email:
                    recipient_emails = [site_settings.email]
                
                # Check if SMTP settings are configured
                if recipient_emails and site_settings and site_settings.smtp_username and site_settings.smtp_password:
                    # Use custom SMTP settings from admin panel
                    from django.core.mail import EmailMessage
                    import smtplib
                    from email.mime.text import MIMEText
                    
                    subject = f"Yeni İletişim Mesajı: {form.cleaned_data.get('subject', 'Genel')}"
                    message_body = f"""
Yeni bir iletişim mesajı alındı:

Ad Soyad: {form.cleaned_data['name']}
E-posta: {form.cleaned_data['email']}
Telefon: {form.cleaned_data.get('phone', 'Belirtilmemiş')}
Konu: {form.cleaned_data.get('subject', 'Genel')}

Mesaj:
{form.cleaned_data['message']}

---
Bu mesaj web sitenizin iletişim formu üzerinden gönderilmiştir.
                    """
                    
                    try:
                        # Create email message
                        email = EmailMessage(
                            subject=subject,
                            body=message_body,
                            from_email=site_settings.email_from or site_settings.smtp_username,
                            to=recipient_emails,
                        )
                        
                        # Configure SMTP connection
                        smtp_host = site_settings.smtp_host or 'smtp.gmail.com'
                        smtp_port = site_settings.smtp_port or 587
                        
                        connection = smtplib.SMTP(smtp_host, smtp_port)
                        if site_settings.smtp_use_tls:
                            connection.starttls()
                        connection.login(site_settings.smtp_username, site_settings.smtp_password)
                        connection.send_message(email.message())
                        connection.quit()
                    except Exception as smtp_error:
                        print(f"SMTP Email gönderme hatası: {smtp_error}")
                        # Fallback to Django's default email backend
                        send_mail(
                            subject=subject,
                            message=message_body,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=recipient_emails,
                            fail_silently=True,
                        )
            except Exception as e:
                # Log error but don't show to user
                print(f"Email gönderme hatası: {e}")
            
            messages.success(request, 'Bizimle iletişime geçtiğiniz için teşekkür ederiz! En kısa sürede size dönüş yapacağız.')
            return redirect('contact')
    else:
        # Pre-fill form with query parameters if available
        initial_data = {}
        if 'name' in request.GET:
            initial_data['name'] = request.GET['name']
        if 'email' in request.GET:
            initial_data['email'] = request.GET['email']
        if 'phone' in request.GET:
            initial_data['phone'] = request.GET['phone']
        if 'message' in request.GET:
            initial_data['message'] = request.GET['message']
        
        form = ContactForm(initial_data)
    
    # Get company info from About model
    try:
        about_info = About.objects.first()
    except About.DoesNotExist:
        about_info = None
    
    # Get SEO settings for contact page
    try:
        seo_settings = SEOSettings.objects.get(page_type='contact')
        page_title = seo_settings.meta_title or 'İletişim | Bize Ulaşın'
        meta_description = seo_settings.meta_description or 'Gayrimenkullerimiz hakkında herhangi bir sorunuz için bize ulaşın. Hayalinizdeki evi bulmanıza yardımcı olmak için buradayız.'
    except SEOSettings.DoesNotExist:
        page_title = 'İletişim | Bize Ulaşın'
        meta_description = 'Gayrimenkullerimiz hakkında herhangi bir sorunuz için bize ulaşın. Hayalinizdeki evi bulmanıza yardımcı olmak için buradayız.'
        seo_settings = None
    
    context = {
        'form': form,
        'about_info': about_info,
        'page_title': page_title,
        'meta_description': meta_description,
        'seo_settings': seo_settings,
    }
    return render(request, 'properties/contact.html', context)


def robots_txt(request):
    """
    Serve robots.txt file
    """
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "# Sitemaps",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
        "",
        "# Disallow admin area",
        "Disallow: /admin/",
        "",
        "# Allow all other pages",
        "Allow: /",
        "Allow: /listings/",
        "Allow: /construction/",
        "Allow: /contact/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def references(request):
    """
    References page with gallery layout
    """
    references = Reference.objects.filter(is_active=True).prefetch_related('images', 'videos').order_by('order')
    
    # Get SEO settings for references page
    try:
        seo_settings = SEOSettings.objects.get(page_type='references')
        page_title = seo_settings.meta_title or 'Referanslar | Çalışmalarımız'
        meta_description = seo_settings.meta_description or 'Referanslarımız ve tamamladığımız projeler hakkında bilgi alın.'
    except SEOSettings.DoesNotExist:
        page_title = 'Referanslar | Çalışmalarımız'
        meta_description = 'Referanslarımız ve tamamladığımız projeler hakkında bilgi alın.'
        seo_settings = None
    
    context = {
        'references': references,
        'page_title': page_title,
        'meta_description': meta_description,
        'seo_settings': seo_settings,
    }
    return render(request, 'properties/references.html', context)


def test_404(request):
    """
    Test view for 404 error page
    """
    # This will raise a 404 error
    raise Http404("Test 404 error")

def test_500(request):
    """
    Test view for 500 error page
    """
    # This will raise a 500 error
    raise Exception("Test 500 error")

def custom_page_not_found(request, exception):
    """
    Custom 404 error handler
    """
    return render(request, 'errors/404.html', status=404)

def custom_server_error(request):
    """
    Custom 500 error handler
    """
    return render(request, 'errors/500.html', status=500)


@require_POST
def newsletter_subscribe(request):
    """
    AJAX endpoint for newsletter subscription
    """
    email = request.POST.get('email', '').strip()
    name = request.POST.get('name', '').strip()
    phone = request.POST.get('phone', '').strip()
    dont_show_again = request.POST.get('dont_show_again') == 'on'
    
    # Basic validation
    if not email or not name:
        return JsonResponse({
            'success': False,
            'message': 'Lütfen tüm zorunlu alanları doldurun.'
        }, status=400)
    
    # Validate email format
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({
            'success': False,
            'message': 'Geçerli bir e-posta adresi girin.'
        }, status=400)
    
    # Get IP address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    
    # Check if email already exists
    subscriber, created = NewsletterSubscriber.objects.get_or_create(
        email=email,
        defaults={
            'name': name,
            'phone': phone,
            'ip_address': ip_address,
            'is_active': True
        }
    )
    
    if not created:
        # Email exists - update info and reactivate if inactive
        if not subscriber.is_active:
            subscriber.is_active = True
            subscriber.name = name
            subscriber.phone = phone
            subscriber.unsubscribed_date = None
            subscriber.save()
            message = 'Bülten aboneliğiniz yeniden aktifleştirildi!'
        else:
            # Already active - update phone if provided
            if phone and phone != subscriber.phone:
                subscriber.phone = phone
                subscriber.save()
            message = 'Teşekkürler! Zaten bülten listemizdesiniz.'
    else:
        message = 'Bültenimize başarıyla abone oldunuz!'
    
    # Create response
    response = JsonResponse({
        'success': True,
        'message': message
    })
    
    # Always set cookie after successful interaction (subscriber won't see popup again)
    # Cookie expires in 365 days
    response.set_cookie(
        'newsletter_dismissed', 
        'true', 
        max_age=365*24*60*60,  # 365 days in seconds
        httponly=False,  # Allow JavaScript to read it
        samesite='Lax'
    )
    
    return response


def newsletter_unsubscribe(request, token):
    """
    Unsubscribe from newsletter using unique token
    """
    try:
        subscriber = NewsletterSubscriber.objects.get(unsubscribe_token=token)
        
        if request.method == 'POST':
            subscriber.is_active = False
            subscriber.unsubscribed_date = timezone.now()
            subscriber.save()
            
            messages.success(request, 'Bülten aboneliğinizden başarıyla çıktınız.')
            return redirect('home')
        
        context = {
            'subscriber': subscriber,
            'page_title': 'Bülten Aboneliğinden Çık',
        }
        return render(request, 'properties/newsletter_unsubscribe.html', context)
        
    except NewsletterSubscriber.DoesNotExist:
        messages.error(request, 'Geçersiz abonelik iptali bağlantısı.')
        return redirect('home')
