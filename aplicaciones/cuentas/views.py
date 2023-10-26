from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from aplicaciones.cuentas.serializers import *
from aplicaciones.cuentas.models import *

# Create your views here.
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

class VerCuentasBloquedasView(ListAPIView):
    queryset = Cuenta.objects.filter(bloqueda=True)
    serializer_class = CuentaSerializers