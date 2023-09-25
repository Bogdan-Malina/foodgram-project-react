### Foodgram

### Как запустить проект:

Из папки infra выполните:
```
docker-compose up --build
```
Зайдите в контейнер foodgram_backend
```
docker container ls

docker exec -it <CONTAINER ID> bash
```
Сделайте миграции
```
python manage.py migrate
```
В infra создайте файл .env с переменными:

DB_ENGINE
DB_NAME
POSTGRES_USER
POSTGRES_PASSWORD
DB_HOST
DB_PORT  


### Автор
Данил Воронин https://github.com/Bogdan-Malina
