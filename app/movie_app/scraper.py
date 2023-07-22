from bs4 import BeautifulSoup
import requests

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



    movies = [{
        "title": t,
        "year": y, 
        "duration": d,
        "ranking": r} for t, y, d, r in zip(titles, year, duration, rankings)]
     
    return {"movies": movies}