# Используем базовый образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей (например, requirements.txt)
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

RUN make migrate head

# Копируем весь код проекта в контейнер
COPY . /app/

# Команда для запуска миграций
CMD ["python", "main.py"]
