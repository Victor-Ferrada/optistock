from django import forms
from .models import Movimiento, Producto
from django import forms
from .models import Detalle

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['tipo', 'rut_usu']  # Ajusta los campos según tu modelo

class ProductoCantidadForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), label="Producto")
    cantidad = forms.IntegerField(min_value=1, label="Cantidad")

class DetalleForm(forms.ModelForm):
    class Meta:
        model = Detalle
        fields = ['id_prod', 'cantidad']