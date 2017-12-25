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
    #url(r'^(?P<queja_id>\d+)/$', views.detalleQueja, name='quejaDetalle'),
    #url(r'^(?P<queja_id>\d+)/editar$', views.listaQuejasPorCategoria, name='quejaEditar'),
    url(r'^buscador$', views.listaQuejasBuscador, name='quejasBuscador'),
    url(r'^ciudadano/$', views.listaQuejasPropias, name='quejasPropias'),
    url(r'^categoria/(?P<categoria_id>\d+)/$', views.listaQuejasPorCategoria, name='quejasCategoria'),
    #url(r'^edit/$', views.editarCategoria, name='editarCategoria'),

]

    
    
