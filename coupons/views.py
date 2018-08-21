from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormView

from .forms import CouponActivateForm


class CouponActivateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'coupons/activate.html'
    form_class = CouponActivateForm
    success_url = '/coupons/activate'
    success_message = "Successfully activated coupon!"

    def get_form_kwargs(self):
        kwargs = super(CouponActivateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
