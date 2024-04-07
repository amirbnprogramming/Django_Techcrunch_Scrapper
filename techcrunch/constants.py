DOMAIN = 'techcrunch.com'
SITE_ADDRESS = 'https://' + DOMAIN
SEARCH_URL = 'https://search.' + DOMAIN + '/search;?p={keyword}' + '&b={start_item}'

WP_URL = SITE_ADDRESS + '/wp-json'

ARTICLES_WP_URL = WP_URL + '/wp/v2/posts?per_page=100&per_page={page_number}'
CATEGORIES_WP_URL = WP_URL + '/wp/v2/categories?per_page=100&page={page_number}'
AUTHORS_WP_URL = WP_URL + '/tc/v1/users?per_page=100&page={page_number}'

ARTICLE_WP_URL = WP_URL + '/wp/v2/posts/{id}'
AUTHOR_WP_URL = WP_URL + '/wp/v2/users/{id}'
CATEGORY_WP_URL = WP_URL + '/wp/v2/categories/{id}'


ARTICLE_LIST_BY_CATEGORY = WP_URL + '/wp/v2/posts?categories={id}&per_page=100&_envelope=true&page={page_number}'
CAT_URL = SITE_ADDRESS + '/category/{category}/'


SEARCH_PAGE_COUNT = 5
MAXIMUM_SEARCH_PAGE_COUNT = 200
MINIMUM_SEARCH_PAGE_COUNT = 1

