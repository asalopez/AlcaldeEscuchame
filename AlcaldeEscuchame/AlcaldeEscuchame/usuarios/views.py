#encoding:utf-8

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.http.response import HttpResponseRedirect
from django import forms
from django.contrib.auth.models import User
from app.forms import RegistroForm
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

@login_required(login_url='/login/')
def perfil(request):
    """Perfil del usuario autenticado"""
    assert isinstance(request, HttpRequest)

     # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/')

    user = request.user
    
    # Datos del modelo (vista)
    data = {
        'usuario': user,
        'title': 'Perfil de usuario',
        'year': datetime.now().year,
    }

    return render(request, 'perfil.html', data)


@login_required
def editarPerfil(request):
    """Edición de perfil del usuario autenticado"""
    assert isinstance(request, HttpRequest)
    
    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/')

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = PerfilForm(request.POST)
        if (form.is_valid()):
                # Guarda el User (model Django) en BD
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            # Valida confirmación password
            print(password)
            print(confirm_password)                

            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Crea el Ciudadano y lo asocia al User anterior
            poblacion = form.cleaned_data["poblacion"]
            telefono = form.cleaned_data["telefono"]
            direccion = form.cleaned_data["direccion"]
            foto = form.cleaned_data["foto"]
            usuario = user

            ciudadano = Ciudadano.objects.create(poblacion = poblacion, telefono = telefono, direccion = direccion, 
                    imagen = foto, usuario = user)

            return HttpResponseRedirect('/login/')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = RegistroForm()
    
    # Datos del modelo (vista)
    data = {
        'form': form,
        'title': 'Registro de ciudadano',
        'year': datetime.now().year,
    }
        
    return render(request, 'app/registro.html', data)