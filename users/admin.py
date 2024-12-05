from django.contrib import admin
from .models import Profile, Libro, Prestamo, Lector

admin.site.register(Profile)
# Registra los modelos
admin.site.register(Libro)
admin.site.register(Prestamo)
admin.site.register(Lector)
