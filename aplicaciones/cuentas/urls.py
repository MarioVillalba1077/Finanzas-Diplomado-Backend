from django.urls import path, include
from .views import *

urlpatterns = [

    path('v1/listar-movimientos', MovimientoListView.as_view()),
    path('v1/buscar-movimientos/<kword1>/<kword2>/<kword3>', MovimientoSearchView.as_view()),

    path('v1/crear-ciudad', CiudadCreateView.as_view()),
    path('v1/listar-ciudades', CiudadListView.as_view()),
    path('v1/modificar-eliminar-ciudad/<pk>', CiudadRetrieveView.as_view()),
    path('v1/buscar-ciudades/<kword>', CiudadSearchView.as_view()),

    path('v1/crear-persona', PersonaCreateView.as_view()),
    path('v1/listar-personas', PersonaListView.as_view()),
    path('v1/modificar-eliminar-persona/<pk>', PersonaRetrieveView.as_view()),
    path('v1/buscar-personas/<kword>', PersonaSearchView.as_view()),

    path('v1/crear-moneda', MonedaCreateView.as_view()),
    path('v1/listar-monedas', MonedaListView.as_view()),
    path('v1/modificar-eliminar-moneda/<pk>', MonedaRetrieveView.as_view()),
    path('v1/buscar-moneda/<kword>', MonedaSearchView.as_view()),

    path('v1/crear-cliente', ClienteCreateView.as_view()),
    path('v1/listar-clientes', ClienteListView.as_view()),
    path('v1/modificar-eliminar-cliente/<pk>', ClienteRetrieveView.as_view()),
    path('v1/buscar-cliente/<kword>', ClienteSearchView.as_view()),

    path('v1/crear-cuente', CuentaCreateView.as_view()),
    path('v1/listar-cuentas', CuentaListView.as_view()),
    path('v1/modificar-eliminar-cuenta/<pk>', CuentaRetrieveView.as_view()),
    path('v1/buscar-cuentas-numero/<kword>', CuentaSearchForNumber.as_view()),
    path('v1/buscar-cuentas-cliente/<kword>', CuentaSearchForCustomer.as_view()),

    path('v1/transferencia', TransferenciaView.as_view()),
    path('v1/retiro', RetiroView.as_view()),
    path('v1/deposito', DepositoView.as_view()),
    path('v1/bloquear-cuenta/', CuentaBloqueoView.as_view()),

    path('v1/listar-cuentas-bloqueadas', VerCuentasBloqueadasView.as_view()),

    path('v1/imprimir-extracto/<kword1>/<kword2>/<kword3>', ImprimirExtracto.as_view()),
]
