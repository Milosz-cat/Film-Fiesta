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

    env = environ.Env()
    environ.Env.read_env()
    api_key = env("TMDB_API_KEY")

    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiODJmMzhjZDllOWIxZjc2N2Q1NjBiNmMxOTdmOGM0YSIsInN1YiI6IjY0YmQzNTkxZTlkYTY5MDEyZTBlNTM1NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0D_TCZv03KxgRTusmTexEEMeQGSJSeiLwdbSkGPc7L8"
    }

    url = "https://api.themoviedb.org/3/discover/movie"

    response = requests.get(url, headers=headers).json()

    print(json.dumps(response, indent=4, sort_keys=True))

    return render(request, "base/list.html")