"""
Definition of urls for Quejas.
"""
#encoding:utf-8

from datetime import datetime
from django.conf.urls import include
from quejas import views
from django.conf.urls import url
import django.contrib.auth.views

urlpatterns = [
    url(r'^$', views.listaQuejas, name='quejas'),
    url(r'^(?P<queja_id>\d+)/$', views.detalleQueja, name='quejaDetalle'),
    url(r'^nueva/', views.formularioQueja, name='nuevaQueja'),
    url(r'^(?P<queja_id>\d+)/editar$', views.formularioQueja, name='editarQueja'),
    url(r'^(?P<queja_id>\d+)/eliminar$', views.eliminarQueja, name='eliminarQueja'),
    url(r'^(?P<queja_id>\d+)/tramitar', views.tramitarQueja, name='tramitarQueja'),
    url(r'^valorar$', views.valorarQueja, name='valorarQueja'),
    url(r'^buscador$', views.listaQuejasBuscador, name='quejasBuscador'),
    url(r'^ciudadano/$', views.listaQuejasPropias, name='quejasPropias'),
    url(r'^funcionario/$', views.listaQuejasTramitables, name='quejasTramitables'),
    url(r'^categoria/(?P<categoria_id>\d+)/$', views.listaQuejasPorCategoria, name='quejasCategoria')
]

    
    
