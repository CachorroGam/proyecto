# Generated by Django 5.0.8 on 2024-12-03 13:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_genero_libros'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='prestamo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='libros_prestados', to='users.prestamo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='libro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prestamos_libro', to='users.libro'),
        ),
    ]
