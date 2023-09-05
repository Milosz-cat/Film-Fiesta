from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from list_management.models import MovieList, PersonList, IMDBTop250, FilmwebTop250, OscarWinner
from .tasks import scrape_imdb_top_250, scrape_filmweb_top_250, scrape_oscar_best_picture
from django.dispatch import Signal
import sys


# After entering homw view, a home_visited signal is sent automatically, the purpose
# of which is to scrape the rankings and Oscars when you first visit the application
home_visited = Signal()


@receiver(post_save, sender=User)
def create_watchlist(sender, instance, created, **kwargs):
    """
    Automatically creates default movie and person lists for a new user upon registration.

    Parameters:
    - sender (Model): The model that sent the signal.
    - instance (User): The user instance that was saved.
    - created (bool): A flag indicating whether a new record was created.
    """
    if created:
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
    """
    Triggers scraping tasks for IMDB Top 250, Filmweb Top 250, and Oscar Best Picture
    if the data doesn't already exist in the database.

    The scraping tasks are asynchronous and are dispatched using the `.delay()` method.
    The `on_home_visited` receiver checks if the application is running in test mode 
    and avoids triggering scraping tasks in such cases.

    Parameters:
    - sender (Model): The model that sent the signal.
    """

    if 'test' in sys.argv:
        return
    
    if not IMDBTop250.objects.exists():
        scrape_imdb_top_250.delay()

    if not FilmwebTop250.objects.exists():
        scrape_filmweb_top_250.delay()

    if not OscarWinner.objects.exists():
        scrape_oscar_best_picture.delay()
