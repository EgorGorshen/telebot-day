from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from src.keyboard import TASK_LEVEL

from src.logger import Logger
from src.states import AddTask
from src.utils import Level
from src.db import DB

user_router = Router()
user_log = Logger("user_log", "log/user.log")
DATA_BASE = DB()


@user_router.message(CommandStart())
@user_log.log_function_call
async def start(message: Message):
    await message.answer("/add_todo")


@user_router.message(Command("add_todo"))
@user_log.log_function_call
async def add_todo(message: Message, state: FSMContext):
    await state.set_state(AddTask.text)
    await message.answer("Добавь таск")


@user_router.message(AddTask.text)
@user_log.log_function_call
async def add_todo_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(AddTask.level)
    await message.answer("Выбери тип таска:", reply_markup=TASK_LEVEL)


@user_router.callback_query(AddTask.level)
@user_log.log_function_call
async def add_todo_level(callback: CallbackQuery, state: FSMContext):
    if callback.message is None:
        raise Exception()

    if callback.data is None:
        await callback.message.edit_text(text="Пустой запрос")
        return

    data = await state.update_data(
        level=int(
            callback.data if callback.data is not None else Level.IMPORTANT_URGENT
        )
    )
    print(data["text"], Level(int(data["level"])))

    DATA_BASE.add_todo(data["text"], Level(int(data["level"])))

    await callback.message.edit_text(f"Добавили: [{Level(int(data['level'])).name}]")
