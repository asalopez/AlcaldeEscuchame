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


    def test_get_listaQuejas(self):
        """Test para el listado de quejas"""
        # Simula Ciudadano 1 registrado y logueado
        self.client.login(username="ciudadano1", password="ciudPass1")
        
        # Acceso al listado de quejas
        url = reverse('quejas')
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Últimas Quejas', 3)


    def test_get_listaQuejas_invalido(self):
        """Test negativo para acceso al listado de quejas mediante un usuario anónimo (no autenticado)"""       
        # Usuario NO autenticado intenta acceder al listado
        url = reverse('quejas')
        response = self.client.get(url)

        # Comprueba que la respuesta recibida sea un Redirect al login
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/login/?next=/quejas/')


    def test_get_listaQuejasPorCategoria(self):
        """Test para el listado de quejas por categoría"""
        # Simula Ciudadano 1 registrado y logueado
        self.client.login(username="ciudadano1", password="ciudPass1")
        
        # Acceso al listado de quejas asociadas a la categoría de Id 1
        url = reverse('quejasCategoria',  kwargs={'categoria_id': 1})
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Listado de quejas', 2)


    def test_get_listaQuejasPorCategoria_invalido(self):
        """Test negativo para acceso al listado de quejas por categoría mediante un usuario anónimo (no autenticado)"""       
        # Usuario NO autenticado intenta acceder al listado de quejas asociadas a la categoría de Id 1
        url = reverse('quejasCategoria',  kwargs={'categoria_id': 1})
        response = self.client.get(url)

        # Comprueba que la respuesta recibida sea un Redirect al login
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/login/?next=/quejas/categoria/1/')


    def test_get_listaQuejasPropias(self):
        """Test para el listado de quejas propias del ciudadano logueado"""
        # Simula Ciudadano 1 registrado y logueado
        self.client.login(username="ciudadano1", password="ciudPass1")
        
        # Acceso al listado de quejas propias
        url = reverse('quejasPropias')
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Listado de quejas', 2)


    def test_get_listaQuejasPropias_invalido1(self):
        """Test negativo para acceso al listado de quejas por categoría mediante un usuario anónimo (no autenticado)"""       
        # Usuario NO autenticado intenta acceder al listado de quejas propias
        url = reverse('quejasPropias')
        response = self.client.get(url)

        # Comprueba que la respuesta recibida sea un Redirect al login
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/login/?next=/quejas/ciudadano/')


    def test_get_listaQuejasPropias_invalido2(self):
        """Test negativo para acceso al listado de quejas por categoría mediante un usuario funcionario""" 
        # Simula Funcionario 1 registrado y logueado
        self.client.login(username="funcionario1", password="funcPass1")

        # Usuario Funcionario intenta acceder al listado de quejas propias
        url = reverse('quejasPropias')
        response = self.client.get(url)

        # Comprueba que la respuesta recibida sea un Redirect al login
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/')


    def test_get_listaQuejasTramitables(self):
        """Test para el listado de quejas tramitables por el funcionariado"""
        # Simula Func 1 registrado y logueado
        self.client.login(username="funcionario1", password="funcPass1")
        
        # Acceso al listado de quejas tramitables
        url = reverse('quejasTramitables')
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Listado de quejas', 2)


    def test_get_listaQuejasTramitables_invalido1(self):
        """Test negativo para acceso al listado de quejas tramitables mediante un usuario anónimo (no autenticado)"""       
        # Usuario NO autenticado intenta acceder al listado de quejas tramitables
        url = reverse('quejasTramitables')
        response = self.client.get(url)

        # Comprueba que la respuesta recibida sea un Redirect al login
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/login/?next=/quejas/funcionario/')


    def test_get_listaQuejasTramitables_invalido2(self):
        """Test negativo para acceso al listado de quejas tramitables mediante un usuario ciudadano"""       
        # Simula Ciudadano 1 registrado y logueado
        self.client.login(username="ciudadano1", password="ciudPass1")

        # Usuario Funcionario intenta acceder al listado de quejas tramitables
        url = reverse('quejasTramitables')
        response = self.client.get(url)

        # Comprueba que la respuesta recibida sea un Redirect al login
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/')


    def test_get_listaQuejasBuscador(self):
        """Test para el listado de quejas mediante el uso del buscador"""
        # Simula Func 1 registrado y logueado
        self.client.login(username="funcionario1", password="funcPass1")
        
        # Acceso al listado de quejas mediante el buscador
        url = reverse('quejasBuscador')
        response = self.client.get(url, {'q': 'Test'})

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Listado de quejas', 2)


    def test_get_listaQuejasBuscador_invalido(self):
        """Test negativo para el listado de quejas mediante el uso del buscador con un usuario anónimo (no autenticado)"""       
        # Usuario NO autenticado intenta acceder al listado de quejas mediante el buscador
        url = reverse('quejasBuscador')
        response = self.client.get(url, {'q': 'Test'})

        # Comprueba que la respuesta recibida sea un Redirect al login
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/login/?next=/quejas/buscador%3Fq%3DTest')


    def test_get_detalleQueja(self):
        """Test para el detalle de una queja"""
        # Simula Ciudadano 1 registrado y logueado
        self.client.login(username="ciudadano1", password="ciudPass1")
        
        # Acceso al detalle de la queja de id indicado
        url = reverse('quejaDetalle',  kwargs={'queja_id': 1})
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detalle de queja', 2)


    def test_get_detalleQueja_invalido(self):
        """Test negativo para el detalle de una queja mediante un usuario anónimo (no autenticado)"""       
        # Usuario NO autenticado intenta acceder al listado de quejas asociadas a la categoría de Id 1
        url = reverse('quejaDetalle',  kwargs={'queja_id': 1})
        response = self.client.get(url)

        # Comprueba que la respuesta recibida sea un Redirect al login
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/login/?next=/quejas/1/')


    def test_get_tramitarQueja(self):
        """Test para la tramitación de una queja (tramitable) mediante un funcionario capacitado para ello"""
        # Simula Ciudadano 1 registrado y logueado
        self.client.login(username="funcionario1", password="funcPass1")
        
        # Tramitación de la queja de id indicado
        url = reverse('tramitarQueja',  kwargs={'queja_id': 37})
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/quejas/37/')


    def test_get_tramitarQueja_invalido1(self):
        """Test negativo para la tramitación de una queja (tramitable) mediante un usuario anónimo (no autenticado)"""       
        # Usuario NO autenticado intenta acceder al listado de quejas asociadas a la categoría de Id 1
        # Tramitación de la queja de id indicado
        url = reverse('tramitarQueja',  kwargs={'queja_id': 37})
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/login/?next=/quejas/37/tramitar')


    def test_get_tramitarQueja_invalido2(self):
        """Test negativo para la tramitación de una queja (tramitable) mediante un usuario ciudadano"""       
        # Simula Ciudadano 1 registrado y logueado
        self.client.login(username="ciudadano1", password="ciudPass1")

        # Tramitación de la queja de id indicado
        url = reverse('tramitarQueja',  kwargs={'queja_id': 37})
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertTrue(isinstance(response, HttpResponseForbidden))


    def test_get_tramitarQueja_invalido3(self):
        """Test negativo para la tramitación de una queja (tramitable) mediante un usuario funcionario NO capacitado"""       
        # Simula Funcionario 2 registrado y logueado
        self.client.login(username="funcionario2", password="funcPass2")

        # Tramitación de la queja de id indicado
        url = reverse('tramitarQueja',  kwargs={'queja_id': 37})
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertTrue(isinstance(response, HttpResponseForbidden))

         
    def test_get_valorarQueja(self):
        """Test para la valoración de una queja por parte de un ciudadano"""
        # Simula Ciudadano 1 registrado y logueado
        self.client.login(username="ciudadano1", password="ciudPass1")

        # Valoración del usuario a la queja con Id 37 con 5 puntos
        url = reverse('valorarQueja')
        response = self.client.get(url, {'puntuacion':5, 'queja': 37})

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/quejas/37/')


    def test_get_valorarQueja_invalido1(self):
        """Test negativo para la valoración de una queja por un usuario (Funcionario) NO capacitado"""
        # Simula Funcionario 1 registrado y logueado
        self.client.login(username="funcionario1", password="funcPass1")

        # Valoración del usuario a la queja con Id 37 con 5 puntos
        url = reverse('valorarQueja')
        response = self.client.get(url, {'puntuacion':5, 'queja': 37})

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertTrue(isinstance(response, HttpResponseForbidden))


    def test_get_valorarQueja_invalido2(self):
        """Test negativo para la valoración de una queja por un ciudadano para una queja propia"""
        # Simula Ciudadano 1 registrado y logueado
        self.client.login(username="ciudadano1", password="ciudPass1")

        # Valoración del usuario a la queja con Id 2 con 5 puntos
        url = reverse('valorarQueja')
        response = self.client.get(url, {'puntuacion':5, 'queja': 2})

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertTrue(isinstance(response, HttpResponseForbidden))


    def test_get_valorarQueja_invalido3(self):
        """Test negativo para la valoración de una queja por parte de un ciudadano con una puntuación incorrecta"""
        # Simula Ciudadano 1 registrado y logueado
        self.client.login(username="ciudadano1", password="ciudPass1")

        # Valoración del usuario a la queja con Id 37 con 10 puntos
        url = reverse('valorarQueja')
        response = self.client.get(url, {'puntuacion':10, 'queja': 37})

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertTrue(isinstance(response, HttpResponseForbidden))
        

    def test_get_eliminarQueja(self):
        """Test para la eliminación de una queja por parte de su autor (ciudadano)"""
        # Simula Ciudadano 1 registrado y logueado
        self.client.login(username="ciudadano1", password="ciudPass1")

        # Ruta para la eliminación de la queja
        url = reverse('eliminarQueja', kwargs={'queja_id': 2})
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response._headers['location'][1] == '/quejas/ciudadano/')


    def test_get_eliminarQueja_invalido1(self):
        """Test negativo para la eliminación de una queja por un usuario que no es su autor"""
        # Simula Funcionario 1 registrado y logueado
        self.client.login(username="funcionario1", password="funcPass1")

        # Ruta para la eliminación de la queja
        url = reverse('eliminarQueja', kwargs={'queja_id': 2})
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertTrue(isinstance(response, HttpResponseForbidden))


    def test_get_eliminarQueja_invalido2(self):
        """Test negativo para la eliminación de una queja por un ciudadano que no es su autor"""
        # Simula Ciudadano 1 registrado y logueado
        self.client.login(username="ciudadano2", password="ciudPass2")

        # Ruta para la eliminación de la queja
        url = reverse('eliminarQueja', kwargs={'queja_id': 2})
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertTrue(isinstance(response, HttpResponseForbidden))


    def test_get_eliminarQueja_invalido3(self):
        """Test negativo para la eliminación de una queja tramitada (NO eliminable) por su autor"""
        # Simula Ciudadano 2 registrado y logueado
        self.client.login(username="ciudadano2", password="ciudPass2")

        # Ruta para la eliminación de la queja
        url = reverse('eliminarQueja', kwargs={'queja_id': 1})
        response = self.client.get(url)

        # Comprueba que la respuesta HTTP sea la correcta
        self.assertTrue(isinstance(response, HttpResponseForbidden))


    def test_form_nuevaQueja(self):
        """Test positivo para la creación de una nueva queja"""
        from quejas.forms import QuejaForm

        # Simula datos válidos para el formulario
        datos = {'titulo': 'Test', 'cuerpo':'Test', 'categoria':2}
        form = QuejaForm(datos)

        # Comprueba que el formulario es válido para esos datos
        self.assertTrue(form.is_valid())


    def test_form_nuevaQueja_invalido(self):
        """Test positivo para la creación de una nueva queja"""
        from quejas.forms import QuejaForm

        # Simula datos válidos para el formulario
        datos = {'titulo': '', 'cuerpo':'Test'}
        form = QuejaForm(datos)

        # Comprueba que el formulario no es válido para esos datos
        self.assertTrue(not form.is_valid())
        self.assertEquals(form.errors['titulo'], ['Este campo es obligatorio.'])
        self.assertEquals(form.errors['categoria'], ['Este campo es obligatorio.'])