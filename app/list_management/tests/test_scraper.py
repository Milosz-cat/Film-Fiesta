from django.test import TestCase
from list_management.models import IMDBTop250, FilmwebTop250, OscarWinner, OscarNomination
from list_management.scraper import IMDBTop250Scraper, FilmwebTop250Scraper, OscarBestPictureScraper

class IMDBTop250ScraperTest(TestCase):
    
    def setUp(self):
        self.scraper = IMDBTop250Scraper()

    def test_scrape_with_limit(self):
        self.scraper.scrape(limit=1)
        
        # Sprawdź, czy w bazie danych jest dokładnie 1 film
        self.assertEqual(IMDBTop250.objects.count(), 1)

class FilmwebTop250ScraperTest(TestCase):

    def setUp(self):
        self.scraper = FilmwebTop250Scraper()

    def test_scrape_with_limit_and_scroll(self):
        self.scraper.scrape(limit=1, scrolls=1)

        # Sprawdź, czy w bazie danych jest dokładnie 1 film
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