"""
Definition of urls for Usuarios.
"""
#encoding:utf-8

from datetime import datetime
from usuarios import views
from django.conf.urls import url
import django.contrib.auth.views

urlpatterns = [
    url(r'^$', views.perfil, name='perfil'),
    url(r'^editar/$', views.editarPerfil, name='editarPerfil'),

]

    
    
