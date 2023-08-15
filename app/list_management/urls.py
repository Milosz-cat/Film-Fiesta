from django.urls import path
from . import views


urlpatterns = [
    path('list/<str:name>/', views.list_movies, name="list"),
    path('rate_movie/<str:title>/<str:year>/<int:rating>/', views.rate_movie, name="rate_movie"),
    path('ranking/<str:name>/', views.ranking, name="ranking"),
    path('add_list', views.add_list, name="add_list"),
    path("choose_list", views.choose_list, name="choose_list"),
    path(
        "add_to_list/<str:movie_title>/<int:movie_year>/<str:name>/",
        views.add_to_list,
        name="add_to_list",
    ),
    path('person_list/<str:name>', views.person_list, name="person_list"),
    path('add_person_to_list/<str:name>/<int:id>', views.add_person_to_list, name="add_person_to_list"),
]
# @login_required
# def rate_movie(request, title, year, rating):
#     user = request.user
#     user_ranking, _ = MovieList.objects.get_or_create(user=user, name='Rated Films')

#     if "." in title:
#         title = title.split(".", 1)[1].strip()

#     tmdb_client = TMDBClient()
#     movie_data = tmdb_client.get_single_movie_core(title, year)

#     # Attempt to retrieve the movie based on the custom_id
#     movie_obj, created = Movie.objects.get_or_create(
#         custom_id=movie_data["id"],
#         title=movie_data["title"],
#         year=movie_data["release_date"],
#         poster_path=movie_data["poster_path"],
#         on_watchlist="watched",

#     )

#     # If the movie already exists or even if it's newly created, we update the rating
#     movie_obj.rating = rating
#     movie_obj.save()

#     user_ranking.movies.add(movie_obj)
    
#     referer = request.META.get("HTTP_REFERER")
#     return redirect(referer)