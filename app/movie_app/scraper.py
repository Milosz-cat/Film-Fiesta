from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

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
    chrome_driver_path = '/usr/local/bin/chromedriver'

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run the browser in headless mode (without GUI).
    driver = webdriver.Chrome(options=options)

    url = "https://www.filmweb.pl/ranking/film"
    driver.get(url)
    
    try:
        # Wait for the page to load and the rankingType__title elements to be present.
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "rankingType__title")))
    except TimeoutException:
        print("Timeout waiting for page to load.")
        driver.quit()
        return None

    # Scroll down to load more movies
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            # Wait for the new movies to load (you may adjust the waiting time as needed).
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "rankingType__title")))
        except TimeoutException:
            break
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Extract data from the loaded page
    titles = [t.text for t in driver.find_elements(By.CLASS_NAME, "rankingType__title")]
    years = [y.text for y in driver.find_elements(By.CLASS_NAME, "rankingType__year")]
    rankings = [r.text for r in driver.find_elements(By.CLASS_NAME, "rankingType__rate--value")]
    poster_paths = [p.get_attribute("src") for p in driver.find_elements(By.TAG_NAME, "img")]

    # Clean up resources
    driver.quit()

    # Create the movies list
    movies = [{
        "title": t,
        "year": y,
        "ranking": r,
        "poster_path": p
    } for t, y, r, p in zip(titles, years, rankings, poster_paths)]

    return movies
