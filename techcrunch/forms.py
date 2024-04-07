from django import forms
from techcrunch import constants
from techcrunch.models import SearchByKeyword


class SearchByKeywordForm(forms.Form):
    keyword = forms.CharField(
        label='Keyword',
        max_length=250,
        widget=forms.TextInput(attrs={'class': 'input--style-1',
                                      'placeholder': 'Keyword to search for . . .',
                                      'type': 'text',
                                      'required': True,
                                      'label_attrs': {'class': 'label'}})
    )
    max_pages = forms.IntegerField(
        label='Page Count',
        min_value=constants.MINIMUM_SEARCH_PAGE_COUNT,
        max_value=constants.MAXIMUM_SEARCH_PAGE_COUNT,
        widget=forms.NumberInput(attrs={'class': 'input--style-1',
                                        'placeholder': 'Number of pages to search for . . .',
                                        'type': 'number',
                                        'required': True,
                                        'label_attrs': {'class': 'label'}})
    )
