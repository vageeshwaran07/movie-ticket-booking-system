from django.contrib import admin
from .models import Show


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):

    # -------- VISIBILITY --------
    def has_module_permission(self, request):
        user = request.user
        return (
            user.is_authenticated
            and hasattr(user, "role")
            and user.role in ["ADMIN", "STAFF"]
        )

    def has_view_permission(self, request, obj=None):
        return request.user.role in ["ADMIN", "STAFF"]

    # -------- ACTION PERMISSIONS --------
    def has_add_permission(self, request):
        return request.user.role in ["ADMIN", "STAFF"]

    def has_change_permission(self, request, obj=None):
        return request.user.role in ["ADMIN", "STAFF"]

    def has_delete_permission(self, request, obj=None):
        return request.user.role == "ADMIN"

    # -------- DATA ISOLATION --------
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.role == "ADMIN":
            return qs

        if request.user.role == "STAFF":
            return qs.filter(
                screen__theatre__theatrestaff__user=request.user
            )

        return qs.none()
