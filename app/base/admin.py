from django.contrib import admin
from .models import Movie, Person, Review, Comment

# Register your models here.
admin.site.register(Movie)
admin.site.register(Person)
admin.site.register(Review)
admin.site.register(Comment)