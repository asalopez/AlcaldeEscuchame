"""
Definition of urls for Comentarios.
"""
#encoding:utf-8

from datetime import datetime
from django.conf.urls import include
from comentarios import views
from django.conf.urls import url
import django.contrib.auth.views

urlpatterns = [
    url(r'^nuevo/$', views.nuevoComentario, name='nuevoComentario')
]
