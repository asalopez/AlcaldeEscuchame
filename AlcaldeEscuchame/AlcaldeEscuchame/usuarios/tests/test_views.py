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


    def test_get_perfil(self):
        """Test para la vista del perfil del usuario logueado"""
        # Simula Ciudadano 1 registrado y logueado
        self.client.login(username="ciudadano1", password="ciudPass1")
        
        # Acceso al perfil del usuario logueado
        url = reverse('perfil')
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Perfil de usuario', 2)


    def test_get_perfil_invalido(self):
        """Test negativo para acceso a la vista del perfil del usuario mediante un usuario anónimo (no autenticado)"""       
        # Usuario NO autenticado intenta acceder a su perfil
        url = reverse('perfil')
        response = self.client.get(url)

        # Comprueba que la respuesta recibida sea un Redirect al login
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/login/?next=/perfil/')


    def test_get_editarPerfil(self):
        """Test para la vista de edición de perfil del usuario logueado"""
        # Simula Funcionario 1 registrado y logueado
        self.client.login(username="funcionario1", password="funcPass1")
        
        # Acceso al perfil del usuario logueado
        url = reverse('editarPerfil')
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Editar Perfil', 2)


    def test_get_editarPerfil_invalido(self):
        """Test negativo para acceso a la vista de edición de perfil del usuario mediante un usuario anónimo (no autenticado)"""       
        # Usuario NO autenticado intenta acceder a su perfil
        url = reverse('editarPerfil')
        response = self.client.get(url)

        # Comprueba que la respuesta recibida sea un Redirect al login
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/login/?next=/perfil/editar/')


    def test_get_editarClaves(self):
        """Test para la vista de edición de claves del usuario logueado"""
        # Simula Ciudadano 1 registrado y logueado
        self.client.login(username="ciudadano1", password="ciudPass1")
        
        # Acceso al perfil del usuario logueado
        url = reverse('cambioClaves')
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cambiar contraseña', 2)


    def test_get_editarClaves_invalido(self):
        """Test negativo para acceso a la vista de edición de claves del usuario mediante un usuario anónimo (no autenticado)"""       
        # Usuario NO autenticado intenta acceder a su perfil
        url = reverse('cambioClaves')
        response = self.client.get(url)

        # Comprueba que la respuesta recibida sea un Redirect al login
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/login/?next=/perfil/editarClaves/')


    def test_form_editarPerfil(self):
        """Test positivo para el formulario de edición de un usuario"""
        from usuarios.forms import EditarPerfilForm

        # Simula datos válidos para el formulario
        datos = {'email':'test@gmail.com', 'first_name':'test', 'last_name':'test', 'poblacion':'test', 'telefono':'987654321', 
                 'direccion':'test', 'foto':'https://farm5.staticflickr.com/4690/38460664095_ae0f647701_o.png'}
        form = EditarPerfilForm(datos)

        # Comprueba que el formulario es válido para esos datos
        self.assertTrue(form.is_valid())

    
    def test_form_editarPerfil_invalido(self):
        """Test negativo para el formulario de edición de un usuario"""
        from usuarios.forms import EditarPerfilForm

        # Simula datos válidos para el formulario
        datos = {'email':'test', 'first_name':'', 'last_name':'', 'poblacion':'test', 'telefono':'987654321', 
                 'direccion':'test', 'foto':''}
        form = EditarPerfilForm(datos)

        # Comprueba que el formulario es válido para esos datos
        self.assertTrue(not form.is_valid())
        self.assertEquals(form.errors['email'][0], 'Introduzca una dirección de correo electrónico válida.')
        self.assertEquals(form.errors['first_name'], ['Este campo es obligatorio.'])
        self.assertEquals(form.errors['last_name'], ['Este campo es obligatorio.'])
        

    def test_form_editarClaves(self):
        """Test positivo para el formulario de edición de claves un usuario"""
        from usuarios.forms import EditarClavesForm

        # Simula Ciudadano 1 registrado y logueado
        self.client.login(username="ciudadano1", password="ciudPass1")

        # Simula datos válidos para el formulario ; ID Usuario = 2 (Ciudadano 1)
        datos = {'idUsuario':2, 'actual_password':'ciudPass1', 'password':'ciudPass1_NEW', 'confirm_password':'ciudPass1_NEW'}
        form = EditarClavesForm(datos)

        # Comprueba que el formulario es válido para esos datos
        self.assertTrue(form.is_valid())

    
    def test_form_editarClaves_invalido1(self):
        """Test negativo para el formulario de edición de claves un usuario"""
        from usuarios.forms import EditarClavesForm

        # Simula datos válidos para el formulario
        datos = {'actual_password':'', 'password':'test_newPass', 'confirm_password':'test_newPass'}
        form = EditarClavesForm(datos)

        # Comprueba que el formulario es válido para esos datos
        self.assertTrue(not form.is_valid())
        self.assertEquals(form.errors['idUsuario'], ['Este campo es obligatorio.'])
        self.assertEquals(form.errors['actual_password'], ['Este campo es obligatorio.'])

    def test_form_editarClaves_invalido2(self):
        """Test negativo para el formulario de edición de claves un usuario"""
        from usuarios.forms import EditarClavesForm

        # Simula datos válidos para el formulario
        datos = {'idUsuario':1, 'actual_password':'test_actualPass', 'password':'test_newPass1', 'confirm_password':'test_newPass2'}
        form = EditarClavesForm(datos)

        # Comprueba que el formulario es válido para esos datos
        self.assertTrue(not form.is_valid())
        self.assertEquals(form.errors['__all__'][0], 'Por favor, introduzca correctamente su contraseña actual para realizar el cambio.')

