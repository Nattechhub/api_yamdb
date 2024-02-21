# Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## Для запуска проекта используются следующие пакеты:
* Python 3.7.9,
* requests==2.26.0
* Django==3.2
* djangorestframework==3.12.4
* PyJWT==2.1.0
* pytest==6.2.4
* pytest-django==4.4.0
* pytest-pythonpath==0.7.3
* djangorestframework-simplejwt
* django-filter

# Как запустить проект:

## Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:aidestob/api_yamdb.git
```

```
cd api_yamdb
```

## Cоздать и активировать виртуальное окружение:

### Для MacOs и Linux
```
python3 -m venv venv 
```

```
source venv/bin/activate
```
### Для Windows
```
python -m venv venv 
```

```
source venv/Scripts/activate
```

## Установить зависимости из файла requirements.txt:

### Для MacOs и Linux
```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

### Для Windows
```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

## Выполнить миграции:

### Для MacOs и Linux
```
python3 manage.py migrate
```
### Для Windows
```
python manage.py migrate
```

Запустить проект:

### Для MacOs и Linux
```
python3 manage.py runserver
```

### Для Windows
```
python manage.py runserver
```
# Примеры использования запросов:

## Запросы к API начинаются с /api/v1/
### Регистрация пользователей и выдача токенов

##### POST /auth/signup/
```
{
  "email": "user@example.com",
  "username": "string"
}
```

### Получение JWT-токена
##### POST /auth/token/
```
{
  "username": "string",
  "confirmation_code": "string"
}
```

### Получение списка всех категорий
##### GET /categories/
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```

### Добавление новой категории
##### POST /categories/
```
{
  "name": "string",
  "slug": "string"
}
```

### Удаление категории
##### DELETE /categories/{slug}/
```
{
  "name": "string",
  "slug": "string"
}
```
### С полным списком возможностей можно ознакомиться в документации:
`<link>` :    http://127.0.0.1:8000/redoc/

## Авторы:
### [Nattechhub](https://github.com/Nattechhub)
### [aidestob](https://github.com/aidestob)
### [Tlos205](https://github.com/Tlos205)
