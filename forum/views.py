from django.shortcuts import render


def index(request):
    context = {
        'title': 'Заголовок страницы',
        'content': 'КАКОЙТО ТЕКСТ'
    }
    return render(request, 'forum/index.html', context=context)


def forum(request):
    return render(request, 'forum/forum.html')


def auth(request):
    return render(request, 'forum/auth.html')
