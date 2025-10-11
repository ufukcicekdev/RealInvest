from .models import About

def about_info(request):
    """
    Context processor to make about information available globally
    """
    try:
        about_content = About.objects.first()
    except About.DoesNotExist:
        about_content = None
    
    return {
        'global_about_info': about_content
    }