from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "order_date", "total_price", "status")
    list_filter = ("status", "order_date")
    search_fields = ("user__name", "status")
    ordering = ("-order_date",)


admin.site.register(Order, OrderAdmin)
