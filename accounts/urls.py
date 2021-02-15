from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("followers/", views.FollowersView.as_view(), name="followers"),
    path("following/", views.FollowingsView.as_view(), name="following"),
    path("register/", views.CustomUserCreateView.as_view(), name="register"),
    path("info/<int:pk>/", views.CustomUserDetailView.as_view(), name="info"),
    path("discover/", views.CustomUserDiscoverView.as_view(), name="discover"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("update/<int:pk>/", views.CustomUserUpdateView.as_view(), name="update"),
    path(
        "password-change/",
        views.password_change_view,
        name="password-change",
    ),
    path(
        "password-change-done/",
        views.CustomUserPasswordChangeDoneView.as_view(),
        name="password-change-done",
    ),
    path("follow/<int:following_id>/", views.toggle_following, name="toggle-following"),
]
