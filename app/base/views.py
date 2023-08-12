from django.shortcuts import render
from base.tmdb_helpers import TMDBClient
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # Render the template with the context
    return render(request, "base/home.html")


def movie(request, title, year):
    # wallpaper = scraper.scrape_movie_wallpaper(title, year)
    if "." in title:
        title = title.split(".", 1)[1].strip()

    tmdb_client = TMDBClient()
    movie = tmdb_client.get_single_movie(title, year)

    return render(request, "base/movie.html", movie)


def person(request, name):

    tmdb_client = TMDBClient()
    person = tmdb_client.search_person(name)
    person_id = person[0]['id']
    person_movies = [
            {
                'title': movie['title'],
                'character': movie['character'],
                'poster_path': movie['poster_path'],
                'year': movie['release_date'][0:4],
                'poster_path': movie['poster_path'],
                
            }
            for movie in tmdb_client.get_movies_by_person(person_id)[0]
    ]

    context = {'person': person[0], 'movies': person_movies}
    print(context)
    
    return render(request, "base/person.html", context)


def search(request):
    
    if request.method == "POST":
        search_term = request.POST.get("search")  # Get the search term from the POST data

        tmdb_client = TMDBClient()  # Create an instance of the TMDBClient class
        movies = tmdb_client.search_movies(search_term)  # Call the search_movie method on the instance


        # Create a new list of movies, each represented as a dictionary with only the desired fields
        movies = [
            {
                "id": movie["id"],
                "title": movie["title"],
                "poster_path": movie["poster_path"],
                "release_date": movie["release_date"][:4],
            }
            for movie in movies
        ]
        context = {"movies": movies}
        # Pass the list of movies to the template via the context
        return render(request, "base/search.html", context)

    return render(request, "base/search.html")



