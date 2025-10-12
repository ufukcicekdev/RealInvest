from .models import About, SiteSettings

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
    
    return {
        'about': about_content,
        'global_site_settings': site_settings
    }