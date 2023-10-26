from django.contrib import admin
from .models import (
    MovieList,
    PersonList,
    IMDBTop250,
    FilmwebTop250,
    OscarWinner,
    OscarNomination,
)

# Register your models here.
admin.site.register(MovieList)
admin.site.register(PersonList)
admin.site.register(IMDBTop250)
admin.site.register(FilmwebTop250)
admin.site.register(OscarWinner)
admin.site.register(OscarNomination)
