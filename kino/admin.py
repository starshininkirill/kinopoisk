from django.contrib import admin
from kino.models import Genre, Film, Country, Year, Rating, Person, Role, PersonsRoles, Review, ReviewRating


class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'film', 'rating')


class PersonsPolesAdmin(admin.ModelAdmin):
    list_display = ('film', 'person', 'role')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('film', 'user', 'type')


class PersonsRolesInline(admin.TabularInline):
    model = PersonsRoles


class FilmAdmin(admin.ModelAdmin):
    inlines = [
        PersonsRolesInline,
    ]


admin.site.register(Genre)
admin.site.register(Film, FilmAdmin)
admin.site.register(Country)
admin.site.register(Year)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Person)
admin.site.register(Role)
admin.site.register(PersonsRoles, PersonsPolesAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewRating)
