from aiogram.fsm.state import StatesGroup, State


class AddTask(StatesGroup):
    text = State()
    level = State()
