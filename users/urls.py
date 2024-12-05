from django.urls import path
from .views import index, profile, RegisterView
from .views import CustomLoginView
from .views import dash_admin, dash_empleado, dash_usuario
from . import views  # Esto importa el archivo views.py en el directorio actual
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('dash_admin/', views.dash_admin, name='dash_admin'),
    path('dash_usuario/', views.dash_usuario, name='dash_usuario'),
    path('dash_empleado/', views.dash_empleado, name='dash_empleado'), # Página del Lector
    path('login/', views.login_view, name='login'),
]
