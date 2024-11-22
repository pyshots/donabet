from django.shortcuts import render
from posts.models import Partido

def home(request):
    partidos = Partido.objects.all()  # Obtén todos los partidos
    context = {
        'partidos': partidos,
    }
    return render(request, 'core/index.html', context)
