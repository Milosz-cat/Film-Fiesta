"""
This module contains asynchronous tasks for scraping movie-related data using Celery.

The tasks in this module are responsible for scraping data from various sources:
- IMDB Top 250 movies
- Filmweb Top 250 movies
- Oscar Best Picture winners

Each task initializes the appropriate scraper, starts the scraping process, and logs the start and completion of the task.

Tasks:
- scrape_imdb_top_250: Scrapes the top 250 movies from IMDB.
- scrape_filmweb_top_250: Scrapes the top 250 movies from Filmweb.
- scrape_oscar_best_picture: Scrapes the Oscar Best Picture winners.

Logging:
- The module uses Python's built-in logging module to log the progress of each task. The logger is named after the module's name.
"""

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
