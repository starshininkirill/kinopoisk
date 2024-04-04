from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.forms import UserCreationForm

from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {
        'form': form,
        'page_title': 'Авторизация',
        }
    return render(request, 'users/login.html', context=context)


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print('valid')

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
        'page_title': 'Регистрация'
    }
    return render(request, 'users/registration.html', context=context)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def profile(request):
    if request.user.is_authenticated == True:
        if request.method == "POST":
            form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('users:profile'))
        else:
            form = UserProfileForm(instance=request.user)
        context = {
            'page_title': 'Профиль',
            'form' : form,
        }
        return render(request, 'users/profile.html', context=context)
    else:
        return(HttpResponseRedirect(reverse('index')))