from django.views.generic import CreateView, ListView, TemplateView, DetailView

from . import models


# DO NOT DISTRUB
class NoteCreateView(TemplateView):
    """ This view will handle the creation of notes, and saving them to the database """

    template_name = "notes/create.html"


class NotesListView(ListView):
    """ This view will handle displaying all the notes in the database """

    model = models.Notes
    template_name = "notes/list.html"


class NotesDetailView(DetailView):
    """ This view will handle displaying the notes from the database """

    model = models.Notes
    template_name = "detail.html"


class PrivateNotesView(ListView):
    """ This view will handle displaying of private notes of the user. """

    model = models.Notes
    template_name = "private.html"

class PublicNotesView(ListView):
    """ This view will handle displaying of publicly available notes """

    model = models.Notes
    template_name = "public.html"
