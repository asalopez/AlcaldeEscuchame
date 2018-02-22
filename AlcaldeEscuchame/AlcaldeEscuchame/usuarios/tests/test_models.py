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


    def test_objeto_actor(self):
        """Tests objeto Actor"""
        from usuarios.models import Actor

        # Crea la categoría
        self.actor = Actor.objects.create(poblacion="Test", telefono="954954954", direccion="Test")

        # Comprueba la creación
        self.assertTrue(isinstance(self.actor, Actor))
        self.assertEqual(self.actor.poblacion, 'Test')
        self.assertEqual(self.actor.telefono, '954954954')
        self.assertEqual(self.actor.direccion, 'Test')
        self.assertIsNone(self.actor.imagen)
        self.assertIsNone(self.actor.usuario)

        

