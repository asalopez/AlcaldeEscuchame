from django.shortcuts import render
from quejas.models import Queja
from usuarios.models import Actor
from comentarios.forms import NuevoComentarioForm
from django.http.response import HttpResponseRedirect
from django.http.request import HttpRequest
from _datetime import datetime
from comentarios.models import Comentario
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def listaComentarios(request):
    """Lista los comentarios del sistema ordenadas por fecha de publicación"""
    assert isinstance(request, HttpRequest)

     # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Obtiene los comentarios ordenados por fecha (de más reciente a menos)
    comentarios = Comentario.objects.order_by('-fecha')
    
    # Datos del modelo (vista)
    data = {
        'comentarios': comentarios,
        'titulo': 'Comentarios',
        'year': datetime.now().year,
    }

    return render(request, 'listadoComentarios.html', data)


@login_required(login_url='/login/')
def nuevoComentario(request):
    """Creación de un nuevo comentario para una queja"""
    assert isinstance(request, HttpRequest)
    
    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = NuevoComentarioForm(request.POST)
        if (form.is_valid()):
            # Obtengo los campos del formulario            
            titulo = form.cleaned_data["titulo"]
            cuerpo = form.cleaned_data["cuerpo"]

            # Otros campos del comentario
            autor = getActor(request.user)
            fecha = datetime.now()
            queja_id = form.cleaned_data["queja"]

            # Valida que la queja indicada es comentable (sigue Abierta)
            queja = Queja.objects.filter(id = queja_id)[0]
            if not queja or queja.estado != 'Abierta':
                return HttpResponseRedirect('/')

            # Inserción del comentario en BD
            comentario = Comentario.objects.create(fecha = fecha, titulo = titulo, cuerpo = cuerpo, queja_id = queja_id,
                    autor = autor)

            return HttpResponseRedirect('/quejas/' + str(queja_id) + '/')
        
    return HttpResponseRedirect('/quejas/' + str(queja_id) + '/')

###### Métodos privados  #####

def getActor(user):
    """ Dado un usuario del modelo Django obtiene el actor asociado """

    # Consulta Administradores
    actores = Actor.objects.filter(usuario = user)
    if (actores.count() > 0):
        return actores[0]

    return None


