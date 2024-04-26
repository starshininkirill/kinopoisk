from django.db import models
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator, MinLengthValidator


class Genre(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    image = models.ImageField(upload_to='genres_images', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Country(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class Year(models.Model):
    year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.year)

    class Meta:
        verbose_name = 'Год'
        verbose_name_plural = 'Года'


class Film(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    duration = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='films_images', null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True, blank=True)
    trailer = models.FileField(upload_to='trailers', validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
                               null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def count_film_votes(self):
        ratings = self.ratings.all()
        return len(ratings)

    def get_average_rating(self):
        ratings = self.ratings.all()
        if len(ratings) != 0:
            return round(sum(rating.rating for rating in ratings) / len(ratings), 1)
        else:
            return 0

    def count_reviews(self, type='all'):
        if type == 'all':
            reviews_len = len(Review.objects.filter(film=self.id))
        else:
            reviews_len = len(Review.objects.filter(film=self.id, type=type))
        return reviews_len

    def count_percent_of_reviews(self, type=None):
        percent = self.count_reviews(type) / self.count_reviews() * 100
        return round(percent, 2)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    class Meta:
        unique_together = ('film', 'user')

        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинг'


class Review(models.Model):
    REVIEW_TYPES = (
        ('neutral', 'Нейтральный'),
        ('like', 'Положительный'),
        ('dislike', 'Отрицательный'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    text = models.TextField(
        validators=[
            MinLengthValidator(50, )
        ]
    )
    type = models.CharField(choices=REVIEW_TYPES, max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.film}'

    class Meta:
        unique_together = ('film', 'user')

        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'

    def count_user_reviews(self):
        return len(self.user.review_set.all())

    def get_positive_reviews(self):
        ratings = self.reviewrating_set.filter(rating='like')
        return len(ratings)

    def get_negative_reviews(self):
        ratings = self.reviewrating_set.filter(rating='dislike')
        return len(ratings)


class ReviewRating(models.Model):
    REVIEW_RATING_TYPES = (
        ('like', 'Положительный'),
        ('dislike', 'Отрицательный'),
    )

    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.CharField(max_length=30, default='like', choices=REVIEW_RATING_TYPES)

    class Meta:
        unique_together = ('review', 'user')

        verbose_name = 'Оценка рецензии'
        verbose_name_plural = 'Оценки рецензии'

    def __str__(self):
        return f'Оценка: {self.review} от {self.user}'


class Role(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'


class Person(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='persons_images', null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Популярный человек'
        verbose_name_plural = 'Популярные люди'

    def get_roles(self):
        roles = self.personsroles_set.values_list('role__name', flat=True).distinct()
        return list(roles)

    def get_genres(self):
        genres = set()
        for role in self.personsroles_set.all():
            genres.update(role.film.genres.all())
        return list(genres)

    def count_films(self):
        films = []
        for role in self.personsroles_set.all():
            films.append(role.film.id)
        return len(set(films))

    def get_range_of_years(self):
        films = []
        for role in self.personsroles_set.all():
            films.append(role.film.year.year)
        films.sort()
        return f'{films[0]} - {films[-1]}'

    def get_top_films(self):
        films = []
        for role in self.personsroles_set.all():
            films.append(role.film)
        films = list(set(films))
        rated_films = [(film, film.get_average_rating()) for film in films]
        sorted_films = sorted(rated_films, key=lambda x: x[1], reverse=True)
        sorted_films_instances = [film[0] for film in sorted_films]
        return sorted_films_instances[0:5]

    def get_films_by_roles(self):
        roles = self.get_roles()
        res = {}
        for role in roles:
            persons_roles = self.personsroles_set.filter(role__name=role)
            films = [persons_role.film for persons_role in persons_roles]
            res[role] = films
        return res


class PersonsRoles(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Роль человека в фильме'
        verbose_name_plural = 'Роли людей в фильмах'
