from django.shortcuts import render
from base.tmdb_helpers import TMDBClient
from django.contrib.auth.decorators import login_required
from list_management.models import MovieList
from base.models import Movie

@login_required
def home(request):

    context = {}
    tmdb_client = TMDBClient()
    trending_movies = [
        {
            'title': movie['title'],
            'popularity': movie.get('popularity', ''),
            'poster_path': movie['poster_path'],
            'custom_id': movie['id'],
            'year': movie['release_date'][0:4] if movie['release_date'] else None
        }
        for movie in tmdb_client.get_trending_movies()  
    ]

    now_playing_movies = [
        {
            'title': movie['title'],
            'popularity': movie.get('popularity', ''),
            'poster_path': movie['poster_path'],
            'custom_id': movie['id'],
            'year': movie['release_date'][0:4] if movie['release_date'] else None
        }
        for movie in tmdb_client.get_now_playing_movies()  
    ]

    user = request.user

    # Get the user's watchlist movies
    user_watchlist = MovieList.objects.get(user=user, name="Watchlist")
    watchlist_movies = user_watchlist.movies.all() if user_watchlist else None  # If MovieList has a many-to-many field called movies



    user_watched_films = MovieList.objects.get(user=user, name="My Films")
    if user_watched_films.movies.exists():
        last_added_movie_id = user_watched_films.movies.last()

        recommendations = [
            {
                'title': movie['title'],
                'popularity': movie.get('popularity', ''),
                'poster_path': movie['poster_path'],
                'custom_id': movie['id'],
                'year': movie['release_date'][0:4] if movie['release_date'] else None
            }
            for movie in tmdb_client.get_movie_recommendations(last_added_movie_id.custom_id)
        ]
    else:
        recommendations = None

    popular_persons = [
        {
            'name': person['name'],
            'popularity': person.get('popularity', ''),
            'profile_path': person['profile_path']
        }
        for person in tmdb_client.get_popular_people()
    ]

    context['popular_persons'] = popular_persons
    context['recommendations'] = recommendations
    context["trending_movies"] = trending_movies
    context["now_playing_movies"] = now_playing_movies
    context["watchlist_movies"] = watchlist_movies
    
    return render(request, "base/home.html", context)


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
        print(movies)
        return render(request, "base/search.html", context)

    return render(request, "base/search.html")



