from django.urls import path

from . import views

app_name = "notes"

urlpatterns = [
    path("create/", views.NoteCreateView.as_view(), name="create"),
    path("list/", views.NotesListView.as_view(), name="list"),
    path("private/", views.PrivateNotesView.as_view(), name="private-list"),
    path("public/", views.PublicNotesView.as_view(), name="public-list"),
    path("bookmarks/", views.BookmarkListView.as_view(), name="bookmarks"),
    path("drafts/", views.DraftView.as_view(), name="drafts"),
    path("<slug:slug>/", views.NotesDetailView.as_view(), name="detail"),
]
