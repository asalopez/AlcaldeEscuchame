#encoding:utf-8

from django.contrib.auth.decorators import login_required
from usuarios.forms import EditarPerfilForm
from _datetime import date
from usuarios.models import Ciudadano, Funcionario, Administrador
from django.shortcuts import render, render_to_response
from django.http.response import HttpResponseRedirect
from django import forms
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

@login_required(login_url='/login/')
def perfil(request):
    """Perfil del usuario autenticado"""
    assert isinstance(request, HttpRequest)

     # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    user = request.user
    actor = getActor(user)
    
    # Datos del modelo (vista)
    data = {
        'actor': actor,
        'tipoActor': actor.__class__.__name__,
        'titulo': 'Perfil de usuario',
        'fecha': date.today(),
        'year': datetime.now().year,
    }

    return render(request, 'perfil.html', data)


@login_required(login_url='/login/')
def editarPerfil(request):
    """Edición de perfil del usuario autenticado"""
    assert isinstance(request, HttpRequest)
    
    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditarPerfilForm(request.POST)
        if (form.is_valid()):
            # Actualiza el User (model Django) en BD
            #password = form.cleaned_data["password"]
            #confirm_password = form.cleaned_data["confirm_password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]            

            user = request.user
            #user.password = password
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Actualiza el Actor en BD
            poblacion = form.cleaned_data["poblacion"]
            telefono = form.cleaned_data["telefono"]
            direccion = form.cleaned_data["direccion"]
            foto = form.cleaned_data["foto"]

            actor = getActor(user)
            actor.poblacion = poblacion
            actor.telefono = telefono
            actor.direccion = direccion
            actor.imagen = foto
            actor.save()

            return HttpResponseRedirect('/perfil/')

        # Si el formulario no es correcto necesitaremos el actor para renderizar actor.usuario.username en la plantilla
        else:
            actor = getActor(request.user)

    # Si se accede al form vía GET o cualquier otro método
    else:
        actor = getActor(request.user)

        datos = {'first_name': actor.usuario.first_name, 'last_name': actor.usuario.last_name, 'email': actor.usuario.email, 
                 'poblacion': actor.poblacion, 'telefono': actor.telefono, 'direccion': actor.direccion, 'foto': actor.imagen}
        form = EditarPerfilForm(datos)
    
    # Datos del modelo (vista)
    data = {
        'form': form,
        'actor': actor,
        'titulo': 'Editar Perfil',
        'year': datetime.now().year,
    }
        
    return render(request, 'edicionPerfil.html', data)


###### Métodos privados  #####

def getActor(user):
    """ Dado un usuario del modelo Django obtiene el actor asociado """

    # Consulta Administradores
    admins = Administrador.objects.filter(usuario = user)
    if (admins.count() > 0):
        return admins[0]

    # Consulta Ciudadanos
    ciudadanos = Ciudadano.objects.filter(usuario = user)
    if (ciudadanos.count() > 0):
        return ciudadanos[0]

    # Consulta Funcionarios
    funcionarios = Funcionario.objects.filter(usuario = user)
    if (funcionarios.count() > 0):
        return funcionarios[0]

    return None


