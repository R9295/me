from django.urls import path

from .views import FeedbackView, BugReportView

urlpatterns = [
    path('me/feedback', FeedbackView.as_view(), name='add_feedback'),
    path('me/bugreport', BugReportView.as_view(), name='bug_report'),
]
