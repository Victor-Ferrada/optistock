from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
from .forms import MovimientoForm, DetalleForm
from .models import Movimiento, Detalle
from inventario.models import Producto









def lista_ventas(request):
    ventas = Movimiento.objects.filter(tipo='VENTA')
    return render(request, 'ventas/lista_ventas.html', {'ventas': ventas})

def detalle_venta(request, id_mov):
    venta = get_object_or_404(Movimiento, pk=id_mov, tipo='VENTA')
    detalles = venta.detalles.all().select_related('id_prod')  # Optimización con select_related
    return render(request, 'ventas/detalle_venta.html', {
        'venta': venta,
        'detalles': detalles
    })


def registrar_venta(request):
    DetalleFormSet = modelformset_factory(
        Detalle, 
        form=DetalleForm, 
        extra=1, 
        can_delete=False
    )

    if request.method == "POST":
        mov_form = MovimientoForm(request.POST)
        detalle_formset = DetalleFormSet(request.POST, queryset=Detalle.objects.none())

        if mov_form.is_valid() and detalle_formset.is_valid():
            try:
                with transaction.atomic():
                    movimiento = mov_form.save(commit=False)
                    total = 0
                    detalles = []

                    # Verificar que al menos hay un producto
                    if not any(form.cleaned_data for form in detalle_formset):
                        raise ValidationError("Debe agregar al menos un producto a la venta.")

                    for detalle_form in detalle_formset:
                        if detalle_form.cleaned_data:
                            detalle = detalle_form.save(commit=False)
                            producto = detalle.id_prod
                            cantidad = detalle.cantidad

                            # Validar stock disponible
                            if producto.stock < cantidad:
                                raise ValidationError(
                                    f"Stock insuficiente para {producto.nombre}. "
                                    f"Stock disponible: {producto.stock}, requerido: {cantidad}."
                                )

                            detalle.precio_uni = producto.precio
                            subtotal = producto.precio * cantidad
                            total += subtotal

                            producto.stock -= cantidad
                            producto.save()

                            detalle.id_mov = movimiento
                            detalles.append(detalle)

                    movimiento.total = total
                    movimiento.save()
                    Detalle.objects.bulk_create(detalles)

                    return redirect('ventas:lista_ventas')

            except ValidationError as e:
                error = str(e)
                return render(request, 'ventas/registrar_venta.html', {
                    'mov_form': mov_form,
                    'detalle_formset': detalle_formset,
                    'error': error
                })
    else:
        mov_form = MovimientoForm()
        detalle_formset = DetalleFormSet(queryset=Detalle.objects.none())

    return render(request, 'ventas/registrar_venta.html', {
        'mov_form': mov_form,
        'detalle_formset': detalle_formset,
    })




