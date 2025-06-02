import asyncio
import logging
import datetime

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_polling

from config import load_config
from app.database.models import init_db, User
from app.bot.handlers import register_all_handlers

async def on_startup(dp: Dispatcher):
    logging.info("Bot starting...")
    # Инициализация базы данных
    Session = init_db()
    dp["db_session"] = Session
    
    # Запуск периодических задач
    asyncio.create_task(scheduler())

async def scheduler():
    """Планировщик для периодических задач"""
    while True:
        # Сброс счетчика hurry в полночь
        now = datetime.datetime.now()
        if now.hour == 0 and now.minute == 0:
            session = dp["db_session"]()
            users = session.query(User).all()
            for user in users:
                user.hurry = 0
            session.commit()
            session.close()
        await asyncio.sleep(60)  # Проверка каждую минуту

def main():
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    
    # Загрузка конфигурации
    config = load_config()
    
    # Инициализация бота и диспетчера
    bot = Bot(token=config.token)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    
    # Регистрация всех обработчиков
    register_all_handlers(dp)
    
    # Запуск бота
    start_polling(dp, on_startup=on_startup, skip_updates=True)

if __name__ == '__main__':
    main() 