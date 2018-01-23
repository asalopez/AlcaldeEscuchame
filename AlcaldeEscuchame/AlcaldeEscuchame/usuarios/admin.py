from django.contrib import admin
from usuarios.models import Actor, ActorAdmin, FuncionarioAdmin, AdministradorAdmin
from usuarios.models import Ciudadano, CiudadanoAdmin, Funcionario, Administrador

# Register your models here.
admin.site.register(Actor, ActorAdmin);
admin.site.register(Ciudadano, CiudadanoAdmin);
admin.site.register(Funcionario, FuncionarioAdmin);
admin.site.register(Administrador, AdministradorAdmin);

