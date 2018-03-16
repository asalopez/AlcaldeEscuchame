from django.contrib import admin
from comentarios.models import Comentario, ComentarioAdminPanel

# Register your models here.
admin.site.register(Comentario, ComentarioAdminPanel)