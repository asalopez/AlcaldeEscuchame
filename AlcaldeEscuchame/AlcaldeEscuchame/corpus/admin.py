from django.contrib import admin
from corpus.models import Corpus, EntradaCorpus, EntradaCorpusAdmin, Modelo, ModeloAdmin

# Register your models here.
admin.site.register(Corpus);
admin.site.register(EntradaCorpus, EntradaCorpusAdmin);
admin.site.register(Modelo, ModeloAdmin);