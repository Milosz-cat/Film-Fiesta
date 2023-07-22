from django.shortcuts import render
import requests
from . import scraper



def home(request):
        
        context = scraper.scrape_imdb_top_250()


        # Render the template with the context
        return render(request, "base/home.html", context)
