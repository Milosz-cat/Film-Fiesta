from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from base.tmdb_helpers import TMDBClient
from base.models import Movie, Person
from list_management.models import MovieList, PersonList, IMDBTop250, FilmwebTop250, OscarWinner
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction


@login_required
def ranking(request, name):
    """
    Handles the display of movie rankings based on the source provided.
    
    The function fetches movie rankings from either IMDb or Filmweb. If the rankings are not available in the database, 
    a message is displayed to the user indicating that the data is being fetched. The user's watched movies are also 
    compared against the rankings to calculate the percentage of movies watched from the list.
    """
    user = request.user
    my_films_list = MovieList.objects.get(user=user, name="My Films")
    my_films_titles = set(my_films_list.movies.values_list('title', flat=True))
    
    if name == "imdb":
        list_title = "IMDb Top 250 Movies"
        description = "IMDb, short for Internet Movie Database, is a widely recognized online database dedicated to movies. The IMDb Top 250 represents a diverse collection of films from various genres, countries, and periods of cinema history. It's updated regularly to reflect changes in user ratings and includes both classic masterpieces and contemporary hits."

        # Check if records exist in the database
        if not IMDBTop250.objects.exists():
            list_title = "We apologize for the inconvenience. This is the first launch of the application, and our scrapers are currently loading content or updating data. Please bear with us for a moment. The entire process should not take more than 2 minutes. Thank you for your understanding!"
            context = {"list_title": list_title}
            return render(request, "list_management/ranking.html", context)

        movies = IMDBTop250.objects.all().order_by('rank')
        wachted_movies = [movie for movie in movies if movie.title[3:] in my_films_titles]
        percentage_watched = round((len(wachted_movies) / len(movies))*100)
        context = {
            "user_list": movies,
            "list_title": list_title,
            "description": description,
            "movies_count": len(wachted_movies),
            "percentage_watched": percentage_watched,
        }

    elif name == "filmweb":
        list_title = "Filmweb Top 250 Movies"
        description = "Filmweb is a popular Polish website dedicated to movies, TV series, and celebrities. Similar to IMDb, Filmweb also has a ranking system that allows users to rate and review films. The Filmweb Top 250 is a list of the highest-rated movies on the platform, based on user ratings."

        # Check if records exist in the database
        if not FilmwebTop250.objects.exists():
            list_title = "We apologize for the inconvenience. This is the first launch of the application, and our scrapers are currently loading content or updating data. Please bear with us for a moment. The entire process should not take more than 2 minutes. Thank you for your understanding!"
            context = {"list_title": list_title}
            return render(request, "list_management/ranking.html", context)

        movies = FilmwebTop250.objects.all().order_by('rank')
        wachted_movies = [movie for movie in movies if movie.original_title in my_films_titles]
        percentage_watched = round((len(wachted_movies) / len(movies))*100)
        context = {
            "user_list": movies,
            "list_title": list_title,
            "description": description,
            "movies_count": len(wachted_movies),
            "percentage_watched": percentage_watched,
        }

    else:
        pass

    return render(request, "list_management/ranking.html", context)


@login_required
def best_picture(request):
    """
    Displays a list of movies that have won the Oscar for Best Picture.
    
    The function fetches the list of Oscar-winning movies from the database. If the data is not available, 
    a message is displayed to the user indicating that the data is being fetched.
    """
    list_title = "Best picture"
    description = "Winner in the best picture category awarded by the oscar awards academy from 1927/1928 to present."

    # Check if records exist in the database
    if not OscarWinner.objects.exists():
            list_title = "We apologize for the inconvenience. This is the first launch of the application, and our scanners are currently loading content or updating data. Please bear with us for a moment. The entire process should not take more than 2 minutes. Thank you for your understanding!"
            context = {"list_title": list_title}
            return render(request, "list_management/best_picture.html", context)

    winners = OscarWinner.objects.all().order_by('year')
    context = {
        "winners": winners,
        "list_title": list_title,
        "description": description,
    }

    return render(request, "list_management/best_picture.html", context)


