"""
Definition of urls for AlcaldeEscuchame.
"""
#encoding:utf-8

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views
from usuarios import views as usuarios_views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Default: bienvenida, contacto, inicio/cierre sesión
    url(r'^$', app.views.home, name='home'),
    url(r'^contacto$', app.views.contact, name='contacto'),
    url(r'^about', app.views.about, name='about'),
    url(r'^login/$', django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Inicio de sesión',
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

     # Editar Perfil
     url(r'^perfil$', usuarios_views.perfil, name='perfil'),

]
