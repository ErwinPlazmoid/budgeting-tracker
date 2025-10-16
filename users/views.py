from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")

class CustomLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    template_name = "users/logout.html"
    next_page = reverse_lazy("login")  # redirect after logout
