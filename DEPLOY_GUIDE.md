# 🚀 Руководство по деплою на PythonAnywhere

Это руководство поможет вам задеплоить ваш Telegram бот рецептов на PythonAnywhere как Flask приложение.

## 📋 Подготовка

### 1. Создание аккаунта на PythonAnywhere
- Зарегистрируйтесь на [pythonanywhere.com](https://www.pythonanywhere.com)
- Выберите бесплатный план (Beginner) или платный (Hacker/Web Dev)

### 2. Подготовка файлов
Убедитесь, что у вас есть все необходимые файлы:
- `app.py` - Flask приложение
- `wsgi.py` - WSGI файл для PythonAnywhere
- `bot.py` - Основной код бота
- `config.py` - Конфигурация
- `api_client.py` - API клиент
- `database.py` - Работа с базой данных
- `requirements.txt` - Зависимости
- `env_example.txt` - Пример переменных окружения

## 🔧 Настройка на PythonAnywhere

### 1. Загрузка файлов
1. Зайдите в **Files** на PythonAnywhere
2. Создайте папку для вашего проекта (например, `recipe_bot`)
3. Загрузите все файлы проекта в эту папку

### 2. Установка зависимостей
1. Откройте **Consoles** → **Bash**
2. Перейдите в папку проекта:
   ```bash
   cd ~/recipe_bot
   ```
3. Создайте виртуальное окружение:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 recipe_bot
   ```
4. Активируйте окружение:
   ```bash
   workon recipe_bot
   ```
5. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Настройка переменных окружения
1. Создайте файл `.env` в папке проекта:
   ```bash
   nano .env
   ```
2. Добавьте ваш токен бота:
   ```
   BOT_TOKEN=your_actual_bot_token_here
   ```

### 4. Настройка WSGI файла
1. Откройте файл `wsgi.py`
2. Замените `yourusername` на ваш username на PythonAnywhere:
   ```python
   path = '/home/yourusername/recipe_bot'  # Замените yourusername
   ```

## 🌐 Настройка Web App

### 1. Создание Web App
1. Перейдите в **Web** на PythonAnywhere
2. Нажмите **Add a new web app**
3. Выберите **Flask**
4. Выберите **Python 3.10**
5. Введите путь к проекту: `/home/yourusername/recipe_bot`

### 2. Настройка WSGI
1. В разделе **Web** найдите **Code** секцию
2. Нажмите на ссылку к WSGI файлу
3. Замените содержимое на:
   ```python
   import sys
   import os
   
   path = '/home/yourusername/recipe_bot'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```
4. Сохраните файл

### 3. Настройка статических файлов
В разделе **Static files** добавьте:
- URL: `/static/`
- Directory: `/home/yourusername/recipe_bot/static/`

## 🚀 Запуск

### 1. Перезагрузка Web App
1. В разделе **Web** нажмите зеленую кнопку **Reload**
2. Дождитесь завершения перезагрузки

### 2. Проверка работы
1. Откройте ваш сайт: `https://yourusername.pythonanywhere.com`
2. Вы должны увидеть страницу со статусом бота
3. Проверьте API эндпоинты:
   - `https://yourusername.pythonanywhere.com/status`
   - `https://yourusername.pythonanywhere.com/health`

### 3. Запуск бота
1. Отправьте POST запрос на `/start` или
2. Используйте консоль:
   ```bash
   curl -X POST https://yourusername.pythonanywhere.com/start
   ```

## 🔍 Мониторинг и отладка

### 1. Логи
- **Error log**: `/var/log/yourusername.pythonanywhere.com.error.log`
- **Access log**: `/var/log/yourusername.pythonanywhere.com.access.log`

### 2. Консоль для отладки
```bash
cd ~/recipe_bot
workon recipe_bot
python app.py
```

### 3. Проверка статуса
```bash
curl https://yourusername.pythonanywhere.com/status
```

## ⚠️ Важные замечания

### 1. Ограничения бесплатного плана
- Приложение "засыпает" после 3 месяцев неактивности
- Ограниченное количество CPU секунд
- Нет возможности использовать HTTPS для webhook

### 2. Предотвращение "засыпания" с UptimeRobot
**Рекомендуется настроить UptimeRobot для постоянного мониторинга:**

1. Зарегистрируйся на [uptimerobot.com](https://uptimerobot.com)
2. Создай монитор:
   - **URL**: `https://yourusername.pythonanywhere.com/ping`
   - **Интервал**: 5 минут
   - **Тип**: HTTP(s)
3. Подробная инструкция: [UPTIMEROBOT_SETUP.md](UPTIMEROBOT_SETUP.md)

**Результат**: Приложение будет работать 24/7 без "засыпания"! 🚀

### 3. Безопасность
- Никогда не коммитьте `.env` файл в Git
- Используйте сильные токены
- Регулярно обновляйте зависимости

### 4. Производительность
- Бот работает в фоновом режиме
- Используйте webhook вместо polling для лучшей производительности
- Мониторьте использование ресурсов

## 🛠 Альтернативные варианты

### 1. Webhook вместо polling
Для лучшей производительности настройте webhook:
1. Получите URL вашего сайта
2. Установите webhook:
   ```python
   bot.set_webhook(url="https://yourusername.pythonanywhere.com/webhook")
   ```

### 2. Платный план
Для продакшена рассмотрите платный план:
- Больше CPU секунд
- Постоянная работа
- HTTPS поддержка
- Больше места на диске

## 📞 Поддержка

Если у вас возникли проблемы:
1. Проверьте логи ошибок
2. Убедитесь, что все зависимости установлены
3. Проверьте правильность токена бота
4. Обратитесь к документации PythonAnywhere

## 🎉 Готово!

Ваш Telegram бот теперь работает на PythonAnywhere! Пользователи могут взаимодействовать с ботом через Telegram, а вы можете мониторить его работу через веб-интерфейс.
