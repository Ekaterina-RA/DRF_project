#Проект "Онлайн-обучение"

##Описание: созданы приложения onlinelearning и users на основе DRF:
1. Данные приложения зарегистрированы в настройках (config\settings.py\installed app)
2. Созданы модели Course, Lesson и User
3.  Описаны CRUD для моделей Course (Viewsets) и Lesson (Generic)
4. Создан файл serializers.py, гдн описаны простые сериализаторы для моделей Course и Lesson
5. Для модели Course добавлено поле lessons_count (поле вывода количества уроков)
6. Создана новая модель Payments, добавлена фильтрация для вывода списка платежей в классе PaymentViewSet
7. Реализован CRUD пользователей, настроена в проекте JWT-авторизация
8. Создана группа модераторов с ограниченными правами

##Установка:
1. Клонируйте репозиторий git@github.com:Ekaterina-RA/DRF_project.git
2. Установите зависимости pip install