from django.contrib import messages


class MessageCreateUpdateMixin:
    """
    Mixin for CreateView and UpdateView
    to add success messages after saving.
    """

    success_message = None

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response


class MessageDeleteMixin:
    """
    Show a flash message after successful delete.
    Override `success_message` in your view.
    """

    success_message = "Deleted successfully."

    def post(self, request, *args, **kwargs):
        messages.warning(request, self.success_message)
        return super().post(request, *args, **kwargs)
