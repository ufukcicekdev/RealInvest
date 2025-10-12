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
    path('test-dropdowns/', views.test_dropdowns, name='test_dropdowns'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]