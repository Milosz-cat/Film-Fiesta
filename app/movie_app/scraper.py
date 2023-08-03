from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

def scrape_imdb_top_250():
    # Downloading imdb top 250 movie's data
    url = "http://www.imdb.com/chart/top"
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        titles = [t.get_text() for t in soup.find_all("h3", class_="ipc-title__text")][1:251]
    except:
        titles = None

    try:
        meta = [m.get_text() for m in soup.find_all("span", class_="sc-14dd939d-6 kHVqMR cli-title-metadata-item")]
        year = [meta[i] for i in range(0, len(meta), 3)]
        duration = [meta[i+1] for i in range(0, len(meta), 3)]
    except:
        year = duration = None

    try:
        rankings = [r.get_text() for r in soup.find_all("span", class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating")]
    except:
        rankings = None

    try:
        poster_paths = [p['src'] for p in soup.find_all("img", class_="ipc-image")]

    except:
        poster_paths = None



    movies = [{
        "title": t,
        "year": y, 
        "duration": d,
        "ranking": r,
        "poster_path": p} for t, y, d, r, p in zip(titles, year, duration, rankings, poster_paths)]
     
    return movies



def scrape_fimlweb_top_250():
    url = "https://www.filmweb.pl/ranking/film"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)



    # Scrolling the page by 1000 pixels each time
    for _ in range(45):  # Increase the number of iterations if needed
        driver.execute_script("window.scrollBy(0, 750);")
        time.sleep(0.2)  # Wait for the page to load

    # Now you can use Selenium to extract data
    titles = [element.text for element in driver.find_elements(By.CSS_SELECTOR, 'h2.rankingType__title')]
    years = [element.text for element in driver.find_elements(By.CSS_SELECTOR, 'span.rankingType__year')]
    rankings = [element.text for element in driver.find_elements(By.CSS_SELECTOR, 'span.rankingType__rate--value')]
    poster_paths = [element.get_attribute('textContent') for element in driver.find_elements(By.CSS_SELECTOR, 'span[itemprop="image"]')]

    # Create the movies list
    movies = [{
        "title": t,
        "year": y,
        "ranking": r,
        "poster_path": p
    } for t, y, r, p in zip(titles, years, rankings, poster_paths)]

    driver.quit()

    return movies

def scrape_movie_wallpaper(title, year):
    # Initialise environment variables
    env = environ.Env()
    environ.Env.read_env()
    
    #klucz API
    api_key = env("GOOGLE_API_KEY")

    #identyfikator silnika wyszukiwania
    cx = env("CX")

    # Zapytanie wyszukiwania
    query = f"{title} {year} movie wallpaper"

    # URL API
    url = f"https://www.googleapis.com/customsearch/v1"

    # Parametry zapytania
    params = {
        'key': api_key,
        'cx': cx,
        'q': query,
        'searchType': 'image',
        'num': 1
    }

    # Wykonaj zapytanie do API
    response = requests.get(url, params=params)
    # Przetwórz odpowiedź
    data = response.json()
    image_url = data['items'][0]['link']

    return image_url

