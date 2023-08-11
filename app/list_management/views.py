from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from base.tmdb_helpers import tmdb_get_single_movie_core
from base.models import Movie, Person
from list_management.models import MovieList, PersonList
from django.contrib import messages
from base import scraper
from django.http import Http404
import environ
import requests

env = environ.Env()
environ.Env.read_env()

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

    return render(request, "list_management/ranking.html", context)

@login_required
def list_movies(request, name):
    context = {}
    if request.method == "POST":

        search_term = request.POST.get("search")  # Get the search term from the POST data
        bearer = env("BEARER")
        headers = {"accept": "application/json", "Authorization": f"Bearer {bearer}"}
        url = f"https://api.themoviedb.org/3/search/movie?query={search_term}"

        response = requests.get(url, headers=headers).json()
        # print(json.dumps(response, indent=4, sort_keys=True))

        movies = response.get("results", [])
        movies = [
            {
                "id": movie["id"],
                "title": movie["title"],
                "poster_path": movie["poster_path"],
                "release_date": movie["release_date"][:4],
            }
            for movie in movies
        ]
        context["search_results"] = movies

    user = request.user
    user_list = MovieList.objects.get(user=user, name=name)
    movies = user_list.movies.all()
    #TODO obsluga bledu brak listy
    context["user_list"] = movies
    context["name"] = user_list.name
    context["description"] = user_list.description
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
        description = request.POST.get('description')
        new_list = MovieList(user=user, name=name, description=description)
        new_list.save()

    return redirect('choose_list')



@login_required
def add_to_list(request, movie_title, movie_year, name):
    user = request.user

    # Pobierz listę użytkownika lub utwórz ją, jeśli nie istnieje
    user_list, _ = MovieList.objects.get_or_create(user=user, name=name)

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
        on_watchlist="yes" if name=='Watchlist' else "no",
    )

    # Dodaj film do watchlisty użytkownika
    user_list.movies.add(movie_obj)
    
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer) 


