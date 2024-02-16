from aiogram.utils import executor
from handlers import engine
from create_bot import dp
from db_operations import create_users_table
import os

async def onStartup(_):
    create_users_table()
    folder_path='photos'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    print('Bot has been launched successfully.')

engine.register_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=onStartup)