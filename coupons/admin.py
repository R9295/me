from django.contrib import admin

from .models import Coupon


class CouponAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        fields = super(CouponAdmin, self).get_readonly_fields(request, obj)
        if obj:
            fields += ('months', 'activated', 'activated_by', )
        return fields


admin.site.register(Coupon, CouponAdmin)
