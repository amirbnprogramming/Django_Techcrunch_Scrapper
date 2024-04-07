from datetime import date

from bs4 import BeautifulSoup as Bs

from Utils.function_decorator import function_caller
from .models import Url, Category, Article, Author, SearchByKeyword, DailyUpdateData, ArticleSearchByKeywordItem

from .constants import SEARCH_URL, ARTICLE_LIST_BY_CATEGORY
from .constants import ARTICLES_WP_URL, ARTICLE_WP_URL
from .constants import AUTHORS_WP_URL, AUTHOR_WP_URL
from .constants import CATEGORIES_WP_URL, CATEGORY_WP_URL

models = {
    'author': {'name': 'authors',
               'model': Author,
               'wp_list': AUTHORS_WP_URL,
               'wp_one': AUTHOR_WP_URL,
               },
    'category': {'name': 'categories',
                 'model': Category,
                 'wp_list': CATEGORIES_WP_URL,
                 'wp_one': CATEGORY_WP_URL,
                 },
    'article': {'name': 'articles',
                'model': Article,
                'wp_list': ARTICLES_WP_URL,
                'wp_one': ARTICLE_WP_URL,
                },
}


class ScrapperHandler:
    def __init__(self):
        self.new_category_items = []
        self.new_article_items = []
        self.new_author_items = []

    @classmethod
    @function_caller
    def article_id_parser(cls, li):
        # region : Explore the Search Page result (Articles) to find article id :
        # region : find article id
        url = li.select_one('div.d-tc>h4>a').get('href')
        url_object = Url(address=url)
        soup = url_object.get_any_soup()
        if soup is not None:
            tag_detail = soup.find('meta', property='mrf:tags').get('content').split(';')
            article_id = ""
            try:
                for detail in tag_detail:
                    if detail.__contains__('ID'):
                        article_id = detail.split(':')[1]
            except Exception:
                print("This Article_ID is not Available")
                article_id = ""
        else:
            article_id = ""
            print("This Article_URL is not Available")

        return article_id

    @function_caller
    def model_maker(self, site_id, model_type):
        scrapped_object, state = models[model_type]['model'].objects.get_or_create(site_id=str(site_id))
        # checking existence
        if state:
            # Get model fields
            address = models[model_type]['wp_one'].format(id=site_id)
            url_object = Url(address=address)
            result_json = url_object.get_json()

            if result_json is not None:
                scrapped_object.slug = result_json["slug"] or "None"
                scrapped_object.url = result_json["link"] or "None"

                if model_type == 'author':
                    scrapped_object.title = result_json["name"] or "None"
                    scrapped_object.author_position = result_json["position"] or "None"
                    scrapped_object.author_avatars = result_json["avatar_urls"]["96"] or "None"
                    scrapped_object.save()
                    # new author item added
                    self.new_author_items.append(scrapped_object)

                elif model_type == 'category':
                    scrapped_object.title = result_json["name"] or "None"

                    scrapped_object.save()
                    # new category item added
                    self.new_category_items.append(scrapped_object.title)

                elif model_type == 'article':
                    scrapped_object.title = result_json["title"]['rendered'] or "None"
                    scrapped_object.image = result_json['yoast_head_json']['og_image'][0]['url'] or "None"
                    scrapped_object.description = result_json['yoast_head_json']['description'] or "None"
                    article_author_value = result_json["author"] or None
                    article_category_value = result_json["categories"] or None

                    if article_category_value is not None and len(article_category_value) > 0:
                        if str(result_json["categories"][0]) != "":
                            # Make or retrieve the category
                            site_id = result_json["categories"][0]
                            article_category_object = self.model_maker(site_id=site_id, model_type='category')

                            # make category model
                            # article_category_object, state = Category.objects.get_or_create(
                            #     site_id=result_json["categories"][0])
                            # if state:
                            # The category is not available in database we should scrape and make it

                    else:
                        article_category_object = None

                    if article_author_value is not None:
                        if str(result_json["author"]) != "":
                            # Make or retrieve the author
                            site_id = result_json["author"]
                            article_author_object = self.model_maker(site_id=site_id, model_type='author')

                            # make author model
                            # article_author_object, state = Author.objects.get_or_create(site_id=result_json["author"])
                            # if state:

                    scrapped_object.category = article_category_object
                    scrapped_object.author = article_author_object
                    scrapped_object.save()

                    self.new_article_items.append(scrapped_object.title)

                # log
                print(f"{model_type.title()}_Name: ({scrapped_object.title}) - site_id:({site_id}) , Added to "
                      f"DATABASE Successfully")
            else:
                print(f"{model_type.title()} with site_id: ({site_id}) , Is Not Found!")
                scrapped_object.delete()
                scrapped_object = None
        else:
            print(f"{model_type.title()}_Name: ({scrapped_object.title}) - site_id:({site_id}) , Available in "
                  f"DATABASE")
        # endregion

        return scrapped_object

    @function_caller
    def daily_scrape(self):
        # region : GET today date and make DailyUpdateData object
        today_date = date.today().strftime("%Y-%m-%d")
        daily_update_data, state = DailyUpdateData.objects.get_or_create(search_date=today_date)
        print(f"DailyUpdateData object created at ({today_date})")
        # endregion

        # region : GET all categories and authors
        model_types = ['category', 'author']
        data_list = self.list_maker(model_types)
        categories_list = data_list['daily_categories']
        # update dailydata object
        daily_update_data.category_items = self.new_category_items
        daily_update_data.author_items = self.new_author_items
        daily_update_data.save()

        print(f"Categories_Scrapped_list:{data_list['daily_categories']}")
        print(f"Authors_Scrapped_list:{data_list['daily_authors']}")
        print(f"Author_news:{self.new_author_items}")
        print(f"Category_news:{self.new_category_items}")
        # endregion
        print(f"Start Scrapping Articles . . . ")
        # region : GO throw all categories
        for category in categories_list:
            paginator = 1
            address = ARTICLE_LIST_BY_CATEGORY.format(id=category.site_id, page_number=paginator)
            articles_list = Url.objects.create(address=address)
            articles_list_json = articles_list.get_json()
            page_limit = int(articles_list_json['headers']['X-WP-TotalPages'])
            print(f"max_page:{page_limit}")
            # region : Articles Paginator Section
            for paginator in range(1, page_limit):
                print(f"PAGE NUMBER ({paginator}) in Category ({category.title})")
                # region : Article Section
                for article in articles_list_json['body']:
                    self.model_maker(model_type='article', site_id=article['id'])
                # endregion

                # region : UPDATE address belong paginator
                articles_list.address = ARTICLE_LIST_BY_CATEGORY.format(id=category.site_id, page_number=paginator + 1)
                articles_list_json = articles_list.get_json()
                # endregion

            # endregion
        # endregion

        # region : Update New Data
        daily_update_data.article_items = self.new_article_items
        daily_update_data.save()
        print(f"Article_news:{self.new_article_items}")
        # endregion

    @function_caller
    def list_maker(self, model_types):
        daily_categories = []
        daily_authors = []
        for model_type in model_types:
            # region : Objects Daily Scrapping
            print(f"Start Scrapping {models[model_type]['name']} . . . ")
            paginator = 1
            while True:
                all_items_list = Url(address=models[model_type]['wp_list'].format(page_number=paginator))
                all_items = all_items_list.get_json()
                if len(all_items) != 0:
                    for item in all_items:
                        # region : object making
                        try:
                            item_site_id = item['id']
                        except KeyError:
                            item_site_id = ""
                            print("Item Not Found!")
                        if item_site_id != "":
                            made_object = self.model_maker(site_id=item_site_id, model_type=model_type)
                            # add created objects to list
                            if model_type == 'category' and made_object is not None:
                                daily_categories.append(made_object)
                            elif model_type == 'author' and made_object is not None:
                                daily_authors.append(made_object)
                        # endregion
                    paginator += 1
                else:
                    break
        # endregion
        data_list = {
            'daily_categories': daily_categories,
            'daily_authors': daily_authors
        }

        return data_list

    @function_caller
    def manual_search_method(self, search_by_keyword_instance: SearchByKeyword):
        search_items = []
        i = 0
        for i in range(1, search_by_keyword_instance.max_pages * 10, 10):

            # region : Create Keyword-URl-Object for each page:
            search_address = SEARCH_URL.format(keyword=search_by_keyword_instance.keyword.slug, start_item=i)
            keyword_url = Url.objects.create(address=search_address)
            # endregion

            # region :log Page
            print("*" * 10)
            print(f'Page ({int(i / 10) + 1}) Detail')
            keyword_search_soup = keyword_url.get_any_soup()
            print("*" * 10)
            # endregion

            # data existence checking:
            if keyword_search_soup is not None:

                # region : find article id and make article model :
                li_items = keyword_search_soup.select("ul.compArticleList>li")
                for li in li_items:
                    article_id = self.article_id_parser(li)
                    if article_id != "":
                        article = self.model_maker(model_type='article', site_id=article_id)
                    if article is not None:
                        search_items.append(str(article.site_id))
                        article_search_by_keyword = ArticleSearchByKeywordItem.objects.create(
                            search_by_keyword=search_by_keyword_instance,
                            article=article
                        )

                # endregion

            # region : Checking the end page conditions
            if keyword_search_soup.find('a', class_='next') is None:
                break
            # endregion

        # region : Check if user enter more than max_pages
        i = int(i / 10) + 1
        if i < search_by_keyword_instance.max_pages:
            # print("*" * 30)
            print(f"Sorry! I found only ({i}) related pages")
            search_by_keyword_instance.max_pages = i
        # endregion

        # region : result detail
        search_by_keyword_instance.new_articles = len(self.new_article_items)
        search_by_keyword_instance.scrapped_articles = '(****)'.join(search_items)
        search_by_keyword_instance.save()
        print(f"({len(self.new_article_items)}) New Items has been searched ")
        # endregion
        return len(search_items)
