from aiogram.utils import executor
from handlers import engine
from create_bot import dp
from db_operations import create_users_table
import os

from aiogram import types, Dispatcher

from aiogram.dispatcher.middlewares import BaseMiddleware

class LoggingMiddleware(BaseMiddleware):
    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        print(f"Received callback_query.data: {callback_query.data}")
        return

async def onStartup(_):
    create_users_table()
    folder_path='photos'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    dp.middleware.setup(LoggingMiddleware())
    print('Bot has been launched successfully.')

engine.register_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=onStartup)

