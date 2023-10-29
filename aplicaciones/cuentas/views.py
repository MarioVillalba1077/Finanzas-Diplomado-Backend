from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from aplicaciones.cuentas.serializers import *
from aplicaciones.cuentas.models import *

# Create your views here.


"""
    MOVIMIENTO
        Read
"""

class MovimientoListView(ListAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializers

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
    Persona
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


class TransferenciaView(APIView):

    def post(self, request):

        nro_cuenta_origen = request.data.get('nro_cuenta_origen')
        nro_cuenta_destino = request.data.get('nro_cuenta_destino')
        monto = request.data.get('monto')
        canal_movimiento = request.data.get('canal')

        # Validar datos necesarios

        if not all([nro_cuenta_origen, nro_cuenta_destino, monto]):
            return Response({"ok": False,
                             "message": "La solicitud no contiene los datos necesarios"},
                            status=status.HTTP_400_BAD_REQUEST)
        # Validar Monto

        try:
            monto = float(monto)
        except Exception:
            return Response({"ok": False,
                             "message": "Dato no válido para Monto"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Si se envió Canal validar el dato

        if canal_movimiento is not None:
            if canal_movimiento != "A" and canal_movimiento != "C" and canal_movimiento != "W":
                return Response({"ok": False,
                                 "message": "Dato no válido para Canal"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            canal_movimiento = "W"

        # Recuperamos Cuenta de Origen

        try:
            cuenta_origen = Cuenta.objects.get(numero_cuenta=nro_cuenta_origen)
        except Cuenta.DoesNotExist:
            return Response({"ok": False,
                             "message": "Cuenta de Origen no encontrada"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Recuperamos Cuenta de Destino

        try:
            cuenta_destino = Cuenta.objects.get(numero_cuenta=nro_cuenta_destino)
        except Cuenta.DoesNotExist:
            return Response({"ok": False,
                             "message": "Cuenta de Destino no encontrada"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validamos que la Cuenta de Origen esté activa

        if cuenta_origen.estado != "A":
            return Response({"ok": False,
                             "message": "La Cuenta de Origen no está Activa"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validamos que la Cuenta de Destino esté activa

        if cuenta_destino.estado != "A":
            return Response({"ok": False,
                             "message": "La Cuenta de Destino no está Activa"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validamos que las Cuentas tengan la misma Moneda

        if cuenta_origen.moneda != cuenta_destino.moneda:
            return Response({"ok": False,
                             "message": "Las Cuentas no manejan la misma Moneda"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validamos el Saldo de la Cuenta Origen

        if cuenta_origen.saldo < monto:
            return Response({"ok": False,
                             "message": "El saldo de la cuenta es inferior al monto a Transferir"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Calcular saldos
        saldo_actual_origen = cuenta_origen.saldo - monto
        saldo_actual_destino = cuenta_destino.saldo + monto

        # Registrar movimientos
        Movimiento.objects.create(cuenta=cuenta_origen,
                                  tipo_movimiento='DEB',
                                  saldo_anterior=cuenta_origen.saldo,
                                  saldo_actual=saldo_actual_origen,
                                  monto_movimiento=monto,
                                  numero_cuenta_origen=nro_cuenta_origen,
                                  numero_cuenta_destino=nro_cuenta_destino,
                                  canal=canal_movimiento)

        Movimiento.objects.create(cuenta=cuenta_destino,
                                  tipo_movimiento='CRE',
                                  saldo_anterior=cuenta_destino.saldo,
                                  saldo_actual=saldo_actual_destino,
                                  monto_movimiento=monto,
                                  numero_cuenta_origen=nro_cuenta_origen,
                                  numero_cuenta_destino=nro_cuenta_destino,
                                  canal=canal_movimiento)

        # Actualizamos el Saldo de las Cuentas

        cuenta_origen.saldo -= monto
        cuenta_destino.saldo += monto
        cuenta_origen.save()
        cuenta_destino.save()

        return Response({"ok": True,
                         "message": "Transferencia Realizada con Éxito"},
                        status=status.HTTP_200_OK)
      
   
    
class RetiroView(APIView):   

    def post(self, request):

        nro_cuenta = request.data.get('nro_cuenta')
        monto = request.data.get('monto')

        # Validar datos necesarios

        if not all([nro_cuenta, monto]):
            return Response({"ok": False,
                             "message": "La solicitud no contiene los datos necesarios"},
                            status=status.HTTP_400_BAD_REQUEST)
        # Validar Monto

        try:
            monto = float(monto)
        except Exception:
            return Response({"ok": False,
                             "message": "Dato no válido para Monto"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Recuperamos la cuenta
        try:
            cuenta = Cuenta.objects.get(numero_cuenta=nro_cuenta)
        except Cuenta.DoesNotExist:
            return Response({"ok": False,
                             "message": "Cuenta no encontrada"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validamos que la Cuenta esté activa

        if cuenta.estado != "A":
            return Response({"ok": False,
                             "message": "La Cuenta no está Activa"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validamos el Saldo de la Cuenta Origen

        if cuenta.saldo < monto:
            return Response({"ok": False,
                             "message": "El saldo de la cuenta es inferior al monto a Transferir"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Calcular saldos
        saldo_actual = cuenta.saldo - monto

        # Registrar movimiento
        Movimiento.objects.create(cuenta=cuenta,
                                  tipo_movimiento='RET',
                                  saldo_anterior=cuenta.saldo,
                                  saldo_actual=saldo_actual,
                                  monto_movimiento=monto,
                                  numero_cuenta_origen=nro_cuenta,
                                  numero_cuenta_destino=nro_cuenta,
                                  canal='C')

        # Actualizamos el Saldo de las Cuentas

        cuenta.saldo -= monto
        cuenta.save()

        return Response({"ok": True,
                         "message": "Retiro registrado con Éxito"},
                        status=status.HTTP_200_OK)


class DepositoView(APIView):

    def post(self, request):

        nro_cuenta = request.data.get('nro_cuenta')
        monto = request.data.get('monto')

        # Validar datos necesarios

        if not all([nro_cuenta, monto]):
            return Response({"ok": False,
                             "message": "La solicitud no contiene los datos necesarios"},
                            status=status.HTTP_400_BAD_REQUEST)
        # Validar Monto

        try:
            monto = float(monto)
        except Exception:
            return Response({"ok": False,
                             "message": "Dato no válido para Monto"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Recuperamos la cuenta
        try:
            cuenta = Cuenta.objects.get(numero_cuenta=nro_cuenta)
        except Cuenta.DoesNotExist:
            return Response({"ok": False,
                             "message": "Cuenta no encontrada"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validamos que la Cuenta esté activa

        if cuenta.estado != "A":
            return Response({"ok": False,
                             "message": "La Cuenta no está Activa"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Calcular saldos
        saldo_actual = cuenta.saldo + monto

        # Registrar movimiento
        Movimiento.objects.create(cuenta=cuenta,
                                  tipo_movimiento='DEP',
                                  saldo_anterior=cuenta.saldo,
                                  saldo_actual=saldo_actual,
                                  monto_movimiento=monto,
                                  numero_cuenta_origen=nro_cuenta,
                                  numero_cuenta_destino=nro_cuenta,
                                  canal='C')

        # Actualizamos el Saldo de las Cuentas

        cuenta.saldo += monto
        cuenta.save()

        return Response({"ok": True,
                         "message": "Depósito registrado con Éxito"},
                        status=status.HTTP_200_OK)

