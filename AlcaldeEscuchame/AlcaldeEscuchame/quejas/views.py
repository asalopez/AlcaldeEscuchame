from django.shortcuts import render
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
    """Lista las quejas del sistema ordenadas por fecha de publicación"""
    assert isinstance(request, HttpRequest)

     # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Obtiene las quejas ordenadas por fecha (de más reciente a menos)
    quejas = Queja.objects.order_by('-fecha')
    actor = obtieneTipoActor(request.user)
    
    # Datos del modelo (vista)
    data = {
        'actor': actor,
        'quejas': quejas,
        'titulo': 'Últimas Quejas',
        'year': datetime.now().year,
    }

    return render(request, 'listadoQuejas.html', data)


@login_required(login_url='/login/')
def listaQuejasPorCategoria(request, categoria_id):
    """Lista las quejas del sistema que pertenecen a la categoria indicada"""
    assert isinstance(request, HttpRequest)

     # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Obtiene las quejas de la categoría indicada
    quejas = Queja.objects.filter(categoriaManual_id = categoria_id)
    actor = obtieneTipoActor(request.user)
    
    # Datos del modelo (vista)
    data = {
        'actor': actor,
        'quejas': quejas,
        'titulo': 'Listado de quejas',
        'year': datetime.now().year,
    }

    return render(request, 'listadoQuejas.html', data)

@login_required(login_url='/login/')
def listaQuejasPropias(request):
    """Lista las quejas del sistema que pertenecen a la categoria indicada"""
    assert isinstance(request, HttpRequest)

    actor = obtieneTipoActor(request.user)

    # Valida que el usuario no sea anónimo (esté registrado y logueado) y sea de tipo Ciudadano
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')
    elif not (actor == 'Ciudadano'):
        return HttpResponseRedirect('/')

    # Obtiene las quejas del actor autenticado (Ciudadano)
    quejas = Queja.objects.filter(ciudadano_id = request.user.id)
    
    # Datos del modelo (vista)
    data = {
        'actor': actor,
        'quejas': quejas,
        'titulo': 'Listado de quejas',
        'year': datetime.now().year,
    }

    return render(request, 'listadoQuejas.html', data)

@login_required(login_url='/login/')
def listaQuejasBuscador(request):
    """Lista las quejas del sistema cuyo título o descripción encajen con la cadena indicada"""
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado) y sea de tipo Ciudadano
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    actor = obtieneTipoActor(request.user)

    # Obtiene el parámetro de búsqueda en la petición y si existe, las quejas asociadas
    cadena = request.GET.get('q')
    quejas = Queja.objects.all()
    if (cadena): 
        # Obtiene las quejas que coincidan con la cadena pasada
        quejas = quejas.filter(Q(titulo__icontains=cadena) | Q(cuerpo__icontains=cadena))
    
    # Datos del modelo (vista)
    data = {
        'actor': actor,
        'quejas': quejas,
        'titulo': 'Listado de quejas',
        'year': datetime.now().year,
    }

    return render(request, 'listadoQuejas.html', data)


###### Métodos privados  #####

def obtieneTipoActor(user):
    """ Dado un usuario del modelo Django obtiene el actor tipo de asociado """

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


