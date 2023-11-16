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

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'Nombre': instance.persona.nombre + ' ' + instance.persona.apellido,
            'fecha_ingreso': instance.fecha_ingreso,
            'calificacion': instance.calificacion,
            'estado': instance.estado,
            'persona': instance.persona.id
        }


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
            'moneda': instance.moneda.descripcion,
            'bloqueada': instance.bloqueada,
        }


class MovimientoSerializers(serializers.ModelSerializer):

    class Meta:
        model = Movimiento
        fields = '__all__'

    def to_representation(self, instance):

        return {
           'id': instance.id,
           'fecha_movimiento': instance.fecha_movimiento.isoformat(),
           'tipo_movimiento': instance.tipo_movimiento,
           'saldo_anterior': instance.saldo_anterior,
           'saldo_actual': instance.saldo_actual,
           'monto_movimiento': instance.monto_movimiento,
           'numero_cuenta_origen': instance.numero_cuenta_origen,
           'numero_cuenta_destino': instance.numero_cuenta_destino,
           'canal': instance.canal,
           'cuenta': instance.cuenta.id,
           'numero_cuenta': instance.cuenta.numero_cuenta,
           'moneda': instance.cuenta.moneda.descripcion,
           'cliente': instance.cuenta.cliente.persona.nombre + ' ' + instance.cuenta.cliente.persona.apellido,
           'nro_documento': instance.cuenta.cliente.persona.numero_documento
        }




