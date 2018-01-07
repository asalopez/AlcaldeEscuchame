from django.shortcuts import render, get_object_or_404, get_object_or_404
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


""" Lista las quejas del sistema ordenadas por fecha de publicación """
@login_required(login_url='/login/')
def listaQuejas(request):
    assert isinstance(request, HttpRequest)

     # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Obtiene las quejas ordenadas por fecha (de más reciente a menos)
    quejas = Queja.objects.order_by('-fecha')
    actor = obtieneTipoActor(request.user)
    usuario = request.user
    
    # Datos del modelo (vista)
    data = {
        'actor': actor,
        'usuario': usuario,
        'quejas': quejas,
        'titulo': 'Últimas Quejas',
        'year': datetime.now().year,
    }

    return render(request, 'listadoQuejas.html', data)


""" Lista las quejas del sistema que pertenecen a la categoria indicada """
@login_required(login_url='/login/')
def listaQuejasPorCategoria(request, categoria_id):
    assert isinstance(request, HttpRequest)

     # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Obtiene las quejas de la categoría indicada
    quejas = Queja.objects.filter(categoriaManual_id = categoria_id)
    actor = obtieneTipoActor(request.user)
    usuario = request.user

    # Datos del modelo (vista)
    data = {
        'actor': actor,
        'usuario': usuario,
        'quejas': quejas,
        'titulo': 'Listado de quejas',
        'year': datetime.now().year,
    }

    return render(request, 'listadoQuejas.html', data)


""" Lista las quejas del sistema que pertenecen al usuario autenticado """
@login_required(login_url='/login/')
def listaQuejasPropias(request):
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado) y sea de tipo Ciudadano
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')
    elif not (request.user.actor.ciudadano):
        return HttpResponseRedirect('/')

    actor = obtieneTipoActor(request.user)
    usuario = request.user

    # Obtiene las quejas del actor autenticado (Ciudadano)
    quejas = Queja.objects.filter(ciudadano_id = usuario.actor.ciudadano.id)
    
    # Datos del modelo (vista)
    data = {
        'actor': actor,
        'usuario': usuario,
        'quejas': quejas,
        'titulo': 'Listado de quejas',
        'year': datetime.now().year,
    }

    return render(request, 'listadoQuejas.html', data)


""" Lista las quejas del sistema cuyo título o descripción encajen con la cadena indicada """
@login_required(login_url='/login/')
def listaQuejasBuscador(request):
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado) y sea de tipo Ciudadano
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    actor = obtieneTipoActor(request.user)
    usuario = request.user

    # Obtiene el parámetro de búsqueda en la petición y si existe, las quejas asociadas
    cadena = request.GET.get('q')
    quejas = Queja.objects.all()
    if (cadena): 
        # Obtiene las quejas que coincidan con la cadena pasada
        quejas = quejas.filter(Q(titulo__icontains=cadena) | Q(cuerpo__icontains=cadena))
    
    # Datos del modelo (vista)
    data = {
        'actor': actor,
        'usuario': usuario,
        'quejas': quejas,
        'titulo': 'Listado de quejas',
        'year': datetime.now().year,
    }

    return render(request, 'listadoQuejas.html', data)


""" Vista detallada de la queja indicada a través de su ID """
@login_required(login_url='/login/')
def detalleQueja(request, queja_id):
    assert isinstance(request, HttpRequest)

     # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Obtiene la queja con ID indicado
    queja = Queja.objects.get(id = queja_id)

    # Obtiene los comentarios y valoraciones de la queja anterior
    comentarios = []
    valoraciones = []
    if (queja):
        comentarios = Comentario.objects.filter(queja = queja).order_by('-fecha')
        valoraciones = Valoracion.objects.filter(queja = queja)
        # Determina si la queja puede ser tramitada por el funcionario logueado (si procede)
        tramitable = esQuejaTramitable(request.user, queja)
        # Determina si la queja puede ser valorada por el ciudadano logueado (si procede)
        valorable = esQuejaValorable(request.user, queja)

    # Calcula la puntuación media de dichas valoraciones
    rating = 0
    if (valoraciones.count() > 0):
        rating = obtieneRatingQueja(valoraciones)

    # Formulario de nuevo comentario
    form = NuevoComentarioForm()
    
    # Datos del modelo (vista)
    data = {
        'actor': request.user,
        'queja': queja,
        'comentarios': comentarios,
        'valoraciones': valoraciones,
        'rating': rating,
        'rangoPuntos': range(0,5),
        'tramitable': tramitable,
        'valorable': valorable,
        'form': form,
        'titulo': 'Detalle de queja',
        'year': datetime.now().year,
    }

    return render(request, 'detalleQueja.html', data)


