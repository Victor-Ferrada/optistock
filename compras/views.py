from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
from .forms import CompraForm, DetalleCompraForm
from .models import Compra, DetalleCompra

def registrar_compra(request):
    DetalleFormSet = modelformset_factory(
        DetalleCompra,
        form=DetalleCompraForm,
        extra=1,
        can_delete=False
    )

    if request.method == "POST":
        compra_form = CompraForm(request.POST)
        detalle_formset = DetalleFormSet(request.POST, queryset=DetalleCompra.objects.none())

        if compra_form.is_valid() and detalle_formset.is_valid():
            try:
                with transaction.atomic():
                    compra = compra_form.save(commit=False)
                    total = 0
                    detalles = []

                    if not any(form.cleaned_data for form in detalle_formset):
                        raise ValidationError("Debe agregar al menos un producto a la compra.")

                    for detalle_form in detalle_formset:
                        if detalle_form.cleaned_data:
                            detalle = detalle_form.save(commit=False)
                            producto = detalle.id_prod
                            cantidad = detalle.cantidad
                            precio_uni = detalle.precio_uni

                            subtotal = precio_uni * cantidad
                            total += subtotal

                            # Actualizar stock y precio del producto
                            producto.stock += cantidad
                            # Actualizar el precio del producto con el nuevo precio de compra
                            producto.precio = precio_uni  # Aquí actualizamos el precio
                            producto.save()

                            detalle.id_compra = compra
                            detalles.append(detalle)

                    compra.total = total
                    compra.save()
                    DetalleCompra.objects.bulk_create(detalles)

                    return redirect('compras:lista_compras')

            except ValidationError as e:
                error = str(e)
                return render(request, 'compras/registrar_compra.html', {
                    'compra_form': compra_form,
                    'detalle_formset': detalle_formset,
                    'error': error
                })
    else:
        compra_form = CompraForm()
        detalle_formset = DetalleFormSet(queryset=DetalleCompra.objects.none())

    return render(request, 'compras/registrar_compra.html', {
        'compra_form': compra_form,
        'detalle_formset': detalle_formset,
    })

def lista_compras(request):
    compras = Compra.objects.all().order_by('-fecha')
    return render(request, 'compras/lista_compras.html', {'compras': compras})

def detalle_compra(request, id_compra):
    compra = get_object_or_404(Compra, pk=id_compra)
    detalles = compra.detalles.all().select_related('id_prod')
    return render(request, 'compras/detalle_compra.html', {
        'compra': compra,
        'detalles': detalles
    })
