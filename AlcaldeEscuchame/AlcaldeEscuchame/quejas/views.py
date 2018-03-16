from django.shortcuts import render, get_object_or_404, get_object_or_404
from app.decorators import usuario_role_ciudadano, usuario_role_funcionario
import scipy
import re
from corpus.models import Modelo
import numpy as np
from scipy.spatial.distance import cosine
from collections import Counter
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from itertools import chain
from corpus.models import EntradaCorpus
from django.http.response import HttpResponseForbidden
import random
import string
from categorias.models import Categoria
from django.urls.base import reverse
from quejas.forms import QuejaForm
from comentarios.forms import NuevoComentarioForm
from math import trunc
from math import ceil
from quejas.models import Valoracion
from comentarios.models import Comentario
from django.db.models.query_utils import Q
from quejas.models import Queja
from _datetime import datetime
from usuarios.models import Funcionario
from usuarios.models import Ciudadano
from usuarios.models import Administrador
from django.http.response import HttpResponseRedirect
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required(login_url='/login/')
def listaQuejas(request):
    """ Lista las quejas del sistema ordenadas por fecha de publicación """
    assert isinstance(request, HttpRequest)

     # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Obtiene las quejas ordenadas por fecha (de más reciente a menos)
    quejas_query = Queja.objects.order_by('-fecha')
    actor = obtieneTipoActor(request.user)
    usuario = request.user

    # Paginación
    paginator = Paginator(quejas_query, 5)
    page = request.GET.get('page')
    try:
        quejas = paginator.page(page)
    except PageNotAnInteger:
        # Si page no es un entero, devuelve la primera página
        quejas = paginator.page(1)
    except EmptyPage:
        # Si page está fuera de rango, devuelve la última página
        quejas = paginator.page(paginator.num_pages)
    
    # Datos del modelo (vista)
    data = {
        'actor': actor,
        'usuario': usuario,
        'quejas': quejas,
        'titulo': 'Últimas Quejas',
        'year': datetime.now().year,
    }

    return render(request, 'listadoQuejas.html', data)


@login_required(login_url='/login/')
def listaQuejasPorCategoria(request, categoria_id):
    """ Lista las quejas del sistema que pertenecen a la categoria indicada """
    assert isinstance(request, HttpRequest)

     # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Obtiene las quejas de la categoría indicada ordenadas por fecha
    quejas_query = Queja.objects.filter(categoriaManual_id = categoria_id).order_by('-fecha')
    actor = obtieneTipoActor(request.user)
    usuario = request.user

    # Paginación
    paginator = Paginator(quejas_query, 5)
    page = request.GET.get('page')
    try:
        quejas = paginator.page(page)
    except PageNotAnInteger:
        # Si page no es un entero, devuelve la primera página
        quejas = paginator.page(1)
    except EmptyPage:
        # Si page está fuera de rango, devuelve la última página
        quejas = paginator.page(paginator.num_pages)

    # Datos del modelo (vista)
    data = {
        'actor': actor,
        'usuario': usuario,
        'quejas': quejas,
        'titulo': 'Listado de quejas',
        'year': datetime.now().year,
    }

    return render(request, 'listadoQuejas.html', data)


@login_required(login_url='/login/')
@usuario_role_ciudadano
def listaQuejasPropias(request):
    """ Lista las quejas del sistema que pertenecen al usuario autenticado """
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    actor = obtieneTipoActor(request.user)
    usuario = request.user

    # Obtiene las quejas del actor autenticado (Ciudadano)
    quejas_query = Queja.objects.filter(ciudadano_id = usuario.actor.ciudadano.id).order_by('-fecha')

    # Paginación
    paginator = Paginator(quejas_query, 5)
    page = request.GET.get('page')
    try:
        quejas = paginator.page(page)
    except PageNotAnInteger:
        # Si page no es un entero, devuelve la primera página
        quejas = paginator.page(1)
    except EmptyPage:
        # Si page está fuera de rango, devuelve la última página
        quejas = paginator.page(paginator.num_pages)
    
    # Datos del modelo (vista)
    data = {
        'actor': actor,
        'usuario': usuario,
        'quejas': quejas,
        'titulo': 'Listado de quejas',
        'year': datetime.now().year,
    }

    return render(request, 'listadoQuejas.html', data)


