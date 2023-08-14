from django.urls import path
from . import views


urlpatterns = [
    path('list/<str:name>/', views.list_movies, name="list"),
    path('ranking/<str:name>/', views.ranking, name="ranking"),
    path('add_list', views.add_list, name="add_list"),
    path("choose_list", views.choose_list, name="choose_list"),
    path(
        "add_to_list/<str:movie_title>/<int:movie_year>/<str:name>/",
        views.add_to_list,
        name="add_to_list",
    ),
    path('actor_list', views.actor_list, name="actor_list"),
    path('add_person_to_list/<str:name>/<int:id>', views.add_person_to_list, name="add_person_to_list"),
]
