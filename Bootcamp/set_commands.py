from aiogram.types import BotCommand

async def set_default_commands(bot):
    bot_commands = ([
        BotCommand(command='/discounts',description='Скидки !'),
        BotCommand(command='/ping',description='Проверка на скорость работы бота.'),
    ])

    await bot.set_my_commands(bot_commands)
