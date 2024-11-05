from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Equipo)
admin.site.register(models.Partido)
admin.site.register(models.ResultadoPartido)
