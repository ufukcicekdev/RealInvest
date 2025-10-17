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
        """Override to set proper Content-Type for favicons"""
        params = self.object_parameters.copy()
        
        # Ensure correct MIME type for favicon files
        if name.endswith('.ico'):
            params['ContentType'] = 'image/x-icon'
        elif name.endswith('.png'):
            params['ContentType'] = 'image/png'
        elif name.endswith('.svg'):
            params['ContentType'] = 'image/svg+xml'
        else:
            # Use mimetypes to guess for other files
            content_type, _ = mimetypes.guess_type(name)
            if content_type:
                params['ContentType'] = content_type
        
        return params