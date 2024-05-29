# Кинопоиск Lite

В проекте Кинопоиск Lite я реализовал часть функционала со всем известного сайта "Кинопоиск".

## Стек

- Python
- Django
- sqlite
- HTML5
- CSS3
- JavaScript

## Функционал

- Просмотр фильмов с описанием, фотографией, трейлером, участниками фильма и другой информацией.
- Оценка фильмов
- Написание рецензий на фильмы, оценка рецензий пользователями
- Поиск фильмов
- Фильтрация фильмов по жанру, стране, году выпуска
- Сортировка фильмов по рейтингу, году выпуска, названию
- Страница с информацией о людях учавствующий в фильме(Режисёры, Актёры и тд.)
- Система администрирования. Весь контент редактируется из админ панели. Разделение пользователей на Роли администраторов и пользователей. Для наглядности пользователь сам может стать администратором при регистрации. Функции удаления и редактирования сущностей ограничены в целях сохранения контента.

## Запуск проекта

1. Склонируйте репозиторий: `git clone https://github.com/starshininkirill/kinopoisk`
2. Создайте виртуальное окружение: `python -m venv venv`
3. Активируйте виртуальное окружение: `source venv/bin/activate` (для Windows: `venv\Scripts\activate`)
4. Установите зависимости: `pip install -r kinopoisk/requirements.txt`
5. Создайте базу данных: `python manage.py migrate`
6. Загрузите базу данных `python manage.py loaddata data.json`
7. Запустите сервер: `python manage.py runserver`

## Скриншоты

![Главная страница](/screenshots/main.png)
![Страница фильма](/screenshots/film.png)
