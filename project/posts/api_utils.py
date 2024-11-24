import requests
from datetime import datetime
from posts.models import Partido, ResultadoPartido, Equipo

# Token de la API
API_TOKEN = "ae7e5fa4e39941918b99d68f7332feb9"
BASE_URL = "https://api.football-data.org/v4/competitions/CL/matches"

def obtener_resultados_partidos(fecha_inicio, fecha_fin):
    """
    Obtiene los resultados de partidos jugados en un rango de fechas.
    """
    headers = {
        "X-Auth-Token": API_TOKEN
    }
    params = {
        "dateFrom": fecha_inicio,
        "dateTo": fecha_fin
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        matches = response.json().get("matches", [])
        resultados = []

        for match in matches:
            if match.get("status") == "FINISHED":
                local = match["homeTeam"]["name"]
                visitante = match["awayTeam"]["name"]
                goles_local = match["score"]["fullTime"]["home"]
                goles_visitante = match["score"]["fullTime"]["away"]

                resultados.append({
                    "local": local,
                    "visitante": visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                })
        return resultados
    else:
        print(f"Error al consultar la API: {response.status_code}")
        return []

def actualizar_resultados_partidos(fecha_inicio, fecha_fin):
    """
    Actualiza el modelo ResultadoPartido con los resultados obtenidos de la API.
    """
    resultados = obtener_resultados_partidos(fecha_inicio, fecha_fin)

    for resultado in resultados:
        try:
            equipo_local = Equipo.objects.get(nombre=resultado["local"])
            equipo_visitante = Equipo.objects.get(nombre=resultado["visitante"])
            partido = Partido.objects.filter(
                equipo_local=equipo_local,
                equipo_visitante=equipo_visitante,
                fecha__date__range=[fecha_inicio, fecha_fin]
            ).first()

            if partido:
                # Determinar resultado para el equipo local
                if resultado["goles_local"] > resultado["goles_visitante"]:
                    resultado_local = "Victoria"
                    resultado_visitante = "Derrota"
                elif resultado["goles_local"] < resultado["goles_visitante"]:
                    resultado_local = "Derrota"
                    resultado_visitante = "Victoria"
                else:
                    resultado_local = "Empate"
                    resultado_visitante = "Empate"

                # Crear o actualizar resultados para ambos equipos
                ResultadoPartido.objects.update_or_create(
                    partido=partido,
                    equipo=equipo_local,
                    defaults={
                        "goles_a_favor": resultado["goles_local"],
                        "goles_en_contra": resultado["goles_visitante"],
                        "resultado": resultado_local
                    }
                )
                ResultadoPartido.objects.update_or_create(
                    partido=partido,
                    equipo=equipo_visitante,
                    defaults={
                        "goles_a_favor": resultado["goles_visitante"],
                        "goles_en_contra": resultado["goles_local"],
                        "resultado": resultado_visitante
                    }
                )
        except Equipo.DoesNotExist:
            print(f"Equipo no encontrado: {resultado['local']} o {resultado['visitante']}")
