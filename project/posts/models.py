from django.db import models

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    liga = models.CharField(max_length=100)  # Copa Libertadores, Serie A...

    def __str__(self):
        return self.nombre

class Partido(models.Model):
    equipo_1 = models.ForeignKey(Equipo, related_name='equipo_1_partidos', on_delete=models.CASCADE)
    equipo_2 = models.ForeignKey(Equipo, related_name='equipo_2_partidos', on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    liga = models.CharField(max_length=100)  # Copa Libertadores, Serie A, etc.
    prediccion = models.CharField(max_length=200, blank=True, null=True)  # Predicción del equipo favorito
    explicacion = models.TextField(blank=True, null=True)  # Explicación generada por GPT

    def __str__(self):
        return f"{self.equipo_1} vs {self.equipo_2} - {self.fecha.strftime('%d/%m/%Y')}"

class ResultadoPartido(models.Model):
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='resultados')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    goles_a_favor = models.IntegerField()  # Goles a favor
    goles_en_contra = models.IntegerField()  # Goles en contra
    resultado = models.CharField(max_length=10)  # 'Victoria', 'Derrota', 'Empate'

    def __str__(self):
        return f"{self.equipo.nombre}: {self.resultado} ({self.goles_a_favor} - {self.goles_en_contra})"
