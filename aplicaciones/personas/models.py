from django.db import models

ESTADOS = [
    ('A', 'Activo'),
    ('B', 'Baja'),
]

# class Ciudad(models.Model):
#     nombre = models.CharField('Nombre Ciudad', max_length=60)
#     departamento = models.CharField('Departamento', max_length=60)
#     codigo_postal = models.IntegerField('Código Postal')

#     class Meta:
#         verbose_name_plural = 'Ciudades'

#     def __str__(self):
#         return f"{self.nombre} - {self.departamento}"

class Persona(models.Model):
    # ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    nombre = models.CharField('Nombre', max_length=60)
    apellido = models.CharField('Apellido', max_length=60)
    tipo_documento = models.CharField('Tipo Documento', max_length=30)
    numero_documento = models.CharField('Nro. Documento', max_length=30)
    direccion = models.CharField('Dirección', max_length=100)
    celular = models.CharField('Celular', max_length=15)
    email = models.EmailField('Email')
    estado = models.CharField('Estado', max_length=1, choices=ESTADOS)

    class Meta:
        verbose_name_plural = 'Personas'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
