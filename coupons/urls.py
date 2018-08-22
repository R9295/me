from django.urls import path

from .views import CouponActivateView

urlpatterns = [
    path('activate', CouponActivateView.as_view(), name='activate'),
]
