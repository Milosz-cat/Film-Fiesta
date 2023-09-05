from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('movie/<str:title>/<str:year>/', views.movie, name="movie"),
    path('person/<str:name>/', views.person, name="person"),
    path('search/', views.search, name="search"),
    path('add_review/<int:movie_id>', views.add_review, name='add_review'),
    path('add_comment/<int:review_id>', views.add_comment, name='add_comment'),
    path('profile_reviews', views.profile_reviews, name='profile_reviews'),
    path('remove_review/<int:pk>', views.remove_review, name='remove_review'),
    path('remove_comment/<int:pk>', views.remove_comment, name='remove_comment'),
]