""" Creación o Edición de una nueva Queja """
@login_required(login_url='/login/')
def formularioQueja(request, queja_id = None):
    assert isinstance(request, HttpRequest)
    
    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Valida que el usuario sea de tipo ciudadano:
    if not (request.user.actor.ciudadano):
        return HttpResponseRedirect('/')

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

                # Categorización automática del sistema de manera aleatoria
                indiceCategoria = categorizacionAutomatica(Categoria.objects.count())
                if (indiceCategoria == -1):
                    categoriaAutomatica = categoriaManual
                else:
                    categoriaAutomatica = Categoria.objects.all()[indiceCategoria]

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
        form = QuejaForm();

    # Datos del modelo (vista)
    categorias = Categoria.objects.all();

    data = {
        'form': form,
        'actor': request.user.get_full_name(),
        'categorias': categorias,
        'titulo': 'Nueva Queja',
        'year': datetime.now().year,
    }
    
    return render(request, 'formularioQueja.html', data)


""" Elimina la queja indicada por su id """
@login_required(login_url='/login/')
def eliminarQueja(request, queja_id):
    assert isinstance(request, HttpRequest)
    
    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Valida que el usuario sea de tipo ciudadano:
    if not (request.user.actor.ciudadano):
        return HttpResponseRedirect('/')

    queja = get_object_or_404(Queja, pk=queja_id)
    # La queja solo puede eliminarse por su autor y si está abierta
    if queja.ciudadano != request.user.actor.ciudadano or queja.estado != 'Abierta':
        return HttpResponseForbidden()

    # Elimina la queja
    queja.delete()

    return HttpResponseRedirect(reverse('quejasPropias'))


""" Tramita la queja indicada por su id """
def tramitarQueja(request, queja_id):
    assert isinstance(request, HttpRequest)
    
    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Valida que el usuario sea de tipo Funcionario:
    if not (request.user.actor.funcionario):
        return HttpResponseRedirect('/')

    queja = get_object_or_404(Queja, pk=queja_id)
    # La queja solo puede tramitarse si está abierta y el Funcionario está a cargo de la categoría en la que el sistema
    # engloba la queja.
    if not esQuejaTramitable(request.user, queja):
        return HttpResponseForbidden()

    # Elimina la queja
    queja.estado = 'Tramitada'
    queja.save()

    return HttpResponseRedirect(reverse('quejaDetalle', kwargs={'queja_id': queja.id}))


""" Crea una nueva valoración para la queja indicada """
def valorarQueja(request):
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado) y sea de tipo Ciudadano
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

""" Dado un usuario del modelo Django obtiene el tipo (nombre de la clase) de actor asociado """
def obtieneTipoActor(user):
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

""" Devuelve un entero (redondeado) con la puntuación media de las valoraciones de la queja """
def obtieneRatingQueja(valoraciones):
    res = 0
    total = 0

    if (valoraciones.count() > 0):
        for v in valoraciones:
            total += v.puntuacion

        res = int(trunc(total/valoraciones.count()));

    return res

"""Genera una referencia que cumpla con el patrón establecido por los requisitos"""
def generaReferencia():
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

"""Categoriza la queja de manera aleatoria"""
def categorizacionAutomatica(numCategorias):
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

""" Dado el usuario autenticado y una queja, determina si es un funcionario y si la queja puede ser tramitada por él """
def esQuejaTramitable(usuario, queja):
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

""" Dado el usuario autenticado y una queja, determina si es un funcionario y si la queja puede ser tramitada por él """
def esQuejaValorable(usuario, queja):
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