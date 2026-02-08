import asyncio
import logging
from handlers.reminders import router as remind_router
from aiogram import Bot, Dispatcher
from db.session import init_db
from handlers.state import router as state_router
from config import BOT_TOKEN
from services.reminder_notifier import SimpleScheduler

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher() 
    init_db()
    dp.include_routers(state_router,remind_router)
    scheduler = SimpleScheduler(BOT_TOKEN)
    scheduler_task = asyncio.create_task(scheduler.run())
    await dp.start_polling(bot)
    scheduler_task.cancel()
    await scheduler.stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())


