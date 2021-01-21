from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from notes import models as notes_models

from . import forms
from . import models as accounts_models


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"


class LogoutView(auth_views.LogoutView):
    template_name = "accounts/logout.html"


class CustomUserCreateView(CreateView):
    template_name = "accounts/register.html"
    form_class = forms.RegistrationForm
    success_message = "You can now login with your new credentials"
    success_url = reverse_lazy("accounts:login")


class CustomUserDetailView(DetailView):
    model = accounts_models.CustomUser

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["notes"] = notes_models.Note.objects.filter(writer=context["object"])
        context["followers"] = accounts_models.UserFollowing.objects.filter(
            user=context["object"]
        ).count()
        return context
