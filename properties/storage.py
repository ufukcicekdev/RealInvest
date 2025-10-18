from storages.backends.s3boto3 import S3Boto3Storage
import os
import mimetypes

class DigitalOceanSpacesStorage(S3Boto3Storage):
    """
    Custom storage class for DigitalOcean Spaces
    """
    def __init__(self, **settings):
        # Set DigitalOcean Spaces specific settings
        settings['access_key'] = os.getenv('AWS_ACCESS_KEY_ID')
        settings['secret_key'] = os.getenv('AWS_SECRET_ACCESS_KEY')
        settings['bucket_name'] = os.getenv('AWS_STORAGE_BUCKET_NAME')
        settings['region_name'] = os.getenv('AWS_S3_REGION_NAME')
        settings['endpoint_url'] = os.getenv('AWS_S3_ENDPOINT_URL')
        settings['default_acl'] = 'public-read'
        settings['file_overwrite'] = False
        settings['object_parameters'] = {
            'CacheControl': 'max-age=86400',
        }
        super().__init__(**settings)
    
    def get_object_parameters(self, name):
        """Override to set proper Content-Type and Cache-Control for different file types"""
        params = self.object_parameters.copy()
        
        # Set longer cache times for static assets (1 year)
        # Images, fonts, CSS, JS should be cached for a long time
        static_extensions = ('.webp', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', 
                           '.woff', '.woff2', '.ttf', '.eot', '.otf',
                           '.css', '.js')
        
        if name.lower().endswith(static_extensions):
            # 1 year cache for static assets (Google's recommendation)
            params['CacheControl'] = 'public, max-age=31536000, immutable'
        else:
            # 1 day cache for other files (like HTML, dynamic content)
            params['CacheControl'] = 'public, max-age=86400'
        
        # Ensure correct MIME type for favicon files
        if name.endswith('.ico'):
            params['ContentType'] = 'image/x-icon'
        elif name.endswith('.png'):
            params['ContentType'] = 'image/png'
        elif name.endswith('.svg'):
            params['ContentType'] = 'image/svg+xml'
        elif name.endswith('.webp'):
            params['ContentType'] = 'image/webp'
        elif name.endswith('.css'):
            params['ContentType'] = 'text/css'
        elif name.endswith('.js'):
            params['ContentType'] = 'application/javascript'
        else:
            # Use mimetypes to guess for other files
            content_type, _ = mimetypes.guess_type(name)
            if content_type:
                params['ContentType'] = content_type
        
        return params