import asyncio
import logging
import time
import sys

from aiogram import Bot, Dispatcher, html , types
from aiogram.types import Message , InlineKeyboardButton , InlineKeyboardMarkup
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import Command , CommandStart
from discounts_parse import find_discounts
from set_commands import set_default_commands

TOKEN = "TOKEN"

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message):
    await message.answer("Привет, это бот для стима.")

@dp.message(Command("discounts1"))
async def command_discounts(message: Message):
    game = find_discounts()[0]
    await message.answer(f"""{game["title"]}
{game["discount"]}
{game["price"]}
{game["link"]}
""")
    
@dp.message(Command("ping"))
async def ping_pong(message: Message):
    await message.answer(
        f"pong!\n{ round(time.time() - float(message.date.timestamp()),2) } seconds"
        )
    
@dp.message(Command("discounts"))
async def test(message: Message):
    global games

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
        InlineKeyboardButton(text='←',   callback_data=f'butt_1_-1_0'),
        InlineKeyboardButton(text=f'1/{len(games)} обновить список',callback_data=f'butt_2_1_0'),
        InlineKeyboardButton(text='→',   callback_data=f'butt_3_1_0')
        ]
    ])

    text = ('Список игр:\n' +
            f'{games[0]['title']}\n' + 
            f'{games[0]['discount']}\n' + 
            f'{games[0]['price']}\n' +
            f'[Сылка на игру]({games[0]['link']})'
            )

    await message.answer(text,reply_markup=markup,parse_mode='Markdown')

@dp.callback_query(lambda c: c.data.startswith(('butt_')))
async def to_query(call:types.CallbackQuery):
    global games

    data = call.data.split('_') 
    # butt_direction_(-1 or 1 for left of right)_page_number

    page_number = int(data[3]) + int(data[2]) 
    
    if data[1] == 'middle': games = find_discounts()
    if -1 == page_number or page_number == len(games): return
    print(0,page_number,len(games))
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
        InlineKeyboardButton(text=f'←',callback_data=f'butt_left_-1_{page_number}'),
        InlineKeyboardButton(text=f'{page_number+1}/{len(games)} обновить список',callback_data=f'butt_middle_0_{page_number}'),
        InlineKeyboardButton(text=f'→',callback_data=f'butt_right_1_{page_number}')
        ]
    ])

    text = ('Список игр:\n' +
            f'{games[page_number]['title']}\n' + 
            f'{games[page_number]['discount']}\n' + 
            f'{games[page_number]['price']}\n' + 
            f'[Сылка на игру]({games[page_number]['link']})'
            )

    #await call.answer('button pressed')
    await call.message.edit_text(reply_markup=markup,text=text,parse_mode='Markdown')

async def main():
    global games 
    games = find_discounts()

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await set_default_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,stream=sys.stdout)
    asyncio.run(main())
