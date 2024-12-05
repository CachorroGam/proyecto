from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import MinLengthValidator
from django.utils import timezone

# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=50, 
        choices=[
            ('Administrador', 'Administrador'), 
            ('Lector', 'Lector'),
            ('Empleado', 'Empleado')
        ], 
        default='Lector'
    )
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)



class Libro(models.Model):
    TITULO_MAX_LENGTH = 200
    AUTOR_MAX_LENGTH = 100
    GENERO_MAX_LENGTH = 50
    ISBN_MAX_LENGTH = 13  # ISBN-13 tiene 13 dígitos
    DESCRIPCION_MAX_LENGTH = 1000

    titulo = models.CharField(max_length=TITULO_MAX_LENGTH)
    autor = models.CharField(max_length=AUTOR_MAX_LENGTH)
    genero = models.CharField(max_length=GENERO_MAX_LENGTH)
    fecha_publicacion = models.DateField()
    isbn = models.CharField(
        max_length=ISBN_MAX_LENGTH,
        unique=True,
        validators=[MinLengthValidator(10)],  # Asegura que el ISBN tenga al menos 10 caracteres
    )
    descripcion = models.TextField(max_length=DESCRIPCION_MAX_LENGTH, blank=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo



class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)  # Usamos DateTimeField para la fecha y hora exacta
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=10, choices=[('prestado', 'Prestado'), ('devuelto', 'Devuelto')], default='prestado'
    )
    dias_prestamo = models.PositiveIntegerField(default=14)  # Cantidad de días que puede durar el préstamo

    def marcar_devuelto(self):
        self.estado = 'devuelto'
        self.fecha_devolucion = timezone.now()
        self.save()

    def esta_vencido(self):
        """Método para saber si el préstamo ha vencido"""
        if self.estado == 'prestado' and self.fecha_devolucion is None:
            return timezone.now() > self.fecha_prestamo + timezone.timedelta(days=self.dias_prestamo)
        return False

    def __str__(self):
        return f'{self.usuario.username} - {self.libro.titulo}'


class Lector(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numero_membresia = models.CharField(max_length=20, unique=True, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)  # Cambio a DateTimeField
    estado_membresia = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username



class Auditoria(models.Model):
    accion = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    detalles = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.accion} por {self.usuario.username} en {self.fecha}"



