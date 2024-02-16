from aiogram import types, Dispatcher
import db_operations as db
from keyboards import user_kb
from aiogram.dispatcher.filters import Text

from handlers.photo_submission import *

async def start_command(message: types.Message):
    if db.check_user_existence(message.chat.id):
        await message.delete()
        await message.answer(
            f'👋 {message.from_user.full_name}, '
            'Вас знову вітає бот для подачі фотографії для оформлення Леокарт!\n'
            '👇 Для початку роботи з ботом натисніть на кнопку нижче.',
            reply_markup=user_kb.start_kb
        )
    else:
        await message.delete()
        await message.answer(
            f'👋 {message.from_user.full_name}, '
            'Вас вітає бот для подачі фотографії для оформлення Леокарт!\n'
            '👇 Для початку роботи з ботом натисніть на кнопку нижче.',
            reply_markup=user_kb.start_kb
        )

        db.add_user(
            message.chat.id,
            message.from_user.username,
            message.from_user.full_name
        )

async def user_menu_call(callback : types.CallbackQuery):
    await callback.message.answer(f'🔸Оберіть наступну дію:', reply_markup=user_kb.menu_kb)
    await callback.answer()

def register_handlers(dp : Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])

    dp.register_callback_query_handler(user_menu_call, lambda c: c.data =='start_cb')

    dp.register_callback_query_handler(submit_photo_command, lambda c: c.data == 'submit_photo_cb', state=None)
    dp.register_message_handler(cancel_command, Text(equals=["відмінити", "скасувати", "відміна"], ignore_case=True), state='*')
    dp.register_message_handler(process_photo,content_types=['photo'], state=PhotoSubmission.photo)
    dp.register_message_handler(process_nickname, state=PhotoSubmission.nickname)
    