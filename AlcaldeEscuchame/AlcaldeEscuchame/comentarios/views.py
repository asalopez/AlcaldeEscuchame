from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse
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

    return render(request, 'comentarios.html', data)


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
            autor = request.user.actor
            fecha = datetime.now()
            queja_id = form.cleaned_data["queja"]

            # Valida que la queja indicada es comentable (sigue Abierta)
            queja = get_object_or_404(Queja, pk = queja_id)
            if not queja or queja.estado != 'Abierta':
                return HttpResponseRedirect('/')

            # Inserción del comentario en BD
            comentario = Comentario.objects.create(fecha = fecha, titulo = titulo, cuerpo = cuerpo, queja_id = queja_id,
                    autor = autor)

            return HttpResponseRedirect(reverse('quejaDetalle', kwargs={'queja_id': queja_id}))

        # Si el Form no es válido
        else:
            queja_id = form.cleaned_data["queja"]
            # Crea una variable de sesión con los errores
            request.session['errores_form'] = form.errors
            # Lleva a la vista de detalle
            return HttpResponseRedirect(reverse('quejaDetalle', kwargs={'queja_id': queja_id}))
        
    return HttpResponseRedirect(reverse('quejaDetalle', kwargs={'queja_id': queja_id}))


