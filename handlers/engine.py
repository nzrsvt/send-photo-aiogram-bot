from aiogram import types, Dispatcher
import db_operations as db
from keyboards import user_kb

async def start_command(message: types.Message):
    if db.check_user_existence(message.chat.id):
        await message.delete()
        await message.answer(
            f'👋{message.from_user.full_name}, '
            'Вас знову вітає бот для подачі фотографії для оформлення Леокарт!\n'
            '👇Для початку роботи з ботом натисніть на кнопку нижче.',
            reply_markup=user_kb.start_kb
        )
    else:
        await message.delete()
        await message.answer(
            f'👋{message.from_user.full_name}, '
            'Вас вітає бот для подачі фотографії для оформлення Леокарт!\n'
            '👇Для початку роботи з ботом натисніть на кнопку нижче.',
            reply_markup=user_kb.start_kb
        )

        db.add_user(
            message.chat.id,
            message.from_user.username,
            message.from_user.full_name
        )

def register_handlers(dp : Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])