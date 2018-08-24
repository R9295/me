from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import LoginView, SignUpView, VerifyView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page='/login'), name='logout'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('verify/<str:token>', VerifyView.as_view(), name='verify')
]
