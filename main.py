import threading
from app.web import app as flask_app
from aiogram import executor
from app.bot import dp

def run_flask():
    flask_app.run(host="0.0.0.0", port=5000)

def run_aiogram():
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_aiogram()