@login_required
def rate_movie(request, title, year, rating):
    """    
    The function first checks if the movie exists in the database. If it does, the rating is updated. 
    If not, a new movie entry is created with the provided rating. The movie is then added to the user's rated list.
    The field for entering the ranking is displayed after pressing the star on any poster using Javascript
    """

    user = request.user
    user_ranking, _ = MovieList.objects.get_or_create(user=user, name="My Films")

    if "." in title:
        title = title.split(".", 1)[1].strip()

    tmdb_client = TMDBClient()
    movie_data = tmdb_client.get_single_movie_core(title, year)
    rating += 1
    try:
        # Attempt to retrieve the movie based on the custom_id
        movie_obj = Movie.objects.get(custom_id=movie_data["id"])
        # If the movie already exists, update the rating
        movie_obj.rating = rating
        movie_obj.save()

    except Movie.DoesNotExist:
        # If the movie doesn't exist, create a new one
        movie_obj = Movie.objects.create(
            title=movie_data["title"],
            year=movie_data["release_date"],
            poster_path=movie_data["poster_path"],
            custom_id=movie_data["id"],
            rating=rating,
            on_watchlist="watched",
        )

    # Always add the movie to user's rated list, regardless of it being new or existing
    user_ranking.movies.add(movie_obj)
    referer = request.META.get("HTTP_REFERER")
    return redirect(referer)


@login_required
def list_movies(request, name):
    """
    This function displays a list of movies for the user. It can either show a predefined list
    or display search results based on the user's input. The user can also view movies they've
    added to their personal lists.
    """

    context = {}
    if request.method == "POST":
        search_term = request.POST.get(
            "search"
        )  # Get the search term from the POST data
        tmdb_client = TMDBClient()  # Create an instance of the TMDBClient class
        movies = tmdb_client.search_movies(
            search_term
        )  # Call the search_movie method on the instance

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
        context["search_results"] = movies

    user = request.user

    # Get the user list or create one if it doesn't exist
    user_list, _ = MovieList.objects.get_or_create(user=user, name=name)
    movies = user_list.movies.all()
    context["user_list"] = user_list.movies.order_by("-rating")
    context["name"] = user_list.name
    context["description"] = user_list.description
    return render(request, "list_management/list.html", context)


@login_required
def choose_list(request):
    """
    This function provides an interface for the user to select from their available movie lists.
    It presents all the movie lists associated with the user.
    """
    user = request.user
    user_lists = MovieList.objects.filter(user=user)

    context = {"user_lists": user_lists}
    return render(request, "list_management/choose_list.html", context)


@login_required
def add_list(request, type):
    """
    This function allows the user to create a new list. Depending on the type specified,
    the user can create a list for movies or persons (actors/directors).
    """
    if request.method == "POST":
        user = request.user
        name = request.POST.get("name")
        description = request.POST.get("description")

        if type == "Movie":
            new_list = MovieList(user=user, name=name, description=description)
        else:
            new_list = PersonList(user=user, name=name, description=description)

        new_list.save()

    referer = request.META.get("HTTP_REFERER")
    return redirect(referer)


@login_required
def add_to_list(request, movie_title, movie_year, name):
    """
    This function lets the user add a specific movie to one of their personal lists.
    It fetches movie details from an external service (TMDB) and then adds it to the specified list.

    The use of `transaction.atomic()` ensures that all the database operations within its block are
    treated as a single unit. This means that if any operation fails, all changes made within the block
    are rolled back, ensuring data integrity. In this context, it ensures that both the creation or
    retrieval of the movie object and its addition to the user's list are successful. If there's an
    issue with any of these operations, no partial data will be saved, preventing potential inconsistencies
    in the database.
    """
    user = request.user

    # Get the user list or create one if it doesn't exist
    user_list, _ = MovieList.objects.get_or_create(user=user, name=name)

    if "." in movie_title:
        movie_title = movie_title.split(".", 1)[1].strip()

    tmdb_client = TMDBClient()
    movie_data = tmdb_client.get_single_movie_core(movie_title, movie_year)

    with transaction.atomic():  # Start of transaction block
        movie_obj, created = Movie.objects.get_or_create(
            title=movie_data["title"],
            year=movie_data["release_date"],
            poster_path=movie_data["poster_path"],
            custom_id=movie_data["id"],
            defaults={"on_watchlist": "yes" if name == "Watchlist" else "no"}
        )

        if not created:
            # If the movie was not created (i.e., it already existed), update the on_watchlist field
            movie_obj.on_watchlist = "yes" if name == "Watchlist" else "no"
            movie_obj.save()

        # Add the movie to the user's watchlist
        user_list.movies.add(movie_obj)

    referer = request.META.get("HTTP_REFERER")
    return redirect(referer)


