import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Cambia 'config.settings' si tiene otro nombre
django.setup()

from posts.data_import import guardar_partidos_pasados
from posts.api_utils import obtener_partidos_pasados

def importar_partidos_champions():
    # Rango de fechas para las primeras 4 jornadas de la Champions League
    fecha_inicio = "2024-09-17"
    fecha_fin = "2024-11-08"  # Fecha estimada de la última jornada

    # Consultar la API
    partidos = obtener_partidos_pasados(fecha_inicio, fecha_fin)

    if partidos:  # Solo guardar si hay partidos
        # Guardar en la base de datos
        guardar_partidos_pasados(partidos)
        print(f"Se han importado {len(partidos)} partidos.")
    else:
        print("No se encontraron partidos en el rango de fechas especificado.")

if __name__ == "__main__":
    importar_partidos_champions()
