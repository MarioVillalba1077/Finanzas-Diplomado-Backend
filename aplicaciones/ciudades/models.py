from django.db import models

class Ciudad(models.Model):
    nombre = models.CharField('Nombre Ciudad', max_length=60)
    departamento = models.CharField('Departamento', max_length=60)
    codigo_postal = models.IntegerField('Código Postal')

    class Meta:
        verbose_name_plural = 'Ciudades'

    def __str__(self):
        return f"{self.nombre} - {self.departamento}"
