from aiogram import Router
from aiogram.filters import CommandStart, Command, state
from aiogram.types import CallbackQuery, Message, message
from aiogram.fsm.context import FSMContext
from src.keyboard import SELECT_TASK_DONE, TASK_LEVEL, TODO_LIST

from src.logger import Logger
from src.states import AddTask, DoneTask
from src.utils import Level
from src.db import DB

user_router = Router()
user_log = Logger("user_log", "log/user.log")
DATA_BASE = DB()


@user_router.message(CommandStart())
@user_log.log_function_call
async def start(message: Message):
    await message.answer("/add_todo /choose_todo")


# >>>>>>>>>>>>>>>>> add todo >>>>>>>>>>>>>>>>>
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

    await state.update_data(
        level=int(
            callback.data if callback.data is not None else Level.IMPORTANT_URGENT
        )
    )
    data = await state.get_data()
    await state.clear()

    a = DATA_BASE.add_todo(data["text"], Level(int(data["level"])))

    await callback.message.edit_text(
        f"Добавили: [{Level(int(data['level'])).name}] + {a}"
    )


# >>>>>>>>>>>>>>>>> choose todo >>>>>>>>>>>>>>>>>
@user_router.message(Command("choose_todo"))
@user_log.log_function_call
async def choose_todo(message: Message, state: FSMContext):
    await state.set_state(DoneTask.choose_level)
    await message.answer("Выбери тип тасков:", reply_markup=TASK_LEVEL)


@user_router.callback_query(DoneTask.choose_level)
@user_log.log_function_call
async def choose_level(callback: CallbackQuery, state: FSMContext):
    if callback.message is None:
        raise Exception()

    if callback.data is None:
        await callback.message.edit_text(text="Пустой запрос")
        return

    if not callback.data.isdigit():
        await callback.message.edit_text(text="Не правильный зарпос")
        return

    todo_list = list(
        filter(lambda x: x[-2] == Level(int(callback.data)), DATA_BASE.get_todo_list())
    )
    await state.set_state(DoneTask.choose_todo)

    await callback.message.edit_text("Выбери таск:", reply_markup=TODO_LIST(todo_list))


@user_router.callback_query(DoneTask.choose_todo)
@user_log.log_function_call
async def choose_todo_task(callback: CallbackQuery, state: FSMContext):
    if callback.message is None:
        raise Exception()

    if callback.data is None:
        await callback.message.edit_text(text="Пустой запрос")
        return

    if not callback.data.isdigit():
        await callback.message.edit_text(text="Не правильный зарпос")
        return

    await state.update_data(task_id=int(callback.data))
    await state.set_state(DoneTask.choose_done)

    await callback.message.edit_text(
        text=f"Изменить статус:",
        reply_markup=SELECT_TASK_DONE,
    )


@user_router.callback_query(DoneTask.choose_done)
@user_log.log_function_call
async def choose_done(callback: CallbackQuery, state: FSMContext):
    if callback.message is None:
        raise Exception()

    if callback.data is None:
        await callback.message.edit_text(text="Пустой запрос")
        return

    if not callback.data.isdigit():
        await callback.message.edit_text(text="Не правильный зарпос")
        return

    data = await state.get_data()
    print(data["task_id"], bool(int(callback.data)))

    await state.clear()
    DATA_BASE.change_status_todo(data["task_id"], bool(int(callback.data)))
    await callback.message.edit_text("Done")
