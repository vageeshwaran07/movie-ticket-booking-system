from django.db import models
from django.conf import settings


class Theatre(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.city})"

class TheatreStaff(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, limit_choices_to = {"role", "STAFF"}
)
    theatre = models.ForeignKey("theatres.Theatre", on_delete = models.CASCADE
     )
    
    created_at = models.DateTimeField(auto_now= True)# Create your models here.

    def __str__(self):
        return f"{self.user.email} -> {self.theatre.name}"
    
class Screen(models.Model):
    theatre = models.ForeignKey(
        "theatres.Theatre",
        on_delete=models.CASCADE,
        related_name="screens"
    )
    name = models.CharField(max_length=50)
    total_seats = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.theatre.name} - {self.name}"
