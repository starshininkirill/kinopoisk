from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from kino.models import Genre, Film, Year, Rating, User, Role, Person, Review, ReviewRating
from kino.services import open_file, get_persons_form_film, get_film_review_or_none
from kino.forms import ReviewForm, FilterForm


def main_page(request, page=1):
    films = Film.get_sorted_films()

    search = None
    persons = None
    if request.GET.get('search'):
        search = request.GET.get('search')
        films = films.filter(name__iregex=search)
        persons = Person.objects.filter(name__iregex=search)

    if request.GET.get('genres'):
        films = films.filter(genres=request.GET.get('genres'))

    if request.GET.get('year'):
        films = films.filter(year=request.GET.get('year'))

    if request.GET.get('country'):
        films = films.filter(country=request.GET.get('country'))

    if request.GET.get('sort'):
        sort_method = request.GET.get('sort')
        if sort_method == 'name':
            films = films.order_by('name')
        if sort_method == '-name':
            films = films.order_by('-name')
        if sort_method == '-rate':
            films = films.reverse()
        if sort_method == 'year':
            films = films.order_by('year__year')
        if sort_method == '-year':
            films = films.order_by('-year__year')
        
    if request.GET:
        get_params = ['?']
        for param, value in request.GET.items():
            if len(get_params) == 1:
                get_params.append(f'{param}={value}')
            else:
                get_params.append(f'&{param}={value}')
        get_params = ''.join(get_params)
    else:
        get_params = ''


    paginator = Paginator(films, 4)
    films_on_page = paginator.get_page(page)

    form = FilterForm(request.GET)
    context = {
        'page_title': 'Главная',
        'films': films_on_page,
        'form': form,
        'search': search,
        'persons': persons,
        'get_params': get_params
    }
    return render(request, template_name='kino/pages/films.html', context=context)


def single_film(request, id):
    film = get_object_or_404(Film, id=id)
    page_form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            try:
                self_review = Review.objects.get(film_id=id, user_id=request.user.id)
            except ObjectDoesNotExist:
                self_review = Review.objects.create(
                    user=request.user,
                    film_id=id,
                    text=form.cleaned_data['text'],
                    type=form.cleaned_data['type']
                )
                self_review.save()
                return redirect('kino:film', id=id)
        else:
            page_form = form

    self_review = get_film_review_or_none(id, request.user.id)
    reviews = film.review_set.all().exclude(id=self_review.id) if self_review else film.review_set.all()
    context = {
        'film': film,
        'reviews': reviews,
        'user': request.user,
        'form': page_form,
        'self_review': self_review
    }

    return render(request, template_name='kino/pages/single-film.html', context=context)


def review(request, id):
    if request.method.lower() == "delete":
        try:
            review = Review.objects.get(pk=id)
            review.delete()
            return HttpResponse(status=204)
        except:
            return HttpResponse(status=404)



def genres(request):
    genres = Genre.objects.all()
    context = {
        'page__title': 'Жанры',
        'genres': genres
    }
    return render(request, 'kino/pages/genres.html', context=context)


def single_genre(request, id):
    genre = get_object_or_404(Genre, id=id)
    films = genre.film_set.all()
    context = {
        'page__title': genre.name,
        'genre': genre,
        'films': films,
    }
    return render(request, 'kino/pages/single-genre.html', context=context)


def single_person(request, id):
    person = Person.objects.get(id=id)
    context = {
        'person': person
    }
    return render(request, 'kino/pages/single-person.html', context=context)


def year(request, year):
    year = Year.objects.get(year=year)
    print(year)
    context = {
        'page__title': 'Год',
        'year': year
    }
    return render(request, 'kino/pages/single-year.html', context=context)


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


def video(request, pk):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response