import json
import requests
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os

# Глобальная переменная для хранения данных
todos_data = []

def hello_world(request):
    html = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Django Project - Главная</title>
        <link href="/static/bootstrap/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="jumbotron bg-light p-5 rounded">
                <h1 class="display-4">Hello world!</h1>
                <p class="lead">Добро пожаловать в Django проект</p>
                <hr class="my-4">
                <p>Практическая работа № 2: Основные понятия Django. Вывод данных</p>
                <div class="mt-4">
                    <a class="btn btn-primary btn-lg" href="/todos/browser/" role="button">Просмотр данных в браузере</a>
                    <a class="btn btn-secondary btn-lg" href="/todos/console/" role="button">Вывод в консоль</a>
                    <a class="btn btn-info btn-lg" href="/api/todos/" role="button">API - Все данные</a>
                </div>
            </div>
        </div>
        <script src="/static/bootstrap/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    return HttpResponse(html)

def fetch_todos_data():
    """Получает данные с API и сохраняет в JSON файл и переменную"""
    global todos_data
    try:
        # Получаем данные с API
        response = requests.get('https://jsonplaceholder.typicode.com/todos/')
        response.raise_for_status()
        todos_data = response.json()
        
        # Сохраняем в JSON файл
        json_file_path = os.path.join(settings.BASE_DIR, 'todos_data.json')
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(todos_data, f, ensure_ascii=False, indent=2)
        
        # Выводим в консоль Django
        print("=" * 50)
        print("Данные получены с API jsonplaceholder:")
        print(f"Всего записей: {len(todos_data)}")
        print("Первые 3 записи:")
        for i, todo in enumerate(todos_data[:3], 1):
            print(f"{i}. ID: {todo['id']}, User ID: {todo['userId']}, Title: {todo['title']}, Completed: {todo['completed']}")
        print("=" * 50)
        
        return todos_data
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return []

def todos_console(request):
    """Выводит данные в консоль Django"""
    fetch_todos_data()
    html = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Вывод в консоль</title>
        <link href="/static/bootstrap/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="alert alert-success" role="alert">
                <h4 class="alert-heading">Готово!</h4>
                <p>Данные получены и выведены в консоль Django. Проверьте консоль, где запущен сервер разработки.</p>
            </div>
            <a href="/" class="btn btn-primary">На главную</a>
            <a href="/todos/browser/" class="btn btn-secondary">Просмотр данных в браузере</a>
        </div>
        <script src="/static/bootstrap/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    return HttpResponse(html)

def todos_browser(request):
    """Выводит данные в веб-браузер через форматирование строки с Bootstrap"""
    data = fetch_todos_data()
    
    if not data:
        return HttpResponse("Ошибка при получении данных с API.")
    
    # Форматируем данные для вывода в браузер с Bootstrap
    html = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Данные с jsonplaceholder API</title>
        <link href="/static/bootstrap/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="mb-4">Данные с jsonplaceholder API</h1>
            <div class="alert alert-info" role="alert">
                Всего записей: <strong>{total}</strong>
            </div>
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>ID</th>
                            <th>User ID</th>
                            <th>Title</th>
                            <th>Completed</th>
                        </tr>
                    </thead>
                    <tbody>
    """.format(total=len(data))
    
    for todo in data[:50]:  # Показываем первые 50 записей
        completed_badge = '<span class="badge bg-success">Да</span>' if todo['completed'] else '<span class="badge bg-danger">Нет</span>'
        html += f"""
                        <tr>
                            <td>{todo['id']}</td>
                            <td>{todo['userId']}</td>
                            <td>{todo['title']}</td>
                            <td>{completed_badge}</td>
                        </tr>
        """
    
    html += f"""
                    </tbody>
                </table>
            </div>
            <div class="mt-3">
                <p class="text-muted">Показано 50 из {len(data)} записей</p>
            </div>
            <div class="mt-4">
                <a href="/" class="btn btn-primary">На главную</a>
                <a href="/todos/console/" class="btn btn-secondary">Вывести в консоль</a>
            </div>
        </div>
        <script src="/static/bootstrap/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    
    return HttpResponse(html)

# Класс-контроллер для обработки запросов с регулярными выражениями
@method_decorator(csrf_exempt, name='dispatch')
class TodosController(View):
    """Класс-контроллер для обработки запросов к данным todos"""
    
    def get(self, request, todo_id=None, user_id=None):
        """Обработка GET запросов"""
        data = fetch_todos_data()
        
        if not data:
            return JsonResponse({'error': 'Данные не найдены'}, status=404)
        
        # Если указан todo_id, возвращаем конкретную задачу
        if todo_id:
            todo = next((t for t in data if t['id'] == int(todo_id)), None)
            if todo:
                return JsonResponse(todo)
            return JsonResponse({'error': f'Задача с ID {todo_id} не найдена'}, status=404)
        
        # Если указан user_id, возвращаем задачи пользователя
        if user_id:
            user_todos = [t for t in data if t['userId'] == int(user_id)]
            return JsonResponse({'user_id': int(user_id), 'todos': user_todos, 'count': len(user_todos)})
        
        # Возвращаем все данные
        return JsonResponse({'todos': data, 'count': len(data)})
    
    def post(self, request):
        """Обработка POST запросов"""
        return JsonResponse({'message': 'POST запрос получен', 'method': 'POST'})
    
    def put(self, request, todo_id=None):
        """Обработка PUT запросов"""
        return JsonResponse({'message': f'PUT запрос для задачи {todo_id}', 'method': 'PUT'})
    
    def delete(self, request, todo_id=None):
        """Обработка DELETE запросов"""
        return JsonResponse({'message': f'DELETE запрос для задачи {todo_id}', 'method': 'DELETE'})

