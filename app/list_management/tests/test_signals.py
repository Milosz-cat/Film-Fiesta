from django.test import TestCase
from django.contrib.auth.models import User
from list_management.models import MovieList, PersonList


class SignalsTest(TestCase):
    def test_create_watchlist_signal(self):
        # Create a new user
        user = User.objects.create_user(username="testuser", password="testpass")

        # Check if the lists were created for the new user
        self.assertTrue(MovieList.objects.filter(user=user, name="Watchlist").exists())
        self.assertTrue(MovieList.objects.filter(user=user, name="My Films").exists())
        self.assertTrue(
            PersonList.objects.filter(user=user, name="Favourite Actors").exists()
        )
        self.assertTrue(
            PersonList.objects.filter(user=user, name="Favourite Directors").exists()
        )
