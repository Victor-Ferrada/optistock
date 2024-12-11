from django.urls import path
from . import views

app_name = 'inventario'
urlpatterns = [
    path('base/', views.base_view, name='base'),
    path('registrar-producto/', views.registrar_producto, name='registrar_producto'),
    path('alerta-stock/', views.generar_alerta_stock, name='alerta_stock'),
    path('registrar-cepillado/<int:producto_id>/', views.registrar_proceso_cepillado, name='registrar_proceso_cepillado'),
    path('lista-productos/', views.lista_productos, name='lista_productos'),
    path('registrar-producto-especial/', views.registrar_producto_especial, name='registrar_producto_especial'),
    path('seleccionar-producto-actualizar/', views.seleccionar_producto_actualizar, name='seleccionar-producto-actualizar'),
    path('actualizar-stock/<int:producto_id>/', views.actualizar_stock, name='actualizar_stock'),
    path('editar-umbrales-de-stock/', views.editar_umbrales_stock, name='editar-umbrales-de-stock'),
    path('selectar_producto_para_cepillar/', views.seleccionar_producto_para_cepillar, name='selectar_producto_para_cepillar'),
]