from django.shortcuts import render
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

    categorias = Categoria.objects.all()
    actor = obtieneTipoActor(request.user)
    
    # Datos del modelo (vista)
    data = {
        'actor': actor,
        'categorias': categorias,
        'titulo': 'Categorías',
        'year': datetime.now().year,
    }

    return render(request, 'listadoCategorias.html', data)


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


