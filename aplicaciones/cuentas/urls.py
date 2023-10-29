from django.urls import path, include
from .views import *

urlpatterns = [
    path('v1/transferencias', TransferenciaView.as_view()),
    path('v1/retiro', RetiroView.as_view()),
]
