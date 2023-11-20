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
