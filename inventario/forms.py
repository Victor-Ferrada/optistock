# inventario/forms.py
from django import forms
from .models import Producto, MovimientoStock


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        exclude = ['cepillado']  # Excluye solo el campo cepillado
        widgets = {
            'categoria': forms.Select(attrs={'onchange': 'toggleDimensions()'}),
            'largo': forms.TextInput(attrs={
                'placeholder': 'Metros o Pulgadas', 
                'class': 'form-control',
            }),
            'ancho': forms.TextInput(attrs={
                'placeholder': 'Pulgadas',
                'class': 'form-control',
            }),
            'alto': forms.TextInput(attrs={
                'placeholder': 'Pulgadas',
                'class': 'form-control',
            }),
        }
        help_texts = {
            'especial': '¿Necesita seguimiento especial?',
        }



    def clean(self):
        cleaned_data = super().clean()
        for field in ['largo', 'ancho', 'alto']:
            if not cleaned_data.get(field):
                cleaned_data[field] = None
        return cleaned_data

class MovimientoStockForm(forms.ModelForm):
    class Meta:
        model = MovimientoStock
        fields = ['cantidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class SeteoStockForm(forms.Form):
    nuevo_stock = forms.IntegerField(
        min_value=0,
        label='Nuevo stock',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

class UmbralStockForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['umbral_stock_invierno', 'umbral_stock_verano']  # Solo permite editar estos campos
        widgets = {
            'umbral_stock_invierno': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'umbral_stock_verano': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
        labels = {
            'umbral_stock_invierno': 'Umbral Mínimo de Stock (Invierno)',
            'umbral_stock_verano': 'Umbral Mínimo de Stock (Verano)',
        }




