from django.contrib import admin

from . import models


class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'hidden','created_at')
    list_filter = ("hidden",)
    search_fields = ['title', 'body', 'slug']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(models.Note, NoteAdmin)

class BookmarkAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Bookmark, BookmarkAdmin)
