from .models import About, SiteSettings, PopupSettings
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
    
    try:
        popup_settings = PopupSettings.get_settings()
    except:
        popup_settings = None
    
    # Get counts for listings and constructions
    listings_count = Listing.objects.filter(is_active=True).count()
    constructions_count = Construction.objects.filter(is_active=True).count()
    
    # Get template class for body
    template_class = ''
    if about_content and about_content.homepage_template:
        template_class = f"{about_content.homepage_template}-active"
    else:
        template_class = 'template1-active'  # Default template
    return {
        'about': about_content,
        'global_site_settings': site_settings,
        'popup_settings': popup_settings,
        'listings_count': listings_count,
        'constructions_count': constructions_count,
        'template_class': template_class,  # Add template class globally
    }