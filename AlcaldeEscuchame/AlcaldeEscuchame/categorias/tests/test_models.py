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


    def test_objeto_categoria(self):
        """Tests objeto categoría"""
        from categorias.models import Categoria

        # Crea la categoría
        self.categoria = Categoria.objects.create(nombre="Test_Nombre", descripcion="Test_Descripción")

        # Comprueba la creación
        self.assertTrue(isinstance(self.categoria, Categoria))
        self.assertEqual(self.categoria.nombre, 'Test_Nombre')
        self.assertEqual(self.categoria.descripcion, 'Test_Descripción')
        self.assertIsNone(self.categoria.imagen)

        

