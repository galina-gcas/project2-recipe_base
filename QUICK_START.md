# ⚡ Быстрый старт - Деплой на PythonAnywhere

## 🎯 Что нужно сделать

### 1. Подготовка (5 минут)
- [ ] Зарегистрироваться на [pythonanywhere.com](https://pythonanywhere.com)
- [ ] Создать Telegram бота у [@BotFather](https://t.me/BotFather)
- [ ] Получить токен бота

### 2. Загрузка файлов (3 минуты)
- [ ] Загрузить все файлы проекта в папку на PythonAnywhere
- [ ] Создать файл `.env` с токеном:
  ```
  BOT_TOKEN=your_bot_token_here
  ```

### 3. Установка зависимостей (2 минуты)
```bash
cd ~/your_project_folder
mkvirtualenv --python=/usr/bin/python3.10 recipe_bot
workon recipe_bot
pip install -r requirements.txt
```

### 4. Настройка Web App (3 минуты)
- [ ] В панели PythonAnywhere: **Web** → **Add a new web app**
- [ ] Выбрать **Flask** и **Python 3.10**
- [ ] Указать путь к проекту
- [ ] Настроить WSGI файл (заменить `yourusername` в `wsgi.py`)

### 5. Запуск (1 минута)
- [ ] Нажать **Reload** в разделе Web
- [ ] Открыть ваш сайт: `https://yourusername.pythonanywhere.com`
- [ ] Отправить POST запрос на `/start` для запуска бота

## 🔗 Полезные ссылки

- **Статус бота**: `https://yourusername.pythonanywhere.com/status`
- **Здоровье приложения**: `https://yourusername.pythonanywhere.com/health`
- **Запуск бота**: `POST https://yourusername.pythonanywhere.com/start`
- **Остановка бота**: `POST https://yourusername.pythonanywhere.com/stop`

## ⚠️ Важно помнить

1. **Замените `yourusername`** на ваш реальный username на PythonAnywhere
2. **Создайте `.env` файл** с токеном бота
3. **Настройте UptimeRobot** для предотвращения "засыпания" (см. ниже)
4. **Логи ошибок** находятся в разделе Web → Error log

## 🔔 Настройка UptimeRobot (рекомендуется)

Для предотвращения "засыпания" приложения на бесплатном плане:

1. **Регистрация**: [uptimerobot.com](https://uptimerobot.com)
2. **Создать монитор**:
   - URL: `https://yourusername.pythonanywhere.com/ping`
   - Интервал: 5 минут
   - Тип: HTTP(s)
3. **Подробная инструкция**: [UPTIMEROBOT_SETUP.md](UPTIMEROBOT_SETUP.md)

**Результат**: Бот будет работать 24/7! 🚀

## 🆘 Если что-то не работает

1. Проверьте логи ошибок в панели PythonAnywhere
2. Убедитесь, что все зависимости установлены
3. Проверьте правильность токена бота
4. Убедитесь, что заменили `yourusername` в `wsgi.py`

## 🎉 Готово!

Ваш бот теперь работает 24/7 на PythonAnywhere! 🚀
