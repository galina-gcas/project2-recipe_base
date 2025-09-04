# config.py
# Конфигурация бота

from dotenv import load_dotenv
import os

load_dotenv()

# Токен Telegram бота (получить у @BotFather)
BOT_TOKEN = os.getenv('BOT_TOKEN')

# API настройки для TheMealDB
MEAL_DB_BASE_URL = "https://www.themealdb.com/api/json/v1/1"

# Настройки базы данных
DATABASE_NAME = "recipes_bot.db"

# Настройки API (если понадобятся другие сервисы)
EDAMAM_APP_ID = os.getenv('EDAMAM_APP_ID', '')
EDAMAM_APP_KEY = os.getenv('EDAMAM_APP_KEY', '')

# Лимиты
MAX_RECIPES_PER_SEARCH = 10
MAX_FAVORITES_PER_USER = 100
