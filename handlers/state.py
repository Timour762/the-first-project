
from aiogram.filters import Command
from aiogram import Router, F
from FSM.context import Form

from datetime import datetime, timezone, timedelta
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from db.crude import save_date_to_db
from keyboards.menu import main_menu_kb, settings

router = Router()


def detect_user_timezone(user_id: int) -> tuple[str, int]:

    return "Москва (UTC+3)", 3

@router.message(Command('start'))
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name} \nВыбери нужную действию:',
                         reply_markup=main_menu_kb())

@router.message(F.text == 'Создать напоминание')
async def create_reminder(message: Message, state: FSMContext):
    await message.answer('Введите описание напоминания:')
    await state.set_state(Form.description)
    timezone_name, timezone_offset = detect_user_timezone(message.from_user.id)

    await state.update_data(
        timezone_name=timezone_name,
        timezone_offset=timezone_offset
    )

@router.message(Form.description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    timezone_name = data.get('timezone_name', 'Москва (UTC+3)')
    await message.answer(f'Описание сохранено: {message.text}')
    await state.set_state(Form.reminder)
    await message.answer('Когда мне это вам напомнить? Формат: дд.мм.гггг чч:мм\n Пример: 31.12.2026 12:30')



@router.message(Form.reminder)
async def process_reminder_date(message: Message, state: FSMContext):
    date_str = message.text.strip()

    try:
        date_obj = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
        now = datetime.now()
        data = await state.get_data()
        timezone_offset = data.get('timezone_offset', 3)
        utc_datetime = date_obj - timedelta(hours=timezone_offset)

        current_utc = datetime.now(timezone.utc).replace(tzinfo=None)


        if date_obj < current_utc:
            await message.answer(" Эта дата уже прошла! Введите будущую дату:")
            return

        await state.update_data(reminder=date_str)

        data = await state.get_data()
        description = data.get('description', 'нет описания')

        await message.answer(
            f"Подтвердите напоминание:\n\n"
            f"Описание: {description}\n"
            f"Дата: {date_str}\n\n"
            f"Если все верно, нажмите 'Подтвердить напоминание'", reply_markup = settings()
        )

        await state.set_state(Form.confirmation)

    except ValueError:
        await message.answer("Неверный формат даты! Введите дату в формате ДД.ММ.ГГГГ ЧЧ:ММ\nПример: 25.12.2024 20:00")



@router.message(Form.confirmation)
async def process_confirmation(message: Message, state: FSMContext):
    if message.text == 'Подтвердить напоминание':
        data = await state.get_data()
        user_id = message.from_user.id
        description = data.get('description')
        reminder_date = data.get('reminder')


        if not all([description, reminder_date]):
            await message.answer("Ошибка: не все данные заполнены. Начните заново.")
            await state.clear()
            return

        try:
            save_date_to_db(
                user_id=user_id,
                description=description,
                date_str=reminder_date,
            )

            await message.answer(
                f"Напоминание успешно создано!\n\n"
                f"Описание: {description}\n"
                f"Дата: {reminder_date}\n\n"
                f"Я напомню вам в указанную дату!"
            )

            await message.answer("Главное меню:", reply_markup=main_menu_kb())
            await state.clear()

        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
            await state.clear()