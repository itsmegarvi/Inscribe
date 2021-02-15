from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
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
        user = self.request.user
        followers = accounts_models.CustomUserFollowing.objects.filter(
            follower=user, user=context["object"]
        ).count()
        buttonClass = "text-info" if followers == 1 else "text-black"
        context["buttonClass"] = buttonClass
        context["followers"] = followers
        return context


class CustomUserDiscoverView(ListView):

    model = accounts_models.CustomUser
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return self.model.objects.filter(first_name__icontains=query)
        else:
            return accounts_models.CustomUser.objects.all()[:10]


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

    model = accounts_models.CustomUserFollowing
    paginate_by = 15
    template_name = "accounts/customuserfollowers_list.html"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        return self.model.objects.filter(
            follower__first_name__icontains=query, user=self.request.user
        )


class FollowingsView(CustomLoginRequiredMixin, ListView):

    model = accounts_models.CustomUserFollowing
    paginate_by = 15
    template_name = "accounts/customuserfollowing_list.html"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        return self.model.objects.filter(
            user__first_name__icontains=query, follower=self.request.user
        )


def toggle_following(request, following_id):
    """When this view receives a request, it will toggle whether the user
    associated with the current request follows the user associated with
    `following_id`."""
    follower = request.user
    following = accounts_models.CustomUser.objects.get(id=following_id)
    if follower == following:
        status = False
        message = "Yoo can not follow yourself!"
        return JsonResponse({"message": message, "status": status}, status=201)
    else:
        try:
            accounts_models.CustomUserFollowing.objects.get(
                follower=follower, user=following
            ).delete()
            status = False
            message = "The user was un-followed successfully!"
        except accounts_models.CustomUserFollowing.DoesNotExist:
            accounts_models.CustomUserFollowing.objects.create(
                user=following, follower=follower
            )
            status = True
            message = "The user was followed successfully!"
    return JsonResponse({"status": status, "message": message})
