# Generated by Django 5.0.8 on 2024-12-03 03:29

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_libro_reservado_por'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='estado_membresia',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='libro',
            name='fecha_registro',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='libro',
            name='numero_membresia',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.DeleteModel(
            name='Lector',
        ),
    ]
