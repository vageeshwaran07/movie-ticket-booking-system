from django.db import models
from theatres.models import Screen
from movies.models import Movie
from django.core.exceptions import ValidationError


class Show(models.Model):
    screen = models.ForeignKey(
        Screen,
        on_delete=models.CASCADE,
        related_name="shows"
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self): 
        overlap_shows = Show.objects.filter(screen = self.screen,
                                            start_time__lt=self.end_time,
                                            end_time__gt=self.start_time).exclude(pk=self.pk)
        
        if overlap_shows.exists():
            raise ValidationError("This screen already has a show during this time")

    def __str__(self):
        return f"{self.movie.title} @ {self.start_time}"
