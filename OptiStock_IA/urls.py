from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

def pagina_inicio(request):
    if request.user.is_authenticated:
        return redirect('inventario:base')
    return redirect('usuario:login')  # Cambiado para usar el namespace

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pagina_inicio, name='pagina_inicio'),
    path('inventario/', include('inventario.urls', namespace='inventario')),
    path('usuario/', include('usuario.urls', namespace='usuario')),
    path('ventas/', include('ventas.urls', namespace='ventas')),
    path('compras/', include('compras.urls', namespace='compras')),
]

# Agregar configuración para archivos estáticos y media en producción
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)