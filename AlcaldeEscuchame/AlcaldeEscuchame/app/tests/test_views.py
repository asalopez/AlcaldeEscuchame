"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import django
from django.urls.base import reverse
from django.http.response import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.test import TestCase


# TODO: Configure your database in settings.py and sync before running tests.

class TestViews(TestCase):
    """Tests para toda la funcionalidad asociada con el Views de la aplicación."""

    if django.VERSION[:2] >= (1, 7):
        # Django >= 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super(TestViews, cls).setUpClass()
            django.setup()


    def test_get_paginaInicio(self):
        """Tests página de inicio"""
        response = self.client.get('/')

        # Comprueba que la respuesta HTTP sea correcta (200 code) y contenga 'Bienvenido' una vez.
        self.assertContains(response, 'Bienvenido', 1, 200)


    def test_get_registro(self):
        """Tests página de registro usuario anónimo"""
        response = self.client.get('/registro')

        # Comprueba que la respuesta HTTP sea correcta (200 code) y contenga 'Registro de ciudadano' dos veces.
        self.assertContains(response, 'Registro de ciudadano', 2, 200)


    def test_get_registro_invalido(self):
        """Test negativo para acceso a la página de registro mediante un usuario autenticado"""
        # Simula usuario registrado y logueado
        self.client.login(username="ciudadano1", password="ciudPass1")

        response = self.client.get('/registro')

        # Comprueba que la respuesta recibida sea un Redirect a la página principal
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)


    def test_form_registro(self):
        """Test positivo para la creación de un nuevo usuario ciudadano"""
        from app.forms import RegistroForm

        # Simula datos válidos para el registro
        datos = {'username':'test_user', 'email':'test@gmail.com', 'password':'top_secret', 'confirm_password':'top_secret',
                 'first_name':'test', 'last_name':'test', 'poblacion':'test', 'telefono':'987654321', 'direccion':'test', 
                 'foto':'https://farm5.staticflickr.com/4690/38460664095_ae0f647701_o.png'}
        form = RegistroForm(datos)

        # Comprueba validez del formulario
        self.assertTrue(form.is_valid())


    def test_post_registro_invalido(self):
        """Test negativo para la creación de un nuevo usuario ciudadano"""
        from app.forms import RegistroForm

        # Simula datos no válidos para el registro
        datos = {'username':'test_user', 'email':'test', 'password':'a', 'confirm_password':'top_secret',
                 'first_name':'', 'last_name':'', 'poblacion':'test', 'telefono':'987654321', 'direccion':'test', 
                 'foto':''}
        form = RegistroForm(datos)

        # Comprueba que el formulario contiene datos no validos
        self.assertTrue(not form.is_valid())
        self.assertEquals(form.errors['password'][0], 'Asegúrese de que este valor tenga al menos 5 caracteres (tiene 1).')
        self.assertEquals(form.errors['email'][0], 'Introduzca una dirección de correo electrónico válida.')
        self.assertEquals(form.errors['first_name'], ['Este campo es obligatorio.'])
        self.assertEquals(form.errors['last_name'], ['Este campo es obligatorio.'])

        
