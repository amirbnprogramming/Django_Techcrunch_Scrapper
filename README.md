
**Django Techcrunch Scrapper**

DjangoTechcrunchScrapper is a Django app to scrape Techcrunch.com website items .
Scrapped Data are authors , categories , articles .
Application development and testing with django v4.2


Quick start
-----------
1. Install all the packages and requirements with :
   
        pip install -r  requirements.txt
   
2. Install broker manager like ``rabbitmq`` or ``redis``
3. Set specific and custome settings for you project in ``settings.py``
4. Set specific and custome settings for you celery in  Celery name space in ``settings.py``

        # CELERY-SETCION
        CELERY_BROKER_URL = 'amqp://localhost:your port' (for rabbitmq)
        CELERY_TIMEZONE = 'Your timezone'
        CELERY_TASK_TIME_LIMIT = 60 * 60
        CELERY_RESULT_BACKEND = 'django-db'
        CELERY_TASK_SERIALIZER = 'json'
        CELERY_RESULT_SERIALIZER = 'json'
  
5. open terminal and  make migrations  for ``models`` :

        python manage.py makemigrations     
        python manage.py migrate     

6.  First of all set the celery beat schedule, go to ``celery.py`` and find  schedule , change it by second to change schedule:

         app.conf.beat_schedule =
           {
                'every-day-start-daily-scrape': {
                    'task': 'techcrunch.tasks.daily_scrape_task',
                    'schedule': 86400,  # One day
                },
            }
7. Before all the things you should be logged in to use specific services , so at first:

          py manage.py createsuperuser
8. Then log in with url ``host:port/admin``        
9. After setting celery settings call ``celery-beat`` and  ``celery-worker`` with each other in two cmd terminal:
   
        celery -A techcrunch_scrapper_with_django worker -l INFO -P eventlet
        celery -A techcrunch_scrapper_with_django beat --loglevel=INFO
10. Then at last run the django server and run the app :

        python manage.py runserver
   
11. Links description :
    
        admin/  => admin panel
        manual_daily_search [name='manual_daily_search']  => manual daily scrapping with out celery beat
        search_keyword [name='search_keyword']  => search by keyword  page
        diagrams/<slug:model_name> [name='diagrams'] => draw diagrams :
        diagrams/author => number of articles of each author
        diagrams/category => number of articles of each category
        diagrams/article => number of articles seach by keyword

12. The result of diagram generating , will be saved in ``basedirectory / exports ... ``



