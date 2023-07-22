from django.shortcuts import render
from . import scraper
from django.http import Http404


def home(request):
        # Render the template with the context
        return render(request, "base/home.html")


def list_movies(request, source):
    context = {}
    if source == 'imdb':
        context = {"movies": scraper.scrape_imdb_top_250()}
    elif source == 'filmweb':
        context = {"movies": scraper.scrape_fimlweb_top_250()}
    else:
        raise Http404("Invalid source.")
    return render(request, "base/list.html", context)
