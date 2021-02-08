from django import forms
from markdownx.fields import MarkdownxFormField

from . import models


class CreateNoteForm(forms.ModelForm):
    body = MarkdownxFormField()

    class Meta:
        model = models.Note
        fields = "__all__"
        exclude = ("slug", "writer")


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ("content",)
        widgets = {"content": forms.Textarea(attrs={"style": "resize: none;"})}
