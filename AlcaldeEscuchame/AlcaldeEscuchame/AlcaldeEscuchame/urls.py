"""
Definition of urls for AlcaldeEscuchame.
"""
#encoding:utf-8

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Default: bienvenida, contacto, inicio/cierre sesión
    url(r'^$', app.views.home, name='home'),
    url(r'^login/$', django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.LoginForm,
            'extra_context':
            {
                'titulo': 'Inicio de sesión',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$', django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^registro$', app.views.registro, name='registro'),

    # Administrador:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
     url(r'^admin/', include(admin.site.urls)),

     # Categorias
     url(r'^categorias/', include('categorias.urls')),

     # Quejas
     url(r'^quejas/', include('quejas.urls')),

     # Comentarios
     url(r'^comentarios/', include('comentarios.urls')),

     # Corpus
     url(r'^corpus/', include('corpus.urls')),

     # Perfil de usuario
     url(r'^perfil/', include('usuarios.urls')),
]
