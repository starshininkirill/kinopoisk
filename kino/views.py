from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint
from django.core.exceptions import ObjectDoesNotExist

from kino.models import Genre, Film, Year, Rating, User, Role, Person, Review, ReviewRating
from kino.services import open_file
from kino.forms import ReviewForm


def main_page(request):
    films = Film.objects.all()
    context = {
        'page_title': 'Главная',
        'films': films
    }
    return render(request, template_name='kino/films.html', context=context)


def single_film(request, id):
    film = get_object_or_404(Film, id=id)
    reviews = film.review_set.all()
    form = ReviewForm()
    persons_objects = film.personsroles_set.all()
    persons = {}
    for person in persons_objects:
        if person.role.name not in persons.keys():
            persons[person.role.name] = [person]
        else:
            persons[person.role.name].append(person)

    context = {
        'film': film,
        'persons': persons,
        'reviews': reviews,
        'user': request.user,
        'form': form
    }
    return render(request, template_name='kino/single_film.html', context=context)


def video(request, pk):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response


def genres(request):
    genres = Genre.objects.all()
    context ={
        'page__title': 'Жанры',
        'genres' : genres
    }
    return render(request, 'kino/genres.html', context=context)

def single_genre(request, id):
    genre =  get_object_or_404(Genre, id=id)
    films = genre.film_set.all()
    context = {
        'page__title': genre.name,
        'genre': genre,
        'films': films,
    }
    return render(request, 'kino/single-genre.html', context=context)

def year(request, year):
    year = Year.objects.get(year=year)
    print(year)
    context = {
        'page__title': 'Год',
        'year': year
    }
    return render(request, 'kino/year.html', context=context)


def single_person(request, id):
    person = Person.objects.get(id=id)
    return render(request, f'{person.name}')


def single_country(request, id):
    return HttpResponse(status=200)


@csrf_exempt
def vote(response):
    film_id = int(response.POST['film'])
    user_id = int(response.POST['user'])
    new_rating = int(response.POST['rating'])
    try:
        rating = Rating.objects.get(film_id=film_id, user_id=user_id)
        rating.rating = new_rating
        rating.save()
    except ObjectDoesNotExist:
        rating = Rating.objects.create(film_id=film_id, user_id=user_id, rating=new_rating)

    data = {
        'message': 'success'
    }
    return JsonResponse(data)


@csrf_exempt
def set_review_rating(response):
    film_id = int(response.POST['film'])
    user_id = int(response.POST['user'])
    review_id = int(response.POST['review'])
    rating_type = response.POST['type']
    try:
        rating = ReviewRating.objects.get(user_id=user_id, review_id=review_id)
        if rating.rating == rating_type:
            return JsonResponse({
                'status': 'Нет обновлений',
                'no_changed': True,
                'created': False,
            })

        rating.rating = rating_type
        rating.save()

        return JsonResponse({
            'status': 'Успешно обновлено',
            'no_changed': False,
            'created': False,
        })
    except ObjectDoesNotExist:
        rating = ReviewRating.objects.create(review_id=review_id, user_id=user_id, rating=rating_type)
        return JsonResponse({
                'status': 'Успешно создано',
                'no_changed': False,
                'created': True,
            })



