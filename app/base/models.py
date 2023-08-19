from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    custom_id = models.IntegerField(primary_key=True, default=None)
    poster_path = models.CharField(max_length=200, default=None)
    rating = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ],
    default=0)
    WATCHLIST_CHOICES = (
        ("yes", "Yes"),
        ("no", "No"),
        ("watched", "Watched"),
    )
    on_watchlist = models.CharField(max_length=10, choices=WATCHLIST_CHOICES, default="no")


    def __str__(self):
        return self.title


class Person(models.Model):
    name = models.CharField(max_length=100)
    custom_id = models.IntegerField(primary_key=True, default=None)
    role = models.CharField(max_length=30)
    profile_path = models.CharField(max_length=200, default=None)

    def __str__(self):
        return self.name
    

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, default=None)
    content = models.CharField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Review by" + self.user.username
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, default=None)
    content = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + "'s comment to " + str(self.review)