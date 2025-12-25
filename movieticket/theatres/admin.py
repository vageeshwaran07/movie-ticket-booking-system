from django.contrib import admin
from .models import Theatre, TheatreStaff, Screen


@admin.register(Theatre)
class TheatreAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request) #SELECT * FROM theatres_theatre;


        # Admin can see all theatres
        if request.user.role == "ADMIN":
            return qs

        # Staff sees only assigned theatres
        if request.user.role == "STAFF":
            return qs.filter(
                theatrestaff__user=request.user
            )

        # Customers see nothing
        return qs.none()
    
    
    #permission hooks
    def has_add_permission(self, request):
        return request.user.role == "ADMIN"
    
    def has_change_permission(self, request):
        return request.user.role == "ADMIN"
    
    def has_delete_permission(self, request):
        return request.user.role == "ADMIN"
    def has_module_permission(self, request):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["ADMIN", "STAFF"]

    def has_view_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["ADMIN", "STAFF"]
    
    
@admin.register(TheatreStaff)
class TheatreStaffAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.role == "ADMIN":
            return qs

        return qs.none()
    
@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Admin sees all screens
        if request.user.role == "ADMIN":
            return qs

        # Staff sees screens only from assigned theatres
        if request.user.role == "STAFF":
            return qs.filter(
                theatre__theatrestaff__user=request.user
            )

        # Safety: others see nothing
        return qs.none()
    
    def has_add_permission(self, request):
        return request.user.role == "ADMIN"
    
    def has_change_permission(self, request):
        return request.user.role == "ADMIN"
    
    def has_delete_permission(self, request):
        return request.user.role == "ADMIN"
    def has_module_permission(self, request):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["ADMIN", "STAFF"]

    def has_view_permission(self, request, obj=None):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["ADMIN", "STAFF"]

