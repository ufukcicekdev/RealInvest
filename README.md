# 🏡 Real Estate Website - Django Project

A modern, responsive real estate website built with Django MVC architecture and Bootstrap 5. This full-featured platform allows real estate agencies to showcase property listings, construction projects, and manage customer inquiries.

## 🌟 Features

### Frontend Features
- **Modern & Responsive Design** - Clean UI optimized for mobile, tablet, and desktop
- **SEO Optimized** - Meta tags, Open Graph, Schema.org structured data, sitemap.xml, robots.txt
- **Property Listings** - Grid layout with search, filter, and pagination
- **Property Detail Pages** - Comprehensive property information with image galleries
- **Construction Projects** - Showcase ongoing and completed developments
- **Contact Form** - Customer inquiry system with email notifications
- **About Page** - Company information, mission, and vision

### Backend Features
- **Django Admin Panel** - Full CRUD operations for all models
- **Image Management** - Upload and manage property and construction images
- **Search & Filtering** - Advanced search by location, type, and status
- **SEO Management** - Dynamic meta tags and structured data
- **Contact Management** - Track and manage customer inquiries

## 📋 Tech Stack

- **Backend**: Django 5.2+
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite (development) - PostgreSQL ready for production
- **Image Processing**: Pillow
- **SEO**: Django Sitemaps, Meta tags, JSON-LD

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Step 1: Clone or Navigate to Project
```bash
cd /Users/mac/Desktop/emlakcı2
```

### Step 2: Activate Virtual Environment
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies (Already done)
```bash
pip install django pillow
```

### Step 4: Create Superuser
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### Step 5: Run Development Server
```bash
python manage.py runserver
```

The website will be available at: `http://127.0.0.1:8000/`
Admin panel: `http://127.0.0.1:8000/admin/`

## 📁 Project Structure

```
emlakcı2/
├── realestate_project/      # Main project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── properties/              # Main app
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── admin.py             # Admin configuration
│   ├── forms.py             # Form definitions
│   ├── urls.py              # App URL routing
│   └── sitemaps.py          # SEO sitemaps
├── templates/               # HTML templates
│   ├── base.html            # Base template with header/footer
│   └── properties/          # App-specific templates
│       ├── home.html        # Homepage
│       ├── listings.html    # Property listings
│       ├── listing_detail.html
│       ├── construction.html
│       ├── about.html
│       └── contact.html
├── static/                  # Static files
│   ├── css/
│   │   └── style.css        # Custom CSS
│   ├── js/
│   │   └── script.js        # Custom JavaScript
│   └── images/              # Static images
├── media/                   # User-uploaded files
│   ├── listings/            # Property images
│   └── construction/        # Construction images
└── manage.py                # Django management script
```

## 🎨 Models

### Listing
- Property information (title, description, price, location)
- Property details (bedrooms, bathrooms, area, floor, age)
- Images (main image + gallery)
- SEO fields (meta title, description, slug)
- Status (active, featured)

### Construction
- Project information (name, description, location)
- Timeline (start date, end date)
- Status (planning, ongoing, completed)
- Image gallery
- SEO fields

### ContactMessage
- User inquiries (name, email, phone, message)
- Tracking (read status, timestamp)

### About
- Company information (singleton model)
- Content (title, description, mission, vision)
- Contact details
- Social media links
- SEO fields

## 🔧 Admin Panel Usage

1. **Access Admin Panel**: Navigate to `http://127.0.0.1:8000/admin/`
2. **Login** with your superuser credentials
3. **Manage Listings**: Add, edit, or delete property listings
4. **Upload Images**: Add multiple images to each listing
5. **Manage Construction**: Add construction projects with galleries
6. **View Messages**: Check customer inquiries from the contact form
7. **Update About**: Edit company information and social links

### Adding a Property Listing
1. Go to Admin → Properties → Listings → Add Listing
2. Fill in all required fields (title, description, price, location)
3. Upload main image
4. Set property details (bedrooms, bathrooms, area)
5. Mark as "Active" and optionally "Featured"
6. Save and add additional images in the gallery

## 🎯 Key Features by Page

### Home Page
- Hero section with call-to-action
- Quick search bar
- Featured properties (6 cards)
- Recent listings (8 cards)
- Why Choose Us section

