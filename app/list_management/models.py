from django.db import models
from django.contrib.auth.models import User
from base.models import Movie, Person

class MovieList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=500, default="")
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return self.user.username + "'s Movie List: " + self.name


class PersonList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, default="")
    persons = models.ManyToManyField(Person)

    def __str__(self):
        return self.user.username + "'s Person List: " + self.name


class IMDBTop250(models.Model):
    rank = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    poster_path = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.rank}. {self.title} ({self.year})"


class FilmwebTop250(models.Model):
    rank = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField()
    poster_path = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.rank}. {self.title} ({self.year})"

    
class OscarWinner(models.Model):
    year = models.CharField(max_length=20)
    release_year = models.IntegerField()
    title = models.CharField(max_length=255)
    poster_path = models.URLField(max_length=500, blank=True, null=True)
    studio = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} ({self.release_year})"

class OscarNomination(models.Model):
    winner = models.ForeignKey(OscarWinner, related_name="nominations", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    studio = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
    
