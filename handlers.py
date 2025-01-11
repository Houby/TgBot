import json
import time

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboard import main_kb
from aiogram.utils.markdown import hbold, hlink

from collectData import collect_data

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет!", reply_markup=main_kb)


@router.message(F.text == '📅 Binance Today')
async def get_binance_today_news(msg: Message):
    request_time = "today"
    await write_message_in_chat(msg, request_time)


@router.message(F.text == '🗓 Binance Month')
async def get_binance_month_news(msg: Message):
    request_time = "month"
    await write_message_in_chat(msg, request_time)


@router.message(F.text == '📜 Binance Year')
async def get_binance_year_news(msg: Message):
    request_time = "year"
    await write_message_in_chat(msg, request_time)


async def write_message_in_chat(msg, request_time):

    await msg.answer('Ожидайте...')

    collect_data(request_time)

    with open('result.json') as file:
        data = json.load(file)

    if data:
        for index, item in enumerate(data):
            card = f'{hlink(item.get("full_title"), item.get("link"))}\n\n' \
                   f'{hbold("Дата: ")}{item.get("date")}'

            if index % 10 == 0:
                time.sleep(2)

            await msg.answer(card)

        await msg.answer("Выдача завершена")

    else:
        await msg.answer("Данных нет")


@router.message()
async def message_handler(msg: Message):
    await msg.answer("Такой команды у бота нет!")
