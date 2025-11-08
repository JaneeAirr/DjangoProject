# Django Project - Практическая работа № 2

Проект Django для работы с API jsonplaceholder и выводом данных.

## Описание

Этот проект реализует:
- Интеграцию с API jsonplaceholder (https://jsonplaceholder.typicode.com/todos/)
- Сохранение данных в JSON файл и переменную
- Вывод данных в консоль Django
- Вывод данных в веб-браузер с форматированием
- Маршрутизацию с регулярными выражениями
- Класс-контроллер для обработки HTTP запросов
- Подключение Bootstrap 5 для стилизации

## Требования

- Python 3.8+
- Django 5.2.8
- requests 2.32.5

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/JaneeAirr/DjangoProject.git
cd DjangoProject
```

2. Создайте виртуальное окружение:
```bash
python -m venv env
```

3. Активируйте виртуальное окружение:
- Windows:
```powershell
.\env\Scripts\Activate.ps1
```
- Linux/Mac:
```bash
source env/bin/activate
```

4. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск

1. Запустите сервер разработки:
```bash
python manage.py runserver
```

2. Откройте в браузере:
```
http://127.0.0.1:8000/
```

## Маршруты

### Веб-интерфейс:
- `/` - Главная страница
- `/todos/console/` - Вывод данных в консоль Django
- `/todos/browser/` - Просмотр данных в браузере (таблица с Bootstrap)

### API (JSON):
- `GET /api/todos/` - Получить все задачи
- `GET /api/todos/{id}/` - Получить задачу по ID
- `GET /api/todos/user/{user_id}/` - Получить задачи пользователя
- `GET /api/todos/{todo_id}/user/{user_id}/` - Комбинированный маршрут

### Методы HTTP:
- `GET` - Получение данных
- `POST` - Создание (пример)
- `PUT` - Обновление (пример)
- `DELETE` - Удаление (пример)

## Структура проекта

```
DjangoProject/
├── env/                    # Виртуальное окружение (не коммитится)
├── static/                 # Статические файлы
│   └── bootstrap/          # Bootstrap 5
├── myproject/              # Основной проект Django
│   ├── views.py           # Views и класс-контроллер
│   ├── urls.py            # URL-маршруты
│   └── settings.py        # Настройки проекта
├── manage.py              # Управление Django
├── requirements.txt       # Зависимости проекта
└── README.md             # Документация
```

## Особенности

- ✅ Работа с внешним API (jsonplaceholder)
- ✅ Сохранение данных в JSON файл
- ✅ Вывод в консоль и браузер
- ✅ Регулярные выражения в маршрутизации
- ✅ Класс-контроллер (Class-based View)
- ✅ Bootstrap 5 для UI
- ✅ RESTful API endpoints

## Автор

Практическая работа по Django

## Лицензия

MIT

