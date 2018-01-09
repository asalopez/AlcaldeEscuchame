from django.shortcuts import render, get_object_or_404, get_object_or_404
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


""" Crea una nueva entrada para el Corpus a partir de la Queja indicada por su Id """
@login_required(login_url='/login/')
def agregarQuejaCorpus(request, queja_id):
    assert isinstance(request, HttpRequest)
    
    # Valida que el usuario no sea anónimo (esté registrado y logueado) y sea staff (administrador)
    if not (request.user.is_authenticated) or not (request.user.is_staff):
        return HttpResponseRedirect('/login/')

    # Valida que el usuario sea de tipo Administrador:
    if not (request.user.actor.administrador):
        return HttpResponseRedirect('/')

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


########################################## Métodos privados  ##################################################################

""" Dado el usuario autenticado como Admin y una Queja, determina si existe Entrada al Corpus sobre dicha queja """
def esQuejaAgregable(usuario, queja):
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