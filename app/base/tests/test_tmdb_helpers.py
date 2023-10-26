from unittest import TestCase, mock
from base.tmdb_helpers import TMDBClient


class TestTMDBClient(TestCase):
    """
    Unit tests for the TMDBClient class in the base.tmdb_helpers module.

    The TMDBClient class provides various methods to interact with the TMDB (The Movie Database)
    API.These unit tests aim to ensure that each method of the TMDBClient class functions as
    expected.

    Mocking is employed in these tests to simulate the behavior of external dependencies, in this
    case, the requests made to the TMDB API. By using the `mock.patch` decorator, we can replace
    the actual `requests.get` method with a mock object. This allows us to control the responses
    returned by the API and ensure that the TMDBClient methods process the data correctly.
    Mocking ensures that the tests are not dependent on the actual API's availability or its real
    data, making the tests more reliable and faster.

    Each test method in this class focuses on a specific method of the TMDBClient and checks its
    functionality based on the mock returned values. The assertions in each test ensure that the
    methods handle the mock data as expected.

    To get more information about every test in this class go to --> base.tmdb_helpers.

    Attributes:
        client (TMDBClient): An instance of the TMDBClient class to be tested.
    """

    def setUp(self):
        self.client = TMDBClient()

    @mock.patch("base.tmdb_helpers.requests.get")
    def test_search_movies(self, mock_get):
        mock_get.return_value.json.return_value = {"results": [{"title": "Inception"}]}
        results = self.client.search_movies("Inception")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Inception")

    @mock.patch("base.tmdb_helpers.requests.get")
    def test_search_movie(self, mock_get):
        mock_get.return_value.json.return_value = {"results": [{"title": "Inception"}]}
        result = self.client.search_movie("Inception", 2010)
        self.assertEqual(result["title"], "Inception")

    @mock.patch("base.tmdb_helpers.requests.get")
    def test_get_movie_persons(self, mock_get):
        mock_get.return_value.json.return_value = {"cast": [], "crew": []}
        result = self.client.get_movie_persons(123)
        self.assertIn("cast", result)
        self.assertIn("crew", result)

    @mock.patch("base.tmdb_helpers.requests.get")
    def test_get_movie_details(self, mock_get):
        mock_get.return_value.json.return_value = {"title": "Inception"}
        result = self.client.get_movie_detalis(123)
        self.assertEqual(result["title"], "Inception")

    @mock.patch("base.tmdb_helpers.requests.get")
    def test_process_cast(self):
        cast_data = [
            {
                "id": 1,
                "name": "Leonardo DiCaprio",
                "character": "Cobb",
                "popularity": 10,
                "profile_path": "/path/to/image.jpg",
            }
        ]
        result = self.client.process_cast(cast_data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Leonardo DiCaprio")
        self.assertEqual(result[0]["character"], "Cobb")

    @mock.patch("base.tmdb_helpers.requests.get")
    def test_process_crew(self):
        crew_data = [
            {
                "id": 1,
                "name": "Christopher Nolan",
                "job": "Director",
                "popularity": 10,
                "profile_path": "/path/to/image.jpg",
                "known_for_department": "Directing",
            }
        ]
        result = self.client.process_crew(crew_data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Christopher Nolan")
        self.assertEqual(result[0]["known_for_department"], "Directing")

    @mock.patch("base.tmdb_helpers.requests.get")
    def test_format_number(self):
        self.assertEqual(self.client.format_number(1000), "1 k $ ")
        self.assertEqual(self.client.format_number(1000000), "1 mln $ ")
        self.assertEqual(self.client.format_number(1000000000), "1 mld $ ")

    @mock.patch("base.tmdb_helpers.requests.get")
    def test_search_person_by_id(self, mock_get):
        mock_get.return_value.json.return_value = {"name": "Leonardo DiCaprio"}
        result = self.client.search_person_by_id(1)
        self.assertEqual(result["name"], "Leonardo DiCaprio")

    @mock.patch("base.tmdb_helpers.requests.get")
    def test_search_person(self, mock_get):
        mock_get.return_value.json.return_value = {
            "results": [{"name": "Leonardo DiCaprio"}]
        }
        results = self.client.search_person("Leonardo DiCaprio")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Leonardo DiCaprio")

    @mock.patch("base.tmdb_helpers.requests.get")
    def test_get_trending_movies(self, mock_get):
        mock_get.return_value.json.return_value = {"results": [{"title": "Inception"}]}
        results = self.client.get_trending_movies()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Inception")

    @mock.patch("base.tmdb_helpers.requests.get")
    def test_get_now_playing_movies(self, mock_get):
        mock_get.return_value.json.return_value = {"results": [{"title": "Inception"}]}
        results = self.client.get_now_playing_movies()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Inception")

    @mock.patch("base.tmdb_helpers.requests.get")
    def test_get_movie_recommendations(self, mock_get):
        mock_get.return_value.json.return_value = {"results": [{"title": "Inception"}]}
        results = self.client.get_movie_recommendations(1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Inception")

    @mock.patch("base.tmdb_helpers.requests.get")
    def test_get_popular_people(self, mock_get):
        mock_get.return_value.json.return_value = {
            "results": [{"name": "Leonardo DiCaprio"}]
        }
        results = self.client.get_popular_people()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Leonardo DiCaprio")
