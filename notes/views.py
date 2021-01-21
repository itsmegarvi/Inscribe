from django.views.generic import DetailView, ListView, TemplateView

from . import models


# DO NOT DISTRUB
class NoteCreateView(TemplateView):
    """ This view will handle the creation of notes, and saving them to the database """

    template_name = "notes/create.html"


class NotesListView(ListView):
    """ This view will handle displaying all the notes in the database """

    model = models.Note
    template_name = "notes/list.html"


class NotesDetailView(DetailView):
    """ This view will handle displaying the notes from the database """

    model = models.Note
    template_name = "notes/detail.html"


class PrivateNotesView(ListView):
    """ This view will handle displaying of private notes of the user. """

    model = models.Note
    template_name = "notes/private.html"
<<<<<<< HEAD
=======

>>>>>>> 176fcab4f04b81687e7b4cab634b7c730c37fd4d

class PublicNotesView(ListView):
    """ This view will handle displaying of publicly available notes """

    model = models.Note
    template_name = "notes/public.html"
