# 📁 Static Files Deployment Guide

## Issue Description
When DEBUG=False in production, Django doesn't serve static files automatically, causing 403 Forbidden errors.

## Solution Implemented

### 1. Static Files Configuration in settings.py

The settings.py file has been configured to handle static files differently for development and production:

#### Development (DEBUG=True):
```python
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
```

#### Production (DEBUG=False):
```python
# AWS S3/DigitalOcean Spaces configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')

# Static files served from S3
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/static/'

# Media files served from S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/media/'
```

### 2. Railway Deployment Configuration

#### Procfile:
```
web: python manage.py collectstatic --noinput && python manage.py migrate && gunicorn realestate_project.wsgi:application --bind 0.0.0.0:$PORT
```

#### railway.json:
```json
{
  "deploy": {
    "startCommand": "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn realestate_project.wsgi:application --bind 0.0.0.0:$PORT"
  }
}
```

### 3. WhiteNoise Integration

WhiteNoise is configured for production to serve static files efficiently:
```python
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
```

## Deployment Steps

### 1. Environment Variables Required
Set these in your Railway dashboard:
```env
DEBUG=False
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=your-region
AWS_S3_ENDPOINT_URL=https://your-region.digitaloceanspaces.com
```

### 2. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 3. Verify Configuration
```bash
python manage.py prepare_static_files --check
```

## Troubleshooting

### Common Issues:

1. **403 Forbidden Errors**: 
   - Ensure DEBUG=False in production
   - Verify AWS credentials are correct
   - Check that the S3 bucket has public read permissions

2. **Static Files Not Found**:
   - Run `collectstatic` command
   - Verify STATIC_ROOT directory exists
   - Check file permissions on static files

3. **CSS/JS Not Loading**:
   - Clear browser cache
   - Check browser developer tools for specific file errors
   - Verify CDN configuration if using one

## Management Commands

### Custom Static Files Command:
```bash
# Check static files configuration
python manage.py prepare_static_files --check

# Collect static files
python manage.py prepare_static_files --collect

# Both operations
python manage.py prepare_static_files --check --collect
```

## Best Practices

1. Always run `collectstatic` before deploying to production
2. Use version control to track static file changes
3. Implement proper caching headers for static assets
4. Monitor static file access logs for 404 errors
5. Regularly audit static file sizes and optimize when needed

This configuration ensures that static files are properly served in both development and production environments without 403 errors.