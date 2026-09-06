FROM python:3.12-slim

# Устанавливаем системные зависимости для psycopg2 и сборки
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]