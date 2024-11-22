from django.shortcuts import render, get_object_or_404
from .models import Partido

def post_detail(request, match_id):
    partido = get_object_or_404(Partido, id=match_id)
    resultados = partido.obtener_resultado()  # Llama a la función del modelo para obtener resultados

    context = {
        'partido': partido,
        'resultados': resultados,
    }
    return render(request, 'posts/base.html', context)