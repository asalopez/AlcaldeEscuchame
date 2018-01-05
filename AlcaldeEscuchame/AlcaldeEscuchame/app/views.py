"""
Definition of views.
"""

#encoding:utf-8

from django.shortcuts import render, render_to_response
from django.http.response import HttpResponseRedirect
from django import forms
from usuarios.models import Ciudadano
from django.contrib.auth.models import User
from app.forms import RegistroForm
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

def home(request):
    """Página de inicio"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'titulo':'Bienvenido',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Página de contacto."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'titulo':'Contacto',
            'descripcion':'Página de contacto',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'titulo':'About',
            'descripcion':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def registro(request):
    """Registro del ciudadano en el sistema"""
    assert isinstance(request, HttpRequest)
    
    # Valida que el usuario sea anónimo (no registrado)
    if (request.user.is_authenticated):
        return HttpResponseRedirect('/')

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = RegistroForm(request.POST)
        if (form.is_valid()):
            # Guarda el User (model Django) en BD
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]              

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
        'titulo': 'Registro de ciudadano',
        'year': datetime.now().year,
    }
        
    return render(request, 'app/registro.html', data)
