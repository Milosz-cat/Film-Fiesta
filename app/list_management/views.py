from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from base.tmdb_helpers import tmdb_get_single_movie_core
from base.models import Movie, Person
from list_management.models import MovieList, PersonList


# Create your views here.
@login_required
def choose_list(request):
    # Render the template with the context
    return render(request, "list_management/choose_list.html")


@login_required
def add_to_watchlist(request, movie_title, movie_year):
    user = request.user

    # Pobierz watchlistę użytkownika lub utwórz ją, jeśli nie istnieje
    user_watchlist, _ = MovieList.objects.get_or_create(user=user, name="Watchlist")

    # Logika do pobrania filmu (zakładam, że masz odpowiednią funkcję do tego)
    movie_data = tmdb_get_single_movie_core(movie_title, movie_year)

    # Pobierz film z bazy danych lub utwórz go, jeśli nie istnieje
    movie_obj, _ = Movie.objects.get_or_create(
        title=movie_data.title,
        year=movie_data.release_date,
        poster_path=movie_data.poster_path,
        custom_id=movie_data.id,
        on_watchlist="yes",
    )

    # Dodaj film do watchlisty użytkownika
    user_watchlist.movies.add(movie_obj)

    return JsonResponse({"status": "success"})
