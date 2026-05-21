from django.contrib import admin
from django.urls import include, path
from temple_app import views

urlpatterns = [
    path('', views.index, name='index'),
    
]