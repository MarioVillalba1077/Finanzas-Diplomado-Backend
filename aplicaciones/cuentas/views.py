from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from aplicaciones.cuentas.serializers import *
from aplicaciones.cuentas.models import Cliente, Persona



"""
    CLIENTE
        Create, Read, Update, Destroy
"""

class ClienteCreateView(CreateAPIView):
    serializer_class = ClienteSerializers

class ClienteListView(ListAPIView):
        queryset = Cliente.objects.all()
        serializer_class = ClienteSerializers

class ClienteSearchView(ListAPIView):
    serializer_class = ClienteSerializers

    def get_queryset(self):
        # Obtener el valor ingresado desde el request
        kword = self.kwargs['kword']

        # Filtrar clientes que coincidan con un nombre o apellido de la tabla persona
        return Cliente.objects.filter(
            Q(persona__nombre__icontains=kword) | Q(persona__apellido__icontains=kword)
        )

class ClienteRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializers