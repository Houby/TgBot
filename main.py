import asyncio
import logging

from aiogram import Bot, Dispatcher, client, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

import getEnv
from keyboard import main_kb

router = Router()


async def main():
    bot = Bot(token=getEnv.bot_token, default=client.default.DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет!", reply_markup=main_kb)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
