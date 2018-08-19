from django.conf.urls import url
from django.urls import path

from .views import HomeView, IndexView, ProfileView, UserView

urlpatterns = [
    path('me/profile', ProfileView.as_view(), name='profile'),
    path('<user_prefix>', UserView.as_view(), name='user'),
    path('me/home', HomeView.as_view(), name='home'),
    url(r'^$', IndexView.as_view(), name='me')
]
