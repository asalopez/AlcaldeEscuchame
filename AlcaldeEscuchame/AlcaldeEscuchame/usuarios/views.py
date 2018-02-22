#encoding:utf-8

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseForbidden
from usuarios.forms import EditarClavesForm
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

    actor = request.user.actor
    
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

    actor = request.user.actor

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditarPerfilForm(request.POST)
        if (form.is_valid()):
            # Actualiza el User (model Django) en BD
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]            

            user = request.user
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Actualiza el Actor en BD
            poblacion = form.cleaned_data["poblacion"]
            telefono = form.cleaned_data["telefono"]
            direccion = form.cleaned_data["direccion"]
            foto = form.cleaned_data["foto"]

            actor.poblacion = poblacion
            actor.telefono = telefono
            actor.direccion = direccion
            actor.imagen = foto
            actor.save()

            return HttpResponseRedirect('/perfil/')

    # Si se accede al form vía GET o cualquier otro método
    else:
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


@login_required(login_url='/login/')
def editarClaves(request):
    """Edición de la clave del usuario autenticado"""
    assert isinstance(request, HttpRequest)
    
    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditarClavesForm(request.POST)
        if (form.is_valid()):
            # Se asegura que la Id que viene del formulario es la misma que la del usuario que realiza la acción
            idUsuario = form.cleaned_data["idUsuario"]
            user = request.user
            if (idUsuario != user.id):
                    return HttpResponseForbidden()

            # Establece la nueva contraseña del usuario
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()

            return HttpResponseRedirect('/')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = EditarClavesForm()
    
    # Datos del modelo (vista)
    data = {
        'form': form,
        'user': request.user,
        'titulo': 'Cambiar contraseña',
        'year': datetime.now().year,
    }
        
    return render(request, 'edicionClaves.html', data)



