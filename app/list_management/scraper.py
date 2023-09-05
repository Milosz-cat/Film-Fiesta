from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from base.tmdb_helpers import TMDBClient
from list_management.models import IMDBTop250, FilmwebTop250, OscarWinner, OscarNomination
import time, re, requests


class IMDBTop250Scraper:
    def __init__(self):
        self.url = "https://www.imdb.com/chart/top/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.8"
        }

    def fetch_data(self):
        response = requests.get(self.url, headers=self.headers)
        return BeautifulSoup(response.text, "html.parser")

    def parse_data(self, soup):
        try:
            titles = [t.get_text() for t in soup.find_all("h3", class_="ipc-title__text")][1:251]
        except:
            titles = None

        meta_containers = soup.find_all("div", class_="sc-b85248f1-5 kZGNjY cli-title-metadata")
        year = []

        for container in meta_containers:
            meta_items = container.find_all("span", class_="sc-b85248f1-6 bnDqKN cli-title-metadata-item")
            if len(meta_items) >= 2:
                try:
                    year.append(meta_items[0].get_text())
                except:
                    year.append(None)
            else:
                year.append(None)

        try:
            poster_paths = [p['src'] for p in soup.find_all("img", class_="ipc-image")]
        except:
            poster_paths = None

        movies = [{
            "title": t,
            "year": y,
            "poster_path": p
        } for t, y, p in zip(titles, year, poster_paths)]

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
                poster_path=movie_data["poster_path"]
            )
            movie.save()

    def scrape(self):
        soup = self.fetch_data()
        movies = self.parse_data(soup)
        self.save_to_db(movies)


class FilmwebTop250Scraper:
    def __init__(self):
        self.url = "https://www.filmweb.pl/ranking/film"
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")

    def fetch_data(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        driver.get(self.url)

        current_num_of_titles = 0

        while True:
            # Scroll the page
            driver.execute_script("window.scrollBy(0, 750);")
            time.sleep(0.5)  # Wait for the page to load

            # Check the number of titles scraped so far
            current_num_of_titles = len(driver.find_elements(By.CSS_SELECTOR, 'h2.rankingType__title a[itemprop="url"]'))

            # If the number of titles reaches 250, break out of the loop
            if current_num_of_titles >= 250:
                break

        return driver


    def parse_data(self, driver):
        try:
            titles = [element.get_attribute('textContent') for element in driver.find_elements(By.CSS_SELECTOR, 'h2.rankingType__title a[itemprop="url"]')]
        except:
            titles = None

        try:
            original_titles = [element.get_attribute('textContent')[:-5] for element in driver.find_elements(By.CSS_SELECTOR, 'p.rankingType__originalTitle')]
        except:
            original_titles = None

        try:
            years = [element.get_attribute('textContent')[-4:] for element in driver.find_elements(By.CSS_SELECTOR, 'p.rankingType__originalTitle')]
        except:
            years = None

        try:
            poster_paths = [element.get_attribute('textContent') for element in driver.find_elements(By.CSS_SELECTOR, 'span[itemprop="image"]')]
        except:
            poster_paths = None

        driver.quit()

        movies = [{
            "title": t,
            'original_title': o,
            "year": y,
            "poster_path": p
        } for t, o, y, p in zip(titles, original_titles, years, poster_paths)]

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
                poster_path=movie_data["poster_path"]
            )
            movie.save()


    def scrape(self):
        driver = self.fetch_data()
        movies = self.parse_data(driver)
        self.save_to_db(movies)


class OscarBestPictureScraper:
    def __init__(self):
        self.url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.8"
        }
        self.tmdb_client = TMDBClient()

    def fetch_data(self):
        response = requests.get(self.url, headers=self.headers)
        return BeautifulSoup(response.text, "html.parser")

    def parse_data(self, soup):
        tables = soup.find_all("table", class_="wikitable")[:-1]
        winners = []

        for table in tables:
            rows = table.find_all("tr")[1:]
            nominations = []
            winner_movie = None
            current_year = None
            for row in rows:
                if len(row.select('td')) == 1:
                    if current_year and winner_movie:
                        winner_movie['nominations'] = nominations
                        winners.append(winner_movie)
                        nominations = []
                        winner_movie = None
                    try:
                        current_year = re.sub(r'\[\w\]', '', row.select('td')[0].get_text(strip=True)).split()[0]
                    except:
                        current_year = None
                else:
                    try:
                        film = row.select('td')[0].get_text(strip=True).replace('/', ' ')
                        studio = row.select('td')[1].get_text(strip=True)
                        is_winner = 'style' in row.attrs and 'background:#FAEB86' in row['style']
                        if is_winner:
                            winner_movie = {
                                'year': current_year,
                                'release_year': current_year[:4],
                                'title': film,
                                'poster_path': self.tmdb_client.get_single_movie_core(film, current_year[:4])['poster_path'],
                                'studio': studio
                            }
                        else:
                            nominations.append({
                                'title': film,
                                'release_year': current_year[:4],
                                'studio': studio
                            })
                    except:
                        continue

            if current_year and winner_movie:
                winner_movie['nominations'] = nominations
                winners.append(winner_movie)

        return winners

    def save_to_db(self, winners):
        for winner_data in winners:
            # Sprawdź, czy film zwycięzca już istnieje w bazie danych
            winner_exists = OscarWinner.objects.filter(title=winner_data["title"], release_year=winner_data["release_year"]).exists()

            if not winner_exists:
                winner, _ = OscarWinner.objects.get_or_create(title=winner_data["title"], release_year=winner_data["release_year"])
                winner.year = winner_data["year"]
                winner.poster_path = winner_data["poster_path"]
                winner.studio = winner_data["studio"]
                winner.save()

                for nomination_data in winner_data["nominations"]:
                    nomination, _ = OscarNomination.objects.get_or_create(
                        title=nomination_data["title"], 
                        release_year=nomination_data["release_year"], 
                        studio=nomination_data["studio"],
                        defaults={'winner': winner}
                    )
                    nomination.winner = winner
                    nomination.save()

    def scrape(self):
        soup = self.fetch_data()
        winners = self.parse_data(soup)
        self.save_to_db(winners)




# def scrape_movie_wallpaper(title, year):
    
#     #klucz API
#     api_key = env("GOOGLE_API_KEY")

#     #identyfikator silnika wyszukiwania
#     cx = env("CX")

#     # Zapytanie wyszukiwania
#     query = f"movie wallpaper {title} {year}"

#     # URL API
#     url = f"https://www.googleapis.com/customsearch/v1"

#     # Parametry zapytania
#     params = {
#         'key': api_key,
#         'cx': cx,
#         'q': query,
#         'searchType': 'image',
#         'num': 1
#     }

#     # Wykonaj zapytanie do API
#     response = requests.get(url, params=params)
#     # Przetwórz odpowiedź
#     data = response.json()
#     image_url = data['items'][0]['link']

#     return image_url


