Сборка проекта
```bash
docker build -t project .
```

Сборка для тестов
```bash
docker build -f src/tests/Dockerfile -t tests .
```

Запуск тестов
```bash
docker run --rm tests
```

Запуск проекта целиком
```bash
docker compose up --build
```