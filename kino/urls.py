from django.urls import path
from kino import views

app_name = 'kino'

urlpatterns = [
    path('film/', views.main_page, name='film'),
    path('film/<int:id>', views.single_film, name='film'),
    path('review/<int:id>', views.review, name='review'),
    path('video/<int:pk>/', views.video, name='video'),
    path('genre/', views.genres, name='genre'),
    path('genre/<int:id>/', views.single_genre, name='genre'),
    path('genre/<int:id>/page-<int:page>/', views.single_genre, name='genre'),
    path('person/<int:id>', views.single_person, name='person'),
    path('vote/', views.vote, name='vote'),
    path('set-review-rating/', views.set_review_rating, name='set_review_rating')
]