import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_app.settings')

app = Celery('movie_app')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

"""
Define the beat schedule for periodic tasks. This configuration sets up three tasks to run at specified intervals.
- scrape_imdb_top_250: This task scrapes the IMDB Top 250 movies. It's scheduled to run every day at midnight.
- scrape_oscar_best_picture: 
    This task scrapes the Oscar Best Picture winners.
    It's scheduled to run at midnight on the 5th of March every year.
    This is likely to coincide with the annual Oscar awards ceremony.
"""
app.conf.beat_schedule = {
    'scrape_imdb_top_250': {
        'task': 'list_management.tasks.scrape_imdb_top_250',
        'schedule': crontab(minute=0, hour=0),  
    },
    'scrape_filmweb_top_250': {
        'task': 'list_management.tasks.scrape_filmweb_top_250',
        'schedule': crontab(minute=5, hour=0),
    },
    'scrape_oscar_best_picture': {
        'task': 'list_management.tasks.scrape_oscar_best_picture',
        'schedule': crontab(minute=0, hour=0, day_of_month='5', month_of_year='3'),
    }
}