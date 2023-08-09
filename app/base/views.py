from django.shortcuts import render
from . import scraper, tmdb_helpers
from django.http import Http404
import requests, environ
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # Render the template with the context
    return render(request, "base/home.html")


def list_movies(request, source):
    context = {}
    if source == "imdb":
        list_title = 'IMDb Top 250 Movies'
        description = "IMDb, short for Internet Movie Database, is a widely recognized online database dedicated to movies. The IMDb Top 250 represents a diverse collection of films from various genres, countries, and periods of cinema history. It's updated regularly to reflect changes in user ratings and includes both classic masterpieces and contemporary hits."
        context = {"movies": scraper.scrape_imdb_top_250(), 'list_title': list_title, 'description': description}
    elif source == "filmweb":
        list_title = 'Filmweb Top 250 Movies'
        description = 'Filmweb is a popular Polish website dedicated to movies, TV series, and celebrities. Similar to IMDb, Filmweb also has a ranking system that allows users to rate and review films. The Filmweb Top 250 is a list of the highest-rated movies on the platform, based on user ratings.'
        context = {"movies": scraper.scrape_fimlweb_top_250(), 'list_title': list_title, 'description': description}
    else:
        raise Http404("Invalid source.")
    return render(request, "base/list.html", context)


def search(request):
    env = environ.Env()
    environ.Env.read_env()
    if request.method == "POST":
        search_term = request.POST.get(
            "search"
        )  # Get the search term from the POST data

        bearer = env("BEARER")

        headers = {"accept": "application/json", "Authorization": f"Bearer {bearer}"}

        url = f"https://api.themoviedb.org/3/search/movie?query={search_term}"  # Add the search term to the query parameters

        response = requests.get(url, headers=headers).json()
        # print(json.dumps(response, indent=4, sort_keys=True))

        # Extract the list of movies from the response
        movies = response.get("results", [])

        # Create a new list of movies, each represented as a dictionary with only the desired fields
        movies = [
            {
                "genre_ids": movie["genre_ids"],
                "title": movie["title"],
                "popularity": movie["popularity"],
                "poster_path": movie["poster_path"],
                "release_date": movie["release_date"],
                "vote_average": movie["vote_average"],
            }
            for movie in movies
        ]
        context = {"movies": movies}
        # Pass the list of movies to the template via the context
        return render(request, "base/search.html", context)

    return render(request, "base/search.html")


def movie(request, title, year):
    # wallpaper = scraper.scrape_movie_wallpaper(title, year)
    if "." in title:
        title = title.split(".", 1)[1].strip()

    movie = tmdb_helpers.tmdb_get_single_movie(title, year)

    return render(request, "base/movie.html", movie)
