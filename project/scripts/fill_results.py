import os
import sys

# Agregar el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar el entorno de Django correctamente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

# Configurar Django
django.setup()

from posts.api_utils import actualizar_resultados_partidos

# Rango de fechas que quieres consultar
fecha_inicio = "2024-09-17"
fecha_fin = "2024-11-06"

# Actualizar los resultados
actualizar_resultados_partidos(fecha_inicio, fecha_fin)
print("Resultados actualizados exitosamente.")
