# from django.contrib import admin
# from django.urls import include, path
# from temple_app import views

# urlpatterns = [
#     path('', views.index, name='index'),
    
# ]

from django.contrib import admin
from django.urls import path
from django.contrib.sitemaps.views import sitemap

from temple_app import views
from temple_app.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', views.index, name='index'),

    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap',
    ),
]