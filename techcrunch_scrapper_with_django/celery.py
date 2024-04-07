import logging
import os
from celery import Celery
from celery.signals import after_setup_logger

from django.conf import settings
from Utils.celer_log_conf import configure_celery_log

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techcrunch_scrapper_with_django.settings')

app = Celery('techcrunch_scrapper_with_django', broker=settings.CELERY_BROKER_URL)


app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'every-day-start-daily-scrape': {
        'task': 'techcrunch.tasks.daily_scrape_task',
        'schedule': 86400,  # One day
    },
}
after_setup_logger.connect(configure_celery_log)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

logging.getLogger('celery').propagate = False

# celery -A techcrunch_scrapper_with_django worker -l INFO -P eventlet
# celery -A techcrunch_scrapper_with_django beat --loglevel=INFO


