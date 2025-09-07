#!/usr/bin/python3.10

"""
WSGI файл для деплоя на PythonAnywhere
Этот файл должен быть в корне проекта
"""

import sys
import os

# Добавляем путь к проекту в PYTHONPATH
path = '/home/yourusername/recipe_bot'  # Замените yourusername на ваш username
if path not in sys.path:
    sys.path.append(path)

# Устанавливаем переменную окружения для Flask
os.environ['FLASK_APP'] = 'app.py'

# Импортируем Flask приложение
from app import app as application

# Автоматически запускаем бота при старте приложения
if __name__ == "__main__":
    # Этот код выполнится только при прямом запуске файла
    pass
