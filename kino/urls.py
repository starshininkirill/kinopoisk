from django.urls import path
from kino import views

app_name = 'kino'

urlpatterns = [
    path('film/', views.main_page, name='film'),
    path('film/<int:id>', views.single_film, name='film'),
    path('video/<int:pk>/', views.video, name='video'),
    path('genre/', views.genres, name='genre'),
    path('genre/<int:id>/', views.single_genre, name='genre'),
    path('year/<int:year>', views.year, name='year'),
    path('country/<int:id>', views.single_country, name='country'),
    path('person/<int:id>', views.single_person, name='person'),
    path('vote/', views.vote, name='vote'),
]