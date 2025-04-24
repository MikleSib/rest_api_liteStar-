1. Клонировать репозиторий:
```bash
git clone https://github.com/MikleSib/rest_api_liteStar-.git
cd /rest_api_liteStar-
```

2. Запустить
```bash
docker-compose up -d
```

API будет доступен по адресу: http://localhost:8000
Swagger UI: http://localhost:8000/schema/swagger

Применить миграции: docker-compose exec app alembic upgrade head

Ушло 2-3 часа, но это еще чет доккер устанавливал зависимости долго
