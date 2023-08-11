from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    custom_id = models.IntegerField(primary_key=True)
    poster_path = models.CharField(max_length=200, default=None)
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
    ROLE_CHOICES = (
        ("actor", "Aktor"),
        ("director", "Reżyser"),
        ("cameraman", "Kamerzysta"),
        ("lighting", "Oświetlenie"),
        ("sound", "Dźwięk"),
        # Dodaj więcej ról według potrzeb
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    movies = models.ManyToManyField("Movie", related_name="people")

    def __str__(self):
        return self.name