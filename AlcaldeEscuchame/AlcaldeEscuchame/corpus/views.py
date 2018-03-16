from django.shortcuts import render, get_object_or_404, get_object_or_404
from app.decorators import usuario_role_administrador
from django.utils.encoding import smart_str
import os
import mimetypes
from wsgiref.util import FileWrapper
from AlcaldeEscuchame import settings
from collections import Counter
import re
from re import split
from corpus.models import Modelo
from categorias.models import Categoria
from corpus.models import Corpus
from corpus.models import EntradaCorpus
from django.http.response import HttpResponseForbidden
from django.urls.base import reverse
from quejas.models import Queja
from _datetime import datetime
from usuarios.models import Administrador
from django.http.response import HttpResponseRedirect
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import numpy as np

@login_required(login_url='/login/')
@usuario_role_administrador
def agregarQuejaCorpus(request, queja_id):
    """ Crea una nueva entrada para el Corpus a partir de la Queja indicada por su Id """
    assert isinstance(request, HttpRequest)
    
    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    queja = get_object_or_404(Queja, pk=queja_id)
    # Crea los campos para la entrada
    if not esQuejaAgregable(request.user, queja):
        return HttpResponseForbidden()

    # Crea la entrada para el corpus a partir de la queja
    corpus = get_object_or_404(Corpus)
    referencia = queja.referencia
    texto = queja.titulo + '\n' + queja.cuerpo
    categoria = queja.categoriaManual

    entrada = EntradaCorpus.objects.create(referencia = referencia, texto = texto, categoria = categoria, corpus = corpus)

    return HttpResponseRedirect('/admin/corpus/entradacorpus/')


@login_required(login_url='/login/')
@usuario_role_administrador
def detalleModeloCorpus(request):
    """ Obtiene el modelo del sistema a partir del cual se calcula la categorización automática """
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    usuario = request.user

    # Obtiene el modelo del sistema
    modelo = Modelo.objects.all().first()
    datos_modelo = {'categorias': 0, 'vocabulario': 0}
    if modelo:
        # Carga el modelo a partir de la ruta guardada en BD
        matriz = np.load(modelo.ruta).item()
        matriz = dict(matriz)

        # Número de categorias consideradas en el modelo
        num_categorias = len(matriz)
        # Número de palabras del vocabulario
        next_value = next(iter(matriz.values()))
        num_palabras = len(next_value)

        datos_modelo = {'categorias': num_categorias, 'vocabulario': num_palabras, 'fecha': modelo.actualizacion}
    else:
        modelo = None
    

    # Datos del modelo (vista)
    data = {
        'admin': usuario,
        'modelo': modelo,
        'datos_modelo': datos_modelo,
        'titulo': 'Modelo del sistema',
        'year': datetime.now().year,
    }

    return render(request, 'detalleModelo.html', data)


@login_required(login_url='/login/')
@usuario_role_administrador
def descargaModeloCorpus(request):
    """ Descarga el fichero Modelo.NPY almacenado en el sistema """
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    file_path = settings.STATIC_ROOT +'/corpus/modelo.npy'
    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)

    response = HttpResponse(file_wrapper, content_type = file_mimetype)
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('modelo.npy')

    return response


@login_required(login_url='/login/')
@usuario_role_administrador
def reconstruyeModelo(request):
    """ Reconstruye el modelo usado para categorizar automáticamente las quejas """
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Obtenemos el vocabulario
    vocabulario = obtieneVocabularioModelo()

    # Obtiene el modelo a partir del vocabulario
    modelo = obtieneMatrizModelo(vocabulario)

    # Ruta donde se alamacenará el fichero NPY con el modelo
    ruta = settings.STATIC_ROOT +'/corpus/modelo.npy'

    # Guarda el modelo como fichero .NPY en la ruta especificada
    np.save(ruta, modelo)
    #read_modelo = np.load(ruta).item()

    # Crea/Actualiza el objeto Modelo en BD
    corpus = Corpus.objects.all().first()
    Modelo.objects.update_or_create(corpus = corpus)

    return HttpResponseRedirect('/corpus/modelo/')



