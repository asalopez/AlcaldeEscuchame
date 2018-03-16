from django.shortcuts import render
from django.db.models.functions.base import Lower
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from _datetime import datetime
from usuarios.models import Funcionario
from usuarios.models import Ciudadano
from usuarios.models import Administrador
from categorias.models import Categoria
from django.http.response import HttpResponseRedirect
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required(login_url='/login/')
def listaCategorias(request):
    """Lista las categorias del sistema"""
    assert isinstance(request, HttpRequest)

     # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Obtiene la ordenación y estable el tipo para la próxima ordenación (click)
    orden, direccion = obtieneParametrosOrdenacion(request)

    # Obtiene las categorías ordenadas según la ordenación
    categorias_query = Categoria.objects.all()
    if (orden is not None):
        categorias_query = categorias_query.order_by(orden)
    usuario = request.user
    actor = obtieneTipoActor(usuario)

    # Si el usuario es tipo Funcionario, obtiene sus categorias
    categoriasFuncionario = []
    if (hasattr(usuario.actor, 'funcionario')):
        categoriasFuncionario = usuario.actor.funcionario.categorias.all()
    
    # Paginación
    paginator = Paginator(categorias_query, 5)
    page = request.GET.get('page')
    try:
        categorias = paginator.page(page)
    except PageNotAnInteger:
        # Si page no es un entero, devuelve la primera página
        categorias = paginator.page(1)
    except EmptyPage:
        # Si page está fuera de rango, devuelve la última página
        categorias = paginator.page(paginator.num_pages)
    
    # Datos del modelo (vista)
    data = {
        'actor': actor,
        'usuario': usuario,
        'categorias': categorias,
        'categoriasFuncionario': categoriasFuncionario,
        'titulo': 'Categorías',
        'direction': direccion,
        'year': datetime.now().year,
    }

    return render(request, 'listadoCategorias.html', data)


########################################## Métodos privados  ##################################################################

def obtieneParametrosOrdenacion(request):
    """ Dada una petición obtiene los parámetros de ordenación """

    # Atributo por el que se pide ordenar
    order_by = request.GET.get('order_by')
    # Tipo de ordenación: ascendente o descendente
    direction = request.GET.get('direction')    
    
    # Si no se han introducido parámetros de ordenación
    if (order_by is None) or (direction is None):
        # Valores vacios
        return None, None
    
    else:
        # Valida los posibles valores para los atributos de ordenación
        if (order_by.lower() != 'nombre') or (direction.lower() != 'asc' and direction.lower() != 'desc') :
            return None, None

        if (order_by.lower() == 'nombre') and (direction.lower() == 'asc'):
            # Devuelve el orden y la dirección (asc = Z -> A)
            return '-nombre', 'asc'
        elif (order_by.lower() == 'nombre') and (direction.lower() == 'desc'):
            # Devuelve el orden y la dirección (desc = A -> Z)
            return 'nombre', 'desc'
    
    return None, None

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


