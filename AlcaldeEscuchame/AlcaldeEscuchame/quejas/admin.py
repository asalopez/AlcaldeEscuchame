from django.contrib import admin
from quejas.models import Valoracion
from quejas.models import Queja

# Register your models here.
admin.site.register(Queja);
admin.site.register(Valoracion);