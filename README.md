# Бот для поиска TRG сессий

## Запуск

### Poetry

```bash
poetry install
```

```bash
poetry shell
```

### .env файл

```bash
make env
```

Далее запишите в него токен бота

### База данных

```bash
make db
```

```bash
make migrate head
```

### Запуск бота

```bash
make run
```

## Руководство разработчику

### Если сделаны изменения в БД, то нужно добавить ревизию

```bash
make revision
```