@login_required(login_url='/login/')
@usuario_role_funcionario
def listaQuejasTramitables(request):
    """ Lista las quejas del sistema que pertenecen a las categorias asignadas al funcionario autenticado """
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')
    
    actor = obtieneTipoActor(request.user)
    usuario = request.user

    # Obtiene las quejas sistema que son tramitables por el funcionario
    categoriasFuncionario = usuario.actor.funcionario.categorias.all()
    quejas_query = []
    for c in categoriasFuncionario:
        q = Queja.objects.filter(categoriaAutomatica = c)
        quejas_query = list(chain(quejas_query, q))

    # Ordena las quejas por fecha
    if quejas_query:
        quejas_query.sort(key = lambda q: q.fecha, reverse = True)

    # Paginación
    paginator = Paginator(quejas_query, 5)
    page = request.GET.get('page')
    try:
        quejas = paginator.page(page)
    except PageNotAnInteger:
        # Si page no es un entero, devuelve la primera página
        quejas = paginator.page(1)
    except EmptyPage:
        # Si page está fuera de rango, devuelve la última página
        quejas = paginator.page(paginator.num_pages)
    
    # Datos del modelo (vista)
    data = {
        'actor': actor,
        'usuario': usuario,
        'quejas': quejas,
        'titulo': 'Listado de quejas',
        'year': datetime.now().year,
    }

    return render(request, 'listadoQuejas.html', data)


@login_required(login_url='/login/')
def listaQuejasBuscador(request):
    """ Lista las quejas del sistema cuyo título o descripción encajen con la cadena indicada """
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado) y sea de tipo Ciudadano
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    actor = obtieneTipoActor(request.user)
    usuario = request.user

    # Obtiene el parámetro de búsqueda en la petición y si existe, las quejas asociadas
    cadena = request.GET.get('q')
    quejas_query = Queja.objects.all().order_by('-fecha')
    if (cadena): 
        # Obtiene las quejas que coincidan con la cadena pasada
        quejas_query = quejas_query.filter(Q(titulo__icontains=cadena) | Q(cuerpo__icontains=cadena))
    
    # Paginación
    paginator = Paginator(quejas_query, 5)
    page = request.GET.get('page')
    try:
        quejas = paginator.page(page)
    except PageNotAnInteger:
        # Si page no es un entero, devuelve la primera página
        quejas = paginator.page(1)
    except EmptyPage:
        # Si page está fuera de rango, devuelve la última página
        quejas = paginator.page(paginator.num_pages)

    # Datos del modelo (vista)
    data = {
        'actor': actor,
        'usuario': usuario,
        'quejas': quejas,
        'titulo': 'Listado de quejas',
        'year': datetime.now().year,
    }

    return render(request, 'listadoQuejas.html', data)


@login_required(login_url='/login/')
def detalleQueja(request, queja_id):
    """ Vista detallada de la queja indicada a través de su ID """
    assert isinstance(request, HttpRequest)

     # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Obtiene la queja con ID indicado
    queja = Queja.objects.get(id = queja_id)

    # Obtiene los comentarios y valoraciones de la queja anterior
    comentarios_query = []
    valoraciones = []
    if (queja):
        comentarios_query = Comentario.objects.filter(queja = queja).order_by('-fecha')
        valoraciones = Valoracion.objects.filter(queja = queja)
        # Determina si la queja puede ser tramitada por el funcionario logueado (si procede)
        tramitable = esQuejaTramitable(request.user, queja)
        # Determina si la queja puede ser valorada por el ciudadano logueado (si procede)
        valorable = esQuejaValorable(request.user, queja)
        # Determina si la queja es agregable al corpus por parte del administrador logueado (si procede)
        agregable = esQuejaAgregable(request.user, queja)

    # Paginación Comentarios
    paginator = Paginator(comentarios_query, 5)
    page = request.GET.get('page')
    try:
        comentarios = paginator.page(page)
    except PageNotAnInteger:
        # Si page no es un entero, devuelve la primera página
        comentarios = paginator.page(1)
    except EmptyPage:
        # Si page está fuera de rango, devuelve la última página
        comentarios = paginator.page(paginator.num_pages)

    # Calcula la puntuación media de dichas valoraciones
    rating = 0
    if (valoraciones.count() > 0):
        rating = obtieneRatingQueja(valoraciones)

    ## Formulario nuevo comentario
    form = NuevoComentarioForm()
    form_errors = []
    # Busca errores del formulario en la sesión
    if (request.session.get('errores_form')):
        # Obtiene los errores si existiesen y elimina la variable
        form_errors = request.session.pop('errores_form', [])

    
    # Datos del modelo (vista)
    data = {
        'actor': request.user,
        'queja': queja,
        'comentarios': comentarios,
        'valoraciones': valoraciones,
        'rating': rating,
        'rangoPuntos': range(0,5),
        'tramitable': tramitable,
        'agregable': agregable,
        'valorable': valorable,
        'form': form,
        'form_errors': form_errors,
        'titulo': 'Detalle de queja',
        'year': datetime.now().year
    }

    return render(request, 'detalleQueja.html', data)


