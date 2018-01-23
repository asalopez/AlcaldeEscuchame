"""
Definition of urls for Categorias.
"""
#encoding:utf-8

from datetime import datetime
from categorias import views
from django.conf.urls import url
import django.contrib.auth.views

urlpatterns = [
    url(r'^$', views.listaCategorias, name='categorias'),
]

    
    
