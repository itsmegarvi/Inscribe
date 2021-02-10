from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from mixins import CustomLoginRequiredMixin

from . import forms, models

USER_MODEL = get_user_model()


class NoteCreateView(CustomLoginRequiredMixin, CreateView):
    """ This view will handle the creation of notes, and saving them to the database """

    template_name = "notes/create.html"
    form_class = forms.NoteCreateOrUpdateForm

    def form_valid(self, form, *args, **kwargs):
        user = self.request.user
        note = form.save(commit=False)
        note.writer = user
        note.save()
        return super().form_valid(form, *args, **kwargs)


class NotesListView(ListView):
    """ This view will handle displaying all the notes in the database """

    model = models.Note
    paginate_by = 10
    template_name = "notes/list.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return self.model.objects.filter(title__icontains=query)
        else:
            return (
                models.Note.objects.annotate(count=Count("bookmark__id"))
                .order_by("-count")
                .filter(hidden=False, draft=False)
            )
        # return sorted(qs, key=lambda x: random.random())


def note_detail(request, slug):
    """This view will display a note and then all the comments associated
    with it. A form to post a comment on the note will be available only to
    logged in users. On submission, the page will be reloaded with either a
    success or an error message depending on whether the comment was
    posted successfully."""

    note = get_object_or_404(models.Note, slug=slug)
    comments = models.Comment.objects.filter(note=note, active=True)
    bookmarks = models.Bookmark.objects.filter(note=note).count()
    user = request.user
    # this class will be applied to the `like` icon and hence it has to be dynamically
    # set depending on whether the current user has bookmarked this note or not
    if not user.is_authenticated:
        buttonClass = "text-info"
    elif models.Bookmark.objects.filter(note=note, user=user).count() == 1:
        buttonClass = "button-liked"
    else:
        buttonClass = "text-info"
    if request.method == "POST":
        comment_form = forms.CommentForm(request.POST or None)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.note = note
            comment.user = request.user
            comment.save()
            messages.add_message(
                request, messages.SUCCESS, "Your comment was posted successfully!"
            )
            # reset the form to make sure that the previously filled in data is
            # not re-rendered
            comment_form = forms.CommentForm()
        else:
            messages.add_message(
                request, messages.ERROR, "There was an error, please try again..."
            )
    else:
        comment_form = forms.CommentForm()
    context = {
        "note": note,
        "comments": comments,
        "bookmarks": bookmarks,
        "comment_form": comment_form,
        "buttonClass": buttonClass,
    }
    return render(request, "notes/detail.html", context)


class PrivateListView(ListView):
    """ This view will handle displaying of private notes of the user. """

    paginate_by = 10
    queryset = models.Note.objects.filter(hidden=True).order_by("-updated_at")
    template_name = "notes/private.html"

    def get_queryset(self, *args, **kwargs):
        user_id = self.kwargs.get("pk")
        user = USER_MODEL.objects.get(id=user_id)
        return models.Note.objects.filter(hidden=True, writer=user).order_by(
            "-updated_at"
        )


class PublicListView(ListView):
    """ This view will handle displaying of publicly available notes """

    paginate_by = 10
    queryset = models.Note.objects.filter(hidden=False).order_by("-updated_at")
    template_name = "notes/public.html"

    def get_queryset(self, *args, **kwargs):
        user_id = self.kwargs.get("pk")
        user = USER_MODEL.objects.get(id=user_id)
        return models.Note.objects.filter(hidden=False, writer=user).order_by(
            "-updated_at"
        )


class DraftListView(ListView):
    """ This view will handle displaying draft notes """

    paginate_by = 10
    queryset = models.Note.objects.filter(draft=True).order_by("-updated_at")
    template_name = "notes/drafts.html"


class BookmarkListView(CustomLoginRequiredMixin, ListView):
    """ This view will handle display of bookmarks """

    paginate_by = 10
    template_name = "notes/bookmarks.html"

    def get_queryset(self, *args, **kwargs):
        user_id = self.kwargs.get("pk")
        user = USER_MODEL.objects.get(id=user_id)
        bookmarks = models.Bookmark.objects.filter(user=user)
        return [bookmark.note for bookmark in bookmarks]


def toggle_bookmark_view(request):
    """When this view receives a request, it will toggle the bookmarked state of a
    particular note (whose `pk` will be present in the POST body) for the given user."""
    user = request.user
    try:
        models.Bookmark.objects.get(
            user=user, note__id=request.POST.get("note_id")
        ).delete()
        status = False
        message = "Your bookmark was removed successfully!"
    except models.Bookmark.DoesNotExist:
        note = models.Note.objects.get(id=request.POST.get("note_id"))
        models.Bookmark.objects.create(user=user, note=note)
        status = True
        message = "The note was bookmarked successfully!"
    return JsonResponse({"status": status, "message": message})


class ReportView(DetailView):
    template_name = "notes/report.html"
    model = models.Note


class NoteUpdateView(UpdateView):
    template_name = "notes/update.html"
    form_class = forms.NoteCreateOrUpdateForm
    model = models.Note
