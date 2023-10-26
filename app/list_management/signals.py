import sys
from django.dispatch import Signal, receiver
from django.core.cache import cache
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from celery.result import AsyncResult
from list_management.models import (
    MovieList,
    PersonList,
    IMDBTop250,
    FilmwebTop250,
    OscarWinner,
)
from .tasks import (
    scrape_imdb_top_250,
    scrape_filmweb_top_250,
    scrape_oscar_best_picture,
)


# After entering homw view, a home_visited signal is sent automatically, the purpose
# of which is to scrape the rankings and Oscars when you first visit the application
home_visited = Signal()


@receiver(post_save, sender=User)
def create_watchlist(_sender, instance, created, **_kwargs):
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
        MovieList.objects.create(user=instance, name="My Films")
        PersonList.objects.create(user=instance, name="Favourite Actors")
        PersonList.objects.create(user=instance, name="Favourite Directors")


def handle_scrape_task(task_name, model, scrape_function):
    """
    Handle the scraping task by checking its state and potentially triggering a new task.

    This function checks the state of a given scraping task. If the task is neither 'PENDING'
    nor 'STARTED' and the data doesn't exist in the provided model, it triggers a new scraping
    task using the given function. The task ID is then stored in the cache.

    Parameters:
    - task_name (str): The name of the task to be used as a key in the cache.
    - model (Model): The Django model to check if data exists.
    - scrape_function (function): The function to call to initiate the scraping task.

    Returns:
    None
    """

    task_id = cache.get(task_name)
    if task_id:
        task_result = AsyncResult(task_id)
        if task_result.state not in ["PENDING", "STARTED"]:
            if not model.objects.exists():
                task = scrape_function.delay()
                cache.set(task_name, task.id)
    else:
        if not model.objects.exists():
            task = scrape_function.delay()
            cache.set(task_name, task.id)


@receiver(home_visited)
def on_home_visited(_sender, **_kwargs):
    """
    Triggers scraping tasks for IMDB Top 250, Filmweb Top 250, and Oscar Best Picture
    if the data doesn't already exist in the database.

    Before triggering a scraping task, the function checks if a task is already running
    or pending by looking up the task ID in the cache. If a task is found and its state
    is either 'PENDING' or 'STARTED', the function will not trigger a new task. If no task
    is found or the task has completed, a new task will be triggered and its ID will be
    stored in the cache.

    The scraping tasks are asynchronous and are dispatched using the `.delay()` method.
    The `on_home_visited` receiver checks if the application is running in test mode
    and avoids triggering scraping tasks in such cases.

    Parameters:
    - sender (Model): The model that sent the signal.
    """

    if "test" in sys.argv:
        return

    handle_scrape_task("imdb_scrape_task_id", IMDBTop250, scrape_imdb_top_250)
    handle_scrape_task("filmweb_scrape_task_id", FilmwebTop250, scrape_filmweb_top_250)
    handle_scrape_task("oscar_scrape_task_id", OscarWinner, scrape_oscar_best_picture)
