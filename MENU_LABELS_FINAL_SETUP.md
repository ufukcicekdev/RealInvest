# Menu Labels - Final Setup Instructions

## What Was Fixed

The issue was that the menu visibility field labels in "Ana Sayfa Ayarları" → "Menü Görünürlüğü" were hardcoded in the model itself, not just the admin panel. 

### Changes Made:

1. **Model fields updated** ([models.py](file:///Users/mac/Desktop/emlakcı2/properties/models.py#L426-L429))
   - Removed hardcoded labels like "İlanlar Sayfasını Göster"
   - Now use generic "Sayfa Görünürlüğü" as base label

2. **Admin form enhanced** ([admin.py](file:///Users/mac/Desktop/emlakcı2/properties/admin.py#L365-L437))
   - Dynamically loads labels from NavigationSettings
   - Falls back to defaults if NavigationSettings doesn't exist
   - Updates both label and help_text for each field

## How To Complete Setup

### Step 1: Run Migrations

You **MUST** run migrations to create the NavigationSettings table:

```bash
# If you have a virtual environment, activate it first:
# source venv/bin/activate  (or your venv name)

python manage.py makemigrations properties
python manage.py migrate
```

### Step 2: Restart Django Server

After running migrations, restart your development server for changes to take effect.

### Step 3: Configure Menu Labels

1. Go to Django admin → **"Menü Etiketleri"**
2. Configure your custom labels (e.g., change "İlanlar" to "Gayrimenkul")
3. Click Save

### Step 4: Verify

1. Go to **"Ana Sayfa Ayarları"** in admin
2. Look at the **"Menü Görünürlüğü"** section
3. You should now see your custom labels!

For example, if you set:
- İlanlar → "Gayrimenkul"
- İnşaatlar → "Projeler"

You'll see:
- ✅ **Gayrimenkul** Sayfasını Göster
- ✅ **Projeler** Sayfasını Göster

## How It Works

```
┌─────────────────────────┐
│  Menü Etiketleri        │
│  (NavigationSettings)   │
│                         │
│  İlanlar → Gayrimenkul  │
│  İnşaatlar → Projeler   │
└───────────┬─────────────┘
            │
            ↓
┌─────────────────────────┐
│  Ana Sayfa Ayarları     │
│  Admin Form             │
│                         │
│  get_form() reads       │
│  NavigationSettings     │
│  and updates labels     │
└───────────┬─────────────┘
            │
            ↓
┌─────────────────────────┐
│  Menü Görünürlüğü       │
│                         │
│  ☑ Gayrimenkul          │
│    Sayfasını Göster     │
│  ☑ Projeler             │
│    Sayfasını Göster     │
└─────────────────────────┘
```

##Troubleshooting

### "Still showing old labels"
- Make sure you ran the migrations
- Restart Django server
- Clear browser cache
- Refresh the admin page

### "Menü Etiketleri not showing in admin"
- Check migrations were applied: `python manage.py showmigrations properties`
- Look for the NavigationSettings migration (should be checked)

### "Error when loading Ana Sayfa Ayarları"
- Check terminal/console for error messages
- The code has fallback to default labels if NavigationSettings doesn't exist

## Files Modified

1. `/properties/models.py` - Updated About model field labels
2. `/properties/admin.py` - Enhanced HomepageSettingsAdmin.get_form()
3. No other changes needed!

---

**Once migrations are run, the dynamic labels will work automatically!** 🎉
