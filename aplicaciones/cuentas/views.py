from django.db.models import Q
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from aplicaciones.cuentas.serializers import *
from aplicaciones.cuentas.models import *
import os
import subprocess

# Create your views here.

"""
    MOVIMIENTO
        Read, Search
"""


class MovimientoListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializers


class MovimientoSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MovimientoSerializers

    def get_queryset(self):
        id_cuenta = self.kwargs['kword1']
        mes = self.kwargs['kword2']
        anho = self.kwargs['kword3']

        return Movimiento.objects.filter(
            Q(fecha_movimiento__month=mes) &
            Q(fecha_movimiento__year=anho) &
            Q(cuenta=id_cuenta)
        )


"""
    CIUDAD
        Create, Read, Update, Destroy
"""


class CiudadCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CiudadSerializers


class CiudadListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializers


class CiudadRetrieveView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializers


class CiudadSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CiudadSerializers

    def get_queryset(self):
        kword = self.kwargs['kword']

        return Ciudad.objects.filter(
            Q(nombre__icontains=kword) | Q(departamento__icontains=kword)
        )


"""
    Persona
        Create, Read, Update, Destroy
"""


class PersonaCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PersonaSerializers


class PersonaListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializers


class PersonaRetrieveView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializers


class PersonaSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PersonaSerializers

    def get_queryset(self):
        kword = self.kwargs['kword']

        return Persona.objects.filter(
            Q(nombre__icontains=kword) | Q(apellido__icontains=kword)
        )


"""
    MONEDA
        Create, Read, Update, Destroy
"""


class MonedaCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MonedaSerializers


class MonedaListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Moneda.objects.all()
    serializer_class = MonedaSerializers


class MonedaSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MonedaSerializers

    def get_queryset(self):
        return Moneda.objects.filter(
            descripcion__icontains=self.kwargs['kword']
        )


class MonedaRetrieveView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Moneda.objects.all()
    serializer_class = MonedaSerializers


"""
    CLIENTE
        Create, Read, Update, Destroy
"""


class ClienteCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClienteSerializers


class ClienteListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializers


class ClienteSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClienteSerializers

    def get_queryset(self):
        # Obtener el valor ingresado desde el request
        kword = self.kwargs['kword']

        # Filtrar clientes que coincidan con un nombre o apellido de la tabla persona
        return Cliente.objects.filter(
            Q(persona__nombre__icontains=kword) | Q(persona__apellido__icontains=kword)
        )


class ClienteRetrieveView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializers


"""
    Modelo: Cuenta
    Opciones: Listar, Buscar por Nro., Buscar por Nombre o Apellido del Cliente, 
        Crear, Actualizar y Eliminar

"""


class CuentaListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cuenta.objects.order_by('id')
    serializer_class = CuentaSerializers


class CuentaSearchForNumber(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CuentaSerializers

    def get_queryset(self):
        return Cuenta.objects.filter(numero_cuenta__icontains=self.kwargs['kword'])


class CuentaSearchForCustomer(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CuentaSerializers

    def get_queryset(self):
        return Cuenta.objects.filter(cliente__persona__nombre__icontains=self.kwargs['kword']) | \
            Cuenta.objects.filter(cliente__persona__apellido__icontains=self.kwargs['kword'])


class CuentaCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CuentaSerializers


class CuentaRetrieveView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CuentaSerializers
    queryset = Cuenta.objects.all()


"""
    OPERACIONES
"""


# Vista para Operación de Transferencia
class TransferenciaView(APIView):
    permission_classes = [IsAuthenticated]

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
      
   
# Vista para Operación de Retiro
class RetiroView(APIView):
    permission_classes = [IsAuthenticated]

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


# Vista para Operación de Depósito
class DepositoView(APIView):
    permission_classes = [IsAuthenticated]

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


# Vista para Bloquear Cuenta
class CuentaBloqueoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Declarar variables y capturar información
        nro_cuenta = request.data.get('nro_cuenta')
        cuenta_existente = True
        cuenta_activa = True
        cuenta_bloqueada = False

        # Validar si está recibiendo el número de cuenta
        if nro_cuenta is None or nro_cuenta == "":
            return Response(
                {"ok": False,
                 "message": "Por favor cargue el número de cuenta"},
                status=status.HTTP_400_BAD_REQUEST)

        # Validar si el número de cuenta existe, está activa o bloqueada
        try:
            cuenta = Cuenta.objects.get(numero_cuenta=nro_cuenta)
        except ObjectDoesNotExist:
            cuenta_existente = False

        if cuenta_existente:
            if cuenta.estado == 'I':
                cuenta_activa = False

            if cuenta.bloqueada:
                cuenta_bloqueada = True

        if not cuenta_existente or not cuenta_activa or cuenta_bloqueada:
            return Response({"ok": False,
                             "message": "La cuenta no existe o probablemente puede que esté bloqueada o inactiva"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Bloquear cuenta
        cuenta.bloqueada = True
        cuenta.save()

        return Response({"ok": True,
                         "message": f"La cuenta {nro_cuenta} se bloqueó correctamente"},
                        status=status.HTTP_200_OK)


# Vista para Listar Cuentas Bloqueadas
class VerCuentasBloqueadasView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cuenta.objects.filter(bloqueada=True)
    serializer_class = CuentaSerializers
      
      
class ImprimirExtracto(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        nombre_archivo = ""
        nombre_archivo_resultado = ""
        nombre_archivo_log = ""

        try:
            id_cuenta = self.kwargs['kword1']
            mes = self.kwargs['kword2']
            anho = self.kwargs['kword3']

            movimientos = Movimiento.objects.filter(
                Q(fecha_movimiento__month=mes) &
                Q(fecha_movimiento__year=anho) &
                Q(cuenta=id_cuenta)
            )

            movimientos_serializer = MovimientoSerializers(movimientos, many=True)

            # Creamos el archivo de texto con el JSON resultado

            nombre_archivo = f"{id_cuenta}_{mes}_{anho}.txt"
            file = open(nombre_archivo, "w")
            file.write(str(movimientos_serializer.data).replace("'", '"'))
            file.close()

            # Le pasamos el archivo al ejecutable que genera el pdf

            p = subprocess.Popen(["GenerarExtracto.exe", nombre_archivo])
            p.wait()
            nombre_archivo_resultado = f"{id_cuenta}_{mes}_{anho}.pdf"
            nombre_archivo_log = f"{id_cuenta}_{mes}_{anho}.log"

            # Verificar que se haya generado el PDF

            if os.path.exists(nombre_archivo_resultado):
                import base64
                short_report = open(nombre_archivo_resultado, 'rb')
                report_encoded = base64.b64encode(short_report.read())
                short_report.close()
                return Response({'ok': True,
                                 'message': 'Extracto generado exitosamente',
                                 'report': report_encoded}, status=status.HTTP_200_OK)
            else:
                return Response({"ok": False,
                                 "resultado": 'El extracto no pudo ser generado'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            return Response({'ok': False,
                             'resultado': 'Error Interno. ' + str(ex)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            if os.path.exists(nombre_archivo):
                os.remove(nombre_archivo)

            if os.path.exists(nombre_archivo_resultado):
                os.remove(nombre_archivo_resultado)

            if os.path.exists(nombre_archivo_log):
                os.remove(nombre_archivo_log)







