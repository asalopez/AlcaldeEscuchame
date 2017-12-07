from django.contrib import admin
from usuarios.models import Ciudadano, Funcionario, Administrador

# Register your models here.
admin.site.register(Ciudadano);
admin.site.register(Funcionario);
admin.site.register(Administrador);

