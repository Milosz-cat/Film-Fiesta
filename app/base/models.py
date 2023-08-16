from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    custom_id = models.IntegerField(primary_key=True, default=None)
    poster_path = models.CharField(max_length=200, default=None)
    rating = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ],
    default=0)
    WATCHLIST_CHOICES = (
        ("yes", "Yes"),
        ("no", "No"),
        ("watched", "Watched"),
    )
    on_watchlist = models.CharField(max_length=10, choices=WATCHLIST_CHOICES, default="no")


    def __str__(self):
        return self.title


class Person(models.Model):
    name = models.CharField(max_length=100)
    custom_id = models.IntegerField(primary_key=True, default=None)
    role = models.CharField(max_length=30)
    profile_path = models.CharField(max_length=200, default=None)

    def __str__(self):
        return self.name