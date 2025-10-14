#!/usr/bin/env python
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realestate_project.settings')
django.setup()

from properties.models import PopupSettings

def create_popup_settings():
    """
    Create or update popup settings with default values
    """
    popup_settings = PopupSettings.get_settings()
    
    # Update with Turkish content
    popup_settings.enabled = True
    popup_settings.title = "Bültenimize Abone Olun!"
    popup_settings.description = "En son emlak fırsatları, yeni projeler ve özel tekliflerden haberdar olmak için e-posta listemize katılın."
    popup_settings.delay_seconds = 3
    popup_settings.show_on_mobile = True
    popup_settings.button_text = "Abone Ol"
    popup_settings.button_color = "#007bff"
    
    popup_settings.save()
    
    print("✓ Popup settings created/updated successfully!")
    print(f"  - Title: {popup_settings.title}")
    print(f"  - Enabled: {popup_settings.enabled}")
    print(f"  - Delay: {popup_settings.delay_seconds} seconds")
    print(f"  - Show on mobile: {popup_settings.show_on_mobile}")

if __name__ == "__main__":
    create_popup_settings()
