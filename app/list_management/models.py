from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from base.models import Movie, Person

# Create your models here.


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

# Sygnał, który jest wywoływany po zapisaniu obiektu User
@receiver(post_save, sender=User)
def create_watchlist(sender, instance, created, **kwargs):
    if created:  # Jeśli to nowy użytkownik
        MovieList.objects.create(
            user=instance, name="Watchlist", description="Movies you'd like to see soon"
        )
        MovieList.objects.create(
            user=instance, name="My Films"
        )
        PersonList.objects.create(
            user=instance, name="Favourite Actors"
        )
        PersonList.objects.create(
            user=instance, name="Favourite Directors"
        )


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