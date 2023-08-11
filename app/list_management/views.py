from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from base.tmdb_helpers import tmdb_get_single_movie_core
from base.models import Movie, Person
from list_management.models import MovieList, PersonList
from django.contrib import messages
from base import scraper
from django.http import Http404


def ranking(request, name):

    if name == "imdb":
        list_title = 'IMDb Top 250 Movies'
        description = "IMDb, short for Internet Movie Database, is a widely recognized online database dedicated to movies. The IMDb Top 250 represents a diverse collection of films from various genres, countries, and periods of cinema history. It's updated regularly to reflect changes in user ratings and includes both classic masterpieces and contemporary hits."
        context = {"user_list": scraper.scrape_imdb_top_250(), 'list_title': list_title, 'description': description}
    elif name == "filmweb":
        list_title = 'Filmweb Top 250 Movies'
        description = 'Filmweb is a popular Polish website dedicated to movies, TV series, and celebrities. Similar to IMDb, Filmweb also has a ranking system that allows users to rate and review films. The Filmweb Top 250 is a list of the highest-rated movies on the platform, based on user ratings.'
        context = {"user_list": scraper.scrape_fimlweb_top_250(), 'list_title': list_title, 'description': description}
    else:
        #TODO obsluga bledu brak listy
        pass

    return render(request, "list_management/list.html", context)

@login_required
def list_movies(request, name):

    user = request.user
    user_list = MovieList.objects.get(user=user, name=name)
    movies = user_list.movies.all()
    #TODO obsluga bledu brak listy
    context = {'user_list': movies, 'list_title': name}
    return render(request, "list_management/list.html", context)

# Create your views here.
@login_required
def choose_list(request):
    user = request.user
    user_lists = MovieList.objects.filter(user=user)
    
    context = {'user_lists': user_lists}
    return render(request, "list_management/choose_list.html", context)


@login_required
def add_list(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        new_list = MovieList(user=user, name=name)
        new_list.save()

    return redirect('choose_list')



@login_required
def add_to_watchlist(request, movie_title, movie_year):
    user = request.user

    # Pobierz watchlistę użytkownika lub utwórz ją, jeśli nie istnieje
    user_watchlist, _ = MovieList.objects.get_or_create(user=user, name="Watchlist")

    if "." in movie_title:
        movie_title = movie_title.split(".", 1)[1].strip()

    # Logika do pobrania filmu (zakładam, że masz odpowiednią funkcję do tego)
    movie_data = tmdb_get_single_movie_core(movie_title, movie_year)

    # Pobierz film z bazy danych lub utwórz go, jeśli nie istnieje
    movie_obj, _ = Movie.objects.get_or_create(
        title=movie_data['title'],
        year=movie_data['release_date'],
        poster_path=movie_data['poster_path'],
        custom_id=movie_data['id'],
        on_watchlist="yes",
    )

    # Dodaj film do watchlisty użytkownika
    user_watchlist.movies.add(movie_obj)

    return JsonResponse({'status': 'success'})
