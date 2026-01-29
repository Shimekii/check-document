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
docker run tests
```

Запуск проекта
```bash
docker run -p 8080:8080 project
```