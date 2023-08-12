from django.shortcuts import render
from tmdb_helpers import TMDBClient
import requests, environ
from django.contrib.auth.decorators import login_required


env = environ.Env()
environ.Env.read_env()

@login_required
def home(request):
    # Render the template with the context
    return render(request, "base/home.html")


def movie(request, title, year):
    # wallpaper = scraper.scrape_movie_wallpaper(title, year)
    if "." in title:
        title = title.split(".", 1)[1].strip()

    movie = TMDBClient.tmdb_get_single_movie(title, year)

    return render(request, "base/movie.html", movie)


def actor(request, id):
    actor = ""

    return render(request, "base/movie.html", actor)


def search(request):
    
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
        print(movies)

        # Create a new list of movies, each represented as a dictionary with only the desired fields
        movies = [
            {
                "genre_ids": movie["genre_ids"],
                "title": movie["title"],
                "popularity": movie["popularity"],
                "poster_path": movie["poster_path"],
                "release_date": movie["release_date"][:4],
            }
            for movie in movies
        ]
        context = {"movies": movies}
        # Pass the list of movies to the template via the context
        return render(request, "base/search.html", context)

    return render(request, "base/search.html")



