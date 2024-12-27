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
from repeat_functions import is_desired_game_on_sale
from set_commands import set_default_commands
from local_info import AUTHOR_IDS , USERS , BOT_TOKEN

TOKEN = BOT_TOKEN

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message):
    await message.answer("Привет, это бот для стима.")
    USERS[message.from_user.id] = []

@dp.message(Command("simple_discounts"))
async def command_discounts(message: Message):
    game = find_discounts()[0]
    await message.answer(f"""{game["title"]}
{game["discount"]}
{game["price"]}
{game["link"]}
""")

@dp.message(Command("contact"))
async def command_discounts(message: Message ):
    if message.text == '/contact':
        await message.answer("""Чтобы передать сообщение создателям бота,
Используйте комманду повторно,\n
"/contact *текст которы желаете передать*"
        """)

    else:
        for author_id in IDS:
            await message.chat.bot.send_message(author_id,f'от:@{message.from_user.username}\n{message.text[9:]}')

        await message.answer('Ваше сообщение успешно отравлено создателям!')

@dp.message(Command("ping"))
async def ping_pong(message: Message):
    await message.answer(
        f"pong!\n{ round(time.time() - float(message.date.timestamp()),2) } seconds"
        )
    
@dp.message(Command("my_desired"))
async def my_desired(message: Message):
    global games

    if message.text == '/my_desired':
        await message.answer(
            """Чтобы проверить есть ли желаемая игра в списке со скидками
Илспользуйте комманду повторно "/my_desired"
Чтобы добавить игру в список желаемых используйте 
/my_desired /https://store.steampowered.com/app/игра

При попытки добваить одну и ту же игру 2 раза она будет удалена из списка
Инофрмация обновилась
        """)
        
    elif message.text.startswith('/my_desired https://store.steampowered.com/app/'):
        game_link = message.text.split()[1]
        if game_link in USERS[message.from_user.id]:
            del USERS[message.from_user.id][USERS[message.from_user.id].index(game_link)]
        else:
            USERS[message.from_user.id].append(game_link)
    
    games = find_discounts()
    sale_desired_games = await is_desired_game_on_sale(message,games)

    if sale_desired_games:
        links = [ game['link'] for game in sale_desired_games ]
        await message.answer(f'Ваши желаемые игры со скидками!\n{'\n'.join(links)}')
    else:
        await message.answer(f'Ваши игры не имеют скидки')

        



@dp.message(Command("discounts"))
async def discounts(message: Message):
    global games

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
        InlineKeyboardButton(text='←',   callback_data=f'butt_1_-1_0'),
        InlineKeyboardButton(text=f'1/{len(games)} обновить список',callback_data=f'butt_2_0_0_0'),
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
    # butt_direction_(-1 or 1 for left of right)_page_number_(0 or 1 only for middle to prevent same text)

    page_number = int(data[3]) + int(data[2]) 
    
    if data[1] == 'middle': 
        games = find_discounts()
        space = 1 if int(data[4]) == 0 else 0
    else:
        space = 0
    print(space)
    if -1 == page_number or page_number == len(games): return

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
        InlineKeyboardButton(text=f'←',callback_data=f'butt_left_-1_{page_number}'),
        InlineKeyboardButton(text=f'{page_number+1}/{len(games)} обновить список',callback_data=f'butt_middle_0_{page_number}_{space}'),
        InlineKeyboardButton(text=f'→',callback_data=f'butt_right_1_{page_number}')
        ]
    ])

    text = (f'Список игр:{' ' * space}\n' +
            f'{games[page_number]['title']}\n' + 
            f'{games[page_number]['discount']}\n' + 
            f'{games[page_number]['price']}\n' + 
            f'[Сылка на игру]({games[page_number]['link']})'
            )

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
