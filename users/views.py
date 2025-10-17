from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from .forms import CustomUserCreationForm

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=True)  # save user to DB
        login(self.request, user)  # optionally log in
        print("✅ USER SAVED:", user.username)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("❌ FORM INVALID:", form.errors)
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    template_name = "users/logout.html"
    next_page = reverse_lazy("login")  # redirect after logout
