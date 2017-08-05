"""webprinter URL Configuration


"""
from django.conf.urls import url
from django.contrib import admin
from app import views

urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^register$',views.client_register),
    url(r'^login',views.login),
    url(r'^manager',views.manager_register),
    url(r'^upload',views.upload),
    url(r'^',views.homepage)
    
]
