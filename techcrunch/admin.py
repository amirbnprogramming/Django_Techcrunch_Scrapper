from django.contrib import admin
from django.contrib.admin import register
from import_export.admin import ImportExportModelAdmin

from techcrunch.models import Url, Category, Author, Article, Keyword, SearchByKeyword, \
    ArticleSearchByKeywordItem


def make_activate(queryset):
    queryset.update(is_active=True)


def make_deactivate(queryset):
    queryset.update(is_active=False)


# Register your models here.


class BaseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    actions = (make_activate, make_deactivate)
    search_fields = ['title']


@register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'created_at']
    list_display_links = ['id', 'address']
    list_filter = ['created_at']
    search_fields = ['address']


@register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ['id', 'site_id', 'title',
                    'is_active', 'created_at', 'updated_at', ]

    search_fields = ['title', 'slug', 'site_id']

    list_filter = ['title', 'is_active', 'created_at', 'updated_at']

    list_display_links = ['id', 'site_id', 'title']


@register(Author)
class AuthorAdmin(BaseAdmin):
    list_display = ['id', 'site_id', 'title', 'author_position',
                    'is_active', 'created_at', 'updated_at', ]

    search_fields = ['title', 'slug', 'site_id', 'author_position']

    list_filter = ['author_position', 'is_active', 'created_at', 'updated_at']

    list_display_links = ['id', 'site_id', 'title']


@register(Article)
class ArticleAdmin(BaseAdmin):
    list_display = ['id', 'site_id', 'title', 'category', 'author', 'image', 'description',
                    'is_active', 'created_at', 'updated_at']

    search_fields = ['title', 'slug', 'site_id', 'author_position']

    list_filter = ['slug', 'category', 'author',
                   'is_active', 'created_at', 'updated_at']

    list_display_links = ['id', 'site_id', 'title']


@register(Keyword)
class KeywordAdmin(BaseAdmin):
    list_display = ['id', 'slug', 'times_searched']
    list_display_links = ['id', 'slug']
    list_filter = []


@register(SearchByKeyword)
class SearchByKeywordAdmin(BaseAdmin):
    list_display = ['keyword', 'max_pages', 'is_active', 'search_at', 'new_articles', 'scrapped_articles']
    list_display_links = ['keyword']
    list_filter = ['search_at', 'is_active']
    search_fields = ['keyword']


@register(ArticleSearchByKeywordItem)
class ArticleSearchByKeywordItemAdmin(BaseAdmin):
    list_display = ['search_by_keyword', 'article', 'is_scrapped']
    list_display_links = ['search_by_keyword']
    list_filter = ['search_by_keyword', 'is_scrapped']
    search_fields = ['search_by_keyword']

