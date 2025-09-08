import os
import threading
from flask import Flask

app = Flask(__name__)

_bot_thread = None


def _run_bot_polling():
    from bot import bot as telegram_bot
    telegram_bot.infinity_polling()


@app.before_first_request
def start_bot_thread():
    global _bot_thread
    if _bot_thread is None or not _bot_thread.is_alive():
        _bot_thread = threading.Thread(target=_run_bot_polling, daemon=True)
        _bot_thread.start()


@app.route("/")
def root():
    return "OK", 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
