# Generated by Django 3.1 on 2022-01-28 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0037_transferenciacuenta'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferenciacuenta',
            name='comprobante',
            field=models.CharField(default='', max_length=15, verbose_name='Comprobante'),
        ),
    ]