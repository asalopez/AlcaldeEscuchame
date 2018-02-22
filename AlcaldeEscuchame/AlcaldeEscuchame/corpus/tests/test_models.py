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


    def test_objeto_corpus(self):
        """Test creación objeto Corpus"""
        from corpus.models import Corpus

        # Crea el objeto
        self.corpus = Corpus.objects.create(nombre='Test_Corpus')

        # Comprueba la creación
        self.assertTrue(isinstance(self.corpus, Corpus))
        self.assertEqual(self.corpus.nombre, 'Test_Corpus')


    def test_objeto_entradaCorpus(self):
        """Test creación objeto EntradaCorpus"""
        from corpus.models import EntradaCorpus

        # Crea el objeto
        self.entradaCorpus = EntradaCorpus.objects.create(texto='Test', corpus_id=1, categoria_id = 2)

        # Comprueba la creación
        self.assertTrue(isinstance(self.entradaCorpus, EntradaCorpus))
        self.assertEqual(self.entradaCorpus.texto, 'Test')


    def test_objeto_modelo(self):
        """Test creación objeto Modelo"""
        from corpus.models import Modelo

        # Crea el objeto
        self.modelo = Modelo.objects.create(corpus_id=2)

        # Comprueba la creación
        self.assertTrue(isinstance(self.modelo, Modelo))
        self.assertTrue(self.modelo.corpus_id, 2)

