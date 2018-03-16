from django.contrib import admin
from quejas.models import Valoracion, ValoracionAdminPanel
from quejas.models import Queja, QuejaAdminPanel

# Register your models here.
admin.site.register(Queja, QuejaAdminPanel)
admin.site.register(Valoracion, ValoracionAdminPanel)