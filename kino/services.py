from django.shortcuts import get_object_or_404
from kino.models import Film, Review
from pathlib import Path


def ranged(file, start=0, end=None, block_size=8192):
    consumed = 0

    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        file.close()


def open_file(request, id):
    film = get_object_or_404(Film, pk=id)

    path = Path(film.trailer.path)

    file = path.open('rb')
    file_size = path.stat().st_size

    content_length = file_size
    status_code = 200
    content_range = request.headers.get('range')

    if content_range is not None:
        content_ranges = content_range.strip().lower().split('=')[-1]
        range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        range_start = max(0, int(range_start)) if range_start else 0
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        content_length = (range_end - range_start) + 1
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        content_range = f'bytes {range_start}-{range_end}/{file_size}'

    return file, status_code, content_length, content_range


def get_film_review_or_none(film_id, user_id):
    try:
        self_review = Review.objects.get(film_id=film_id, user_id=user_id)
    except:
        self_review = None
    return self_review


def get_persons_form_film(persons_objects):
    persons = {}
    for person in persons_objects:
        if person.role.name not in persons.keys():
            persons[person.role.name] = [person]
        else:
            persons[person.role.name].append(person)
    return persons


