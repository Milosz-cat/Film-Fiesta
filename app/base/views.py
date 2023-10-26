from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from base.tmdb_helpers import TMDBClient
from list_management.models import MovieList
from base.models import Movie, Review, Comment
from django.contrib import messages
from django.db import transaction
from list_management.signals import home_visited


@login_required
def home(request):
    """
    Render the home page of the application.

    All views use @login_required decorator that redirects to login if the user
    is not authenticated.

    After entering this view, a home visited signal is sent automatically, the purpose
    of which is to scrape the rankings and Oscars when you first visit the application

    This view fetches (from TMDB API), process and send to template trending movies,
    movies that are currently playing, popular persons and movies from the user's watchlist.
    It also provides movie recommendations based on the last movie added to the user's
    "My Films" list.
    """

    home_visited.send(sender=home)

    context = {}
    tmdb_client = TMDBClient()
    trending_movies = [
        {
            "title": movie["title"],
            "popularity": movie.get("popularity", ""),
            "poster_path": movie["poster_path"],
            "custom_id": movie["id"],
            "year": movie["release_date"][0:4] if movie["release_date"] else None,
        }
        for movie in tmdb_client.get_trending_movies()
    ]

    now_playing_movies = [
        {
            "title": movie["title"],
            "popularity": movie.get("popularity", ""),
            "poster_path": movie["poster_path"],
            "custom_id": movie["id"],
            "year": movie["release_date"][0:4] if movie["release_date"] else None,
        }
        for movie in tmdb_client.get_now_playing_movies()
    ]

    user = request.user

    # Get the user's watchlist movies
    user_watchlist = MovieList.objects.get(user=user, name="Watchlist")
    watchlist_movies = user_watchlist.movies.all() if user_watchlist else None

    user_watched_films = MovieList.objects.get(user=user, name="My Films")
    last_added_movie = user_watched_films.movies.first()

    if last_added_movie:
        recommendations = [
            {
                "title": movie["title"],
                "popularity": movie.get("popularity", ""),
                "poster_path": movie["poster_path"],
                "custom_id": movie["id"],
                "year": movie["release_date"][0:4] if movie["release_date"] else None,
            }
            for movie in tmdb_client.get_movie_recommendations(
                last_added_movie.custom_id
            )
        ]
    else:
        recommendations = None

    popular_persons = [
        {
            "id": person["id"],
            "name": person["name"],
            "popularity": person.get("popularity", ""),
            "profile_path": person["profile_path"],
            "known_for_department": person["known_for_department"],
        }
        for person in tmdb_client.get_popular_people()
    ]

    context["popular_persons"] = popular_persons
    context["recommendations"] = recommendations
    context["trending_movies"] = trending_movies
    context["now_playing_movies"] = now_playing_movies
    context["watchlist_movies"] = watchlist_movies

    return render(request, "base/home.html", context)


@login_required
def movie(request, title, year):
    """
    Display detailed information about a specific movie.

    This view fetches detailed information about a movie based on its
    title and release year. It displays the movie's details, cast, crew,
    and user reviews.

    If movie title contains number (24. Title), it will be removed.
    """
    if "." in title:
        title = title.split(".", 1)[1].strip()

    tmdb_client = TMDBClient()
    movie_info = tmdb_client.get_single_movie(title, year)

    try:
        movie_reviews = Movie.objects.get(custom_id=movie_info["movie"]["id"])
        reviews = Review.objects.filter(movie=movie_reviews)
        movie_info["reviews"] = reviews
    except Movie.DoesNotExist:
        movie_reviews = None

    return render(request, "base/movie.html", movie_info)


