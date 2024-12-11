# inventario/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction  # Añade esta importación
from django.utils.timezone import now  # Añade esta importación
from .models import Producto, MovimientoStock
from .forms import ProductoForm, MovimientoStockForm, SeteoStockForm  # Añade SeteoStockForm aquí
from .forms import UmbralStockForm
from django.forms import modelformset_factory


def base_view(request):
    return render(request, 'inventario/index.html')

# 1. Registrar un producto
def registrar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.umbral_stock_invierno = 10  # Valor por defecto
            producto.umbral_stock_verano = 5     # Valor por defecto
            producto.save()
            messages.success(request, f'Producto "{producto.nombre}" registrado con éxito.')
            return redirect('inventario:lista_productos')
        else:
            print("Errores del formulario:", form.errors)
    else:
        form = ProductoForm()
    
    return render(request, 'inventario/registrar_producto.html', {'form': form})


# 2. Actualizar stock
def seleccionar_producto_actualizar(request):
    productos = Producto.objects.all()

    # Filtros opcionales
    categoria = request.GET.get('categoria')
    nombre = request.GET.get('nombre')
    cepillado = request.GET.get('cepillado')

    if categoria:
        productos = productos.filter(categoria=categoria)
    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    if cepillado:
        productos = productos.filter(cepillado=(cepillado == 'true'))

    return render(request, 'inventario/seleccionar_producto_actualizar.html', {'productos': productos})



