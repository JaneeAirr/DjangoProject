import json
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from collections import defaultdict
import os

# Глобальная переменная для хранения данных
todos_data = []

def home(request):
    """Главная страница"""
    return render(request, 'home.html')

def login_view(request):
    """Страница входа"""
    return render(request, 'login.html')

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
    return render(request, 'todos_console.html')

def todos_list(request):
    """Список задач с группировкой по пользователям"""
    data = fetch_todos_data()
    
    if not data:
        return render(request, 'todos_list.html', {'todos': [], 'todos_by_user': {}})
    
    # Группируем задачи по пользователям
    todos_by_user = defaultdict(list)
    for todo in data:
        todos_by_user[todo['userId']].append(todo)
    
    # Сортируем по user_id
    todos_by_user = dict(sorted(todos_by_user.items()))
    
    context = {
        'todos': data,
        'todos_by_user': todos_by_user,
    }
    
    return render(request, 'todos_list.html', context)

def todo_detail(request, todo_id):
    """Детальная информация о задаче"""
    data = fetch_todos_data()
    
    if not data:
        return HttpResponse("Данные не загружены", status=404)
    
    todo = next((t for t in data if t['id'] == int(todo_id)), None)
    
    if not todo:
        return HttpResponse("Задача не найдена", status=404)
    
    context = {
        'todo': todo,
    }
    
    return render(request, 'todo_detail.html', context)

def todos_browser(request):
    """Выводит данные в веб-браузер через форматирование строки с Bootstrap (старая версия)"""
    data = fetch_todos_data()
    
    if not data:
        return HttpResponse("Ошибка при получении данных с API.")
    
    # Редирект на новую страницу списка
    return todos_list(request)

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

