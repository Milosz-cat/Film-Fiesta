from django.test import TestCase
from list_management.models import (
    MovieList,
    PersonList,
    IMDBTop250,
    FilmwebTop250,
    OscarWinner,
    OscarNomination,
)
from django.contrib.auth.models import User


class MovieListTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser")
        MovieList.objects.create(user=user, name="Test Movie List")

    def test_movie_list_creation(self):
        movie_list = MovieList.objects.get(name="Test Movie List")
        self.assertEqual(movie_list.name, "Test Movie List")


class PersonListTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser")
        PersonList.objects.create(user=user, name="Test Person List")

    def test_person_list_creation(self):
        person_list = PersonList.objects.get(name="Test Person List")
        self.assertEqual(person_list.name, "Test Person List")


class IMDBTop250TestCase(TestCase):
    def setUp(self):
        IMDBTop250.objects.create(rank=1, title="Test Movie", year=2020)

    def test_imdb_top250_creation(self):
        movie = IMDBTop250.objects.get(rank=1)
        self.assertEqual(movie.title, "Test Movie")


class FilmwebTop250TestCase(TestCase):
    def setUp(self):
        FilmwebTop250.objects.create(rank=1, title="Test Movie", year=2020)

    def test_filmweb_top250_creation(self):
        movie = FilmwebTop250.objects.get(rank=1)
        self.assertEqual(movie.title, "Test Movie")


class OscarWinnerTestCase(TestCase):
    def setUp(self):
        OscarWinner.objects.create(
            year="2020", release_year=2020, title="Test Winner", studio="Test Studio"
        )

    def test_oscar_winner_creation(self):
        winner = OscarWinner.objects.get(title="Test Winner")
        self.assertEqual(winner.studio, "Test Studio")


class OscarNominationTestCase(TestCase):
    def setUp(self):
        winner = OscarWinner.objects.create(
            year="2020", release_year=2020, title="Test Winner", studio="Test Studio"
        )
        OscarNomination.objects.create(
            winner=winner,
            title="Test Nominee",
            release_year=2020,
            studio="Test Studio Nominee",
        )

    def test_oscar_nomination_creation(self):
        nominee = OscarNomination.objects.get(title="Test Nominee")
        self.assertEqual(nominee.studio, "Test Studio Nominee")
