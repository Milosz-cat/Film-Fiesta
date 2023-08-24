import logging
from list_management.scraper import IMDBTop250Scraper, FilmwebTop250Scraper, OscarBestPictureScraper
from celery import shared_task

# Set up logging
logger = logging.getLogger(__name__)

@shared_task
def scrape_imdb_top_250():
    logger.info("Starting IMDB Top 250 scraping task...")
    scraper = IMDBTop250Scraper()
    scraper.scrape()
    logger.info("Finished IMDB Top 250 scraping task.")

@shared_task
def scrape_filmweb_top_250():
    logger.info("Starting Filmweb Top 250 scraping task...")
    scraper = FilmwebTop250Scraper()
    scraper.scrape()
    logger.info("Finished Filmweb Top 250 scraping task.")

@shared_task
def scrape_oscar_best_picture():
    logger.info("Starting Oscar Best Picture scraping task...")
    scraper = OscarBestPictureScraper()
    scraper.scrape()
    logger.info("Finished Oscar Best Picture scraping task.")
