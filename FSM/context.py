from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class Form(StatesGroup):
    description = State()
    reminder = State()
    confirmation = State()


