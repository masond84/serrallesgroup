from celery import shared_task
from .main_scraper import run_scraper
@shared_task
def run_scraper_task():
    run_scraper()