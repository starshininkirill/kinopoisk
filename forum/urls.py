from django.urls import path
from forum.views import forum

app_name = 'forum'

urlpatterns = [
    path('', forum, name='index'),
]