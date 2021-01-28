from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _
from markdownx.utils import markdownify


class Note(models.Model):
    title = models.CharField(
        max_length=100, unique=True, help_text=_("The title of the note")
    )
    writer = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        help_text=_("Author of the note"),
    )
    description = models.CharField(
        max_length=200,
        help_text=_(
            "A brief description of the note that will be displayed in the note preview."
        ),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text=_("The date and time the note was published at")
    )
    body = models.TextField(help_text=_("Main body of the note"))
    draft = models.BooleanField(
        default=False,
        help_text=_("Whether the note is a to be saved as a draft or published"),
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text=_("The date and time the note was updated at")
    )
    hidden = models.BooleanField(
        default=False, help_text=_("Whether the file will be visible to other people")
    )
    slug = models.SlugField(
        max_length=200, unique=True, help_text=_("The unique slug to the note")
    )

    # Create a property that returns the markdown instead
    @property
    def formatted_markdown(self):
        return markdownify(self.body)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("notes:detail", kwargs={"slug": self.slug})


class Comment(models.Model):
    note = models.ForeignKey(
        "notes.Note", on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
    )
    content = models.TextField(help_text=_("The comment is written in here"))
    posted_on = models.DateTimeField(
        auto_now_add=True, help_text=_("The time comment was posted")
    )
    parent = models.ForeignKey(
        "notes.Comment",
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE,
    )
    active = models.BooleanField(
        default="True", help_text=_("Allows to remove unwanted comments via admin page")
    )

    class Meta:
        ordering = ["-posted_on"]

    def __str__(self):
        return "Comment {} by {}".format(self.user.username, self.body)


class Bookmark(models.Model):
    note = models.ForeignKey(
        "notes.Note", on_delete=models.CASCADE, help_text=_("Note that is bookmarked")
    )
    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        help_text=_("User deleted then so does this post"),
    )

    def __str__(self):
        return f"{self.note} liked by {self.user.full_name()}"
