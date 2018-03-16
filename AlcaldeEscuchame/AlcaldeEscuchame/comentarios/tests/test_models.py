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


    def test_objeto_comentario(self):
        """Test creación objeto comentario"""
        from comentarios.models import Comentario

        # Crea el objeto
        self.comentario = Comentario.objects.create(titulo='Test_Titulo', cuerpo='Test_Cuerpo')

        # Comprueba la creación
        self.assertTrue(isinstance(self.comentario, Comentario))
        self.assertEqual(self.comentario.titulo, 'Test_Titulo')
        self.assertEqual(self.comentario.cuerpo, 'Test_Cuerpo')

