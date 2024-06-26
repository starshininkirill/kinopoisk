from django import template
from kino.models import Rating, Film

register = template.Library()


@register.inclusion_tag('kino/components/count_percent_of_review.html')
def count_percent_of_review(film=None, type=None):
    if film and type:
        try:
            film = Film.objects.get(pk=film.id)
            return {'percent': film.count_percent_of_reviews(type)}
        except:
            return {'percent': 0}
    return {'percent': 0}


@register.inclusion_tag('kino/components/count_review.html')
def count_review(film=None, type='all'):
    if film:
        try:
            film = Film.objects.get(pk=film.id)
            count = film.count_reviews(type)
            return {'count': count}
        except:
            return {'count': 0}
    return {'count': 0}


@register.inclusion_tag('kino/components/review_rating.html')
def review_rating(user=None, review=None):
    data = {
        'review': review,
        'user': user,
        'is_positive': False,
        'is_negative': False,
    }
    if user and review:
        try:
            rating_review = review.reviewrating_set.filter(user=user)[0]
            if rating_review.rating == 'like':
                data['is_positive'] = True
            elif rating_review.rating == 'dislike':
                data['is_negative'] = True
        except:
            pass

    return data


@register.inclusion_tag('kino/components/votes.html')
def votes(user=None, film=None):
    nums = range(1, 11)
    if user and film:
        try:
            current_vote = Rating.objects.get(user=user, film=film).rating
        except:
            current_vote = None
    return {
        'nums': nums,
        'user': user,
        'film': film,
        'current_vote': current_vote
    }


@register.inclusion_tag('kino/components/film.html')
def film(film=None):
    film = Film.objects.get(pk=film)

    return {
        'film': film,
    }
