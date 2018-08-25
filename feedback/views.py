from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import FeedbackForm


class FeedbackView(LoginRequiredMixin, FormView):
    form_class = FeedbackForm
    template_name = 'feedback/feedback.html'
    success_url = reverse_lazy('feedback:add_feedback')
    login_url = settings.LOGIN_URL

    def get_initial(self):
        initial = super(FeedbackView, self).get_initial()
        initial['user'] = str(self.request.user.pk)
        initial['type'] = 'FEEDBACK'
        return initial

    def form_valid(self, form):
        form.save()
        return super(FeedbackView, self).form_valid(form)
