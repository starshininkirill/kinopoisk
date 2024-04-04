from django.urls import path
from users.views import user_login, registration, logout_user, profile

app_name = 'users'

urlpatterns = [
    path('login/', user_login, name='login'),
    path('registration/', registration, name='registration'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),
]