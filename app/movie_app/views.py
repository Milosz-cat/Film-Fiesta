from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import re


def home(request):
        # Downloading imdb top 250 movie's data
        url = "http://www.imdb.com/chart/top"
        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all <h3> elements with class "ipc-title__text"
        title_elements = soup.find_all("h3", class_="ipc-title__text")

        # Extract the text content of each <h3> element
        titles = []
        for t in title_elements:
                titles.append(t.get_text())

        # Select a subset of titles
        titles = titles[1:251]

        # Pass the titles to the template context
        context = {"titles": titles}

        # Render the template with the context
        return render(request, "base/home.html", context)
