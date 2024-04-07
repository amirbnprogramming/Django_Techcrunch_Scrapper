import datetime
import os

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Count
from matplotlib import pyplot as plt

from . import constants
from .scraper_handler import ScrapperHandler
from .models import SearchByKeyword, Keyword, Author, Category

models = {'author': Author,
          'category': Category,
          'keyword': Keyword}


@shared_task()
def search_by_keyword_task(user_name, keyword, max_page=constants.SEARCH_PAGE_COUNT):
    User = get_user_model()
    current_user = User.objects.get(username=user_name)
    print(f'search_by_keyword_task => {keyword} - pages({max_page}) by user ({current_user}) Started')
    keyword, _ = Keyword.objects.get_or_create(
        slug=keyword,
    )
    keyword.times_searched += 1
    keyword.save()

    scraper_handler = ScrapperHandler()

    search_by_keyword = SearchByKeyword.objects.create(
        user=current_user,
        keyword=keyword,
        max_pages=max_page
    )
    scraped_item_count = scraper_handler.manual_search_method(search_by_keyword_instance=search_by_keyword)

    print(
        f'search_by_keyword_task => {keyword} - pages({search_by_keyword.max_pages}) by user ({current_user}) finished')

    return {
        'keyword': keyword.slug,
        'max_page': max_page,
        'scraped_item_count': scraped_item_count,
        'status': 'finished',
    }


@shared_task()
def daily_scrape_task():
    print(f'daily_scrape_task => by (Automation)  Started')
    scraper_handler = ScrapperHandler()
    scraper_handler.daily_scrape()
    print(f'daily_scrape_task => by (Automation) finished')


@shared_task()
def diagram_generator_task(model_name, current_user):
    print(f'diagram_generator_task => for ({model_name}) diagram Started')
    dictionary_data = {}
    if model_name == 'keyword':
        y_text = 'Search_Times'
        keyword_search_time = models[model_name].objects.annotate(search_time=Count('search_by_keyword'))
        for item in keyword_search_time:
            dictionary_data[item.slug] = item.search_time
    elif model_name == 'category' or model_name == 'author':
        y_text = 'Articles'
        articles_number = models[model_name].objects.annotate(article_count=Count('article'))
        for item in articles_number:
            dictionary_data[item.title] = item.article_count

    x = list(dictionary_data.keys())
    y = list(dictionary_data.values())

    plt.figure(figsize=(50, 10))
    plt.bar(x, y)
    plt.xlabel(model_name.title())
    plt.ylabel(y_text)
    plt.title(f'{model_name.title()} - {y_text}')
    plt.tick_params(axis='x', labelsize=5, rotation=90)
    plt.tight_layout()
    # file path section :
    current_date = datetime.datetime.today()
    base_dir = settings.BASE_DIR
    directory_path = os.path.join(base_dir, 'exports',
                                  'exported_diagrams',
                                  str(current_date.year),
                                  str(current_date.month),
                                  str(current_date.day),
                                  )
    os.makedirs(directory_path, exist_ok=True)
    file_name = f'{model_name.title()}_Report_by_({current_user}).png'
    export_path = os.path.join(directory_path, file_name)
    plt.savefig(export_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'diagram_generator_task => for ({model_name}) diagram finished')

# celery -A good_reads_scraper_with_django worker -l INFO -P eventlet
# celery -A good_reads_scraper_with_django beat --loglevel=INFO