@login_required(login_url='/login/')
@usuario_role_ciudadano
def formularioQueja(request, queja_id = None):
    """ Creación o Edición de una nueva Queja """
    assert isinstance(request, HttpRequest)
    
    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Busca la queja y valida su edición
    if queja_id:
        queja = get_object_or_404(Queja, pk=queja_id)
        # La queja solo puede editarse por su autor y si está abierta
        if queja.ciudadano != request.user.actor.ciudadano or queja.estado != 'Abierta':
            return HttpResponseForbidden()

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = QuejaForm(request.POST)
        if (form.is_valid()):
            # Obtengo los campos del formulario            
            titulo = form.cleaned_data["titulo"]
            cuerpo = form.cleaned_data["cuerpo"]
            categoriaManual = form.cleaned_data["categoria"]

            # Otros campos de la queja
            ciudadano = request.user.actor.ciudadano
            fecha = datetime.now()

            # Si estamos Editando
            if queja_id and queja:
                # Actualización de la queja en BD
                queja.titulo = titulo
                queja.cuerpo = cuerpo
                queja.categoriaManual = categoriaManual
                queja.save()

            # Si estamos Creando
            else:
                estado = 'Abierta'
                referencia = generaReferencia()

                # Consulta la variable de sesión que confirma la categorización y la elimina
                confirmaCategoria = request.session.pop('confirmaCategoria', False)

                # Categorización automática del sistema de manera aleatoria
                #indiceCategoria = categorizacionAutomaticaRandom(Categoria.objects.count())
                #if (indiceCategoria == -1):
                #    categoriaAutomatica = categoriaManual
                #else:
                #    categoriaAutomatica = Categoria.objects.all()[indiceCategoria]

                # Categorización automática del sistema
                categoriaAutomatica = categorizacionAutomatica(cuerpo)
                
                # Si la categorización automática falla (o no existe modelo disponible), prevalece la cateogría manual
                if (categoriaAutomatica is None):
                    categoriaAutomatica = categoriaManual
                # Si la categorización es distinta a la del usuario y NO la ha confirmado, pide confirmación (variable de sesión)
                elif (categoriaManual != categoriaAutomatica) and not(confirmaCategoria):
                    # Activa la confirmación para la siguiente llamada
                    request.session['confirmaCategoria'] = True
                    # Datos del formulario pidiendo confirmación
                    datosForm = {'titulo': titulo, 'cuerpo': cuerpo, 'categoria': categoriaManual.id}
                    form = QuejaForm(datosForm)
                    data = {
                        'form': form,
                        'actor': request.user.get_full_name(),
                        'categorias': Categoria.objects.all(),
                        'categorizacion': categoriaAutomatica,
                        'titulo': 'Nueva Queja',
                        'boton_submit': 'Continuar con la publicación',
                        'year': datetime.now().year,
                    }

                    return render(request, 'formularioQueja.html', data)

                # Inserción de la queja en BD
                queja = Queja.objects.create(fecha = fecha, referencia = referencia, titulo = titulo, cuerpo = cuerpo, estado = estado,
                    ciudadano = ciudadano, categoriaManual = categoriaManual, categoriaAutomatica = categoriaAutomatica)

            return HttpResponseRedirect(reverse('quejasPropias'))

    # Si se accede al form vía GET pidiendo edición rellena el formulario
    elif queja_id and queja:
        datos = {'titulo': queja.titulo, 'cuerpo': queja.cuerpo, 'categoria': queja.categoriaManual.id}
        form = QuejaForm(datos)

    # Si se accede al form vía GET pidiendo creación
    else:
        # Crea variable en sesión para confirmar categorización
        request.session['confirmaCategoria'] = False
        form = QuejaForm();

    # Datos del modelo (vista)
    categorias = Categoria.objects.all();

    data = {
        'form': form,
        'actor': request.user.get_full_name(),
        'categorias': categorias,
        'categorizacion': None,
        'titulo': 'Nueva Queja',
        'boton_submit': 'Publicar queja',
        'year': datetime.now().year,
    }
    
    return render(request, 'formularioQueja.html', data)


