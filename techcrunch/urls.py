from django.urls import path

from .views import search_by_keyword_view, manual_daily_search_view, diagrams

urlpatterns = [
    path('manual_daily_search', manual_daily_search_view, name='manual_daily_search'),
    path('search_keyword', search_by_keyword_view, name='search_keyword'),
    path('diagrams/<slug:model_name>', diagrams, name='diagrams'),
]
