from django.db import models
from aplicaciones.ciudades.models import Ciudad

ESTADOS = [
    ('A', 'Activo'),
    ('B', 'Baja'),
]

class Persona(models.Model):
    nombre = models.CharField('Nombre', max_length=60)
    apellido = models.CharField('Apellido', max_length=60)
    tipo_documento = models.CharField('Tipo Documento', max_length=30)
    numero_documento = models.CharField('Nro. Documento', max_length=30)
    direccion = models.CharField('Dirección', max_length=100)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    celular = models.CharField('Celular', max_length=15)
    email = models.EmailField('Email')
    estado = models.CharField('Estado', max_length=1, choices=ESTADOS, default='Activo')

    class Meta:
        verbose_name_plural = 'Personas'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
