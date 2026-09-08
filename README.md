# DRF Project "Онлайн-обучение"

Полнофункциональный Django REST Framework проект с автоматическим деплоем через GitHub Actions.

## 🚀 Возможности проекта

- ✅ REST API с аутентификацией JWT
- ✅ Админ-панель Django
- ✅ Интеграция со Stripe для платежей
- ✅ Асинхронные задачи через Celery + Redis
- ✅ Автоматическое тестирование (CI/CD)
- ✅ Docker-контейнеризация
- ✅ Deploy (Yandex Cloud)
- ✅ Nginx reverse proxy
- ✅ PostgreSQL база данных

## 🛠 Технологии

**Backend:**
- Python 3.12
- Django 5.2.4
- Django REST Framework 3.16.0
- SimpleJWT 5.5.1 (аутентификация)
- Celery 5.5.3 (асинхронные задачи)
- Stripe API (платежи)
- drf-yasg (документация API)
- 
**База данных:**
- PostgreSQL 15

**Кэширование и очереди:**
- Redis 7

**DevOps:**
- Docker & Docker Compose
- Nginx (reverse proxy)
- GitHub Actions (CI/CD)
- Yandex Cloud (production server)

## 📦 Локальная установка

### Требования
- Python 3.12+
- PostgreSQL 15+
- Redis 7+

### Шаги установки

1. Клонируйте репозиторий:
   git clone https://github.com/Ekaterina-RA/DRF_project.git
   cd DRF_project
2. Создайте виртуальное окружение командами:
 - python -m venv venv
 - venv\Scripts\activate (Windows)
3. Установите зависимости: pip install -r requirements.txt
4. Настройте переменные окружения в файле .env (в корне проекта)
5. Примените миграции: python manage.py migrate
6. Создайте суперпользователя: python manage.py createsuperuser
7. Запустите сервер: python manage.py runserver

###№ Запуск через Docker
1. Собираем и запускаем контейнеры проекта: docker compose -f docker-compose-dep.yml up -d --build
2.Применяем миграции: docker exec -it drf_project-web-1 python manage.py migrate
3. Создаем суперпользователя: docker exec -it drf_project-web-1 python manage.py createsuperuser

###Полезные ссылки
📚 API Документация
API документация доступна через drf-yasg:
Swagger UI: http://51.250.101.46/swagger/
ReDoc: http://51.250.101.46/redoc/

Проект развернут по адресу: http://51.250.101.46/admin/

🤝 Автор
Екатерина
GitHub: @Ekaterina-RA