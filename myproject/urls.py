"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hello_world, name='hello_world'),
    
    # Маршруты для работы с данными todos
    path('todos/console/', views.todos_console, name='todos_console'),
    path('todos/browser/', views.todos_browser, name='todos_browser'),
    
    # Маршрутизация с регулярными выражениями для класса-контроллера
    # Универсальный маршрут с опциональными параметрами (самый специфичный - должен быть первым)
    re_path(r'^api/todos/(?P<todo_id>\d+)/user/(?P<user_id>\d+)/$', views.TodosController.as_view(), name='todos_complex'),
    
    # Получить todos по user_id (например: /api/todos/user/1/)
    re_path(r'^api/todos/user/(?P<user_id>\d+)/$', views.TodosController.as_view(), name='todos_by_user'),
    
    # Получить конкретный todo по id (например: /api/todos/1/)
    re_path(r'^api/todos/(?P<todo_id>\d+)/$', views.TodosController.as_view(), name='todo_detail'),
    
    # Получить все todos (самый общий - должен быть последним)
    re_path(r'^api/todos/$', views.TodosController.as_view(), name='todos_all'),
]
