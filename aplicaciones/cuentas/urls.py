from django.urls import path, include
from .views import *

urlpatterns = [
    path('v1/transferencia', TransferenciaView.as_view()),
    path('v1/retiro', RetiroView.as_view()),
    path('v1/deposito', DepositoView.as_view()),

    path('v1/listar-cuentas', CuentaListView.as_view()),
    path('v1/buscar-cuentas-numero/<kword>', CuentaSearchForNumber.as_view()),
    path('v1/buscar-cuentas-cliente/<kword>', CuentaSearchForCustomer.as_view()),
    path('v1/crear-cuenta', CuentaCreateView.as_view()),
    path('v1/modificar-eliminar-cuenta/<pk>', CuentaRetrieveView.as_view()),

    path('v1/bloquear-cuenta/', CuentaBloqueoView.as_view()),
]
