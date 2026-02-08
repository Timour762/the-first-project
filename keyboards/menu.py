from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Создать напоминание')],
            [KeyboardButton(text='Мои напоминание')]
        ],
        resize_keyboard=True,
    )
def settings():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Подтвердить напоминание')],
        ]
    )

def remind():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Просмотр напоминание')],
            [KeyboardButton(text='Удаление напоминание')]
        ]
    )