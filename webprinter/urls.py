from django.conf.urls import url
from django.contrib import admin
from app import views





urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^register$',views.client_create),
    url(r'^login',views.login),
    url(r'^upload',views.upload,name ='upload'),
    url(r'^manager',views.ManagerView.as_view(),name='manager_create'),
    url(r'^',views.homepage)
    
]
