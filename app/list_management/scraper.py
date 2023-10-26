import time, re, logger

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from base.tmdb_helpers import TMDBClient

from list_management.models import (
    IMDBTop250,
    FilmwebTop250,
    OscarWinner,
    OscarNomination,
)

logger = logger.getLogger(__name__)


class BaseScraper:
    """
    Abstract base class for BeautifulSoup scrapers.

    Attributes:
    - url (str): The URL of the page to scrape.
    - headers (dict): Headers for the HTTP request.

    Methods:
    - fetch_data(): Retrieves the HTML content of the page.
    - scrape(limit=None): Orchestrates the scraping process.
    """

    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
            (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36""",
            "Accept-Language": "en-US,en;q=0.8",
        }

    def fetch_data(self):
        response = requests.get(self.url, headers=self.headers)
        return BeautifulSoup(response.text, "html.parser")

    def parse_data(self, soup, limit):
        """Parse data from the soup object. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method.")

    def save_to_db(self, _):
        """Save movies to the database. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method.")

    def scrape(self, limit=None):
        soup = self.fetch_data()
        movies = self.parse_data(soup, limit)
        self.save_to_db(movies)


class IMDBTop250Scraper(BaseScraper):
    """
    A BeautifulSoup scraper for fetching and parsing the top 250 movies from IMDB.

    The limit of scrapped movies is set for testing purposes.

    Methods:
    - parse_data(soup, limit=None): Parses the HTML content to extract movie details.
    - save_to_db(movies): Saves the parsed movie details to the database.
    """

    def __init__(self):
        super().__init__("https://www.imdb.com/chart/top/")

    def parse_data(self, soup, limit=None):
        try:
            titles = [
                t.get_text() for t in soup.find_all("h3", class_="ipc-title__text")
            ][1:251]
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            titles = None

        meta_containers = soup.find_all(
            "div", class_="sc-c7e5f54-7 brlapf cli-title-metadata"
        )
        year = []

        for container in meta_containers:
            meta_items = container.find_all(
                "span", class_="sc-c7e5f54-8 hgjcbi cli-title-metadata-item"
            )
            if len(meta_items) >= 2:
                try:
                    year.append(meta_items[0].get_text())
                except Exception as e:
                    logger.error(f"An error occurred: {e}")
                    year.append(None)
            else:
                year.append(None)

        try:
            poster_paths = [p["src"] for p in soup.find_all("img", class_="ipc-image")]
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            poster_paths = None

        movies = [
            {"title": t, "year": y, "poster_path": p}
            for t, y, p in zip(titles, year, poster_paths)
        ]

        if not movies:
            logger.info(
                "You can't scrape data."
                "Check whether the names of the HTML elements on the page have not changed."
            )

        if limit:
            movies = movies[:limit]

        return movies

    def save_to_db(self, movies):
        # Delete all existing movies
        IMDBTop250.objects.all().delete()

        # Iterate through the scraped movies and save them to the database
        for rank, movie_data in enumerate(movies, start=1):
            movie = IMDBTop250(
                rank=rank,
                title=movie_data["title"],
                year=movie_data["year"],
                poster_path=movie_data["poster_path"],
            )
            movie.save()


class FilmwebTop250Scraper:
    """
    A Selenium Webdriver scraper for fetching and parsing the top 250 movies from Filmweb.
    We use Selenium instead of BeautifulSoup because we need a scroll down mechanism.
    This is due to the fact that the Filmweb site uses a lazy loading mechanism to load data

    The limit of scrapped movies is set for testing purposes.


    Attributes:
    - url (str): The URL of the Filmweb top 250 movies page.
    - options (Options): Selenium webdriver options.

    Methods:
    - fetch_data(scrolls=None): Retrieves the HTML content of the Filmweb top 250 movies
    page using Selenium.
    - parse_data(driver, limit=None): Parses the HTML content to extract movie details.
    - save_to_db(movies): Saves the parsed movie details to the database.
    - scrape(limit=None, scrolls=None): Orchestrates the scraping process.
    """

    def __init__(self):
        self.url = "https://www.filmweb.pl/ranking/film"
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")

    def fetch_data(self, scrolls=None):
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=self.options
        )
        driver.get(self.url)

        current_num_of_titles = 0
        scroll_count = 0

        while True:
            # Scroll the page
            driver.execute_script("window.scrollBy(0, 750);")
            time.sleep(0.5)  # Wait for the page to load

            # Check the number of titles scraped so far
            current_num_of_titles = len(
                driver.find_elements(
                    By.CSS_SELECTOR, 'h2.rankingType__title a[itemprop="url"]'
                )
            )

            # Increase the scroll count
            scroll_count += 1

            # Break the loop if the number of titles reaches 250 or the number of scrolls
            # reaches the limit
            if scrolls:
                if scroll_count >= scrolls:
                    break
            else:
                if current_num_of_titles >= 250:
                    break

        return driver

    def parse_data(self, driver, limit=None):
        try:
            titles = [
                element.get_attribute("textContent")
                for element in driver.find_elements(
                    By.CSS_SELECTOR, 'h2.rankingType__title a[itemprop="url"]'
                )
            ]
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            titles = None

        try:
            original_titles = [
                element.get_attribute("textContent")[:-5]
                for element in driver.find_elements(
                    By.CSS_SELECTOR, "p.rankingType__originalTitle"
                )
            ]
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            original_titles = None

        try:
            years = [
                element.get_attribute("textContent")[-4:]
                for element in driver.find_elements(
                    By.CSS_SELECTOR, "p.rankingType__originalTitle"
                )
            ]
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            years = None

        try:
            poster_paths = [
                element.get_attribute("textContent")
                for element in driver.find_elements(
                    By.CSS_SELECTOR, 'span[itemprop="image"]'
                )
            ]
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            poster_paths = None

        driver.quit()

        movies = [
            {"title": t, "original_title": o, "year": y, "poster_path": p}
            for t, o, y, p in zip(titles, original_titles, years, poster_paths)
        ]

        if not movies:
            logger.info(
                "You can't scrape data."
                "Check whether the names of the HTML elements on the page have not changed."
            )

        if limit:
            movies = movies[:limit]

        return movies

    def save_to_db(self, movies):
        # Delete all existing movies
        FilmwebTop250.objects.all().delete()

        # Iterate through the scraped movies and save them to the database
        for rank, movie_data in enumerate(movies, start=1):
            movie = FilmwebTop250(
                rank=rank,
                title=movie_data["title"],
                original_title=movie_data["original_title"],
                year=movie_data["year"],
                poster_path=movie_data["poster_path"],
            )
            movie.save()

    def scrape(self, limit=None, scrolls=None):
        driver = self.fetch_data(scrolls)
        movies = self.parse_data(driver, limit)
        self.save_to_db(movies)


class OscarBestPictureScraper(BaseScraper):
    """
    A BeautifulSoup scraper for fetching and parsing Oscar Best Picture winners and
    their nominations from Wikipedia.

    The limit of scrapped movies is set for testing purposes.

    Attributes:
    - tmdb_client (TMDBClient): An instance of the TMDBClient to fetch movie posters.

    Methods:
    - parse_data(soup, limit=None): Parses the HTML content to extract details of Oscar
    winners and their nominations.
    - save_to_db(winners): Saves the parsed details to the database.
    """

    def __init__(self):
        super().__init__("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture")
        self.tmdb_client = TMDBClient()

    def parse_data(self, soup, limit=None):
        tables = soup.find_all("table", class_="wikitable")[:-1]
        winners = []

        for table in tables:
            rows = table.find_all("tr")[1:]
            nominations = []
            winner_movie = {}
            current_year = ""

            for row in rows:
                if len(row.select("td")) == 1:
                    if current_year and winner_movie:
                        winner_movie["nominations"] = nominations
                        winners.append(winner_movie)
                        nominations = []
                        winner_movie = {}
                    try:
                        current_year_text = row.select("td")[0].get_text(strip=True)
                        current_year = re.sub(r"\[\w\]", "", current_year_text).split()[
                            0
                        ]
                    except Exception as e:
                        logger.error(f"An error occurred: {e}")
                        current_year = ""

                else:
                    try:
                        film = (
                            row.select("td")[0].get_text(strip=True).replace("/", " ")
                        )
                        studio = row.select("td")[1].get_text(strip=True)
                        is_winner = (
                            "style" in row.attrs
                            and "background:#FAEB86" in row["style"]
                        )
                        if is_winner:
                            winner_movie = {
                                "year": current_year,
                                "release_year": current_year[:4]
                                if current_year
                                else None,
                                "title": film,
                                "poster_path": self.tmdb_client.get_single_movie_core(
                                    film, current_year[:4] if current_year else None
                                )["poster_path"],
                                "studio": studio,
                            }
                        else:
                            nominations.append(
                                {
                                    "title": film,
                                    "release_year": current_year[:4]
                                    if current_year
                                    else None,
                                    "studio": studio,
                                }
                            )
                    except Exception as e:
                        logger.error(f"An error occurred: {e}")
                        continue

            if current_year and winner_movie:
                winner_movie["nominations"] = nominations
                winners.append(winner_movie)

        return winners[:limit] if limit else winners

    def save_to_db(self, winners):
        for winner_data in winners:
            # Check if the winner already exists in the database
            winner_exists = OscarWinner.objects.filter(
                title=winner_data["title"], release_year=winner_data["release_year"]
            ).exists()

            if not winner_exists:
                winner, _ = OscarWinner.objects.get_or_create(
                    title=winner_data["title"], release_year=winner_data["release_year"]
                )
                winner.year = winner_data["year"]
                winner.poster_path = winner_data["poster_path"]
                winner.studio = winner_data["studio"]
                winner.save()

                for nomination_data in winner_data["nominations"]:
                    nomination, _ = OscarNomination.objects.get_or_create(
                        title=nomination_data["title"],
                        release_year=nomination_data["release_year"],
                        studio=nomination_data["studio"],
                        defaults={"winner": winner},
                    )
                    nomination.winner = winner
                    nomination.save()


# def scrape_movie_wallpaper(title, year):
#     api_key = env("GOOGLE_API_KEY")
#     cx = env("CX")
#     query = f"movie wallpaper {title} {year}"
#     url = f"https://www.googleapis.com/customsearch/v1"

#     params = {
#         'key': api_key,
#         'cx': cx,
#         'q': query,
#         'searchType': 'image',
#         'num': 1
#     }

#     response = requests.get(url, params=params)
#     data = response.json()
#     image_url = data['items'][0]['link']

#     return image_url
