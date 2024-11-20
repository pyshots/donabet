import requests
from time import sleep
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from posts.models import Equipo, Partido
from django.conf import settings

def fetch_and_save_partidos():
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token": settings.FOOTBALL_DATA_API_KEY}

    # Champions League
    competencias = ["CL"]

    # Fecha de hoy y 1 mes hacia adelante (ajusta según tus necesidades)
    start_date = datetime.now()  # Fecha actual
    end_date = start_date + timedelta(weeks=4)  # Ajusta el período según lo necesario
    max_days = 10  # Máximo de días permitidos por la API

    for competencia in competencias:
        current_date = start_date

        while current_date <= end_date:
            # Establecer el rango de fechas
            date_from = current_date.strftime("%Y-%m-%d")
            date_to = (current_date + timedelta(days=max_days - 1)).strftime("%Y-%m-%d")

            # Ajustar el rango si excede la fecha final
            if datetime.strptime(date_to, "%Y-%m-%d") > end_date:
                date_to = end_date.strftime("%Y-%m-%d")

            params = {
                "competitions": competencia,
                "dateFrom": date_from,
                "dateTo": date_to,
            }

            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()

                for match in data.get("matches", []):
                    # Crear o recuperar los equipos
                    equipo_local, _ = Equipo.objects.get_or_create(
                        nombre=match["homeTeam"]["name"]
                    )
                    equipo_visitante, _ = Equipo.objects.get_or_create(
                        nombre=match["awayTeam"]["name"]
                    )

                    # Crear o actualizar el partido
                    Partido.objects.update_or_create(
                        equipo_local=equipo_local,
                        equipo_visitante=equipo_visitante,
                        fecha=make_aware(datetime.fromisoformat(match["utcDate"].replace("Z", ""))),
                        competencia=competencia,
                        defaults={"prediccion": None, "explicacion": None},
                    )
            elif response.status_code == 429:
                # Manejar el límite de solicitudes alcanzado
                wait_time = int(response.json().get("message").split()[-2])  # Extraer el tiempo de espera
                print(f"Limit reached. Waiting {wait_time} seconds...")
                sleep(wait_time + 1)  # Dormir el tiempo recomendado + un segundo de margen
                continue  # Reintentar la solicitud
            else:
                print(f"Error al obtener datos para {competencia}: {response.status_code}")
                print(f"Detalles: {response.text}")

            # Avanzar al siguiente rango de fechas
            current_date += timedelta(days=max_days)

    print("Matches fetched and saved successfully")