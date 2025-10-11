# 🚀 Production Deployment Guide

## Pre-Deployment Checklist

### 1. Environment Variables
Create a `.env` file (do not commit this to git):

```env
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 2. Update settings.py

```python
import os
from pathlib import Path

# Secret key from environment
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')

# Debug mode
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Allowed hosts
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'realestate_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# Security settings
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 3. Install Production Dependencies

```bash
pip install gunicorn psycopg2-binary python-decouple whitenoise
pip freeze > requirements.txt
```

### 4. Configure Static Files (WhiteNoise)

Add to `settings.py`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## Deployment Options

### Option 1: Deploy to Railway

1. Install Railway CLI:
```bash
npm i -g @railway/cli
```

2. Login to Railway:
```bash
railway login
```

3. Initialize project:
```bash
railway init
```

4. Add PostgreSQL:
```bash
railway add
# Select PostgreSQL
```

5. Deploy:
```bash
railway up
```

6. Set environment variables in Railway dashboard

### Option 2: Deploy to DigitalOcean

1. Create a Droplet (Ubuntu 22.04)

2. SSH into your server:
```bash
ssh root@your-server-ip
```

3. Update system:
```bash
apt update && apt upgrade -y
```

4. Install dependencies:
```bash
apt install python3-pip python3-venv nginx postgresql postgresql-contrib
```

5. Create database:
```bash
sudo -u postgres psql
CREATE DATABASE realestate_db;
CREATE USER realestate_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE realestate_db TO realestate_user;
\q
```

6. Clone your repository:
```bash
git clone your-repository-url
cd your-project
```

7. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

8. Run migrations:
```bash
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

9. Configure Gunicorn:
Create `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=gunicorn daemon for realestate
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/your-project
ExecStart=/root/your-project/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/root/your-project/realestate.sock \
          realestate_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

10. Start Gunicorn:
```bash
systemctl start gunicorn
systemctl enable gunicorn
```

11. Configure Nginx:
Create `/etc/nginx/sites-available/realestate`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /root/your-project;
    }
    
    location /media/ {
        root /root/your-project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/root/your-project/realestate.sock;
    }
}
```

12. Enable site:
```bash
ln -s /etc/nginx/sites-available/realestate /etc/nginx/sites-enabled
nginx -t
systemctl restart nginx
```

13. Setup SSL with Let's Encrypt:
```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d your-domain.com -d www.your-domain.com
```

### Option 3: Deploy to Heroku

1. Install Heroku CLI:
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. Login:
```bash
heroku login
```

3. Create Procfile:
```
web: gunicorn realestate_project.wsgi --log-file -
```

4. Create runtime.txt:
```
python-3.11.0
```

5. Create app:
```bash
heroku create your-app-name
```

6. Add PostgreSQL:
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

7. Set environment variables:
```bash
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
```

8. Deploy:
```bash
git push heroku main
```

9. Run migrations:
```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

---

## Post-Deployment

### 1. Test Everything
- [ ] Homepage loads correctly
- [ ] All pages are accessible
- [ ] Images load properly
- [ ] Forms work
- [ ] Admin panel accessible
- [ ] SSL certificate active
- [ ] Mobile responsive

### 2. Setup Monitoring
- Use services like:
  - Sentry (error tracking)
  - Google Analytics (traffic)
  - Uptime Robot (uptime monitoring)

### 3. Backup Strategy
- Database backups (daily)
- Media files backups (weekly)
- Code repository (GitHub/GitLab)

### 4. Performance Optimization
- Enable caching (Redis/Memcached)
- Use CDN for static files
- Optimize images
- Enable gzip compression

---

## Maintenance

### Regular Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
systemctl restart gunicorn
systemctl restart nginx
```

### Database Backup
```bash
# Backup
pg_dump realestate_db > backup_$(date +%Y%m%d).sql

# Restore
psql realestate_db < backup_20231015.sql
```

---

## Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic --clear
systemctl restart nginx
```

### 502 Bad Gateway
```bash
systemctl status gunicorn
journalctl -u gunicorn
systemctl restart gunicorn
```

### Database connection issues
- Check DATABASE_URL environment variable
- Verify PostgreSQL is running
- Check database credentials

---

## Security Best Practices

1. **Never commit sensitive data** (.env, secret keys)
2. **Use strong passwords** for database and admin
3. **Keep Django updated** to latest stable version
4. **Enable HTTPS only** in production
5. **Regular backups** of database and media
6. **Monitor logs** for suspicious activity
7. **Use firewall** to restrict access
8. **Disable DEBUG** in production
9. **Set ALLOWED_HOSTS** correctly
10. **Use environment variables** for secrets

---

## Cost Estimates

### Railway/Heroku
- Starter: $5-10/month
- Hobby: $15-25/month
- Production: $50-100/month

### DigitalOcean
- Basic Droplet: $6/month
- 2GB RAM: $12/month
- 4GB RAM: $24/month
- + Database: $15/month

### AWS/GCP
- Variable based on usage
- Typically $20-100/month for small site

---

## Support Resources

- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- Gunicorn: https://gunicorn.org/
- Nginx: https://nginx.org/en/docs/
- PostgreSQL: https://www.postgresql.org/docs/

---

**Good luck with your deployment! 🚀**
