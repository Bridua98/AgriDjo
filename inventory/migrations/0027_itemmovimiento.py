# Generated by Django 3.1 on 2022-01-05 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0026_auto_20220103_1952'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemMovimiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Cantidad')),
                ('costo', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Costo')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Precio')),
                ('fechaDocumento', models.DateField(verbose_name='Fecha Documento')),
                ('secuenciaOrigen', models.IntegerField()),
                ('detalleSecuenciaOrigen', models.IntegerField()),
                ('esVigente', models.BooleanField(default=True, verbose_name='Vigente?')),
                ('tipoMovimiento', models.CharField(choices=[('CM', 'COMPRAS'), ('VT', 'VENTAS'), ('A+', 'AJUSTES STOCK +'), ('A-', 'AJUSTES STOCK -'), ('AC', 'ACOPIOS'), ('AA', 'ACTIVIDADES AGRICOLAS')], max_length=50)),
                ('deposito', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.deposito', verbose_name='Deposito')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.item', verbose_name='Item')),
            ],
        ),
    ]