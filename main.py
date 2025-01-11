import asyncio
import logging

from aiogram import Bot, Dispatcher, client
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import router

import getEnv
import settings


if settings.prod:
    used_bot_token = getEnv.bot_token
else:
    used_bot_token = getEnv.dev_bot_token


async def main():
    bot = Bot(token=used_bot_token, default=client.default.DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
