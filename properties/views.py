from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from .models import Listing, Construction, About, ContactMessage, SiteSettings, CustomSection, BannerImage
from .forms import ContactForm

# Create your views here.

def home(request):
    """
    Home page view displaying featured listings, hero section, and about info
    """
    featured_listings = Listing.objects.filter(is_active=True, is_featured=True)[:6]
    recent_listings = Listing.objects.filter(is_active=True)[:8]
    
    # Get about content for homepage
    try:
        about_content = About.objects.first()
        # Get visible custom sections if about_content exists
        if about_content:
            custom_sections = about_content.visible_custom_sections.filter(is_active=True).order_by('order')
            # Get banner images
            banner_images = about_content.banner_images.filter(is_active=True).order_by('order')
            # Debug: Print banner images count
            print(f"Banner images count: {banner_images.count()}")
            for banner in banner_images:
                print(f"Banner: {banner.image.url if banner.image else 'No image'}")
        else:
            custom_sections = CustomSection.objects.none()
            banner_images = BannerImage.objects.none()
            print("No about content found")
    except About.DoesNotExist:
        about_content = None
        custom_sections = CustomSection.objects.none()
        banner_images = BannerImage.objects.none()
        print("About.DoesNotExist exception")
    
    # Get site settings
    try:
        site_settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        site_settings = None
    
    # If no about_content exists, get all active custom sections
    if not about_content:
        custom_sections = CustomSection.objects.filter(is_active=True).order_by('order')
        banner_images = BannerImage.objects.filter(is_active=True).order_by('order')
    
    # Debug: Print banner images information
    print(f"Final banner images count: {banner_images.count()}")
    print(f"Banner images exists: {banner_images.exists()}")
    
    context = {
        'featured_listings': featured_listings,
        'recent_listings': recent_listings,
        'about': about_content,
        'site_settings': site_settings,
        'custom_sections': custom_sections,
        'banner_images': banner_images,
        'page_title': 'Modern Emlak | Hayalinizdeki Gayrimenkulü Bulun',
        'meta_description': 'Geniş emlak ilanlarımıza göz atın. Satılık veya kiralık daire, ev, villa ve ticari gayrimenkuller bulun.',
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
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'selected_type': property_type,
        'selected_status': status,
        'page_title': 'Gayrimenkul İlanları | Tüm Gayrimenkullere Göz Atın',
        'meta_description': 'Kapsamlı gayrimenkul ilanlarımıza göz atın. Satılık veya kiralık daire, ev, villa ve ticari gayrimenkuller bulun.',
    }
    return render(request, 'properties/listings.html', context)


def listing_detail(request, slug):
    """
    Individual listing detail page
    """
    listing = get_object_or_404(Listing, slug=slug, is_active=True)
    related_listings = Listing.objects.filter(
        is_active=True,
        location=listing.location
    ).exclude(id=listing.id)[:3]
    
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
    
    context = {
        'projects': projects,
        'selected_status': status,
        'page_title': 'İnşaat Projeleri | Devam Eden ve Tamamlananlar',
        'meta_description': 'İnşaat projelerimizi keşfedin. Devam eden ve tamamlanmış emlak gelişim ve inşaat projelerini görüntüleyin.',
    }
    return render(request, 'properties/construction.html', context)


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
    
    # Get company info from SiteSettings model
    try:
        site_settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        site_settings = None
    
    context = {
        'form': form,
        'about_info': site_settings,
        'page_title': 'İletişim | Bize Ulaşın',
        'meta_description': 'Gayrimenkullerimiz hakkında herhangi bir sorunuz için bize ulaşın. Hayalinizdeki evi bulmanıza yardımcı olmak için buradayız.',
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


def test_dropdowns(request):
    """Test view for dropdown styling"""
    return render(request, 'test_dropdowns.html')
