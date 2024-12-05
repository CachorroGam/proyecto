from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm

from django.contrib.auth.models import Group

# Crear roles
admin_group, created = Group.objects.get_or_create(name='Administrador')
empleado_group, created = Group.objects.get_or_create(name='Empleado')  # Cambiado de 'Bibliotecario' a 'Empleado'
usuario_group, created = Group.objects.get_or_create(name='Usuario')


def index(request):
    return render(request, 'users/index.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        # Configura la expiración de la sesión si "remember me" está desmarcado
        if not remember_me:
            self.request.session.set_expiry(0)  # Expira al cerrar el navegador
            self.request.session.modified = True

        # Redirige según el grupo del usuario
        user = self.request.user

        if user.groups.filter(name='Administradores').exists():
            # Redirigir a la página de administración si es un Administrador
            messages.success(self.request, '¡Bienvenido Administrador!')
            return redirect('users/dash_admin')  # Cambia por la URL de la página del Administrador

        elif user.groups.filter(name='Empleados').exists():
            # Redirigir a la página de Empleados si es un Empleado
            messages.success(self.request, '¡Bienvenido Empleado!')
            return redirect('users/dash_empleado')  # Cambia por la URL de la página de Empleados

        elif user.groups.filter(name='Lectores').exists():
            # Redirigir a la página de Lectores si es un Lector
            messages.success(self.request, '¡Bienvenido Lector!')
            return redirect('users/dash_lector')  # Cambia por la URL de la página de Lectores

        # Si el usuario no pertenece a ningún grupo específico, redirigir a la página principal
        messages.success(self.request, '¡Bienvenido a la plataforma!')
        return super().form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})




def dash_admin(request):
    return render(request, 'users/dash_admin.html')



def dash_empleado(request):
    # Lógica para la vista del panel de administración
    return render(request, 'users/dash_empleado.html')



def dash_usuario(request):
    # Lógica para la vista del panel de administración
    return render(request, 'users/dash_usuario.html')



from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirigir según el grupo/rol del usuario
            if user.groups.filter(name='Administrador').exists():
                return redirect('dash_admin')
            elif user.groups.filter(name='Empleado').exists():  # Cambiado de 'Bibliotecario' a 'Empleado'
                return redirect('dash_empleado')
            elif user.groups.filter(name='Usuario').exists():
                return redirect('dash_usuario')
            else:
                return render(request, 'sin_permiso.html', {'mensaje': 'No tiene rol asignado'})
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})