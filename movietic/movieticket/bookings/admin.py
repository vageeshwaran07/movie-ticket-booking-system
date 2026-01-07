from django.contrib import admin
from .models import Booking, BookingSeat


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "show_id", "total_amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__email", "payment_id")


@admin.register(BookingSeat)
class BookingSeatAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "seat_id", "price")