@login_required(login_url='/login/')
@usuario_role_ciudadano
def eliminarQueja(request, queja_id):
    """ Elimina la queja indicada por su id """
    assert isinstance(request, HttpRequest)
    
    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    queja = get_object_or_404(Queja, pk=queja_id)
    # La queja solo puede eliminarse por su autor y si está abierta
    if queja.ciudadano != request.user.actor.ciudadano or queja.estado != 'Abierta':
        return HttpResponseForbidden()

    # Elimina la queja
    queja.delete()

    return HttpResponseRedirect(reverse('quejasPropias'))


@login_required(login_url='/login/')
@usuario_role_funcionario
def tramitarQueja(request, queja_id):
    """ Tramita la queja indicada por su id """
    assert isinstance(request, HttpRequest)
    
    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Valida que el usuario sea de tipo Funcionario:
    #if not (hasattr(request.user.actor, 'funcionario')):
    #    return HttpResponseForbidden()

    queja = get_object_or_404(Queja, pk=queja_id)
    # La queja solo puede tramitarse si está abierta y el Funcionario está a cargo de la categoría en la que el sistema
    # engloba la queja.
    if not esQuejaTramitable(request.user, queja):
        return HttpResponseForbidden()

    # Elimina la queja
    queja.estado = 'Tramitada'
    queja.save()

    return HttpResponseRedirect(reverse('quejaDetalle', kwargs={'queja_id': queja.id}))


@login_required(login_url='/login/')
@usuario_role_ciudadano
def valorarQueja(request):
    """ Crea una nueva valoración para la queja indicada """
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Obtienes los parámetros de la URL
    queja_id = request.GET.get('queja')
    queja = get_object_or_404(Queja, pk=queja_id)
    puntos = int(request.GET.get('puntuacion'))

    # La queja solo puede valorarse una vez por cada Ciudadano (siempre que no sea su autor)
    # La puntuación debe pertenecer al rango [1,5]
    if not esQuejaValorable(request.user, queja) or not(puntos in range(1,6)):
        return HttpResponseForbidden()

    ciudadano = request.user.actor.ciudadano
    
    # Inserción de la queja en BD
    valoracion = Valoracion.objects.create(queja = queja, ciudadano = ciudadano, puntuacion = puntos)
    
    return HttpResponseRedirect(reverse('quejaDetalle', kwargs={'queja_id': queja.id}))


########################################## Métodos privados  ##################################################################

def obtieneTipoActor(user):
    """ Dado un usuario del modelo Django obtiene el tipo (nombre de la clase) de actor asociado """
    # Consulta Administradores
    admins = Administrador.objects.filter(usuario = user)
    if (admins.count() > 0):
        return admins[0].__class__.__name__

    # Consulta Ciudadanos
    ciudadanos = Ciudadano.objects.filter(usuario = user)
    if (ciudadanos.count() > 0):
        return ciudadanos[0].__class__.__name__

    # Consulta Funcionarios
    funcionarios = Funcionario.objects.filter(usuario = user)
    if (funcionarios.count() > 0):
        return funcionarios[0].__class__.__name__

    return None

def obtieneRatingQueja(valoraciones):
    """ Devuelve un entero (redondeado) con la puntuación media de las valoraciones de la queja """
    res = 0
    total = 0

    if (valoraciones.count() > 0):
        for v in valoraciones:
            total += v.puntuacion

        res = int(trunc(total/valoraciones.count()));

    return res

def generaReferencia():
    """Genera una referencia que cumpla con el patrón establecido por los requisitos"""
    res = ''

    # Caracteres que pueden formar parte de la cadena
    letras = string.ascii_letters
    letras_numeros = letras + string.digits

    # Primera parte del patrón: YY (dos letras)
    res += ''.join(random.choices(letras, k=2))

    # Concatena el guión
    res += ''.join('-')

    # Parte final del patrón: XXXX (letras o dígitos)
    res += ''.join(random.choices(letras_numeros, k=4))

    return res

