from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from aplicaciones.cuentas.serializers import *
from aplicaciones.cuentas.models import Cliente, Persona


"""
    CIUDAD
        Create, Read, Update, Destroy
"""
class CiudadCreateView(CreateAPIView):
    serializer_class = CiudadSerializers

class CiudadListView(ListAPIView):
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializers

class CiudadRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializers

"""
    PERSONA
        Create, Read, Update, Destroy
"""

class PersonaCreateView(CreateAPIView):
    serializer_class = PersonaSerializers

class PersonaListView(ListAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializers

class PersonaRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializers


"""
    CLIENTE
        Create, Read, Update, Destroy
"""

class ClienteCreateView(CreateAPIView):
    serializer_class = ClienteSerializers

class ClienteListView(ListAPIView):
        queryset = Cliente.objects.all()
        serializer_class = ClienteSerializers

class ClienteRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializers

"""
    CUENTA
        Create, Read, Update, Destroy
"""

class CuentaCreateView(CreateAPIView):
    serializer_class = CuentaSerializers
class CuentaListView(ListAPIView):
        queryset = Cuenta.objects.all()
        serializer_class = CuentaSerializers
class CuentaRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = Cuenta.objects.all()
    serializer_class = CuentaSerializers

class CuentaBloqueoView(APIView):
    queryset = Cuenta.objects.all()
    serializer_class = CuentaSerializers

    def post(self, request):

        # Declarar variables y capturar información
        nro_cuenta = request.data.get('nro_cuenta')
        cuenta_existente = True
        cuenta_activa = True
        cuenta_bloqueada = False

        # Validar si está recibiendo el número de cuenta
        if nro_cuenta is None or nro_cuenta == "":
            return Response(
                {"error": "Por favor cargue el número de cuenta"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar si el número de cuenta existe, está activa o bloqueada
        try:
            cuenta= Cuenta.objects.get(numero_cuenta=nro_cuenta)
        except ObjectDoesNotExist:
            cuenta_existente = False

        if cuenta_existente:
            if cuenta.estado == 'I':
                cuenta_activa = False

            if cuenta.bloqueada:
                cuenta_bloqueada = True

        if not cuenta_existente or not cuenta_activa or cuenta_bloqueada:
            return Response(
                {"message": "La cuenta no existe o probablemente puede que esté bloqueada o inactiva"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Bloquear cuenta
        cuenta.bloqueada = True
        cuenta.save()

        return Response(
            {"OK": f"La cuenta {nro_cuenta} se bloqueó correctamente"},
            status=status.HTTP_200_OK
        )

"""
    MONEDA
        Create, Read, Update, Destroy
"""

class MonedaCreateView(CreateAPIView):
    serializer_class = MonedaSerializers

class MonedaListView(ListAPIView):
    queryset = Moneda.objects.all()
    serializer_class = MonedaSerializers

class MonedaRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = Moneda.objects.all()
    serializer_class = MonedaSerializers



