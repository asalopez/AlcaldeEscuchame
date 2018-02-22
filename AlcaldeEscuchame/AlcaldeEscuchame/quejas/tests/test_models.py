"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import django
from django.test import TestCase

# TODO: Configure your database in settings.py and sync before running tests.

class TestModels(TestCase):
    """Tests para toda la funcionalidad asociada con los Models de la aplicación."""

    if django.VERSION[:2] >= (1, 7):
        # Django >= 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super(TestModels, cls).setUpClass()
            django.setup()


    def test_objeto_queja(self):
        """Tests objeto Queja"""
        from quejas.models import Queja

        # Crea el objeto
        self.queja = Queja.objects.create(referencia = "TT-TTTT", titulo = "Test", cuerpo = "Test", estado = "Abierta", ciudadano_id = 2, categoriaManual_id = 3, 
            categoriaAutomatica_id = 3)

        # Comprueba la creación
        self.assertTrue(isinstance(self.queja, Queja))
        self.assertEqual(self.queja.referencia, 'TT-TTTT')
        self.assertEqual(self.queja.titulo, 'Test')
        self.assertEqual(self.queja.cuerpo, 'Test')
        self.assertEqual(self.queja.estado, 'Abierta')
        self.assertEqual(self.queja.ciudadano_id, 2)
        self.assertEqual(self.queja.categoriaManual_id, 3)
        self.assertEqual(self.queja.categoriaAutomatica_id, 3)


    def test_objeto_valoracion(self):
        """Tests objeto Valoracion"""
        from quejas.models import Valoracion

        # Crea el objeto
        self.valoracion = Valoracion.objects.create(queja_id = 37, ciudadano_id = 2, puntuacion = 5)

        # Comprueba la creación
        self.assertTrue(isinstance(self.valoracion, Valoracion))
        self.assertEqual(self.valoracion.queja_id, 37)
        self.assertEqual(self.valoracion.ciudadano_id, 2)
        self.assertEqual(self.valoracion.puntuacion, 5)


        
