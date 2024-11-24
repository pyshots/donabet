from django.db import models
from django.core.exceptions import ValidationError

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    competencia = models.CharField(max_length=100)  # Ejemplo: Copa Libertadores, Serie A

    def __str__(self):
        return self.nombre

    def obtener_ultimos_partidos(self, limite=4):
        """
        Devuelve los últimos `limite` partidos (local y visitante) del equipo.
        """
        partidos_local = self.partidos_como_local.order_by('-fecha')[:limite]
        partidos_visitante = self.partidos_como_visitante.order_by('-fecha')[:limite]
        partidos = list(partidos_local) + list(partidos_visitante)
        return partidos


    def contar_resultados(self, limite=4):
        """
        Cuenta las victorias, empates y derrotas de un equipo en los últimos `limite` partidos.
        """
        partidos = self.obtener_ultimos_partidos(limite)
        victorias = 0
        empates = 0
        derrotas = 0

        for partido in partidos:
            resultado = partido.obtener_resultado()
            for res in resultado:
                if res.startswith(self.nombre):
                    if 'Victoria' in res:
                        victorias += 1
                    elif 'Empate' in res:
                        empates += 1
                    elif 'Derrota' in res:
                        derrotas += 1

        return victorias, empates, derrotas

class Partido(models.Model):
    equipo_local = models.ForeignKey(Equipo, related_name='partidos_como_local', on_delete=models.CASCADE)
    equipo_visitante = models.ForeignKey(Equipo, related_name='partidos_como_visitante', on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    competencia = models.CharField(max_length=100)  # Ejemplo: Copa Libertadores, Serie A
    prediccion = models.CharField(max_length=200, blank=True, null=True)
    explicacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante} - {self.fecha.strftime('%d/%m/%Y')}"

    def obtener_resultado(self):
        """
        Devuelve los resultados asociados al partido en un formato amigable.
        """
        resultados = self.resultados.all()
        if not resultados.exists():
            return ["Resultados no disponibles"]
        
        return [
            f"{resultado.equipo.nombre}: {resultado.resultado} ({resultado.goles_a_favor} - {resultado.goles_en_contra})"
            for resultado in resultados
        ]

    def generar_prediccion(self):
        """
        Genera el pronóstico del partido basado en los últimos resultados de los equipos.
        """
        victorias_local, empates_local, derrotas_local = self.equipo_local.contar_resultados()
        victorias_visitante, empates_visitante, derrotas_visitante = self.equipo_visitante.contar_resultados()

        # Compara victorias, empates y derrotas para determinar el pronóstico
        if victorias_local > victorias_visitante:
            self.prediccion = f"{self.equipo_local} ganará el partido"
            self.explicacion = f"El {self.equipo_local} ha tenido un desempeño mejor que el {self.equipo_visitante} en sus últimos 4 partidos."
        elif victorias_visitante > victorias_local:
            self.prediccion = f"{self.equipo_visitante} ganará el partido"
            self.explicacion = f"El {self.equipo_visitante} ha tenido un desempeño mejor que el {self.equipo_local} en sus últimos 4 partidos."
        else:
            self.prediccion = "Es muy probable un empate"
            self.explicacion = f"Ambos equipos tienen un desempeño similar en sus últimos 4 partidos: {self.equipo_local} ganó {victorias_local}, empató {empates_local}, y perdió {derrotas_local}. Mientras que {self.equipo_visitante} ganó {victorias_visitante}, empató {empates_visitante}, y perdió {derrotas_visitante}."
        
        # Guarda los cambios
        self.save()


class ResultadoPartido(models.Model):
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='resultados')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    goles_a_favor = models.IntegerField()
    goles_en_contra = models.IntegerField()
    resultado = models.CharField(max_length=10)  # Ejemplo: 'Victoria', 'Derrota', 'Empate'
    api_id = models.CharField(max_length=100, blank=True, null=True)  # Identificador opcional de la API para evitar duplicados

    def __str__(self):
        return f"{self.equipo.nombre}: {self.resultado} ({self.goles_a_favor} - {self.goles_en_contra})"

    def clean(self):
        """
        Verifica si el resultado ya existe para el mismo partido y equipo.
        """
        if self.api_id:
            if ResultadoPartido.objects.filter(api_id=self.api_id).exists():
                raise ValidationError(f"El resultado con ID {self.api_id} ya existe.")