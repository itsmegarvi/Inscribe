from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """The LoginRequiredMixin extended to add a relevant message to the
    messages framework by setting the ``permission_denied_message``
    attribute."""

    permission_denied_message = "You have to be logged in to access that page"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                request, messages.WARNING, self.permission_denied_message
            )
            return self.handle_no_permission()
        return super(CustomLoginRequiredMixin, self).dispatch(request, *args, **kwargs)
