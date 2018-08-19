from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import UserCreationForm


class SignUpView(FormView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = '/accounts/thanks'

    def form_valid(self, form):
        form.save()
        # TODO send confirmation email
        return super().form_valid(form)


class ThanksView(TemplateView):
    template_name = 'registration/thanks.html'
