from django.db import models
from django.utils.timezone import now

class Producto(models.Model):
    CATEGORIAS = [
        ('Madera', 'Madera'),
        ('Planchas', 'Planchas'),
        ('Otros', 'Otros'),
        ('Especial', 'Especial'),
    ]

    ESTACIONES = [
        ('invierno', 'Invierno'),
        ('verano', 'Verano'),
    ]

    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.PositiveIntegerField()
    
    # Nuevos campos para umbrales de stock
    umbral_stock_invierno = models.PositiveIntegerField(default=10, blank=True, null=True)
    umbral_stock_verano = models.PositiveIntegerField(default=5, blank=True, null=True)
    
    largo = models.FloatField(blank=True, null=True)
    ancho = models.FloatField(blank=True, null=True)
    alto = models.FloatField(blank=True, null=True)
    cepillado = models.BooleanField(default=False)
    especial = models.BooleanField(default=False)

    def get_umbral_actual(self):
        """
        Determina el umbral de stock según la estación actual
        """
        from django.utils import timezone
        mes_actual = timezone.now().month
        
        # Define los meses de invierno y verano (hemisferio sur)
        meses_invierno = [6, 7, 8]  # Junio, Julio, Agosto
        meses_verano = [12, 1, 2]   # Diciembre, Enero, Febrero
        
        if mes_actual in meses_invierno:
            return self.umbral_stock_invierno
        elif mes_actual in meses_verano:
            return self.umbral_stock_verano
        else:
            # Para meses intermedios, usar un umbral intermedio
            return (self.umbral_stock_invierno + self.umbral_stock_verano) // 2

    def esta_bajo_minimo(self):
        """
        Verifica si el stock está por debajo del umbral actual
        """
        return self.stock <= self.get_umbral_actual()

    def __str__(self):
        return self.nombre

class MovimientoStock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()  # Cantidad a aumentar o disminuir
    fecha = models.DateTimeField(default=now)  # Fecha y hora de la operación

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades"
