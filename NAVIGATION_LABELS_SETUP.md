# Navigation Labels Setup Guide

## Overview
You can now customize the navigation menu labels (like "İlanlar", "İletişim", etc.) through the Django admin panel. When you change these labels, they will automatically update in both:
1. The header navigation menu
2. The "Menü Görünürlüğü" (Menu Visibility) section in homepage settings

## Setup Steps

### 1. Create and Apply Database Migration

First, you need to create the database migration for the new `NavigationSettings` model:

```bash
# Activate your virtual environment first (if you have one)
# Then run:
python manage.py makemigrations properties
python manage.py migrate
```

### 2. Access Navigation Labels in Admin

After running the migration:

1. Go to your Django admin panel: `http://your-domain/admin/`
2. Look for **"Menü Etiketleri"** (Navigation Labels) in the sidebar under "Properties" section
3. Click on it to configure the labels

### 3. Configure Menu Labels

You'll see fields for:
- **Ana Sayfa Menü Etiketi** (Home menu label) - Default: "Ana Sayfa"
- **İlanlar Menü Etiketi** (Listings menu label) - Default: "İlanlar"
- **İnşaatlar Menü Etiketi** (Construction menu label) - Default: "İnşaatlar"
- **Referanslar Menü Etiketi** (References menu label) - Default: "Referanslar"
- **İletişim Menü Etiketi** (Contact menu label) - Default: "İletişim"

### 4. Example Usage

For example, if you want to change "İlanlar" to "Gayrimenkul":

1. Go to **Menü Etiketleri** in admin
2. Change **İlanlar Menü Etiketi** field to "Gayrimenkul"
3. Click **Save**

Now:
- The header menu will show "Gayrimenkul" instead of "İlanlar"
- In **Ana Sayfa Ayarları** → **Menü Görünürlüğü**, you'll see "Gayrimenkul Sayfasını Göster" instead of "İlanlar Sayfasını Göster"

## How It Works

### In the Header Navigation
The template uses:
```django
{{ nav_settings.listings_label|default:"İlanlar" }}
```

This means:
- If you've set a custom label, it will use that
- If not set, it falls back to the default "İlanlar"

### In Homepage Settings
The admin panel dynamically updates the field labels based on your navigation settings, so you always see the current menu label you've configured.

## Files Modified

1. **properties/models.py** - Added `NavigationSettings` model
2. **properties/admin.py** - Added admin for `NavigationSettings` and updated `About` admin
3. **properties/context_processors.py** - Added `nav_settings` to context
4. **templates/base.html** - Updated navigation menu to use dynamic labels

## Troubleshooting

### Labels not updating?
- Make sure you've run the migrations
- Clear your browser cache
- Restart your Django development server

### Can't see "Menü Etiketleri" in admin?
- Check that migrations have been applied
- Verify the model is imported in admin.py

### Labels showing as default in "Menü Görünürlüğü"?
- Refresh the admin page after saving navigation labels
- The labels update when you load the homepage settings page

## Benefits

✅ **No code changes needed** - All labels managed through admin panel
✅ **Consistent labeling** - Same label used everywhere (header & settings)
✅ **Multi-language ready** - Easy to change labels for different languages
✅ **User-friendly** - Non-technical users can manage menu labels
