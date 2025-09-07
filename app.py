from flask import Flask, request, jsonify
import threading
import time
import os
from bot import bot
from config import BOT_TOKEN

app = Flask(__name__)

# Глобальная переменная для хранения потока бота
bot_thread = None
bot_running = False

def run_bot():
    """Функция для запуска бота в отдельном потоке"""
    global bot_running
    try:
        print("🤖 Запуск Telegram бота...")
        bot_running = True
        bot.infinity_polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"❌ Ошибка в работе бота: {e}")
        bot_running = False

@app.route('/')
def home():
    """Главная страница - показывает статус бота"""
    status = "🟢 Работает" if bot_running else "🔴 Остановлен"
    return f"""
    <html>
        <head>
            <title>Recipe Bot Status</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .status {{ font-size: 24px; margin: 20px 0; }}
                .info {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>🍽️ Recipe Telegram Bot</h1>
            <div class="status">Статус: {status}</div>
            <div class="info">
                <h3>Информация о боте:</h3>
                <p>• Бот работает в фоновом режиме</p>
                <p>• API: TheMealDB</p>
                <p>• Функции: поиск рецептов, сохранение в избранное</p>
                <p>• База данных: SQLite</p>
            </div>
            <div class="info">
                <h3>Доступные эндпоинты:</h3>
                <ul>
                    <li><code>GET /</code> - Эта страница</li>
                    <li><code>GET /status</code> - Статус бота (JSON)</li>
                    <li><code>POST /start</code> - Запустить бота</li>
                    <li><code>POST /stop</code> - Остановить бота</li>
                    <li><code>GET /health</code> - Проверка здоровья приложения</li>
                    <li><code>GET /ping</code> - Простой пинг для UptimeRobot</li>
                    <li><code>GET /uptime</code> - Статус для мониторинга</li>
                </ul>
            </div>
            <div class="info">
                <h3>🔔 UptimeRobot настройка:</h3>
                <p>Для предотвращения "засыпания" приложения настройте мониторинг:</p>
                <ul>
                    <li><strong>URL:</strong> <code>https://yourusername.pythonanywhere.com/ping</code></li>
                    <li><strong>Интервал:</strong> 5 минут</li>
                    <li><strong>Тип:</strong> HTTP(s)</li>
                </ul>
            </div>
        </body>
    </html>
    """

@app.route('/status')
def status():
    """API эндпоинт для проверки статуса бота"""
    return jsonify({
        'bot_running': bot_running,
        'bot_token_configured': bool(BOT_TOKEN),
        'status': 'running' if bot_running else 'stopped',
        'timestamp': time.time()
    })

@app.route('/start', methods=['POST'])
def start_bot():
    """API эндпоинт для запуска бота"""
    global bot_thread, bot_running
    
    if bot_running:
        return jsonify({'message': 'Бот уже запущен', 'status': 'already_running'})
    
    if not BOT_TOKEN:
        return jsonify({'error': 'BOT_TOKEN не настроен'}, 400)
    
    try:
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        
        # Ждем немного, чтобы убедиться, что бот запустился
        time.sleep(2)
        
        return jsonify({
            'message': 'Бот успешно запущен',
            'status': 'started',
            'bot_running': bot_running
        })
    except Exception as e:
        return jsonify({'error': f'Ошибка запуска бота: {str(e)}'}, 500)

@app.route('/stop', methods=['POST'])
def stop_bot():
    """API эндпоинт для остановки бота"""
    global bot_running
    
    if not bot_running:
        return jsonify({'message': 'Бот уже остановлен', 'status': 'already_stopped'})
    
    try:
        bot.stop_polling()
        bot_running = False
        return jsonify({
            'message': 'Бот остановлен',
            'status': 'stopped',
            'bot_running': bot_running
        })
    except Exception as e:
        return jsonify({'error': f'Ошибка остановки бота: {str(e)}'}, 500)

@app.route('/health')
def health_check():
    """Эндпоинт для проверки здоровья приложения"""
    return jsonify({
        'status': 'healthy',
        'bot_running': bot_running,
        'timestamp': time.time()
    })

@app.route('/ping')
def ping():
    """Простой эндпоинт для UptimeRobot - возвращает только статус"""
    return "OK", 200

@app.route('/uptime')
def uptime():
    """Эндпоинт для UptimeRobot с дополнительной информацией"""
    return jsonify({
        'status': 'online',
        'bot_running': bot_running,
        'uptime': time.time(),
        'message': 'Recipe Bot is running'
    }), 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook для получения обновлений от Telegram (альтернатива polling)"""
    if request.is_json:
        update = request.get_json()
        try:
            bot.process_new_updates([update])
            return jsonify({'status': 'ok'})
        except Exception as e:
            return jsonify({'error': str(e)}, 500)
    return jsonify({'error': 'Invalid request'}, 400)

if __name__ == '__main__':
    # Проверяем наличие токена
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN не настроен! Создайте .env файл с токеном.")
        print("Пример: BOT_TOKEN=your_bot_token_here")
    else:
        print("✅ BOT_TOKEN найден")
    
    # Запускаем Flask приложение
    print("🚀 Запуск Flask приложения...")
    app.run(debug=False, host='0.0.0.0', port=5000)
