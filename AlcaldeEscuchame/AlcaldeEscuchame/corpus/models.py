from django.db import models
from AlcaldeEscuchame import settings
from django.core.validators import RegexValidator
import corpus
from categorias.models import Categoria
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

# Corpus: nombre
class Corpus(models.Model):    
    nombre = models.CharField(max_length = 80, null = True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Corpus"


# EntradaCorpus: referencia, texto, corpus, categoría.
class EntradaCorpus(models.Model):
    referencia = models.CharField(max_length = 7, editable = False, null = True, blank = True, default = "", validators = [RegexValidator(regex = r'^([a-zA-Z]{2})-([a-zA-Z0-9]{4})$', message = 'La referencia no cumple el patrón solicitado.')])
    texto = models.TextField(max_length = 6000, help_text = 'Formato recomentado: título, salto de línea y cuerpo.')

    # Relaciones
    corpus = models.ForeignKey(Corpus, on_delete = models.CASCADE)
    categoria = models.ForeignKey(Categoria, null = True, verbose_name = 'Categorización')

    def __str__(self):
        return 'Entrada corpus ' + str(self.id)

    class Meta:
        verbose_name_plural = "Entradas corpus"


# Clase que define los campos a mostrar en el Panel de Administración para el listado de entradas
class EntradaCorpusAdmin(admin.ModelAdmin):
    list_display = ('corpus', 'referencia', 'categoria')


# Modelo: fecha actualización, matriz de ponderación, corpus.
class Modelo(models.Model):
    actualizacion = models.DateTimeField(verbose_name = "Última actualización", auto_now = True)
    ruta = models.FilePathField(settings.STATIC_ROOT +'/corpus/modelo.npy', null = True, editable = False)

    # Relaciones
    corpus = models.OneToOneField(Corpus, on_delete = models.CASCADE, primary_key = True)

    def __str__(self):
        return 'Modelo ' + self.corpus.nombre

    
# Clase que define los campos a mostrar en el Panel de Administración para el listado de modelos
class ModeloAdmin(admin.ModelAdmin):
    list_display = ('corpus', 'actualizacion')