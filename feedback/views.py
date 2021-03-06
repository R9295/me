from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import FeedbackForm


class FeedbackView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = FeedbackForm
    template_name = 'feedback/feedback.html'
    success_url = reverse_lazy('feedback:add_feedback')
    success_message = 'Thanks for your feedback!'
    login_url = settings.LOGIN_URL

    def get_initial(self):
        initial = super(FeedbackView, self).get_initial()
        initial['user'] = str(self.request.user.pk)
        initial['type'] = 'FEEDBACK'
        return initial

    def form_valid(self, form):
        form.save()
        return super(FeedbackView, self).form_valid(form)


class BugReportView(FeedbackView):
    template_name = 'feedback/bug_report.html'
    success_message = 'We really appreciate this! We will reach out, if needed, \
    for more information and the reward'
    success_url = reverse_lazy('feedback:bug_report')

    def get_initial(self):
        initial = super(BugReportView, self).get_initial()
        initial['type'] = 'BUG'
        return initial
