from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import LoginForm, UserCreationForm, SetPasswordForm, PasswordResetForm
from .models import User
from django.contrib.auth import views
from django.urls import reverse_lazy


class SignUpView(SuccessMessageMixin, FormView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = '/accounts/signup'
    success_message = 'Thanks for signing up!'

    def form_valid(self, form):
        user = form.save()
        send_mail(
            'Please verify your email',
            'http://localhost:8000/accounts/verify/{}'.format(user.verification_token),
            'aarnavbos@gmail.com',
            [user.email],
            # TODO handle fail
            fail_silently=False,
        )
        return super().form_valid(form)


class VerifyView(TemplateView):
    template_name = 'app/thanks.html'

    def get(self, request, *args, **kwargs):
            user = get_object_or_404(User, verification_token=self.kwargs.get('token'), is_active=False)
            if not user.is_active:
                user.is_active = True
                user.save()
            return super(VerifyView, self).get(args, kwargs)


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')


# TODO make sure email actually exists in form else raise validation error
class PasswordResetView(views.PasswordResetView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('accounts:password_reset_done')


class LoginView(BaseLoginView):
    form_class = LoginForm
