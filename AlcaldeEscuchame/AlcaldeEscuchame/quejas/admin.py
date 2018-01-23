from django.contrib import admin
from quejas.models import Valoracion, ValoracionAdmin
from quejas.models import Queja, QuejaAdmin

# Register your models here.
admin.site.register(Queja, QuejaAdmin);
admin.site.register(Valoracion, ValoracionAdmin);