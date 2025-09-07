# project2-recipe_base
A Telegram bot offering a wide selection of recipes


# 🍽 Recipe Telegram Bot

Telegram bot for searching recipes and saving favorites.

## 🚀 Features

- 🔍 Recipe search via TheMealDB API  
- ⭐️ Save favorite recipes  
- 📱 User-friendly interface with inline buttons  
- 🖼 View dish images  

## 📋 Installation and Launch

1. Clone the repository and navigate to the folder:
      cd "Project 2 — Recipe"
   

2. Install dependencies:
      pip install -r requirements.txt
   

3. Create a bot in Telegram:
   - Find @BotFather in Telegram  
   - Create a new bot with the command /newbot  
   - Copy the generated token  

4. Configure the token:
   - Create an environment variable BOT_TOKEN with your token  
   - Or replace YOUR_BOT_TOKEN_HERE in config.py  

5. Run the bot:
      python bot.py
   

## 🛠 Project Structure

Project 2 — Recipe/  
├── bot.py              # Main bot file  
├── config.py           # Configuration and settings  
├── requirements.txt    # Python dependencies  
└── README.md           # Documentation  

## 🔧 Configuration

In config.py you can change:  
- Bot token  
- API URL for recipes  
- Search limits  
- Database settings  

## 🚀 Деплой на PythonAnywhere

Для деплоя на PythonAnywhere как Flask приложение:

1. **Подготовка**: Следуйте инструкциям в [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)
2. **Файлы для деплоя**:
   - `app.py` - Flask приложение
   - `wsgi.py` - WSGI конфигурация
   - `requirements.txt` - обновлен с Flask
   - `env_example.txt` - пример переменных окружения

3. **Быстрый старт**:
   ```bash
   # Загрузите файлы на PythonAnywhere
   # Установите зависимости
   pip install -r requirements.txt
   # Создайте .env файл с BOT_TOKEN
   # Настройте Web App в панели PythonAnywhere
   ```

## 📝 TODO

- [x] Integration with TheMealDB API  
- [x] Database for favorite recipes  
- [x] Recipe search by name and ingredients  
- [x] View detailed recipe information  
- [x] Favorites system  
- [x] Flask app for deployment

## 🤖 Bot Commands

- /start - Start the bot and open the main menu  
- 🔍 Search recipes - Find new recipes  
- ⭐️ My recipes - View favorite recipes  


