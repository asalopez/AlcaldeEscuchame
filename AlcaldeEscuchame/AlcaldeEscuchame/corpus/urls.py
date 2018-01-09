"""
Definition of urls for Quejas.
"""
#encoding:utf-8

from datetime import datetime
from django.conf.urls import include
from corpus import views
from django.conf.urls import url
import django.contrib.auth.views

urlpatterns = [
    url(r'^(?P<queja_id>\d+)/agregar/$', views.agregarQuejaCorpus, name='agregarQuejaCorpus'),
]

    
    
