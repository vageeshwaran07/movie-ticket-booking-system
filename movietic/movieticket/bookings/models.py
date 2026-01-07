from django.db import models
from users.models import User
from shows.models import Show

class Booking(models.Model):
    STATUS_CHOICES = (
        ("CONFIRMED", "Confirmed"),
        ("FAILED", "Failed"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show_id = models.IntegerField()
    total_amount = models.IntegerField()
    payment_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Booking {self.id} - {self.status}"
    

class BookingSeat(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="seats"
    )
    seat_id = models.CharField(max_length=10)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.seat_id} - Booking {self.booking.id}"
