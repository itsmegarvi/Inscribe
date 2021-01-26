from django.views.generic import DetailView, ListView, TemplateView

from . import models


# DO NOT DISTRUB
class NoteCreateView(TemplateView):
    """ This view will handle the creation of notes, and saving them to the database """

    template_name = "notes/create.html"


class NotesListView(ListView):
    """ This view will handle displaying all the notes in the database """

    model = models.Note
    paginate_by = 10
    template_name = "notes/list.html"


class NotesDetailView(DetailView):
    """ This view will handle displaying the notes from the database """

    model = models.Note
    template_name = "notes/detail.html"


class PrivateNotesView(ListView):
    """ This view will handle displaying of private notes of the user. """

    paginate_by = 10
    queryset = models.Note.objects.filter(hidden = True).order_by("-updated_at")
    template_name = "notes/private.html"


class PublicNotesView(ListView):
    """ This view will handle displaying of publicly available notes """

    paginate_by = 10
    queryset = models.Note.objects.filter(hidden = False).order_by("-updated_at")
    template_name = "notes/public.html"


class DraftView(ListView):
    """ This view will handle displaying draft notes """

    paginate_by = 10
    queryset = models.Note.objects.filter(draft = True).order_by("-updated_at")
    template_name = "notes/drafts.html"


class BookmarkListView(ListView):
    """ This view will handle display of bookmarks """

    paginate_by = 10
    template_name = "notes/bookmarks.html"

    def get_queryset(self, *args, **kwargs):
        bookmarks = models.Bookmark.objects.filter(user = self.request.user)
        notes = []
        for bookmark in bookmarks:
            notes.append(bookmark.note)
        print(notes)
        return notes
