from .models import About, SiteSettings
from .models import Listing, Construction

def about_info(request):
    """
    Context processor to make about information available globally
    """
    try:
        about_content = About.objects.first()
    except About.DoesNotExist:
        about_content = None
    
    try:
        site_settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        site_settings = None
    
    # Get counts for listings and constructions
    listings_count = Listing.objects.filter(is_active=True).count()
    constructions_count = Construction.objects.filter(is_active=True).count()
    
    return {
        'about': about_content,
        'global_site_settings': site_settings,
        'listings_count': listings_count,
        'constructions_count': constructions_count
    }