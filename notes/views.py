import random

from django.views.generic import CreateView, DetailView, ListView
from mixins import CustomLoginRequiredMixin

from . import forms, models


class NoteCreateView(CustomLoginRequiredMixin, CreateView):
    """ This view will handle the creation of notes, and saving them to the database """

    template_name = "notes/create.html"
    form_class = forms.CreateNoteForm

    def form_valid(self, form, *args, **kwargs):
        user = self.request.user
        note = form.save(commit=False)
        note.writer = user
        note.save()
        return super().form_valid(form, *args, **kwargs)


class NotesListView(ListView):
    """ This view will handle displaying all the notes in the database """

    # model = models.Note
    paginate_by = 10
    template_name = "notes/list.html"

    def get_queryset(self, *args, **kwargs):
        qs = models.Note.objects.filter(hidden=False, draft=False)
        return sorted(qs, key=lambda x: random.random())


class NotesDetailView(DetailView):
    """ This view will handle displaying the notes from the database """

    model = models.Note
    template_name = "notes/detail.html"


class PrivateNotesView(ListView):
    """ This view will handle displaying of private notes of the user. """

    paginate_by = 10
    queryset = models.Note.objects.filter(hidden=True).order_by("-updated_at")
    template_name = "notes/private.html"


class PublicNotesView(ListView):
    """ This view will handle displaying of publicly available notes """

    paginate_by = 10
    queryset = models.Note.objects.filter(hidden=False).order_by("-updated_at")
    template_name = "notes/public.html"


class DraftView(ListView):
    """ This view will handle displaying draft notes """

    paginate_by = 10
    queryset = models.Note.objects.filter(draft=True).order_by("-updated_at")
    template_name = "notes/drafts.html"


class BookmarkListView(CustomLoginRequiredMixin, ListView):
    """ This view will handle display of bookmarks """

    paginate_by = 10
    template_name = "notes/bookmarks.html"

    def get_queryset(self, *args, **kwargs):
        bookmarks = models.Bookmark.objects.filter(user=self.request.user)
        return [bookmark.note for bookmark in bookmarks]
