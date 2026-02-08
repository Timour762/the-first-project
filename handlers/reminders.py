import sqlite3
from datetime import datetime
from db.crude import get_reminder_by_id, get_reminder_by
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.menu import main_menu_kb, remind
from aiogram import Router, F
from aiogram.types import Message
from db.crude import delete_reminder, get_reminders
router = Router()


@router.message(F.text == 'Мои напоминание')
async def set(message: Message):
    await message.answer('Выберите:',reply_markup=remind())

@router.message(F.text == 'Просмотр напоминание')
async def settings(message: Message):
    user_id = message.from_user.id
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    try:


        reminders = get_reminders(tg_id=user_id)

        if not reminders:
            await message.answer(
                "У вас нет активных напоминаний.\n"
                "Создайте новое напоминание!",
                reply_markup=main_menu_kb()
            )
            return

        response = "Ваши активные напоминания:\n\n"

        for i, reminder in enumerate(reminders, 1):
            reminder_id,description, reminder_time = reminder

            try:
                dt = datetime.strptime(reminder_time, "%d.%m.%Y %H:%M")
                formatted_time = dt.strftime("%d %B %Y в %H:%M")
            except:
                formatted_time = reminder_time
            response += f"**{i}.id: {reminder_id}\n {description}**\n"
            response += f"   {formatted_time}\n"

        response += f"Всего: {len(reminders)} напоминаний"

        await message.answer(
            response,
            parse_mode='Markdown',
            reply_markup=main_menu_kb()
        )

    except Exception as e:
        await message.answer(
            f"Ошибка при получении напоминаний: {e}",
            reply_markup=main_menu_kb()
        )
    finally:
        conn.close()


@router.message(F.text == 'Удаление напоминание')
async def delete_by_id(message: Message, state: FSMContext):
    user_id = message.from_user.id

    # Получаем все напоминания пользователя
    user_reminders = get_reminder_by(user_id)
    if not user_reminders:
        await message.answer("У вас нет напоминаний для удаления")
        return


    text = "Ваши напоминания:\n\n"
    for rem_id, desc in user_reminders:
        text += f"id: {rem_id} - {desc}\n"

    text += "\nНапишите ID напоминания, которое хотите удалить:"
    await message.answer(text)

@router.message()
async def delete_remind(message: Message):
    user_id = message.from_user.id
    if not message.text.isdigit():
        await message.answer('Введите цифру!')
        return
    number = int(message.text)

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()


    all_reminders = get_reminder_by_id(reminder_id=number, tg_id=user_id)

    if all_reminders is None:
        user_reminders = get_reminder_by(user_id,)

        if user_reminders:
            text = f"Не найдено напоминание с ID {number}\n\n"
            text += "Ваши напоминания:\n"
            for rem_id, desc in user_reminders:
                text += f"{rem_id} - {desc}\n"
        else:
            text = "У вас нет напоминаний"

        await message.answer(text)
        conn.close()
        return

    description = all_reminders[0]

    cursor.execute("DELETE FROM recipes WHERE id = ? AND user_id = ?",
                   (number, user_id))
    conn.commit()
    conn.close()

    await message.answer(f"Напоминание удалено!\n"
                         f"{description}\n"
                         f"ID: {number}")