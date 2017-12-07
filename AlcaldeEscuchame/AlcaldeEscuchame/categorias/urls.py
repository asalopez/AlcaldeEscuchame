from django.conf.urls import url
from . import views

# Definimos las rutas a las vistas de categoría
urlpatterns = [
    url(r'^$', views.index, name='index'), # Por defecto
]
