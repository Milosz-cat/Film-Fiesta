import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_app.settings')

app = Celery('movie_app')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'scrape_imdb_top_250': {
        'task': 'list_management.tasks.scrape_imdb_top_250',
        'schedule': crontab(minute=0, hour=0),  # This specifies midnight every day
    },
    'scrape_filmweb_top_250': {
        'task': 'list_management.tasks.scrape_filmweb_top_250',
        'schedule': crontab(minute=5, hour=0),
    },
    'scrape_oscar_best_picture': {
        'task': 'list_management.tasks.scrape_oscar_best_picture',
        'schedule': crontab(minute=0, hour=0, day_of_month='5', month_of_year='3'),  # This specifies midnight on 5th March every year
    }
}