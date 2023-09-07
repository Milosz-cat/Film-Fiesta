from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Movie(models.Model):
    """Represents a movie with its details such as title, year, poster, and rating."""
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    custom_id = models.IntegerField(primary_key=True, default=None)
    poster_path = models.URLField(max_length=200, default=None)
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
    """Represents a person involved in movies, such as actors or directors, with their name and role."""
    name = models.CharField(max_length=100)
    custom_id = models.IntegerField(primary_key=True, default=None)
    role = models.CharField(max_length=30)
    profile_path = models.URLField(max_length=200, default=None)

    def __str__(self):
        return self.name
    

class TimestampedModel(models.Model):
    """Abstract model for common fields and methods in Review and Comment models."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    content = models.CharField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This ensures that this model won't be used to create any database table

    def __str__(self):
        return f"{self.user.username}'s {self.__class__.__name__}"


class Review(TimestampedModel):
    """Represents a user's review for a specific movie."""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"Review by {self.user.username}"


class Comment(TimestampedModel):
    """Represents a user's comment on a movie review."""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.user.username}'s comment to {str(self.review)}"