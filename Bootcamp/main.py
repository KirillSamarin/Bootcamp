import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.filters.command import Command
from discounts_parse import find_discounts

TOKEN = "7682498533:AAFrfIybI6yHwc5NygJQRf26cja1_iKLxfo"

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message):
    await message.answer("Привет, это бот для стима.")

@dp.message(Command("discounts"))
async def command_discounts(message):
    game = find_discounts()[0]
    await message.answer(f"""{game["title"]}
{game["discount"]}
{game["price"]}
{game["link"]}
""")

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
