from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os

AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
              'Movies', api_key=os.environ.get('AIRTABLE_API_KEY'))


def home(request):
    user_query = request.GET.get('user_query', '')
    search_result = AT.get_all(formula="FIND('"+user_query+"', LOWER({Name}))")
    frontend_data = {
        'search_result': search_result
    }
    return render(request, 'movies/home.html', frontend_data)


def create(request):
    if request.method == "POST":
        try:
            data = {
                'Name': request.POST.get('name'),
                'Pictures': [{'url': request.POST.get('image') or 'https://s3.amazonaws.com/speedsport-news/speedsport-news/wp-content/uploads/2018/07/01082232/image-not-found.png'}],
                'Rating': int(request.POST.get('rating')),
                'Notes': request.POST.get('notes')
            }
            response = AT.insert(data)
            movie_name = response.get('fields').get('Name')
            messages.success(request, 'Created Movie: {}'.format(movie_name))
        except Exception as e:
            messages.warning(request, 'Error creating a movie: {}'.format(e))
    return redirect('home')


def update(request, movie_id):
    if request.method == "POST":
        try:
            data = {
                'Name': request.POST.get('name'),
                'Pictures': [{'url': request.POST.get('image') or 'https://s3.amazonaws.com/speedsport-news/speedsport-news/wp-content/uploads/2018/07/01082232/image-not-found.png'}],
                'Rating': int(request.POST.get('rating')),
                'Notes': request.POST.get('notes')
            }
            response = AT.update(movie_id, data)
            movie_name = response.get('fields').get('Name')
            messages.info(request, 'Updated Movie: {}'.format(movie_name))
        except Exception as e:
            messages.warning(request, 'Error updating movie: {}'.format(e))
    return redirect('home')


def delete(request, movie_id):        
    if request.method == "POST":
        try:
            movie_name = AT.get(movie_id).get('fields').get('Name')
            AT.delete(movie_id)
            messages.warning(request, 'Deleted Movie: {}'.format(movie_name))
        except Exception as e:
            messages.warning(request, 'Error deleting movie: {}'.format(e))
    return redirect('home')