@login_required
def person(request, name):
    """
    Display detailed information about a specific person in the film industry.

    This view fetches and displays a person's profile, including their filmography as an actor
    and director. It also calculates the percentage of the person's (as actor and director)
    movies that the user has watched.
    """

    tmdb_client = TMDBClient()
    person_info = tmdb_client.search_person(name)
    person_id = person_info[0]["id"]

    cast_movies, director_movies = tmdb_client.get_movies_by_person(person_id)

    # Filter and structure movies where the person is an actor
    person_movies_as_actor = [
        {
            "title": movie["title"],
            "character": movie.get("character", ""),
            "poster_path": movie["poster_path"],
            "year": movie["release_date"][0:4] if movie["release_date"] else None,
        }
        for movie in cast_movies
        if movie["release_date"] and "/" not in movie["title"]
    ]

    # Filter and structure movies where the person is a director
    person_movies_as_director = [
        {
            "title": movie["title"],
            "poster_path": movie["poster_path"],
            "year": movie["release_date"][0:4] if movie["release_date"] else None,
        }
        for movie in director_movies
        if movie["release_date"] and "/" not in movie["title"]
    ]

    user = request.user
    my_films_list = MovieList.objects.get(user=user, name="My Films")
    # retrieve the titles of movies in the user's "My Films" list
    my_films_titles = set(my_films_list.movies.values_list("title", flat=True))

    # Check how many movies from person_movies_as_actor are in the user's list
    if person_movies_as_actor:
        wachted_actor_movies = len(
            [
                movie
                for movie in person_movies_as_actor
                if movie["title"] in my_films_titles
            ]
        )
        percentage_watched_actor = round(
            (wachted_actor_movies / len(person_movies_as_actor)) * 100
        )
    if person_movies_as_director:
        wachted_director_movies = len(
            [
                movie
                for movie in person_movies_as_director
                if movie["title"] in my_films_titles
            ]
        )
        percentage_watched_director = round(
            (wachted_director_movies / len(person_movies_as_director)) * 100
        )

    biography = tmdb_client.search_person_by_id(person_id)["biography"]

    context = {
        "person": person_info[0],
        "movies": person_movies_as_actor,
        "movies_director": person_movies_as_director,
        "biography": biography,
        "id": person_id,
    }

    if person_movies_as_actor:
        context["actor_movies_count"] = wachted_actor_movies
        context["percentage_watched_actor"] = percentage_watched_actor
    if person_movies_as_director:
        context["director_movies_count"] = wachted_director_movies
        context["percentage_watched_director"] = percentage_watched_director

    return render(request, "base/person.html", context)


@login_required
def search(request):
    """
    Handle movie search functionality.

    This view allows users to search for movies by title. The results are fetched from the TMDB API
    and displayed in a paginated format.
    """

    if request.method == "POST":
        search_term = request.POST.get("search")

        tmdb_client = TMDBClient()
        results = tmdb_client.search_movies(search_term)

        results = [
            {
                "id": movie["id"],
                "title": movie["title"],
                "poster_path": movie["poster_path"],
                "release_date": movie["release_date"][:4],
            }
            for movie in results
        ]
        context = {"movies": results}
        return render(request, "base/search.html", context)

    return render(request, "base/search.html")


@login_required
def add_review(request, movie_id):
    """
    Allow users to add a review for a specific movie.

    Users can submit their reviews for a movie. Once submitted, the review is saved to the database,
    and the user is redirected back to the movie's detail page with a success message.
    """
    user = request.user

    # Try to get the movie from the database
    movie_with_no_review = Movie.objects.filter(custom_id=movie_id).first()

    # If the movie doesn't exist in the database, fetch its details and create it
    if not movie_with_no_review:
        tmdb_client = TMDBClient()
        movie_data = tmdb_client.get_movie_detalis(movie_id)

        user_list = MovieList.objects.get(user=user, name="My Films")

        with transaction.atomic():  # Start of transaction block
            movie_with_no_review, _ = Movie.objects.get_or_create(
                title=movie_data["title"],
                year=movie_data["release_date"][:4],
                poster_path=movie_data["poster_path"],
                custom_id=movie_data["id"],
                defaults={"on_watchlist": "watched"},
            )

            # Add the movie to the user's "My Films" list
            user_list.movies.add(movie_with_no_review)

    # Proceed to add the review
    if request.method == "POST":
        content = request.POST.get("content")
        review = Review(movie=movie_with_no_review, user=user, content=content)
        review.save()
        messages.success(request, "Your review has been successfully created.")

    referer = request.META.get("HTTP_REFERER")
    return redirect(referer)


@login_required
def add_comment(request, review_id):
    """Allow the user to add a comment to a specific review and redirect back
    to the movie's page."""

    review = get_object_or_404(Review, pk=review_id)

    if request.method == "POST":
        content = request.POST.get("comment_content")

        comment = Comment(review=review, user=request.user, content=content)
        comment.save()
        messages.success(request, "Your comment has been successfully created.")

    referer = request.META.get("HTTP_REFERER")
    return redirect(referer)


@login_required
def profile_reviews(request):
    """Render the user's profile page showing all their reviews and comments."""

    user = request.user
    reviews = Review.objects.filter(user=user)
    comments = Comment.objects.filter(user=user)

    context = {"reviews": reviews, "comments": comments}
    return render(request, "base/reviews.html", context)


@login_required
def remove_review(request, pk):
    """Allow the user to delete a specific review and redirect back to the referring page."""

    review = get_object_or_404(Review, pk=pk)
    review.delete()

    referer = request.META.get("HTTP_REFERER")
    return redirect(referer)


@login_required
def remove_comment(request, pk):
    """Allow the user to delete a specific comment and redirect back to the referring page."""

    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()

    referer = request.META.get("HTTP_REFERER")
    return redirect(referer)
