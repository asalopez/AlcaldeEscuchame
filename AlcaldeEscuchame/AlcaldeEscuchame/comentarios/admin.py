from django.contrib import admin
from comentarios.models import Comentario, ComentarioAdmin

# Register your models here.
admin.site.register(Comentario, ComentarioAdmin);