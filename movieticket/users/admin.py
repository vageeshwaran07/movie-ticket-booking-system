
from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "role", "is_staff", "is_active")

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # only when creating user
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

