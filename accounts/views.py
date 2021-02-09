from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, UpdateView)
from mixins import CustomLoginRequiredMixin
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
        context["followers"] = accounts_models.CustomUserFollowing.objects.filter(
            user=context["object"]
        ).count()
        return context


class CustomUserDiscoverView(ListView):

    model = accounts_models.CustomUser
    paginate_by=20

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(first_name__icontains=query                )
            return object_list
        else:
            return (
                accounts_models.CustomUser.objects.all()[:10]                )


class ProfileView(CustomLoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"


class CustomUserUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = accounts_models.CustomUser
    fields = ("first_name", "last_name", "username", "email")

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("accounts:info", kwargs={"pk": self.object.pk})


@login_required
def password_change_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was updated successfully!")
            return redirect(reverse("accounts:password-change-done"))
        else:
            messages.info(request, "Please correct the errors below ")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "accounts/password-change.html", {"form": form})


class CustomUserPasswordChangeDoneView(
    CustomLoginRequiredMixin, auth_views.PasswordChangeDoneView
):
    template_name = "accounts/password-change-done.html"


class FollowersView(CustomLoginRequiredMixin, ListView):
    paginate_by = 15
    template_name = "accounts/customuserfollowers_list.html"

    def get_queryset(self, *args, **kwargs):
        return accounts_models.CustomUserFollowing.objects.filter(user=self.request.user)


class FollowingsView(CustomLoginRequiredMixin, ListView):
    paginate_by = 15
    template_name = "accounts/customuserfollowing_list.html"

    def get_queryset(self, *args, **kwargs):
        return accounts_models.CustomUserFollowing.objects.filter(
            follower=self.request.user
        )
