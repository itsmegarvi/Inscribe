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
    list_display = ('user', 'content', 'note', 'posted_on', 'active')
    list_filter = ('active', 'posted_on')
    search_fields = ('user', 'content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)