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
cd infra
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
