from rest_framework import serializers
from .models import *


class CiudadSerializers(serializers.ModelSerializer):

    class Meta:
        model = Ciudad
        fields = '__all__'


class PersonaSerializers(serializers.ModelSerializer):

    class Meta:
        model = Persona
        fields = '__all__'


class ClienteSerializers(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = '__all__'


class MonedaSerializers(serializers.ModelSerializer):

    class Meta:
        model = Moneda
        fields = '__all__'


class CuentaSerializers(serializers.ModelSerializer):

    class Meta:
        model = Cuenta
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'cliente': instance.cliente.persona.nombre + ' ' + instance.cliente.persona.apellido,
            'numero_cuenta': instance.numero_cuenta,
            'fecha_alta': instance.fecha_alta,
            'tipo_cuenta': instance.tipo_cuenta,
            'estado': instance.estado,
            'saldo': instance.saldo,
            'numero_contrato': instance.numero_contrato,
            'costo_mantenimiento': instance.costo_mantenimiento,
            'promedio_acreditacion': instance.promedio_acreditacion,
            'moneda': instance.moneda.descripcion
        }


class MovimientoSerializers(serializers.ModelSerializer):

    class Meta:
        model = Movimiento
        fields = '__all__'