def actualizar_stock(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = SeteoStockForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Guardamos el stock anterior para el registro
                    stock_anterior = producto.stock
                    nuevo_stock = form.cleaned_data['nuevo_stock']
                    
                    # Creamos un registro del cambio
                    MovimientoStock.objects.create(
                        producto=producto,
                        cantidad=nuevo_stock - stock_anterior,  # La diferencia como movimiento
                        fecha=now()
                    )
                    
                    # Actualizamos el stock
                    producto.stock = nuevo_stock
                    producto.save()
                    
                    messages.success(
                        request, 
                        f'Stock actualizado correctamente. '
                        f'Stock anterior: {stock_anterior}, '
                        f'Nuevo stock: {nuevo_stock}'
                    )
                    return redirect('inventario:seleccionar-producto-actualizar')
                    
            except Exception as e:
                messages.error(request, f'Error al actualizar el stock: {str(e)}')
    else:
        form = SeteoStockForm(initial={'nuevo_stock': producto.stock})

    return render(request, 'inventario/actualizar_stock.html', {
        'form': form, 
        'producto': producto
    })

    # Actualizar el formulario con información del stock actual
    form.fields['cantidad'].widget.attrs.update({
        'placeholder': f'Stock actual: {producto.stock}',
        'class': 'form-control'
    })
    form.fields['cantidad'].label = 'Cantidad a modificar (use números negativos para disminuir)'

    context = {
        'form': form,
        'producto': producto
    }

    return render(request, 'inventario/actualizar_stock.html', context)


# 3. Generar alerta de stock.
def generar_alerta_stock(request):
    from django.utils import timezone
    
    # Determinar la estación actual
    mes_actual = timezone.now().month
    
    # Definir meses de invierno y verano (hemisferio sur)
    meses_invierno = [6, 7, 8]  # Junio, Julio, Agosto
    meses_verano = [12, 1, 2]   # Diciembre, Enero, Febrero
    
    # Productos con stock bajo según la estación
    productos_bajo_stock = []
    
    for producto in Producto.objects.all():
        # Determinar el umbral actual según la estación
        if mes_actual in meses_invierno:
            umbral = producto.umbral_stock_invierno
        elif mes_actual in meses_verano:
            umbral = producto.umbral_stock_verano
        else:
            # Para meses intermedios, usar un umbral intermedio
            umbral = (producto.umbral_stock_invierno + producto.umbral_stock_verano) // 2
        
        # Verificar si el stock está por debajo del umbral
        if producto.stock <= umbral:
            productos_bajo_stock.append({
                'producto': producto,
                'stock_actual': producto.stock,
                'umbral': umbral,
                'umbral_invierno': producto.umbral_stock_invierno,
                'umbral_verano': producto.umbral_stock_verano
            })
    
    # Ordenar productos por stock más bajo
    productos_bajo_stock.sort(key=lambda x: x['stock_actual'])
    
    context = {
        'productos_bajo_stock': productos_bajo_stock,
        'total_alertas': len(productos_bajo_stock),
        'estacion_actual': 'Invierno' if mes_actual in meses_invierno else 'Verano' if mes_actual in meses_verano else 'Temporada intermedia'
    }
    
    return render(request, 'inventario/alerta_stock.html', context)

def editar_umbrales_stock(request):
    productos = Producto.objects.all()
    
    if request.method == 'POST':
        for producto in productos:
            form = UmbralStockForm(request.POST, instance=producto, prefix=str(producto.id))
            if form.is_valid():
                form.save()
                print(f"Formulario guardado para {producto.nombre}")
            else:
                print(f"Errores en el formulario de {producto.nombre}: {form.errors}")
                # Agregar el error al mensaje para mostrarlo al usuario
                messages.error(request, f"Error al guardar el producto {producto.nombre}: {form.errors}")
        
        messages.success(request, 'Umbrales de stock actualizados correctamente.')
        return redirect('inventario:editar-umbrales-de-stock')
    
    formset = [UmbralStockForm(instance=producto, prefix=str(producto.id)) for producto in productos]
    
    return render(request, 'inventario/editar_umbrales_stock.html', {
        'formset': formset,
        'productos': productos
    })


# 4. Registrar procesos adicionales (cepillado).
def seleccionar_producto_para_cepillar(request):
    # Obtener filtros desde la solicitud GET
    categoria = request.GET.get('categoria', '')
    nombre = request.GET.get('nombre', '')

    # Filtrar productos
    productos = Producto.objects.filter(categoria='Madera')  # Solo mostrar productos de la categoría Madera
    if categoria:
        productos = productos.filter(categoria=categoria)
    if nombre:
        productos = productos.filter(nombre__icontains=nombre)

    return render(request, 'inventario/selectar_producto_para_cepillar.html', {'productos': productos})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Producto

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Producto

def registrar_proceso_cepillado(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if producto.categoria != 'Madera':
        messages.error(request, 'Solo se pueden registrar procesos de cepillado en productos de la categoría Madera.')
        return redirect('inventario:selectar_producto_para_cepillar')
    
    # Nueva validación para productos ya cepillados
    if producto.cepillado:
        messages.error(request, 'Este producto ya ha sido cepillado previamente.')
        return redirect('inventario:selectar_producto_para_cepillar')
    
    if request.method == 'POST':
        cantidad_cepillar = int(request.POST.get('cantidad', 0))
        stock_original = producto.stock  # Guardamos el stock original para validación
        
        if cantidad_cepillar <= 0:
            messages.error(request, 'La cantidad debe ser mayor a 0.')
        elif cantidad_cepillar > stock_original:
            messages.error(request, f'No hay suficiente stock. Solo hay {stock_original} disponibles.')
        else:
            # Reducir el stock del producto original
            nuevo_stock_original = stock_original - cantidad_cepillar
            producto.stock = nuevo_stock_original
            
            # Solo marcar como cepillado si todo el stock fue cepillado
            if nuevo_stock_original == 0:
                producto.cepillado = True
            
            producto.save()
            
            # Crear o actualizar el producto cepillado
            nombre_cepillado = f"{producto.nombre} CEPI"
            
            producto_cepillado, creado = Producto.objects.get_or_create(
                nombre=nombre_cepillado,
                categoria=producto.categoria,
                cepillado=True,
                defaults={
                    'stock': 0,
                    'precio': producto.precio + 3000,
                    'largo': producto.largo,
                    'ancho': producto.ancho,
                    'alto': producto.alto
                }
            )
            
            # Actualizar las dimensiones y precio solo si es necesario
            if not creado:
                if (producto_cepillado.largo != producto.largo or 
                    producto_cepillado.ancho != producto.ancho or 
                    producto_cepillado.alto != producto.alto or 
                    producto_cepillado.precio != producto.precio + 3000):
                    
                    producto_cepillado.largo = producto.largo
                    producto_cepillado.ancho = producto.ancho
                    producto_cepillado.alto = producto.alto
                    producto_cepillado.precio = producto.precio + 3000
            
            # Añadir el stock cepillado
            producto_cepillado.stock += cantidad_cepillar
            producto_cepillado.save()
            
            messages.success(
                request, 
                f"Se han cepillado {cantidad_cepillar} unidad(es). "
                f"Stock original restante: {nuevo_stock_original}. "
                f"Stock producto cepillado: {producto_cepillado.stock}"
            )
        
        return redirect('inventario:selectar_producto_para_cepillar')
    
    return render(request, 'inventario/registrar_proceso_cepillado.html', {'producto': producto})



# 5. Visualizar y filtrar productos.

def lista_productos(request):
    productos = Producto.objects.all()

    # Filtros
    categoria = request.GET.get('categoria')
    nombre = request.GET.get('nombre')
    cepillado = request.GET.get('cepillado')

    if categoria:
        productos = productos.filter(categoria=categoria)
    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    if cepillado:
        productos = productos.filter(cepillado=(cepillado == 'true'))

    return render(request, 'inventario/lista_productos.html', {'productos': productos})


# 6. Registrar productos especiales.

def registrar_producto_especial(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            if producto.categoria != 'Especial':
                messages.error(request, 'Solo se pueden registrar productos especiales en esta funcionalidad.')
            else:
                producto.especial = True
                producto.save()
                messages.success(request, 'Producto especial registrado con éxito.')
                return redirect('inventario:lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'inventario/registrar_producto_especial.html', {'form': form})

