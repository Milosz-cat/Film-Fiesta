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
    
    # Get movies by person
    cast_movies, director_movies = tmdb_client.get_movies_by_person(person_id)
    
    # Filter and structure movies where the person is an actor
    person_movies_as_actor = [
        {
            'title': movie['title'],
            'character': movie.get('character', ''),
            'poster_path': movie['poster_path'],
            'year': movie['release_date'][0:4] if movie['release_date'] else None
        }
        for movie in cast_movies if movie['release_date'] and '/' not in movie['title']
    ]
    
    # Filter and structure movies where the person is a director
    person_movies_as_director = [
        {
            'title': movie['title'],
            'poster_path': movie['poster_path'],
            'year': movie['release_date'][0:4] if movie['release_date'] else None
        }
        for movie in director_movies if movie['release_date'] and '/' not in movie['title']
    ]
    
    # Get biography
    biography = tmdb_client.search_person_by_id(person_id)['biography']
    
    # Create the context for rendering
    context = {
        'person': person[0],
        'movies': person_movies_as_actor,
        'movies_director': person_movies_as_director,
        'biography': biography
    }
    
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



