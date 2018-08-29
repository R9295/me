from django.urls import path

from .views import AnalyticsSuperUserView, AnalyticsUserView, CounterView

urlpatterns = [
    path('', AnalyticsSuperUserView.as_view(), name='analytics_super_user'),
    path('me', AnalyticsUserView.as_view(), name='analytics_user'),
    path('increment/<str:user_id>/<str:platform>',
         CounterView.as_view(),
         name='increment'),
]
