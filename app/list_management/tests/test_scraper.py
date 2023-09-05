from django.test import TestCase
from list_management.models import IMDBTop250, FilmwebTop250, OscarWinner, OscarNomination
from list_management.scraper import IMDBTop250Scraper, FilmwebTop250Scraper, OscarBestPictureScraper

class IMDBTop250ScraperTest(TestCase):
    """
    Test case for the IMDBTop250Scraper class.

    This test case focuses on verifying the functionality of the IMDBTop250Scraper class.
    The scraper is designed to fetch movie data from the IMDB Top 250 list and populate
    the database with the scraped data.

    Methods:
    - setUp: Initializes the scraper instance for testing.
    - test_scrape_with_limit: Tests the scraper's ability to fetch a limited number of movies
      (in this case, just one movie) and ensures that the database reflects the correct count
      of scraped movies.
    """
    def setUp(self):
        self.scraper = IMDBTop250Scraper()


    def test_scrape_with_limit(self):
        self.scraper.scrape(limit=1)
        
        # Check if there's exactly 1 movie in the database
        self.assertEqual(IMDBTop250.objects.count(), 1)

class FilmwebTop250ScraperTest(TestCase):

    def setUp(self):
        self.scraper = FilmwebTop250Scraper()


    def test_scrape_with_limit_and_scroll(self):
        self.scraper.scrape(limit=1, scrolls=1)

        self.assertEqual(FilmwebTop250.objects.count(), 1)

class OscarBestPictureScraperTest(TestCase):

    def setUp(self):
        self.scraper = OscarBestPictureScraper()

    def test_scrape_with_limit(self):
        self.scraper.scrape(limit=1)
        
        # Check if there's exactly 1 winner in the database
        self.assertEqual(OscarWinner.objects.count(), 1)

        # Check if there are any nominations related to that winner
        winner = OscarWinner.objects.first()
        self.assertTrue(OscarNomination.objects.filter(winner=winner).exists())