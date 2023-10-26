from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from aplicaciones.cuentas.serializers import *
from aplicaciones.cuentas.models import *

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