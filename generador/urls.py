from django.urls import path
from .views import generar_contrato, descargar_contrato, historial_contratos

urlpatterns = [
    path('', generar_contrato, name='generar_contrato'),
    path('descargar/<int:contrato_id>/', descargar_contrato, name='descargar_contrato'),
    path('historial/', historial_contratos, name='historial_contratos')
]