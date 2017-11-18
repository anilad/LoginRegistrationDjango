from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^process$', views.process), 
    url(r'^success$', views.success), 
    url(r'^logout$', views.logout),
]