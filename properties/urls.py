from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('listings/', views.listings, name='listings'),
    path('listing/<slug:slug>/', views.listing_detail, name='listing_detail'),
    path('construction/', views.construction, name='construction'),
    # About page has been removed, content moved to homepage
    path('contact/', views.contact, name='contact'),
    path('references/', views.references, name='references'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    
    # Newsletter endpoints
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('newsletter/unsubscribe/<str:token>/', views.newsletter_unsubscribe, name='newsletter_unsubscribe'),
    
    # Test error pages
    path('test-404/', views.test_404, name='test_404'),
    path('test-500/', views.test_500, name='test_500'),
]