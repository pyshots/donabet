import requests
from datetime import datetime

# Reemplazar con tu token
API_TOKEN = "ae7e5fa4e39941918b99d68f7332feb9"
BASE_URL = "https://api.football-data.org/v4/competitions/CL/matches"

def obtener_partidos_pasados(fecha_inicio, fecha_fin):
    headers = {
        "X-Auth-Token": API_TOKEN
    }
    params = {
        "dateFrom": fecha_inicio,
        "dateTo": fecha_fin
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json().get("matches", [])
    else:
        print(f"Error al consultar la API: {response.status_code}")
        return []
