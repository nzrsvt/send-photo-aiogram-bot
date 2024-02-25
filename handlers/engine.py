from aiogram import types, Dispatcher
import db_operations as db
from keyboards import user_kb, admin_kb
from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.dispatcher.filters import ContentTypeFilter
from aiogram.types import MediaGroup, InputMediaDocument
import aiogram.dispatcher.filters
from aiogram_media_group import media_group_handler
from aiogram.dispatcher.filters import MediaGroupFilter
import asyncio

from handlers.user_actions import * 
from handlers.admin_actions import * 

from additional_functions import cancel_command, secret_command
from config import secret_word

async def start_command(message: types.Message):
    if db.check_user_existence(message.chat.id):
        await message.delete()
        await message.answer(
            f'👋 {message.from_user.full_name}, '
            'Вас знову вітає бот для надсилання фотографій!',
            reply_markup=user_kb.start_kb
        )
    else:
        await message.delete()
        await message.answer(
            f'👋 {message.from_user.full_name}, '
            'Вас вітає бот для надсилання фотографій!',
            reply_markup=user_kb.start_kb
        )

        db.add_user(
            message.chat.id,
            message.from_user.username,
            message.from_user.full_name
        )

async def menu_call(callback : types.CallbackQuery):
    if callback.data == "start_cb":
        if db.check_user_instagram_existence(callback.from_user.id):
            is_admin = db.check_is_admin(callback.from_user.id)
            await callback.message.answer('🔸 Оберіть наступну дію:',
                                          reply_markup = admin_kb.action_choose_kb if is_admin 
                                          else user_kb.action_choose_kb
                                          )
        else:
            await callback.message.answer('⬇️ Для початку роботи з ботом потрібно вказати свій Instagram-нікнейм. Натисніть на кнопку нижче.',reply_markup=user_kb.enter_instagram_kb)
    else:
        await callback.message.answer('🔸 Оберіть наступну дію:',reply_markup=user_kb.action_choose_kb)
    await remove_previous_kb(callback)
    await callback.answer()

def register_handlers(dp : Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])

    dp.register_callback_query_handler(menu_call, lambda c: c.data in ['start_cb', 'return_to_menu_cb'])

    dp.register_callback_query_handler(enter_instagram_nickname_command, lambda c: c.data in ['enter_instagram_cb', 'change_instagram_cb'], state=None)

    dp.register_message_handler(secret_command, Text(equals=secret_word), state='*')

    dp.register_message_handler(process_instagram_nickname, state=InstagramEntering.instagram_nickname)

    dp.register_message_handler(cancel_command, Text(equals=["відмінити", "скасувати", "відміна"], ignore_case=True), state='*')

    dp.register_message_handler(process_instagram_nickname, state=InstagramChanging.instagram_nickname)
    
    dp.register_callback_query_handler(send_photo_command, lambda c: c.data == 'send_photo_cb', state=None)
    dp.register_message_handler(process_photo_group, MediaGroupFilter(is_media_group=True), content_types=['photo', 'document'], state=PhotoSending.photo)
    dp.register_message_handler(process_photo, content_types=['photo', 'document'], state=PhotoSending.photo)
    
    dp.register_callback_query_handler(manage_photos_command, lambda c: c.data == 'manage_photos_cb')
    dp.register_callback_query_handler(delete_photo_command, lambda c: c.data.startswith('del'))


    dp.register_callback_query_handler(add_admin_command, lambda c: c.data == 'add_admin_cb', state=None)
    dp.register_message_handler(process_username, state=AdminAdding.username)