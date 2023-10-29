from django.urls import path
from . import views

urlpatterns = [
    path('listar/', views.listar_ciudades, name='listar_ciudades'),
    path('buscar/', views.buscar_ciudades, name='buscar_ciudades'),
    path('crear/', views.crear_ciudad, name='crear_ciudad'),
    path('editar_eliminar/<int:ciudad_id>/', views.editar_eliminar_ciudad, name='editar_eliminar_ciudad'),
]
