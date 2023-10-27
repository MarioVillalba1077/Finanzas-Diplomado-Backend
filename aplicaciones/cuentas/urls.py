from django.urls import path, include
from .views import *

urlpatterns = [
    path('v1/transferencia', TransferenciaView.as_view()),
    path('v1/retiro', RetiroView.as_view()),
    path('v1/deposito', DepositoView.as_view()),
]
