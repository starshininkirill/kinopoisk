from django import template
import kino.views as views
from kino.models import Rating, Film

register = template.Library()


@register.inclusion_tag('kino/components/review_rating.html')
def review_rating(user=None, review=None):
    print(user, review)


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
