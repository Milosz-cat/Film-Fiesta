from django.test import TestCase
from base.models import Movie, Person, Review, Comment
from django.contrib.auth.models import User

class MovieModelTest(TestCase):
    def setUp(self):
        Movie.objects.create(title="Test Movie", year=2023, custom_id=1, poster_path="test_path")

    def test_movie_creation(self):
        movie = Movie.objects.get(custom_id=1)
        self.assertEqual(movie.title, "Test Movie")
        self.assertEqual(movie.year, 2023)

class PersonModelTest(TestCase):
    def setUp(self):
        Person.objects.create(name="Test Person", custom_id=1, role="Actor", profile_path="test_path")

    def test_person_creation(self):
        person = Person.objects.get(custom_id=1)
        self.assertEqual(person.name, "Test Person")
        self.assertEqual(person.role, "Actor")

class ReviewModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        movie = Movie.objects.create(title="Test Movie", year=2023, custom_id=1, poster_path="test_path")
        Review.objects.create(user=user, movie=movie, content="Test Review")

    def test_review_creation(self):
        review = Review.objects.get(content="Test Review")
        self.assertEqual(review.user.username, "testuser")
        self.assertEqual(review.movie.title, "Test Movie")

class CommentModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        movie = Movie.objects.create(title="Test Movie", year=2023, custom_id=1, poster_path="test_path")
        review = Review.objects.create(user=user, movie=movie, content="Test Review")
        Comment.objects.create(user=user, review=review, content="Test Comment")

    def test_comment_creation(self):
        comment = Comment.objects.get(content="Test Comment")
        self.assertEqual(comment.user.username, "testuser")
        self.assertEqual(comment.review.content, "Test Review")

