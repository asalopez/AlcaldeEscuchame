from django.contrib import admin
from usuarios.models import Actor, ActorAdminPanel, FuncionarioAdminPanel, AdministradorAdmin
from usuarios.models import Ciudadano, CiudadanoAdminPanel, Funcionario, Administrador

# Register your models here.
admin.site.register(Actor, ActorAdminPanel)
admin.site.register(Ciudadano, CiudadanoAdminPanel)
admin.site.register(Funcionario, FuncionarioAdminPanel)
admin.site.register(Administrador, AdministradorAdmin)

