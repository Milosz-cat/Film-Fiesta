from django.db import models
from django.contrib.auth.models import User
from base.models import Movie, Person


class BaseList(models.Model):
    """Abstract model for user's lists."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, default="")

    class Meta:  # This ensures that this model won't be used to create any database table
        abstract = True

    def __str__(self):
        return f"{self.user.username}'s {self.__class__.__name__}: {self.name}"


class MovieList(BaseList):
    """Model representing a user's list of movies."""

    movies = models.ManyToManyField(Movie)


class PersonList(BaseList):
    """Model representing a user's list of film industry persons."""

    persons = models.ManyToManyField(Person)


class BaseTopMovie(models.Model):
    """Abstract model for IMDB and Filmweb rankings."""

    title = models.CharField(max_length=255)
    year = models.IntegerField()
    rank = models.PositiveIntegerField(unique=True)
    poster_path = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.title} ({self.year})"


class IMDBTop250(BaseTopMovie):
    """Model representing a movie ranked in the IMDB Top 250."""


class FilmwebTop250(BaseTopMovie):
    """Model representing a movie ranked in the Filmweb Top 250."""

    original_title = models.CharField(max_length=255, blank=True, null=True)


class BaseOscarMovie(models.Model):
    """Abstract model for Oscars and Nominations."""

    release_year = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    studio = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.title} ({self.release_year})"


class OscarWinner(BaseOscarMovie):
    """Model representing a movie that won an Oscar. Designed for effective scrapping"""

    year = models.CharField(max_length=20)
    poster_path = models.URLField(max_length=500, blank=True, null=True)


class OscarNomination(BaseOscarMovie):
    """Model representing a movie nominated for an Oscar.  Designed for effective scrapping"""

    winner = models.ForeignKey(
        OscarWinner, related_name="nominations", on_delete=models.CASCADE
    )
