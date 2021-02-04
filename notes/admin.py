from django.contrib import admin

from . import models


@admin.register(models.Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "hidden", "created_at")
    list_filter = ("hidden",)
    search_fields = ["title", "body", "slug"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(models.Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