### Listings Page
- All property listings in grid layout
- Search by title/location
- Filter by property type and status
- Pagination (9 items per page)
- Responsive card design

### Listing Detail Page
- Full property information
- Image gallery
- Property features (icons)
- Contact agent form
- Related properties
- Social sharing buttons
- JSON-LD structured data

### Construction Page
- Gallery layout of projects
- Filter by status (planning/ongoing/completed)
- Modal popups with full project details
- Multiple images per project

### About Page
- Company introduction
- Mission and vision statements
- Why Choose Us features
- Contact information
- Social media links

### Contact Page
- Contact form (name, email, phone, subject, message)
- Company contact information
- Working hours
- Map placeholder (ready for Google Maps)
- FAQ accordion section

## 🔍 SEO Features

- **Dynamic Meta Tags**: Each page has unique title and description
- **Open Graph Tags**: Optimized for social media sharing
- **JSON-LD Structured Data**: Schema.org markup for search engines
- **Sitemap.xml**: Auto-generated sitemap at `/sitemap.xml`
- **Robots.txt**: Search engine directives at `/robots.txt`
- **Semantic HTML**: Proper heading structure and ARIA labels
- **Image Alt Tags**: All images have descriptive alt text
- **URL Structure**: Clean, SEO-friendly URLs with slugs

## 📱 Responsive Design

The website is fully responsive and tested on:
- Mobile devices (320px+)
- Tablets (768px+)
- Desktop (1024px+)
- Large screens (1920px+)

## 🎨 Customization

### Changing Colors
Edit `static/css/style.css` and modify the CSS variables:
```css
:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    /* ... other colors */
}
```

### Adding New Pages
1. Create view in `properties/views.py`
2. Add URL pattern in `properties/urls.py`
3. Create template in `templates/properties/`

### Modifying Templates
All templates extend `base.html` which includes header and footer. Edit individual page templates in `templates/properties/`.

## 🚀 Production Deployment

### Before Deploying
1. Update `settings.py`:
   - Set `DEBUG = False`
   - Add your domain to `ALLOWED_HOSTS`
   - Configure production database (PostgreSQL recommended)
   - Set up email backend for contact form notifications
   - Configure static files with WhiteNoise or CDN
   - Set secure `SECRET_KEY` from environment variable

2. Collect static files:
```bash
python manage.py collectstatic
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

### Recommended Production Stack
- **Web Server**: Nginx
- **WSGI Server**: Gunicorn
- **Database**: PostgreSQL
- **Cache**: Redis
- **Media Storage**: AWS S3 or similar
- **Hosting**: DigitalOcean, AWS, Heroku, or Railway

## 📝 Adding Content

### Initial Setup Steps
1. **Create Superuser** (if not done): `python manage.py createsuperuser`
2. **Access Admin Panel**: Login at `/admin/`
3. **Add About Page Content**: Properties → About Page → Add (only one instance allowed)
4. **Add Property Listings**: Properties → Listings → Add
5. **Add Construction Projects**: Properties → Construction Projects → Add
6. **Upload Images**: Use inline image forms when editing listings/projects

## 🔒 Security Features

- CSRF protection on all forms
- SQL injection prevention (Django ORM)
- XSS protection (Django template escaping)
- Secure password hashing
- Admin panel protection

## 🐛 Troubleshooting

### Images Not Showing
- Check `MEDIA_URL` and `MEDIA_ROOT` in settings.py
- Ensure media files are served in development (already configured)

### Admin Panel CSS Missing
- Run `python manage.py collectstatic`
- Check static files configuration

### 404 on Pages
- Verify URL patterns in `urls.py`
- Check template paths

## 📧 Contact Form Email Setup

To enable email notifications for contact form submissions, add to `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 🎯 Future Enhancements

- User authentication and saved favorites
- Property comparison feature
- Advanced search with price range and amenities
- Virtual tour integration
- Blog section for real estate news
- Testimonials/reviews
- Multi-language support
- Google Maps integration
- Email notifications for new listings
- PDF brochure generation

## 📄 License

This project is created for educational and commercial purposes.

## 👨‍💻 Support

For questions or issues, please refer to Django documentation:
- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)

---

**Built with ❤️ using Django & Bootstrap 5**
