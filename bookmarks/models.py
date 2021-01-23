from django.db import models
from django.utils.translation import gettext as _
from notes.models import Note


class Bookmark(models.model):
    note = models.ForeignKey(
    "Note",
    on_delete=models.PROTECT
)
    saved = models.BooleanField(
    default=False,
    help_text=_("Wether the note will be in bookmarks or not ")
)
