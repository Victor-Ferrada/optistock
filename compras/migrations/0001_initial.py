# Generated by Django 5.1.3 on 2024-12-12 00:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0003_alter_producto_umbral_stock_invierno_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id_compra', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('proveedor', models.CharField(max_length=100)),
                ('rut_usu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleCompra',
            fields=[
                ('num_transac', models.AutoField(primary_key=True, serialize=False)),
                ('precio_uni', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cantidad', models.PositiveIntegerField()),
                ('id_compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='compras.compra')),
                ('id_prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.producto', verbose_name='Producto')),
            ],
        ),
    ]