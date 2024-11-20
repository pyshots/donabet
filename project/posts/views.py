from django.shortcuts import render
from . import models

def home(request):
    # Obtener solo los partidos de la Champions League (CL)
    matches = models.Partido.objects.filter(competencia="CL").select_related('equipo_local', 'equipo_visitante')
    
    #  contexto con los partidos
    context = {"matches": matches}
    
    return render(request, "posts/index.html", context)