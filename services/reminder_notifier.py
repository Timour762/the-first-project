import asyncio
import sqlite3
from datetime import datetime
from aiogram import Bot



class SimpleScheduler:

    def __init__(self, bot_token):
        self.bot = Bot(token=bot_token)
        self.running = True

    def get_todays_reminders(self):

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        today = datetime.now().strftime("%d.%m.%Y")

        cursor.execute('''
        SELECT id, user_id, description, data 
        FROM recipes 
        WHERE is_active = 1 AND data LIKE ?
        ''', (f"{today}%",))

        reminders = cursor.fetchall()
        conn.close()

        return reminders

    def should_send_now(self, reminder_time_str, current_time):

        try:

            reminder_time = datetime.strptime(reminder_time_str, "%d.%m.%Y %H:%M")

            if reminder_time <= current_time:
                return True
        except:
            pass
        return False

    async def send_reminder(self, user_id, description, reminder_time):

        try:
            message = f"НАПОМИНАНИЕ!\n\n{description}\n\nВремя: {reminder_time}"
            await self.bot.send_message(chat_id=user_id, text=message)
            return True
        except:
            return False

    def mark_as_sent(self, reminder_id):

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE recipes SET is_active = 0 WHERE id = ?", (reminder_id,))
        conn.commit()
        conn.close()

    async def check_reminders(self):

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Проверяю напоминания...")

        reminders = self.get_todays_reminders()

        if not reminders:
            print("На сегодня напоминаний нет")
            return

        current_time = datetime.now()

        for reminder in reminders:
            reminder_id, user_id, description, reminder_time = reminder

            if self.should_send_now(reminder_time, current_time):
                print(f"Отправляю напоминание: {description}")
                success = await self.send_reminder(user_id, description, reminder_time)

                if success:
                    self.mark_as_sent(reminder_id)
                    print(f"Отправлено пользователю {user_id}")


        while self.running:
            try:
                await self.check_reminders()
            except Exception as e:
                print(f"Ошибка: {e}")

            await asyncio.sleep(60)

    async def run(self):

        while self.running:
            try:
                await self.check_reminders()
            except Exception as e:
                print(f"Ошибка: {e}")

            await asyncio.sleep(60)

    async def stop(self):
        self.running = False
        await self.bot.close()