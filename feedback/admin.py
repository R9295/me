from django.contrib import admin

from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        fields = super(FeedbackAdmin, self).get_readonly_fields(request, obj)
        fields += ('user', 'date', 'message', 'type', 'id')
        return fields


admin.site.register(Feedback, FeedbackAdmin)
