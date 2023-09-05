from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from base.models import Movie, Review, Comment

class ViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='12345')
        self.movie = Movie.objects.create(title="Test Movie", year=2023, custom_id=1, poster_path="test_path")
        self.review = Review.objects.create(user=self.user, movie=self.movie, content="Test Review")
        self.comment = Comment.objects.create(user=self.user, review=self.review, content="Test Comment")

        self.client.login(username='testuser', password='12345')  # Logging in the user

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/home.html')

    def test_movie_view(self):
        response = self.client.get(reverse('movie', args=['Inception', 2010]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/movie.html')

    def test_person_view(self):
        response = self.client.get(reverse('person', args=['Leonardo DiCaprio']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/person.html')

    def test_search_view(self):
        response = self.client.post(reverse('search'), {'search': 'Inception'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/search.html')

    def test_add_review_view(self):
        response = self.client.post(reverse('add_review', args=[1]), {'content': 'New Review'}, HTTP_REFERER=reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_add_comment_view(self):
        response = self.client.post(reverse('add_comment', args=[self.review.pk]), {'comment_content': 'New Comment'}, HTTP_REFERER=reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_profile_reviews_view(self):
        response = self.client.get(reverse('profile_reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/reviews.html')

    def test_remove_review_view(self):
        response = self.client.get(reverse('remove_review', args=[self.review.pk]), HTTP_REFERER=reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_remove_comment_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('remove_comment', args=[self.comment.pk]), HTTP_REFERER=reverse('home'))
        self.assertEqual(response.status_code, 302)

