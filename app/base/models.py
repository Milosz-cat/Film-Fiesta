from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=30)
    year = models.IntegerField()
    custom_id = models.IntegerField(primary_key=True)
    on_watchlist = models.BooleanField(default=False)

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


class MovieList(models.Model):
    name = models.CharField(max_length=100)
    TYPE_CHOICES = (
        ("movies", "Filmy"),
        ("directors", "Reżyserzy"),
        ("actors", "Aktorzy"),
        ("crew", "Ekipa"),  # Lista zawierająca różne role za kulisami
        # Dodaj więcej typów list według potrzeb
    )
    list_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    movies = models.ManyToManyField("Movie", blank=True, related_name="movie_lists")
    people = models.ManyToManyField("Person", blank=True, related_name="person_lists")

    def __str__(self):
        return self.name