########################################## Métodos privados  ##################################################################

def esQuejaAgregable(usuario, queja):
    """ Dado el usuario autenticado como Admin y una Queja, determina si existe Entrada al Corpus sobre dicha queja """
    res = False

    try:
        # Si el usuario autenticado tiene permisos de administrador
        if (usuario.is_staff and usuario.actor.administrador != None):
            # Comprueba si hay alguna Entrada al Corpus con esa referencia
            entradasCorpus = EntradaCorpus.objects.filter(referencia = queja.referencia).count()
            if (entradasCorpus == 0):
                res = True

    except Administrador.DoesNotExist:
        return False;

    return res


def obtieneVocabularioModelo():
    """ Obtiene el vocabulario que conformará el Modelo para la categorización automática"""

    # Lista de palabras que conforman el vocabulario
    res = []
    
    # Obtiene las entradas (quejas) que conforman el corpus
    entradas = EntradaCorpus.objects.all()
    # Recorre cada entrada del corpus
    for e in entradas:
        # Pone el texto en minúscula
        texto = e.texto.lower()

        # Obtiene las palabras (términos alfanuméricos)
        palabras = re.findall('\w+', texto)

        # Agrega las palabras al vocabulario
        res.extend(palabras)

    # Transforma la lista en un conjunto para eliminar repetidas
    res = set(res)

    # Elimina las StopWords del vocabulario
    res = eliminaStopWords(res)

    # Formatea el vocabulario quitando acentos y 'ñ' de cada palabra
    res = [p.replace('ñ', 'n').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u') for p in res]

    return res
    

def obtieneMatrizModelo(vocabulario):
    """ Dado el vocabulario, obtiene las entradas agrupadas por categorías y crea la matriz contando las apariciones de esas palabras en cada una """

    # Diccionario que representa el Modelo: Claves = Ids categorias ; Valores = Diccionario como Vector de Frecuencia respecto al vocabulario.
    res = {}

    categorias = Categoria.objects.all()
    # Para cada categoría
    for categoria in categorias:
        entradas = EntradaCorpus.objects.filter(categoria = categoria)

        # Para cada entrada relacionada con esa categoria
        for entrada in entradas:
            # Obtiene la lista de palabras formateadas que conforman la entrada
            texto = entrada.texto.lower()
            palabras = re.findall('\w+', texto)
            palabras_entrada = [p.replace('ñ', 'n').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u') for p in palabras]

            # Cuenta el número de apariciones de las palabras del vocabulario en la entrada
            frecuencia = Counter()
            # Recorre cada palabra del Vocabulario
            for p_vocab in vocabulario:
                # Cuenta las apariciones de la palabra del vocabulario en la entrada
                count = palabras_entrada.count(p_vocab)
                # Normaliza y guarda
                frecuencia[p_vocab] = count

        # Creo el vector de conteo (frecuencias) como un diccionario
        vector_conteo = dict(frecuencia)

        # Normalizo el vector de conteo
        factor = 1.0/sum(vector_conteo.values())
        vector_conteo = {k: v*factor for k, v in vector_conteo.items() }

        # Agrego el par (Categoria-VectorConteo) al modelo
        res[categoria.id] = dict(vector_conteo)

    return res


def eliminaStopWords(palabras):
    """ Dada una lista de palabras no repetidas, eliminas las consideradas palabras huecas """

    res = []

    # Carga el fichero de palabras huecasç
    ruta = settings.STATIC_ROOT + '/corpus/stopWords.txt'
    #f = open(ruta, 'r')
    with open(ruta,'r', encoding="ISO-8859-1") as f:
        stopWords = f.read().splitlines()
        stopWords = set(stopWords)

    # Elimina de la lista esas palabras
    res = palabras.difference(stopWords)

    return res


