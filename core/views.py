from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import ProfileForm
from .models import Profile


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = ProfileForm
    login_url = settings.LOGIN_URL
    template_name = 'app/profile.html'
    success_url = '/me/profile'
    success_message = 'Successfully updated your profile.'

    def get_initial(self):
        initial = super(ProfileView, self).get_initial()
        initial['user'] = str(self.request.user.pk)
        return initial

    def get_form_kwargs(self):
        form_kwargs = super(ProfileView, self).get_form_kwargs()
        # check if user has profile, and if they do,
        # populate the form with data
        if Profile.objects.filter(user=form_kwargs['initial']['user']).count() != 0:
            form_kwargs['instance'] = Profile.objects.get(user=form_kwargs['initial']['user'])
        return form_kwargs

    def form_valid(self, form):
        form.save()
        return super(ProfileView, self).form_valid(form)


class UserView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data()
        context['user'] = get_object_or_404(Profile, prefix=self.kwargs.get('user_prefix'), active=True)
        self.profile = context['user']
        return context

    def get_template_names(self):
        return ['themes/{0}.html'.format(self.profile.theme.pk)]


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = settings.LOGIN_URL
    template_name = 'app/home.html'


class IndexView(TemplateView):
    template_name = 'app/index.html'
