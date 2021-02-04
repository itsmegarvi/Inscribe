from django import forms
from markdownx.fields import MarkdownxFormField

from . import models
from .models import Comment

class CreateNoteForm(forms.ModelForm):
    body = MarkdownxFormField()

    class Meta:
        model = models.Note
        fields = "__all__"
        exclude = ("slug", "writer")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user', 'posted_on', 'content', 'parent')
