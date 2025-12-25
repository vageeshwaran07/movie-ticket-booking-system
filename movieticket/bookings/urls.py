from django.urls import path
from .views import save_booking

urlpatterns = [
    path("save-booking/", save_booking),
]
