<<<<<<< HEAD
# api_yamdb
# Описание:  

Проект YaMDb (REST API) собирает отзывы пользователей на различные произведения.  
Реализовано на `Djangorestframework 3.12.4` Аутентификация на основе `JWT`. Читать контент могут все, вносить и изменять только аутентифицированные пользователи.  
Предоставляет ответы от сервера в формате JSON для последующей сериалиализации на стороне фронта.  
Это первый совместный проект, было сложно но интересно. 

  
# Установка:

Клонировать репозиторий и перейти в него в командной строке:  
`git clone https://github.com/mark-rom/api_yamdb.git`  
`cd api_yamdb`  
  
Cоздать и активировать виртуальное окружение:  
`python3.9 -m venv env`  
`source env/bin/activate` - для Mac OS  
`source venv/Scripts/activate` - для Windows OS  
  
Установить зависимости из файла requirements.txt:  
  
`python3 -m pip install --upgrade pip`  
`pip install -r requirements.txt`  
  
Выполнить миграции:  
  
`python3 manage.py makemigrations`  
`python3 manage.py migrate`  
  
 Залить базу данных из csv файлов:  
  
`python3 manage.py unpackingcsv`
  
Запустить проект:  
  
`python3 manage.py runserver`  
  
# Алгоритм регистрации пользователей
  
1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.  
2. YaMDB отправляет письмо с кодом подтверждения `confirmation_code` на адрес `email`. В проекте реализован бэкенд почтового сервиса, папка - `sent_emails`.  
3. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен).  
4. При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле.  
=======
# infra_sp2
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». 
Список категорий (Category) может быть расширен администратором. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. 
В каждой категории есть произведения: книги, фильмы или музыка. Произведению может быть присвоен жанр (Genre) из списка предустановленных. 
Новые жанры может создавать только администратор.

> К проекту по адресу http://127.0.0.1/redoc/ подключена документация API YaMDb. В ней описаны возможные запросы к API и структура ожидаемых ответов.
Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.

## _Запуск_:
 - Клонируйте репозиторий на свою локальную машину:
```sh
https://github.com/aimerkz/infra_sp2.git
сcd infra
```
 - Cоздайте в папке /infra файл .env и заполните его переменными окружения:
```sh
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем c postgresql

DB_NAME=postgres # имя базы данных

POSTGRES_USER=postgres # логин для подключения к базе данных

POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)

DB_HOST=db # название сервиса (контейнера)

DB_PORT=5432 # порт для подключения к БД

SECRET_KEY=ваш секретный ключ
```
- Находясь в папке /infra, запустите сборку образа Docker:
```sh
docker-compose up -d
```
- Выполните миграции:
```sh
docker-compose exec web python manage.py migrate
```

- Создайте суперпользователя:
```sh
docker-compose exec web python manage.py createsuperuser
```
- Выполните команду collectstatic:
```sh
docker-compose exec web python manage.py collectstatic --no-input
```
- Заполните базу тестовыми данными:
```sh
docker-compose exec web python manage.py loaddata fixtures.json
```
- Перейдите по адресу:
```sh
http://localhost/api/v1
```
>>>>>>> 0feb7f4b917f9ebd63fe3fb39f34c56564eefa49
