## Foodgram - Cервис для публикации рецептов. Авторизированные пользователи могут создавать рецепты, подписываться на понравившихся авторов, добавлять рецепты в избранное и список покупок, скачивать список покупок в формате csv.

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Bogdan-Malina/foodgram-project-react.git
```

```
cd foodgram-project-react/infra
```
В папке infra создайте и заполните .env файл:

```
DB_ENGINE='django.db.backends.postgresql'
DB_NAME='postgres'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='postgres'
DB_HOST='db'
DB_PORT=5432
```

Из папки infra выполните:
```
docker-compose up --build

```
Зайдите в контейнер infra_backend_1
```
docker exec -it infra_backend_1 bash
```
Сделайте миграции
```
python manage.py makemigrations
```
```
python manage.py migrate
```


### Автор
Данил Воронин https://github.com/Bogdan-Malina
