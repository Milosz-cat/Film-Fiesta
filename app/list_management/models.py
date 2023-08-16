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