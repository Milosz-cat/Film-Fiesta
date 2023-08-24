from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from list_management.models import MovieList, PersonList, IMDBTop250, FilmwebTop250, OscarWinner
from .tasks import scrape_imdb_top_250, scrape_filmweb_top_250, scrape_oscar_best_picture
from django.dispatch import Signal

# Define a new signal
home_visited = Signal()

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


@receiver(home_visited)
def on_home_visited(sender, **kwargs):
    if not IMDBTop250.objects.exists():
        scrape_imdb_top_250.delay()

    if not FilmwebTop250.objects.exists():
        scrape_filmweb_top_250.delay()

    if not OscarWinner.objects.exists():
        scrape_oscar_best_picture.delay()
