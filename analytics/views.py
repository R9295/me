from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.timezone import now
from django.views.generic import TemplateView, View

from accounts.models import User
from core.models import Profile

from .models import ProfileAnalytics


class AnalyticsSuperUserView(LoginRequiredMixin, TemplateView):
    login_url = settings.LOGIN_URL
    template_name = 'analytics/analytics.html'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return HttpResponse(status=403)
        return super(AnalyticsSuperUserView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AnalyticsSuperUserView, self).get_context_data()
        users = User.objects.filter(is_active=True)
        context['total_users'] = users.count()
        context['logged_today'] = users.filter(last_login__gte=now() - relativedelta(days=1)).count()
        context['signed_up_today'] = users.filter(date_joined=now() - relativedelta(days=1)).count()
        return context


class CounterView(View):

    def get(self, request, *args, **kwargs):
        profile_id = kwargs.get('profile_id')
        platform = kwargs.get('platform')
        redir = request.GET.get('redir')
        if profile_id and platform:
            try:
                a = ProfileAnalytics.objects.get(profile=profile_id)
                setattr(a, platform+'_visits', getattr(a, platform+'_visits') + 1)
                a.save()
            except ProfileAnalytics.DoesNotExist:
                pass
            if redir:
                return redirect(redir)
            else:
                return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)


class AnalyticsUserView(LoginRequiredMixin, TemplateView):
    login_url = settings.LOGIN_URL
    template_name = 'analytics/user.html'

    def get(self, request, *args, **kwargs):
        if Profile.objects.filter(user=self.request.user).count() == 0:
            self.template_name = 'analytics/no_profile.html'
        return super(AnalyticsUserView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AnalyticsUserView, self).get_context_data()
        if self.template_name != 'analytics/no_profile.html':
            context['data'] = ProfileAnalytics.objects.get(profile=self.request.user.profile)
            context['profile'] = self.request.user.profile
        return context