@login_required
def person_list(request, name):
    """
    This function displays a list of persons, which can be actors or directors, based on the 
    user's search or a predefined list. The user can also view persons they've added to their personal lists.
    """
    user = request.user
    user_list, _ = PersonList.objects.get_or_create(user=user, name=name)

    context = {}
    if request.method == "POST":
        search_term = request.POST.get("search")
        tmdb_client = TMDBClient()
        persons = tmdb_client.search_person(search_term)

        persons = [
            {
                "id": actor["id"],
                "name": actor["name"],
                "profile_path": actor["profile_path"],
                "role": actor["known_for_department"],
            }
            for actor in persons
        ]
        context["search_results"] = persons

    persons = user_list.persons.all()
    context["user_list"] = persons
    context["name"] = name
    return render(request, "list_management/person_list.html", context)


@login_required
def add_person_to_list(request, name, id):
    """
    This function allows the user to add a specific person (actor or director) to one of their personal lists.
    It fetches person details from an external service (TMDB) and then adds them to the specified list.
    """
    user = request.user

    known_for_department = name

    if name == 'Acting':
        known_for_department = 'Favourite Actors'
    elif name == 'Directing':
        known_for_department = 'Favourite Directors'

    user_list, _ = PersonList.objects.get_or_create(user=user, name=known_for_department)

    tmdb_client = TMDBClient()
    person = tmdb_client.search_person_by_id(id)

    person, _ = Person.objects.get_or_create(
        name=person["name"],
        role=person["known_for_department"],
        profile_path=person["profile_path"],
        custom_id=person["id"],
    )

    user_list.persons.add(person)

    referer = request.META.get("HTTP_REFERER")
    return redirect(referer)


@login_required
def person_choose_list(request):
    """
    This function provides an interface for the user to select from their available person lists. 
    It presents all the person lists (like favorite actors or directors) associated with the user.
    """
    user = request.user
    user_lists = PersonList.objects.filter(user=user)

    context = {"user_lists": user_lists}
    return render(request, "list_management/person_choose_list.html", context)


@login_required
def remove_list(request, name, type):
    """
    This function allows the user to delete one of their personal lists. The user can remove either
    a movie list or a person list, depending on the type specified.
    """
    user = request.user

    if type == "Movie":
        list_to_remove = MovieList.objects.filter(user=user, name=name).first()
    else:
        list_to_remove = PersonList.objects.filter(user=user, name=name).first()

    if list_to_remove:
        if name in ["Watchlist", "My Films", "Favourite Actors", "Favourite Directors"]:
            messages.error(
                request,
                "You cannot delete this list because it is the primary list that every user has!",
            )
        else:
            list_to_remove.delete()

    referer = request.META.get("HTTP_REFERER")
    return redirect(referer)


@login_required
def remove_from_list(request, name, type, id):
    """
    This function lets the user remove a specific item (movie or person) from one of their personal lists.
    The item is identified by its unique ID and is removed from the specified list.
    """
    user = request.user

    if type == "Movie":
        list_to_remove_from = MovieList.objects.filter(user=user, name=name).first()
        if list_to_remove_from:
            movie_to_remove = Movie.objects.filter(custom_id=id).first()
            if movie_to_remove:
                list_to_remove_from.movies.remove(movie_to_remove)
    else:
        list_to_remove_from = PersonList.objects.filter(user=user, name=name).first()
        if list_to_remove_from:
            person_to_remove = Person.objects.filter(custom_id=id).first()
            if person_to_remove:
                list_to_remove_from.persons.remove(person_to_remove)

    referer = request.META.get("HTTP_REFERER")
    return redirect(referer)