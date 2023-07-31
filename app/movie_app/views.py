from django.shortcuts import render
from . import scraper
from django.http import Http404
import requests, environ, json

def home(request):
        # Render the template with the context
        return render(request, "base/home.html")


def list_movies(request, source):
    context = {}
    if source == 'imdb':
        context = {"movies": scraper.scrape_imdb_top_250()}
    elif source == 'filmweb':
        context = {"movies": scraper.scrape_fimlweb_top_250()}
    else:
        raise Http404("Invalid source.")
    return render(request, "base/list.html", context)


def movies(request):

    if request.method == "POST":
        search_term = request.POST.get('search')  # Get the search term from the POST data
        env = environ.Env()
        environ.Env.read_env()
        bearer = env("BEARER")

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {bearer}"
        }

        url = f"https://api.themoviedb.org/3/search/movie?query={search_term}"  # Add the search term to the query parameters

        response = requests.get(url, headers=headers).json()
        #print(json.dumps(response, indent=4, sort_keys=True))
        
        # Extract the list of movies from the response
        movies = response.get('results', [])

        # Create a new list of movies, each represented as a dictionary with only the desired fields
        movies = [
            {
                'genre_ids': movie['genre_ids'],
                'title': movie['title'],
                'popularity': movie['popularity'],
                'poster_path': movie['poster_path'],
                'release_date': movie['release_date'],
                'vote_average': movie['vote_average'],
            }
            for movie in movies
        ]

        # Pass the list of movies to the template via the context
        return render(request, "base/movie.html", {'movies': movies})

    return render(request, "base/movie.html")
