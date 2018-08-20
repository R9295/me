from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .forms import LoginForm
from .views import SignUpView, ThanksView

urlpatterns = [
    path('login', LoginView.as_view(form_class=LoginForm), name='login'),
    path('logout', LogoutView.as_view(next_page='/login'), name='logout'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('thanks', ThanksView.as_view(), name='thanks'),
]
