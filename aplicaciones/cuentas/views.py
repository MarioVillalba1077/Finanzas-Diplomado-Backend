from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from aplicaciones.cuentas.serializers import *
from aplicaciones.cuentas.models import Cliente, Persona



"""
    MONEDA
        Create, Read, Update, Destroy
"""

class MonedaCreateView(CreateAPIView):
    serializer_class = MonedaSerializers

class MonedaListView(ListAPIView):
    queryset = Moneda.objects.all()
    serializer_class = MonedaSerializers

class MonedaSearchView(ListAPIView):
    serializer_class = MonedaSerializers

    def get_queryset(self):
        return Moneda.objetcs.filter(
            descripcion__icontains=self.kwargs['kword']
        )

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

