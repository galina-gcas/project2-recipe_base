#!/usr/bin/env python3
"""
Скрипт для автоматического запуска бота при старте приложения
Этот файл можно использовать для автоматического запуска бота
"""

import os
import time
import requests
from config import BOT_TOKEN

def start_bot_automatically():
    """Автоматически запускает бота через API"""
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN не настроен!")
        return False
    
    # URL вашего приложения (замените на ваш)
    app_url = "https://yourusername.pythonanywhere.com"  # Замените yourusername
    
    try:
        # Проверяем статус
        response = requests.get(f"{app_url}/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('bot_running'):
                print("✅ Бот уже запущен")
                return True
        
        # Запускаем бота
        print("🚀 Запускаем бота...")
        response = requests.post(f"{app_url}/start", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('message', 'Бот запущен')}")
            return True
        else:
            print(f"❌ Ошибка запуска: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

if __name__ == "__main__":
    start_bot_automatically()
