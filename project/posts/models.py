from django.db import models

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    competencia = models.CharField(max_length=100)  # Ejemplo: Copa Libertadores, Serie A

    def __str__(self):
        return self.nombre

class Partido(models.Model):
    equipo_local = models.ForeignKey(Equipo, related_name='partidos_como_local', on_delete=models.CASCADE)
    equipo_visitante = models.ForeignKey(Equipo, related_name='partidos_como_visitante', on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    competencia = models.CharField(max_length=100)  # Ejemplo: Copa Libertadores, Serie A
    prediccion = models.CharField(max_length=200, blank=True, null=True)  # Predicción del equipo favorito
    explicacion = models.TextField(blank=True, null=True)  # Explicación generada por GPT

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante} - {self.fecha.strftime('%d/%m/%Y')}"

    def obtener_resultado(self):
        """
        Devuelve los resultados asociados al partido en un formato amigable.
        """
        resultados = self.resultados.all()
        return [
            f"{resultado.equipo.nombre}: {resultado.resultado} ({resultado.goles_a_favor} - {resultado.goles_en_contra})"
            for resultado in resultados
        ]


class ResultadoPartido(models.Model):
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='resultados')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    goles_a_favor = models.IntegerField()  # Goles a favor
    goles_en_contra = models.IntegerField()  # Goles en contra
    resultado = models.CharField(max_length=10)  # Ejemplo: 'Victoria', 'Derrota', 'Empate'

    def __str__(self):
        return f"{self.equipo.nombre}: {self.resultado} ({self.goles_a_favor} - {self.goles_en_contra})"
