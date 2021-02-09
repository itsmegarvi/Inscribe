from django.urls import path

from . import views

app_name = "notes"

urlpatterns = [
    path("create/", views.NoteCreateView.as_view(), name="create"),
    path("list/", views.NotesListView.as_view(), name="list"),
    path("private/", views.PrivateListView.as_view(), name="private"),
    path("public/", views.PublicListView.as_view(), name="public"),
    path("bookmarks/", views.BookmarkListView.as_view(), name="bookmarks"),
    path("drafts/", views.DraftListView.as_view(), name="drafts"),
    path("toggle-bookmark/", views.toggle_bookmark_view, name="toggle-bookmark"),
    path("<slug:slug>/", views.note_detail, name="detail"),
]
