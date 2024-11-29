from aiogram import Bot, Dispatcher    
#from .env import TOKEN
import os
from dotenv import load_dotenv

import asyncio
import logging

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

logging.basicConfig(level=logging.DEBUG)

async def main():
    from handlers.admin import dp
    
    try:
        await dp.start_polling(bot)
        print('Bot start!')
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped!')