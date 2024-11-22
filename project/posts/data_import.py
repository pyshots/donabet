from posts.models import Partido, Equipo
from datetime import datetime

def guardar_partidos_pasados(partidos):
    for partido in partidos:
        equipo_local, _ = Equipo.objects.get_or_create(nombre=partido["homeTeam"]["name"])
        equipo_visitante, _ = Equipo.objects.get_or_create(nombre=partido["awayTeam"]["name"])

        # Convertir fecha a objeto datetime
        fecha = datetime.fromisoformat(partido["utcDate"].replace("Z", "+00:00"))

        # Evitar duplicados con get_or_create
        Partido.objects.get_or_create(
            equipo_local=equipo_local,
            equipo_visitante=equipo_visitante,
            fecha=fecha,
            competencia="CL"
        )
