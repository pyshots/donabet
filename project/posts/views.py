from django.shortcuts import render, get_object_or_404
from .models import Partido, ResultadoPartido, Equipo

def calcular_estadisticas(equipo):
    """
    Calcula las estadísticas de los últimos 4 partidos de un equipo, 
    considerando tanto partidos como local como visitante.
    """
    # Obtenemos los últimos 4 resultados para el equipo
    resultados = ResultadoPartido.objects.filter(equipo=equipo).order_by('-partido__fecha')[:4]
    
    victorias = 0
    empates = 0
    derrotas = 0

    for resultado in resultados:
        if resultado.resultado == 'Victoria':
            victorias += 1
        elif resultado.resultado == 'Empate':
            empates += 1
        elif resultado.resultado == 'Derrota':
            derrotas += 1

    return {"victorias": victorias, "empates": empates, "derrotas": derrotas}

def generar_pronostico(partido):
    """
    Genera el pronóstico para un partido específico.
    """
    estadisticas_local = calcular_estadisticas(partido.equipo_local)
    estadisticas_visitante = calcular_estadisticas(partido.equipo_visitante)

    if estadisticas_local["victorias"] > estadisticas_visitante["victorias"]:
        prediccion = f"{partido.equipo_local.nombre} ganará el partido"
        explicacion = (
            f"En sus últimos 4 partidos, {partido.equipo_local.nombre} ganó "
            f"{estadisticas_local['victorias']} partidos, empató {estadisticas_local['empates']} "
            f"y perdió {estadisticas_local['derrotas']}. "
            f"Por otro lado, {partido.equipo_visitante.nombre} ganó {estadisticas_visitante['victorias']}, "
            f"empató {estadisticas_visitante['empates']} y perdió {estadisticas_visitante['derrotas']}."
        )
    elif estadisticas_local["victorias"] < estadisticas_visitante["victorias"]:
        prediccion = f"{partido.equipo_visitante.nombre} ganará el partido"
        explicacion = (
            f"En sus últimos 4 partidos, {partido.equipo_visitante.nombre} ganó "
            f"{estadisticas_visitante['victorias']} partidos, empató {estadisticas_visitante['empates']} "
            f"y perdió {estadisticas_visitante['derrotas']}. "
            f"Por otro lado, {partido.equipo_local.nombre} ganó {estadisticas_local['victorias']}, "
            f"empató {estadisticas_local['empates']} y perdió {estadisticas_local['derrotas']}."
        )
    else:
        prediccion = "El partido terminará en empate"
        explicacion = (
            f"Ambos equipos han tenido un desempeño similar en sus últimos 4 partidos: "
            f"{partido.equipo_local.nombre} ganó {estadisticas_local['victorias']}, empató "
            f"{estadisticas_local['empates']} y perdió {estadisticas_local['derrotas']}, mientras que "
            f"{partido.equipo_visitante.nombre} ganó {estadisticas_visitante['victorias']}, empató "
            f"{estadisticas_visitante['empates']} y perdió {estadisticas_visitante['derrotas']}."
        )

    partido.prediccion = prediccion
    partido.explicacion = explicacion
    partido.save()

def post_detail(request, match_id):
    partido = get_object_or_404(Partido, id=match_id)

    # Solo generar la predicción si no existe
    if not partido.prediccion:
        generar_pronostico(partido)

    context = {
        'partido': partido,
    }
    return render(request, 'posts/base.html', context)
