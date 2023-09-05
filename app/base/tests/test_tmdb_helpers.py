# from unittest import TestCase, mock
# from base.tmdb_helpers import TMDBClient

# class TestTMDBClient(TestCase):

#     def setUp(self):
#         self.client = TMDBClient()

#     @mock.patch('base.tmdb_helpers.requests.get')
#     def test_search_movies(self, mock_get):
#         mock_get.return_value.json.return_value = {'results': [{'title': 'Inception'}]}
#         results = self.client.search_movies("Inception")
#         self.assertEqual(len(results), 1)
#         self.assertEqual(results[0]['title'], 'Inception')

#     @mock.patch('base.tmdb_helpers.requests.get')
#     def test_search_movie(self, mock_get):
#         mock_get.return_value.json.return_value = {'results': [{'title': 'Inception'}]}
#         result = self.client.search_movie("Inception", 2010)
#         self.assertEqual(result['title'], 'Inception')

#     @mock.patch('base.tmdb_helpers.requests.get')
#     def test_get_movie_persons(self, mock_get):
#         mock_get.return_value.json.return_value = {'cast': [], 'crew': []}
#         result = self.client.get_movie_persons(123)
#         self.assertIn('cast', result)
#         self.assertIn('crew', result)

#     @mock.patch('base.tmdb_helpers.requests.get')
#     def test_get_movie_details(self, mock_get):
#         mock_get.return_value.json.return_value = {'title': 'Inception'}
#         result = self.client.get_movie_detalis(123)
#         self.assertEqual(result['title'], 'Inception')

#     @mock.patch('base.tmdb_helpers.requests.get')
#     def test_process_cast(self, mock_get):
#         cast_data = [
#             {
#                 'id': 1,
#                 'name': 'Leonardo DiCaprio',
#                 'character': 'Cobb',
#                 'popularity': 10,
#                 'profile_path': '/path/to/image.jpg'
#             }
#         ]
#         result = self.client.process_cast(cast_data)
#         self.assertEqual(len(result), 1)
#         self.assertEqual(result[0]['name'], 'Leonardo DiCaprio')
#         self.assertEqual(result[0]['character'], 'Cobb')

#     @mock.patch('base.tmdb_helpers.requests.get')
#     def test_process_crew(self, mock_get):
#         crew_data = [
#             {
#                 'id': 1,
#                 'name': 'Christopher Nolan',
#                 'job': 'Director',
#                 'popularity': 10,
#                 'profile_path': '/path/to/image.jpg',
#                 'known_for_department': 'Directing'
#             }
#         ]
#         result = self.client.process_crew(crew_data)
#         self.assertEqual(len(result), 1)
#         self.assertEqual(result[0]['name'], 'Christopher Nolan')
#         self.assertEqual(result[0]['known_for_department'], 'Directing')

#     @mock.patch('base.tmdb_helpers.requests.get')
#     def test_format_number(self, mock_get):
#         self.assertEqual(self.client.format_number(1000), "1 k $ ")
#         self.assertEqual(self.client.format_number(1000000), "1 mln $ ")
#         self.assertEqual(self.client.format_number(1000000000), "1 mld $ ")

#     @mock.patch('base.tmdb_helpers.requests.get')
#     def test_get_single_movie(self, mock_get):
#         mock_get.return_value.json.return_value = {'results': [{'id': 1, 'title': 'Inception', 'poster_path': '/path/to/image.jpg', 'release_date': '2010-07-16'}]}
#         result = self.client.get_single_movie("Inception", 2010)
#         self.assertEqual(result['movie']['title'], 'Inception')

#     @mock.patch('base.tmdb_helpers.requests.get')
#     def test_search_person_by_id(self, mock_get):
#         mock_get.return_value.json.return_value = {'name': 'Leonardo DiCaprio'}
#         result = self.client.search_person_by_id(1)
#         self.assertEqual(result['name'], 'Leonardo DiCaprio')

#     @mock.patch('base.tmdb_helpers.requests.get')
#     def test_search_person(self, mock_get):
#         mock_get.return_value.json.return_value = {'results': [{'name': 'Leonardo DiCaprio'}]}
#         results = self.client.search_person("Leonardo DiCaprio")
#         self.assertEqual(len(results), 1)
#         self.assertEqual(results[0]['name'], 'Leonardo DiCaprio')

#     @mock.patch('base.tmdb_helpers.requests.get')
#     def test_get_trending_movies(self, mock_get):
#         mock_get.return_value.json.return_value = {'results': [{'title': 'Inception'}]}
#         results = self.client.get_trending_movies()
#         self.assertEqual(len(results), 1)
#         self.assertEqual(results[0]['title'], 'Inception')

#     @mock.patch('base.tmdb_helpers.requests.get')
#     def test_get_now_playing_movies(self, mock_get):
#         mock_get.return_value.json.return_value = {'results': [{'title': 'Inception'}]}
#         results = self.client.get_now_playing_movies()
#         self.assertEqual(len(results), 1)
#         self.assertEqual(results[0]['title'], 'Inception')

#     @mock.patch('base.tmdb_helpers.requests.get')
#     def test_get_movie_recommendations(self, mock_get):
#         mock_get.return_value.json.return_value = {'results': [{'title': 'Inception'}]}
#         results = self.client.get_movie_recommendations(1)
#         self.assertEqual(len(results), 1)
#         self.assertEqual(results[0]['title'], 'Inception')

#     @mock.patch('base.tmdb_helpers.requests.get')
#     def test_get_popular_people(self, mock_get):
#         mock_get.return_value.json.return_value = {'results': [{'name': 'Leonardo DiCaprio'}]}
#         results = self.client.get_popular_people()
#         self.assertEqual(len(results), 1)
#         self.assertEqual(results[0]['name'], 'Leonardo DiCaprio')


