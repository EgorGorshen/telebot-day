from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.utils import Level


TASK_LEVEL = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="ВАЖНОЕ СРОЧНОЕ", callback_data=str(Level.IMPORTANT_URGENT)
            )
        ],
        [
            InlineKeyboardButton(
                text="ВАЖНОЕ НЕ СРОЧНОЕ", callback_data=str(Level.IMPORTANT_NOT_URGENT)
            )
        ],
        [
            InlineKeyboardButton(
                text="НЕВАЖНОЕ СРОЧНОЕ", callback_data=str(Level.UNIMPORTANT_URGENT)
            )
        ],
        [
            InlineKeyboardButton(
                text="НЕВАЖНОЕ СРОЧНОЕ", callback_data=str(Level.UNIMPORTANT_NOT_URGENT)
            )
        ],
    ]
)

TODO_LIST = lambda todo_list: InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=task[1], callback_data=str(task[0]))]
        for task in todo_list
    ]
)

SELECT_TASK_DONE = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅", callback_data="1"),
            InlineKeyboardButton(text="❌", callback_data="0"),
        ],
    ]
)
