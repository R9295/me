from django.contrib.auth.views import (LogoutView, PasswordChangeDoneView,
                                       PasswordResetCompleteView,
                                       PasswordResetDoneView)
from django.urls import path

from accounts import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page='/'), name='logout'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('verify/<str:token>', views.VerifyView.as_view(), name='verify'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
]
