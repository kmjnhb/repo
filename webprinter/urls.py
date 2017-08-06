from django.conf.urls import url
from django.contrib import admin
from app import views
from app import manager_crud_view



urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^register$',views.client_create),
    url(r'^login',views.login),
    url(r'^upload',views.upload,name ='upload'),

    url(r'^franchise/managers/create',manager_crud_view.CreateManager.as_view(),name='manager_create'),
    url(r'^franchise/managers/(?P<pk>[\w.@+-]+)/edit/$', manager_crud_view.UpdateManager.as_view()),
    url(r'^franchise/managers/(?P<pk>[\w.@+-]+)/delete/$', manager_crud_view.DeleteManager.as_view()),
    url(r'^franchise/managers/',manager_crud_view.manager_list)
   # url(r'^',views.homepage)
    
]
