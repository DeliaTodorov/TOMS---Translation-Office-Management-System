from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("number", "client", "language_pair", "translator",
                    "status", "deadline", "cost")
    list_filter = ("status", "urgency", "domain", "language_pair")
    search_fields = ("number", "client__name")      # "__" = caută prin relație
    readonly_fields = ("number", "created_at", "updated_at")
    date_hierarchy = "deadline"
