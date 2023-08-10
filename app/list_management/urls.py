from django.urls import path
from . import views


urlpatterns = [
    path('list/<str:name>/', views.list_movies, name="list"),
    path("choose_list", views.choose_list, name="choose_list"),
    path(
        "add_to_watchlist/<str:movie_title>/<int:movie_year>/",
        views.add_to_watchlist,
        name="add_to_watchlist",
    ),
]
