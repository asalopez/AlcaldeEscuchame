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


    def test_get_listaComentarios(self):
        """Tests listado de comentarios"""

        # Simula Ciudadano 1 registrado y logueado
        self.client.login(username="ciudadano1", password="ciudPass1")
        
        # Queja_Id = 1 ; Queja con comentarios
        url = reverse('quejaDetalle', kwargs={'queja_id': 1})
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Comentarios', 3)


    def test_get_listaComentarios_invalida(self):
        """Test negativo para acceso al listado de comentarios mediante un usuario anónimo (no autenticado)"""
       
        # Queja_Id = 1 ; Queja con comentarios
        url = reverse('quejaDetalle', kwargs={'queja_id': 1})
        response = self.client.get(url)

        # Comprueba que la respuesta recibida sea un Redirect al login
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/login/?next=/quejas/1/')


    def test_form_nuevoComentario(self):
        """Test positivo para la creación de un nuevo comentario asociado a una queja"""
        from comentarios.forms import NuevoComentarioForm

        # Simula datos válidos para el formulario ; Queja_Id = 2
        datos = {'titulo': 'Test', 'cuerpo':'Test', 'queja':2}
        form = NuevoComentarioForm(datos)

        # Comprueba que el formulario es válido para esos datos
        self.assertTrue(form.is_valid())


    def test_form_nuevoComentario_invalido(self):
        """Test negativo para la creación de un nuevo comentario asociado a una queja"""
        from comentarios.forms import NuevoComentarioForm

        # Simula datos no válidos para el formulario: titulo vacío y sin queja asociada
        datos = {'titulo': '', 'cuerpo':'Test'}
        form = NuevoComentarioForm(datos)

        # Comprueba que el formulario no es válido para esos datos
        self.assertTrue(not form.is_valid())
        self.assertEquals(form.errors['titulo'], ['Este campo es obligatorio.'])
        self.assertEquals(form.errors['queja'], ['Este campo es obligatorio.'])