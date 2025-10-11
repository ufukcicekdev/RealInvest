from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Listing, Construction


class ListingSitemap(Sitemap):
    """
    Sitemap for property listings
    """
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Listing.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_date


class ConstructionSitemap(Sitemap):
    """
    Sitemap for construction projects
    """
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Construction.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_date


class StaticViewSitemap(Sitemap):
    """
    Sitemap for static pages
    """
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['home', 'listings', 'construction', 'about', 'contact']

    def location(self, item):
        return reverse(item)
