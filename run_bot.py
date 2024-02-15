from aiogram.utils import executor
from handlers import engine
from create_bot import dp
from db_operations import create_users_table

async def onStartup(_):
    print('Bot has been launched successfully.')
    create_users_table()

engine.register_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=onStartup)