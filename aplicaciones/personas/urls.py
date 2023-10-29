from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_personas, name='listar_personas'),
    path('buscar/', views.buscar_personas, name='buscar_personas'),
    path('crear/', views.crear_persona, name='crear_persona'),
    path('editar_eliminar/<int:persona_id>/', views.editar_eliminar_persona, name='editar_eliminar_persona'),
]
