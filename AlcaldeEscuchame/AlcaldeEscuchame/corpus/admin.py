from django.contrib import admin
from corpus.models import Corpus, EntradaCorpus, Modelo

# Register your models here.
admin.site.register(Corpus);
admin.site.register(EntradaCorpus);
admin.site.register(Modelo);