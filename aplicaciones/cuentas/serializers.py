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


class MovimientoSerializers(serializers.ModelSerializer):

    class Meta:
        model = Movimiento
        fields = '__all__'




