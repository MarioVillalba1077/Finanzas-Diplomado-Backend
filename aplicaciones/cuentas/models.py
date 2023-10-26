from django.db import models

# Create your models here.

ESTADOS = [
    ('A', 'Activo'),
    ('B', 'Baja'),
]


class Ciudad(models.Model):

    nombre = models.CharField('Nombre Ciudad', max_length=60)
    departamento = models.CharField('Departamento', max_length=60)
    codigo_postal = models.IntegerField('Código Postal')

    class Meta:
        verbose_name_plural = 'Ciudades'

    def __str__(self):
        return f"{self.nombre} - {self.departamento}"


class Persona(models.Model):

    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
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


class Cliente(models.Model):

    CALIFICACIONES = [
        ('M', 'Mala'),
        ('B', 'Buena'),
        ('E', 'Excelente'),
    ]

    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    calificacion = models.CharField('Calificación', max_length=1, choices=CALIFICACIONES)
    estado = models.CharField('Estado', max_length=1, choices=ESTADOS)

    class Meta:
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f"{self.persona.__str__()}"


class Moneda(models.Model):

    descripcion = models.CharField('Descripción', max_length=40)
    simbolo = models.CharField('Símbolo', max_length=10)

    class Meta:
        verbose_name_plural = 'Monedas'

    def __str__(self):
        return f"{self.descripcion} - {self.simbolo}"


class Cuenta(models.Model):
    activo = 'Activo'
    inactivo = 'Inactivo'

    ESTADOS = [
        ('A', activo),
        ('I', inactivo)
    ]
    TIPOS_CUENTA = [
        ('C', 'Cuenta Corriente'),
        ('A', 'Caja de Ahorro'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    numero_cuenta = models.CharField('Nro. Cuenta', max_length=30, unique=True)
    fecha_alta = models.DateTimeField('Fecha Alta', auto_now_add=True)
    tipo_cuenta = models.CharField('Tipo de Cuenta', max_length=1, choices=TIPOS_CUENTA)
    estado = models.CharField('Estado', max_length=1, choices=ESTADOS)
    saldo = models.FloatField('Saldo')
    numero_contrato = models.CharField('Nro. Contrato', max_length=40)
    costo_mantenimiento = models.FloatField('Costo Mantenimiento')
    promedio_acreditacion = models.FloatField('Promedio Acreditación')
    bloqueada = models.BooleanField('Bloqueada', default=False)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Cuentas'

    def __str__(self):
        return f"{self.numero_cuenta} - {self.cliente}"


class Movimiento(models.Model):

    TIPOS_MOVIMIENTO = [
        ('DEP', 'Depósito'),
        ('RET', 'Retiro'),
        ('DEB', 'Débito'),
        ('CRE', 'Crédito'),
    ]

    CANALES = [
        ('W', 'Web'),
        ('C', 'Caja'),
        ('A', 'App'),
    ]
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    fecha_movimiento = models.DateTimeField('Fecha Movimiento', auto_now_add=True)
    tipo_movimiento = models.CharField('Tipo de Movimiento', max_length=3, choices=TIPOS_MOVIMIENTO)
    saldo_anterior = models.FloatField('Saldo Anterior')
    saldo_actual = models.FloatField('Saldo Actual')
    monto_movimiento = models.FloatField('Monto Movimiento')
    numero_cuenta_origen = models.CharField('Nro. Cuenta Origen', max_length=30)
    numero_cuenta_destino = models.CharField('Nro. Cuenta Destino', max_length=30)
    canal = models.CharField('Canal', max_length=1, choices=CANALES)

    class Meta:
        verbose_name_plural = 'Movimientos'
