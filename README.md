### 🏬 Онлайн платформа торговой сети электроники

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2-092E20)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.16-9B59B6)](https://www.django-rest-framework.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17+-4169E1)](https://postgresql.org)


**Проект реализован в качестве тестового задания**

*Реализованы следующие ключевые функции:*

- Иерархическая система торговой сети (5 уровней)
- `REST API` для управления объектами сети
- Административная панель с кастомными действиями
- Интеграция с `Celery` для фоновых задач
- Работа с `PostgreSQL`

---
#### Структура проекта

```
    core
    ├── apps                 # Бизнес-логика
    │   ├── retail           # Розничная сеть
    │   │   └── management   # Заполнение базы данных
    │   └── users            # Аутентификация
    └── project              # Конфигурация
        └── settings         # Настройка под разные среды (dev/prod, celery)
```
---

#### :desktop_computer: Установка Linux

* Клонируем проект [***Online-retail-platform***](https://github.com/yakhovets-o/Online-retail-platform)
* Установите виртуальное окружение:  ```python -m venv venv```
* Активируйте виртуальное окружение: ```source venv/bin/activate```
* Установите внешние библиотеки, выполнив: ```pip install -r requirements.prod.txt``` и ```requirements.dev.txt```
* Запуск `PostgreSQL`: ```docker-compose up -d retail-db```
* Применение миграций: ```python manage.py makemigrations``` ```python manage.py migrate```
* Создание суперпользователя: ```python manage.py createsuperuser```
* Запуск сервера: ```python manage.py runserver```
* `Celery`: ```celery -A core.project beat --loglevel=info``` и ```celery -A core.project worker -l DEBUG -P solo```
* Создание тестовых данных (при необходимости, количество по вкусу) `Faker`: ```python manage.py fill_bd --suppliers 40 --products 5 --users 3``` 

*Стандартного конфига должно хватить на все (кроме отправки qr на почту)*

---
#### Примеры 
* ***Увеличение, Уменьшение долгов***

![Увеличение, Уменьшение долгов](https://github.com/user-attachments/assets/6faec2f3-dde3-42f0-85fc-da0946bccb42)


* ***Прощение долгов***
![Прощение долгов](https://github.com/user-attachments/assets/074b1dcf-96ae-4a06-9395-ebaeb8f9d1d4)

* ***QR***

![Письмо на почту](https://github.com/user-attachments/assets/c4b31888-7594-4107-96ec-4a9a9b701f16)

* ***API***

![API](https://github.com/user-attachments/assets/3de9ffc8-6d67-4473-a6ea-43f4d628511a)




---
#### 🛶  Что было реализовано помимо ТЗ:
* ***Автоматическая генерация документации `API`*** -  ```drf-yasg``` ```http://127.0.0.1:8000/swagger/```


![API дока](https://github.com/user-attachments/assets/e9bba1b1-2283-4ad7-8d9c-e1e35656d41b)

* ***Кастомная админка `django`*** - ```django-unfold```



![Админка](https://github.com/user-attachments/assets/eee9cee7-7f0c-4868-aa72-977d8f82ab75)

* ***Улучшение визуальной составляющей*** - ```black```, ```isort``` 
* ***Для более приятной работы с бд*** - ```docker compose postgres``` 

---
#### 🪁  Что хотел бы добавить, но не хватило времени или компетенций

* ***Написание тестов***
* ***Более продвинутую работу с линтерами (`Ruff`)***
* ***Более продвинутую работу с контейнеризацией***
* ***Stub-файлы  для типизации***
* ***Работу с логами***


