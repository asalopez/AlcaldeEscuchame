"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import django
from django.apps import AppConfig
from django.urls.base import reverse
from django.http.response import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.test import TestCase

# TODO: Configure your database in settings.py and sync before running tests.

class TestViews(TestCase):
    """Tests para toda la funcionalidad asociada con el controlador de la aplicación."""

    if django.VERSION[:2] >= (1, 7):
        # Django >= 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super(TestViews, cls).setUpClass()
            django.setup()


    def test_get_listaCategorias(self):
        """Tests listado de categorías"""
        # Simula Ciudadano 1 registrado y logueado
        self.client.login(username="ciudadano1", password="ciudPass1")
        
        url = reverse('categorias')
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Categorías', 3)


    def test_get_listaCategorias_invalida(self):
        """Test negativo para acceso al listado de categorías mediante un usuario anónimo (no autenticado)"""       
        # Usuario NO autenticado intenta acceder a las categorías
        url = reverse('categorias')
        response = self.client.get(url)

        # Comprueba que la respuesta recibida sea un Redirect al login
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/login/?next=/categorias/')

        

