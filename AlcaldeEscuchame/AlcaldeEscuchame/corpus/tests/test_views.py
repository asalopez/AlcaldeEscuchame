"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import django
from django.http.response import HttpResponseForbidden
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


    def test_get_detalleModeloCorpus(self):
        """Tests acceso al detalle del Corpus"""
        from django.contrib.auth.models import User

        # Simula login del administrador
        user = User.objects.get(username = 'alvarosl')
        self.client.user = user
        self.client._login(self.client.user)
        
        # URL a la vista de detalle
        url = reverse('verModeloCorpus')
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Modelo del sistema', 2)


    def test_get_detalleModeloCorpus_invalido(self):
        """Test negativo para acceso al detalle del Corpus mediante un usuario anónimo (no autenticado)"""
       
        # URL a la vista de detalle
        url = reverse('verModeloCorpus')
        response = self.client.get(url)

        # Comprueba que la respuesta recibida sea un Redirect al login
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/login/?next=/corpus/modelo/')


    def test_get_agregaQuejaAlCorpus(self):
        """Test positivo para comprobar que un admin puede agregar una queja al Corpus del sistema"""
        from django.contrib.auth.models import User

        # Simula login del administrador
        user = User.objects.get(username = 'alvarosl')
        self.client.user = user
        self.client._login(self.client.user)

        # Queja Id = 5 ; es una ueja agregable (es decir, no pertenece al corpus)
        url = reverse('agregarQuejaCorpus', kwargs={'queja_id': 5})
        response = self.client.get(url)

        # Comprueba que la respuesta recibida es un Redirect al lista de Entradas (quejas) del Corpus
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/admin/corpus/entradacorpus/')


    def test_get_agregaQuejaAlCorpus_invalido1(self):
        """Test negativo para comprobar que un usuario que no es Admin no puede agregar una queja al Corpus del sistema"""
        # Simula login de ciudadano
        self.client.login(username="ciudadano1", password="ciudPass1")

        # Queja Id = 5 ; es una queja agregable (es decir, no pertenece al corpus)
        url = reverse('agregarQuejaCorpus', kwargs={'queja_id': 5})
        response = self.client.get(url)

        # Comprueba que la respuesta recibida es un Redirect al lista de Entradas (quejas) del Corpus
        self.assertTrue(isinstance(response, HttpResponseForbidden))


    def test_get_agregaQuejaAlCorpus_invalido2(self):
        """Test negativo para comprobar que no puede agregarse al Corpus una queja que ya ha sido agregada"""
        from django.contrib.auth.models import User

        # Simula login del administrador
        user = User.objects.get(username = 'alvarosl')
        self.client.user = user
        self.client._login(self.client.user)

        # Queja Id = 4 ; es una queja ya agregada
        url = reverse('agregarQuejaCorpus', kwargs={'queja_id': 4})
        response = self.client.get(url)

        # Comprueba que la respuesta recibida es un Redirect al lista de Entradas (quejas) del Corpus
        self.assertTrue(isinstance(response, HttpResponseForbidden))

    
    def test_get_descargaModeloCorpus(self):
        """Test que comprueba que el Modelo del sistema solo puede ser descargado por administradores"""
        from django.contrib.auth.models import User

        # Simula login del administrador
        user = User.objects.get(username = 'alvarosl')
        self.client.user = user
        self.client._login(self.client.user)

        # URL a la descarga del corpus
        url = reverse('descargaModelo')
        response = self.client.get(url)

        # Comprueba que la respuesta recibida 200 OK
        self.assertEqual(response.status_code, 200)


    def test_get_descargaModeloCorpus_invalido(self):
        """Test que comprueba que el Modelo del sistema no puede ser descargado por usuarios anónimos"""
        # URL a la descarga del corpus
        url = reverse('descargaModelo')
        response = self.client.get(url)

        # Comprueba que la respuesta recibida es un Redirect al lista de Entradas (quejas) del Corpus
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/login/?next=/corpus/descargaModelo/')


    def test_get_reconstruyeModeloCorpus(self):
        """Test que comprueba que el Modelo del sistema solo puede ser construido/reconstruido por administradores"""
        from django.contrib.auth.models import User

        # Simula login del administrador
        user = User.objects.get(username = 'alvarosl')
        self.client.user = user
        self.client._login(self.client.user)

        # URL a la descarga del corpus
        url = reverse('reconstruyeModelo')
        response = self.client.get(url)

        # Comprueba que la respuesta recibida es un Redirect al detalle del Modelo
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/corpus/modelo/')


    def test_get_reconstruyeModeloCorpus_invalido(self):
        """Test que comprueba que el Modelo del sistema no puede ser construido/reconstruido por funcionarios"""
        # Simula login de funcionario
        self.client.login(username="funcionario1", password="funcPass1")

        # URL a la descarga del corpus
        url = reverse('reconstruyeModelo')
        response = self.client.get(url)

        # Comprueba que la respuesta recibida es un Forbidden
        self.assertTrue(isinstance(response, HttpResponseForbidden))
       
