import asyncio
import logging
import sys

from dotenv import load_dotenv
from os import environ
from handlers import router

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

dp = Dispatcher()

async def main() -> None:
    dp.include_router(router)
    load_dotenv()
    token = environ['TOKEN']
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())