def categorizacionAutomaticaRandom(numCategorias):
    """Categoriza la queja de manera aleatoria"""
    # Toma un número aleatorio del 1 al 100
    num = random.randint(1,100)
    # Toma el resto para ver si es par
    par = num % 2 == 0

    # Si el número es par, la categorización automática coincidirá con la decisión del ciudadano (categoría manual)
    if par:
        return -1

    # Si es impar, devuelve un índice aleatorio (para tomar una posición aleatoria en el array de categorías).
    else:
        return random.randint(0, numCategorias-1)

def esQuejaTramitable(usuario, queja):
    """ Dado el usuario autenticado y una queja, determina si es un funcionario y si la queja puede ser tramitada por él """
    res = False

    try:
        # Si el usuario autenticado es un funcionario y la queja está 'Abierta'
        if (usuario.actor.funcionario != None and queja.estado == 'Abierta'):
            # Categorías en las que trabaja el funcionario
            categoriasFuncionario = usuario.actor.funcionario.categorias.all()

            # Si la queja está categorizada por el sistema dentro de alguna de las anteriores
            if (queja.categoriaAutomatica in categoriasFuncionario):
                res = True

    except Funcionario.DoesNotExist:
        return False;

    return res

def esQuejaValorable(usuario, queja):
    """ Dado el usuario autenticado y una queja, determina si es un ciudadano y si la queja puede ser valorada por él """
    res = False

    try:
        # Si el usuario autenticado es un Ciudadano y la queja que intenta valorar no es suya
        if (usuario.actor.ciudadano != None and queja.ciudadano != usuario.actor.ciudadano):
            # Comprueba que el ciudadano no haya valorado ya esa queja
            valoraciones = Valoracion.objects.filter(ciudadano = usuario.actor.ciudadano, queja = queja).count()
            if (valoraciones == 0):
                res = True

    except Ciudadano.DoesNotExist:
        return False;

    return res

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

def categorizacionAutomatica(texto):
    """ Categoriza la queja (su texto) a partir del Modelo del sistema """

    # Obtiene el modelo del sistema y lo carga
    modelo = Modelo.objects.all().first()
    # En caso de no existir, devuelve None
    if (modelo is None) or not(modelo.ruta):
        return None

    matriz = np.load(modelo.ruta).item()
    matriz = dict(matriz)

    # Obtiene el vocabulario del propio modelo
    vocab_matriz = next(iter(matriz.values()))
    vocabulario = list(vocab_matriz)

    # Obtiene el vector de conteo para la queja indicada como un diccionario
    vector_conteo = obtieneVectorConteoQueja(texto, vocabulario)

    # Calcula las distancias cosenos entre el vector de la queja y las almacena indexada por categoría
    distancias = {}
    vector_queja = list(vector_conteo.values())
    for c in matriz.keys():
        vector_categoria = list(matriz[c].values())
        distancia = scipy.spatial.distance.cosine(vector_queja, vector_categoria)
        distancias[c] = distancia
    
    # Obtiene el índice (key) con la menor distancia distancia (value)
    i_menor_distancia = min(distancias, key = distancias.get)
    # Obtiene la categoria que corresponde al índice de menor distancia
    result = Categoria.objects.get(pk = i_menor_distancia)

    return result

def obtieneVectorConteoQueja(texto, vocabulario):
    """ Dado el texto de una queja y el vocabulario del Modelo, obtiene el vector de conteo normalizado """

    texto = texto.lower()
    palabras = re.findall('\w+', texto)
    palabras_queja = [p.replace('ñ', 'n').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u') for p in palabras]

    # Cuenta el número de apariciones de las palabras del vocabulario en la queja
    frecuencia = Counter()
    # Recorre cada palabra del Vocabulario
    for p_vocab in vocabulario:
        # Cuenta las apariciones de la palabra del vocabulario en la queja
        count = palabras_queja.count(p_vocab)
        # Normaliza y guarda
        frecuencia[p_vocab] = count

    # Creo el vector de conteo (frecuencias) como un diccionario
    vector_conteo = dict(frecuencia)

    # Normaliza teniento en cuenta que no se puede dividir por 0 (caso en que ninguna palabra del texto de la queja esté en el vocabulario del modelo)
    divisor = sum(vector_conteo.values())
    if (divisor == 0): 
        divisor = 1
    factor = 1.0/divisor
    vector_conteo = {k: v*factor for k, v in vector_conteo.items() }

    return vector_conteo
