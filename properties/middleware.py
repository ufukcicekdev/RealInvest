# Custom middleware for performance optimization

class PerformanceCacheMiddleware:
    """
    Middleware to add cache headers for static and media files
    Improves browser caching and reduces server load
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Set cache headers for static files
        if request.path.startswith('/static/') or '/static/' in request.path:
            # Cache static files for 1 year (immutable)
            response['Cache-Control'] = 'public, max-age=31536000, immutable'
            response['Expires'] = self._get_expires_date(365)
        
        # Set cache headers for media files  
        elif request.path.startswith('/media/') or '/media/' in request.path:
            # Cache media files for 1 year
            response['Cache-Control'] = 'public, max-age=31536000'
            response['Expires'] = self._get_expires_date(365)
        
        # Set cache headers for HTML pages
        elif request.path.endswith('.html') or not ('.' in request.path.split('/')[-1]):
            # Cache HTML pages for 1 hour, but revalidate
            response['Cache-Control'] = 'public, max-age=3600, must-revalidate'
            response['Expires'] = self._get_expires_date(0.04)  # ~1 hour
        
        return response
    
    def _get_expires_date(self, days):
        """Generate Expires header value"""
        from datetime import datetime, timedelta
        from email.utils import formatdate
        
        expires = datetime.utcnow() + timedelta(days=days)
        return formatdate(expires.timestamp(), usegmt=True)


class SecurityHeadersMiddleware:
    """
    Middleware to add security headers for better performance and security
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Add Permissions Policy for performance
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response
