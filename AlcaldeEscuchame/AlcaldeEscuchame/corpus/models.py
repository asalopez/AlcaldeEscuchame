from django.db import models
import corpus
from categorias.models import Categoria

# Create your models here.
class Corpus(models.Model):    
    nombre = models.CharField(max_length = 80, null = True);

    def __str__(self):
        return self.nombre;

    class Meta:
        verbose_name_plural = "Corpus";

class EntradaCorpus(models.Model):
    texto = models.TextField(max_length = 6000, help_text = 'Formato recomentado: título, salto de línea y cuerpo.');

    # Relaciones
    corpus = models.ForeignKey(Corpus, on_delete = models.CASCADE);
    categoria = models.ForeignKey(Categoria, null = True, verbose_name = 'Categorización');

    def __str__(self):
        return 'Entrada corpus ' + str(self.id);

    class Meta:
        verbose_name_plural = "Entradas corpus";

class Modelo(models.Model):
    actualizacion = models.DateTimeField(verbose_name = "Última actualización", auto_now = True);
    #matriz = models.ArrayField();

    # Relaciones
    corpus = models.OneToOneField(Corpus, on_delete = models.CASCADE, primary_key = True);

    def __str__(self):
        return 'Modelo ' + self.corpus.nombre;