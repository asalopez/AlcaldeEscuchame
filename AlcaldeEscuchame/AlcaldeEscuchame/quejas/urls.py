"""
Definition of urls for Quejas.
"""
#encoding:utf-8

from datetime import datetime
from quejas import views
from django.conf.urls import url
import django.contrib.auth.views

urlpatterns = [
    url(r'^$', views.listaQuejas, name='quejas'),
    #url(r'^edit/$', views.editarCategoria, name='editarCategoria'),

]

    
    
