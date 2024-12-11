from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('registrar/', views.registrar_venta, name='registrar_venta'),
    path('lista/', views.lista_ventas, name='lista_ventas'),
    path('detalle/<int:id_mov>/', views.detalle_venta, name='detalle_venta'),
]
