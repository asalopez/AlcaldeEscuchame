from django.contrib import admin
from corpus.models import Corpus, EntradaCorpus, EntradaCorpusAdminPanel, Modelo, ModeloAdminPanel

# Register your models here.
admin.site.register(Corpus)
admin.site.register(EntradaCorpus, EntradaCorpusAdminPanel)
admin.site.register(Modelo, ModeloAdminPanel)