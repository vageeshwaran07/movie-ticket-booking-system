from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    duration_minutes = models.PositiveIntegerField()
    language = models.CharField(max_length=50)
    release_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
