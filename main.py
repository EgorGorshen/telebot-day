import logging, asyncio, sys, dotenv, os
from typing import NoReturn
from aiogram import Bot, Dispatcher
from src.db import DB
from src.handlers import user_router


dotenv.load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN", NoReturn)
USER_ID = os.getenv("BOT_TOKEN", NoReturn)


async def main() -> None:
    if BOT_TOKEN is NoReturn:
        raise Exception("ERROR: bot token not found")

    bot = Bot(BOT_TOKEN)
    disp = Dispatcher()

    disp.include_router(user_router)

    await disp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    sys.exit(asyncio.run(main()))
