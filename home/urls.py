from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("discover/", views.DiscoverView.as_view(), name="discover"),
    path("faq/", views.FAQView.as_view(), name="faq"),
]
