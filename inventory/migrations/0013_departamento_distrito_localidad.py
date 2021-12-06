# Generated by Django 3.1 on 2021-12-06 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_pais'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200, unique=True, verbose_name='Descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='Distrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200, unique=True, verbose_name='Descripcion')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.departamento', verbose_name='Departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200, unique=True, verbose_name='Descripcion')),
                ('distrito', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.distrito', verbose_name='Distrito')),
            ],
        ),
    ]