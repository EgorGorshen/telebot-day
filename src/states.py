from aiogram.fsm.state import StatesGroup, State


class AddTask(StatesGroup):
    text = State()
    level = State()


class DoneTask(StatesGroup):
    choose_level = State()
    choose_todo = State()
    choose_done = State()
