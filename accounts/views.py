from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormView

from .forms import LoginForm, UserCreationForm


class SignUpView(SuccessMessageMixin, FormView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = '/accounts/signup'
    success_message = 'Thanks for signing up!'

    def form_valid(self, form):
        form.save()
        # TODO send confirmation email
        return super().form_valid(form)


class LoginView(BaseLoginView):
    form_class = LoginForm
