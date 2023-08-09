from django.urls import path
from . import views


urlpatterns = [
    path("choose_list", views.choose_list, name="choose_list"),
]
