from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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

