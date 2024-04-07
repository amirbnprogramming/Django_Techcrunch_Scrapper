from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render

from techcrunch.forms import SearchByKeywordForm
from techcrunch.tasks import search_by_keyword_task, daily_scrape_task, diagram_generator_task


# Create your views here.
def manual_daily_search_view(request):
    daily_scrape_task.delay()
    return HttpResponse('hi')


@login_required
def diagrams(request, model_name):
    current_user = request.user.username
    diagram_generator_task.delay(model_name=model_name, current_user=current_user)
    return HttpResponse("Plot PNG Picture will be generate in current directory soon.")


@login_required
def search_by_keyword_view(request):
    current_user_user_name = request.user.username
    if request.method == 'POST':
        form = SearchByKeywordForm(request.POST)
        if form.is_valid():
            result = search_by_keyword_task.delay(
                user_name=current_user_user_name,
                keyword=form.cleaned_data['keyword'],
                max_page=form.cleaned_data['max_pages'],
            )
            print(f'techcrunch_search_by_keyword_task:({result})', )
    else:
        form = SearchByKeywordForm()

    return render(request, 'techcrunch/search_temp/index.html', {'form': form})


