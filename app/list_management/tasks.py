"""
This module contains asynchronous tasks for scraping movie-related data using Celery.

The tasks in this module are responsible for scraping data from various sources:
- IMDB Top 250 movies
- Filmweb Top 250 movies
- Oscar Best Picture winners

Each task initializes the appropriate scraper, starts the scraping process, logs the start and completion of the task, and then deletes its associated task ID from the cache. This ensures that the task can be re-triggered in the future if necessary.

Tasks:
- scrape_imdb_top_250: Scrapes the top 250 movies from IMDB and deletes its task ID from the cache upon completion.
- scrape_filmweb_top_250: Scrapes the top 250 movies from Filmweb and deletes its task ID from the cache upon completion.
- scrape_oscar_best_picture: Scrapes the Oscar Best Picture winners and deletes its task ID from the cache upon completion.

Cache Management:
- After each task completes its scraping process, it removes its associated task ID from the cache. This ensures that the system knows the task has completed and can be re-triggered if necessary.

Logging:
- The module uses Python's built-in logging module to log the progress of each task. The logger is named after the module's name.
"""

import logging
from list_management.scraper import IMDBTop250Scraper, FilmwebTop250Scraper, OscarBestPictureScraper
from celery import shared_task
from django.core.cache import cache

# Set up logging
logger = logging.getLogger(__name__)

@shared_task
def scrape_imdb_top_250():
    logger.info("Starting IMDB Top 250 scraping task...")
    scraper = IMDBTop250Scraper()
    scraper.scrape()
    logger.info("Finished IMDB Top 250 scraping task.")
    cache.delete('imdb_scrape_task_id')

@shared_task
def scrape_filmweb_top_250():
    logger.info("Starting Filmweb Top 250 scraping task...")
    scraper = FilmwebTop250Scraper()
    scraper.scrape()
    logger.info("Finished Filmweb Top 250 scraping task.")
    cache.delete('filmweb_scrape_task_id')

@shared_task
def scrape_oscar_best_picture():
    logger.info("Starting Oscar Best Picture scraping task...")
    scraper = OscarBestPictureScraper()
    scraper.scrape()
    logger.info("Finished Oscar Best Picture scraping task.")
    cache.delete('oscar_scrape_task_id')