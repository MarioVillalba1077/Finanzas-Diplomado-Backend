from django.urls import path, include
from . import views

urlpatterns = [

    # CLIENTE
    path('crear-cliente/', views.ClienteCreateView.as_view()),
    path('listar-cliente/', views.ClienteListView.as_view()),
    path('editar-cliente/<int:pk>', views.ClienteRetrieveView.as_view()),

    # MONEDA
    path('crear-moneda/', views.MonedaCreateView.as_view()),
    path('listar-moneda/', views.MonedaListView.as_view()),
    path('editar-moneda/<int:pk>/', views.MonedaRetrieveView.as_view()),

    # MOVIMIENTO
    path('listar-movimiento/', views.CuentaListView.as_view()),

    # CUENTA
    path('bloquear-cuenta/<int:pk>', views.CuentaBloqueoView.as_view()),

]